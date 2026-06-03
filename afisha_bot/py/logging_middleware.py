import os
from datetime import datetime
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Update, Message, CallbackQuery


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any]
    ) -> Any:
        # ✅ В aiogram 3.x пользователя берём из data, а не из event
        user = data.get("event_from_user")

        if user:
            # Создаем папку для логов, если её нет
            log_file = os.path.join(r"C:\afisha_bot\py\logs", f"{user.id}.log")

            # Определяем, какое действие совершил пользователь
            event_obj = event.event  # Вложенное событие (Message, CallbackQuery и т.д.)

            if isinstance(event_obj, Message) and event_obj.text:
                action = f"Сообщение: {event_obj.text}"
            elif isinstance(event_obj, CallbackQuery) and event_obj.data:
                action = f"Нажал кнопку: {event_obj.data}"
            elif isinstance(event_obj, Message):
                action = f"Действие: {event_obj.content_type}"
            else:
                action = f"Действие: {type(event_obj).__name__}"

            # Время берём из события (если есть) или текущее
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Формируем строку лога
            username = user.username or "no_username"
            full_name = user.full_name
            log_entry = (
                f"[{timestamp}] "
                f"User {full_name} (@{username}, id={user.id}): "
                f"{action}\n"
            )

            # Записываем в файл
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)

        # Обязательно вызываем следующий обработчик!
        return await handler(event, data)