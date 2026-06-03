import aiohttp
import time
from config import VK_TOKEN, VK_GROUPS, VK_EVENT_KEYWORDS


async def get_group_wall(group_id: str, session: aiohttp.ClientSession, count: int = 20):

    api_url = "https://api.vk.com/method/wall.get"

    params = {
        "domain": group_id,
        "count": count,
        "v": "5.199",
        "access_token": VK_TOKEN,
        "filter": "owner"
    }

    try:
        async with session.get(api_url, params=params, timeout=10, ssl=False) as response:
            if response.status != 200:
                print(f"VK API вернул статус {response.status} для {group_id}")
                return []

            data = await response.json()

            if "error" in data:
                print(f"Ошибка VK API ({group_id}): {data['error'].get('error_msg', 'Неизвестно')}")
                return []

            items = data.get("response", {}).get("items", [])
            return items

    except Exception as e:
        print(f"Ошибка при запросе к {group_id}: {e}")
        return []


def is_event_post(text: str) -> bool:
    # проверка по ключевым словам
    text_lower = text.lower()
    matches = sum(1 for keyword in VK_EVENT_KEYWORDS if keyword in text_lower)
    return matches >= 2 and len(text) > 50


async def get_vk_events():

    print("Ищу события в VK")

    all_events = []
    seen_keys = set()

    async with aiohttp.ClientSession() as session:
        for group_id in VK_GROUPS:
            posts = await get_group_wall(group_id, session)

            for post in posts:
                text = post.get("text", "").strip()

                if not is_event_post(text):
                    continue

                owner_id = post.get("owner_id")
                post_id = post.get("id")
                post_url = f"https://vk.com/wall{owner_id}_{post_id}"

                date_ts = post.get("date", 0)
                date_str = time.strftime("%d.%m.%Y", time.localtime(date_ts)) if date_ts else ""

                unique_key = f"{owner_id}_{post_id}"
                if unique_key in seen_keys:
                    continue
                seen_keys.add(unique_key)

                first_line = text.split("\n")[0][:100].strip()
                description = text[:200].replace("\n", " ").strip()
                if len(text) > 200:
                    description += "..."

                all_events.append({
                    'title': first_line,
                    'description': description,
                    'date': date_str,
                    'url': post_url,
                    'group': group_id
                })

    all_events.sort(key=lambda x: x.get('date', ''), reverse=True)

    return all_events