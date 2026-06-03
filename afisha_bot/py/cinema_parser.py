import time
import aiohttp
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from config import CACHE, CINEMAS, CACHE_LIFETIME

async def get_movies_list_megakino():

    # Проверяем кэш
    if CACHE['movies'] and (time.time() - CACHE['timer']) < CACHE_LIFETIME:
        print("Используем кэш ")
        return CACHE['movies']

    print("Кэш устарел")

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0")

    driver = None
    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

        driver.get("https://megakino42.ru/events")

        # Прокрутка страницы
        last_height = driver.execute_script("return document.body.scrollHeight")
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        img_tags = driver.find_elements(By.CSS_SELECTOR, "div[class='EventTilesList_event-list-wrap__0Y4HP event-list-wrap rental EventTilesList_limit-width__nmU1i'] img.Image_image__vhbZk")

        movies = []
        for i, img in enumerate(img_tags):
            try:
                title = img.get_attribute("alt")
                image_url = img.get_attribute("src")

                # фильтруем заглушки
                if (title and len(title.strip()) > 2 and image_url and not image_url.startswith('data:image')):
                    movies.append({
                        'name': title.strip(),
                        'image': image_url
                    })
            except Exception:
                continue

        # дубликаты
        unique_movies = []
        seen_names = set()
        for movie in movies:
            if movie['name'] not in seen_names:
                unique_movies.append(movie)
                seen_names.add(movie['name'])

        # кэш
        CACHE['movies'] = unique_movies
        CACHE['timer'] = time.time()
        CACHE['collages'] = {}

        return unique_movies

    except Exception as e:
        print(f"Ошибка Selenium: {e}")
        return CACHE['movies']
    finally:
        if driver:
            driver.quit()

async def get_movie_all(movie_name: str, date_str: str):

    result = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    async with aiohttp.ClientSession() as session:
        for cinema_name, base_url in CINEMAS.items():
            url = base_url.format(date_str=date_str)
            print(f"{cinema_name}: {url}")

            try:
                async with session.get(url, headers=headers, timeout=10) as response:
                    response.raise_for_status()
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')

                    # Ищем блоки сеансов
                    blocks = soup.find_all('div', class_="EventList_details__eUbW4 details EventList_event-bg__T40q1")

                    sessions = []
                    for block in blocks:
                        block_text = block.get_text(strip=True)

                        if movie_name.replace(" ", "").lower() in block_text.replace(" ", "").lower():
                            time_tags = block.find_all('div', class_="Show_show-time__iv3r5")
                            cost_tags = block.find_all('div', class_="Show_price__YStM_")

                            for i, time_tag in enumerate(time_tags):
                                if i < len(cost_tags):  # Защита от IndexError
                                    sessions.append(
                                        f"{time_tag.get_text(strip=True)} — {cost_tags[i].get_text(strip=True)}"
                                    )

                    if not sessions:
                        sessions.append('Нет сеансов')
                    result[cinema_name] = sessions

            except Exception as e:
                print(f"Ошибка при парсинге {cinema_name}: {e}")
                continue

    return result