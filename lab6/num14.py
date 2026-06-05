class MailServer:
    def __init__(self, Name):
        self.Name = Name
        self.Mailbox = {}

    def add_user(self, User):
        if User not in self.Mailbox:
            self.Mailbox[User] = []

    def receive_mail(self, User, Message):
        if User not in self.Mailbox:
            self.Mailbox[User] = []
        self.Mailbox[User].append(Message)

    def get_mail(self, User):
        if User not in self.Mailbox or not self.Mailbox[User]:
            return []
        Messages = self.Mailbox[User]
        self.Mailbox[User] = []
        return Messages

    def has_mail(self, User):
        return User in self.Mailbox and len(self.Mailbox[User]) > 0

    def __str__(self):
        return f"Server: {self.Name}"


class MailClient:
    def __init__(self, Server, User, AvailableServers):
        self.Server = Server
        self.User = User
        self.AvailableServers = AvailableServers
        self.Server.add_user(User)

    def receive_mail(self):
        Messages = self.Server.get_mail(self.User)
        if Messages:
            print(f"{self.User} получил {len(Messages)} сообщений:")
            for Msg in Messages:
                print(f"  От: {Msg['from']}@{Msg['from_server']}")
                print(f"  Сообщение: {Msg['message']}")
        else:
            print(f"У {self.User} нет новых сообщений")
        return Messages

    def send_mail(self, TargetServerName, TargetUser, Message):
        if TargetServerName not in self.AvailableServers:
            print(f"Ошибка: сервер {TargetServerName} недоступен для отправки")
            return False

        TargetServer = self.AvailableServers[TargetServerName]
        MailData = {
            'from': self.User,
            'from_server': self.Server.Name,
            'to': TargetUser,
            'message': Message
        }
        TargetServer.receive_mail(TargetUser, MailData)
        print(f"Сообщение отправлено пользователю {TargetUser}@{TargetServerName}")
        return True


# Интерфейс для демонстрации
class MailSystem:
    def __init__(self):
        self.Servers = {}
        self.Clients = {}

    def add_server(self, Name):
        if Name not in self.Servers:
            self.Servers[Name] = MailServer(Name)
            print(f"Сервер {Name} добавлен")

    def create_client(self, ServerName, UserName):
        if ServerName not in self.Servers:
            print(f"Ошибка: сервер {ServerName} не существует")
            return None

        ClientKey = f"{UserName}@{ServerName}"
        if ClientKey in self.Clients:
            print(f"Клиент {ClientKey} уже существует")
            return self.Clients[ClientKey]

        Client = MailClient(self.Servers[ServerName], UserName, self.Servers)
        self.Clients[ClientKey] = Client
        print(f"Клиент {ClientKey} создан")
        return Client

    def list_servers(self):
        print("Доступные серверы:")
        for Name in self.Servers:
            print(f"  - {Name}")


# Демонстрация работы системы
print("\nСИСТЕМА ПОЧТОВЫХ СЕРВЕРОВ")

System = MailSystem()

System.add_server("gmail.com")
System.add_server("mail.ru")
System.add_server("yandex.ru")


Client1 = System.create_client("gmail.com", "alice")
Client2 = System.create_client("mail.ru", "bob")
Client3 = System.create_client("yandex.ru", "charlie")

print("\nОТПРАВКА СООБЩЕНИЙ")

Client1.send_mail("mail.ru", "bob", "Привет, Боб!")
Client1.send_mail("yandex.ru", "charlie", "Здравствуй, Чарли!")
Client2.send_mail("gmail.com", "alice", "Ответ от Боба")

print("\nПОПЫТКА ОТПРАВКИ НА НЕДОСТУПНЫЙ СЕРВЕР")

Client1.send_mail("unknown.com", "user", "Тест")

print("\nПОЛУЧЕНИЕ ПОЧТЫ")

Client2.receive_mail()
Client3.receive_mail()

print("\nПОВТОРНОЕ ПОЛУЧЕНИЕ (почта уже удалена)")

Client2.receive_mail()

print("\nСПИСОК СЕРВЕРОВ")

System.list_servers()