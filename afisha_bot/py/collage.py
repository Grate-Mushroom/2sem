from PIL import Image, ImageDraw, ImageFont
import aiohttp
import io
import os

async def create_movies_collage(movies: list, output_path: str = "temp_collage.jpg"):
    # скачать картинки
    images = []
    headers = {"User-Agent": "Mozilla/5.0"}

    async with aiohttp.ClientSession() as session:
        for movie in movies[:6]:
            if not movie.get('image'):
                continue

            try:
                async with session.get(movie['image'], headers=headers, timeout=10) as resp:
                    if resp.status == 200:
                        img_data = await resp.read()

                        if len(img_data) < 1000:
                            continue
                        img = Image.open(io.BytesIO(img_data))
                        img = img.resize((200, 300), Image.Resampling.LANCZOS)
                        images.append((img, movie['name']))
            except Exception:
                continue

    if not images:
        return None

    # Создаем коллаж
    collage_width = 200 * 3
    collage_height = 300 * 2 + 50

    collage = Image.new('RGB', (collage_width, collage_height), '#1a1a2e')

    # Размещаем картинки
    for idx, (img, name) in enumerate(images):
        row = idx // 3
        col = idx % 3
        x = col * 200
        y = 50 + row * 300
        collage.paste(img, (x, y))

    # Сохраняем
    try:
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        collage.save(output_path, "JPEG", quality=85)
        return output_path
    except Exception:
        return None