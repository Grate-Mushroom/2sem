from datetime import datetime, timedelta

class Presentation:
    def __init__(self, topic, start_time, duration):
        self.topic = topic
        self.start_time = start_time
        self.duration = duration

    def get_end_time(self):
        return self.start_time + timedelta(minutes=self.duration)

    def overlaps_with(self, other):
        return self.start_time < other.get_end_time() and other.start_time < self.get_end_time()

    def __str__(self):
        return f"{self.topic} ({self.start_time.strftime('%H:%M')} - {self.get_end_time().strftime('%H:%M')})"

class Conference:
    def __init__(self, name):
        self.name = name
        self.presentations = []

    def add_presentation(self, presentation):
        for existing in self.presentations:
            if presentation.overlaps_with(existing):
                return False, f"Конфликт: '{presentation.topic}' пересекается с '{existing.topic}'"
        self.presentations.append(presentation)
        self.presentations.sort(key=lambda p: p.start_time)
        return True, f"Выступление '{presentation.topic}' добавлено"

    def get_total_duration(self):
        return sum(p.duration for p in self.presentations)

    def get_longest_break(self):
        if len(self.presentations) < 2:
            return 0
        max_break = 0
        for i in range(len(self.presentations) - 1):
            current_end = self.presentations[i].get_end_time()
            next_start = self.presentations[i + 1].start_time
            break_time = (next_start - current_end).seconds // 60
            max_break = max(max_break, break_time)
        return max_break

    def get_schedule(self):
        if not self.presentations:
            return "Расписание пусто"
        schedule = f"\nРасписание конференции '{self.name}':\n"
        for i, p in enumerate(self.presentations, 1):
            schedule += f"{i}. {p}\n"
        return schedule

    def get_statistics(self):
        if not self.presentations:
            return "Нет данных для статистики"
        stats = "\nСтатистика:\n"
        stats += f"Количество выступлений: {len(self.presentations)}\n"
        stats += f"Общая длительность: {self.get_total_duration()} мин\n"
        stats += f"Самый длинный перерыв: {self.get_longest_break()} мин\n"
        return stats

def parse_time(time_str):
    try:
        return datetime.strptime(time_str, "%H:%M")
    except ValueError:
        return None

def main():
    print("СИСТЕМА ПЛАНИРОВАНИЯ КОНФЕРЕНЦИЙ")

    conference_name = input("\nВведите название конференции: ")
    conference = Conference(conference_name)

    while True:
        print("\n" + "=" * 50)
        print("МЕНЮ:")
        print("1. Добавить выступление")
        print("2. Показать расписание")
        print("3. Показать статистику")
        print("4. Выход")

        choice = input("\nВыберите действие: ")

        if choice == "1":
            print("\n--- Добавление выступления ---")
            topic = input("Тема выступления: ")

            while True:
                time_str = input("Время начала (ЧЧ:ММ): ")
                start_time = parse_time(time_str)
                if start_time:
                    break
                print("Неверный формат времени. Используйте ЧЧ:ММ")

            while True:
                try:
                    duration = int(input("Длительность (минут): "))
                    if duration > 0:
                        break
                    print("Длительность должна быть положительным числом")
                except ValueError:
                    print("Введите целое число")

            presentation = Presentation(topic, start_time, duration)
            success, message = conference.add_presentation(presentation)
            print(message)

        elif choice == "2":
            print(conference.get_schedule())

        elif choice == "3":
            print(conference.get_statistics())

        elif choice == "4":
            break

        else:
            print("\nНеверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()