import json
import os
import asyncio
from datetime import datetime

REMINDERS_FILE = "reminders.json"


def load_reminders():
    if not os.path.exists(REMINDERS_FILE):
        return []
    with open(REMINDERS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_reminders(reminders):
    with open(REMINDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(reminders, f, ensure_ascii=False, indent=4)


async def add_reminder_to_file(user_id: int, name: str, reminder_time_iso: str):
    reminders = load_reminders()
    reminders.append({
        "user_id": user_id,
        "name": name,
        "time": reminder_time_iso,
        "sent": False
    })
    save_reminders(reminders)
    print(f"Напоминание сохранено: {name}")


async def check_reminders_loop(bot):
    print("Фоновая проверка напоминаний запущена")
    while True:
        await asyncio.sleep(60)
        reminders = load_reminders()
        now = datetime.now()
        updated = False

        for reminder in reminders:
            if not reminder.get("sent"):
                try:
                    target_time = datetime.fromisoformat(reminder["time"])
                    if now >= target_time:
                        print(f"Отправка напоминания: {reminder['name']} -> {reminder['user_id']}")
                        await bot.send_message(
                            chat_id=reminder["user_id"],
                            text=f"*Напоминание!*\n\n{reminder['name']}",
                            parse_mode="Markdown"
                        )
                        reminder["sent"] = True
                        updated = True
                except Exception as e:
                    print(f"Ошибка напоминания: {e}")

        if updated:
            save_reminders(reminders)