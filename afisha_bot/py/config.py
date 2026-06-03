BOT_TOKEN = "8953737415:AAGKFcScx1HWDORY_PErlAj0J26xNPf1WuA"

CINEMAS = {
    "Юбилейный": "https://megakino42.ru/?date={date_str}&facility=ooo-kino-42" ,
    "КиноКосмос": "https://kinokosmos42.ru/?date={date_str}&facility=kosmos" ,
    "Кинорио": "https://kinorio42.ru/?date={date_str}&facility=rio-sinema",
}

# Общий кэш
CACHE = {
    'movies': [],
    'timer': 0,
    'collages': {},
}
CACHE_LIFETIME = 3600

VK_TOKEN = "39fa44b939fa44b939fa44b9123abb30bf339fa39fa44b953e58508bed5e2b27ed4b641"

VK_CITY_ID = 189  # Кемерово

VK_GROUPS = [
    "otdohni42",
    "afisha_kuzbassonline",
    "afisha_kemerovo_gorodzovet",
]

# Ключевые слова
VK_EVENT_KEYWORDS = [
    "анонс", "билеты", "концерт", "выставка",
    "спектакль", "фестиваль", "мероприятие", "приглашаем",
    "состоится", "начнется", "начнётся"
]