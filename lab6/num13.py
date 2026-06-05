import math

class Weapon:
    def __init__(self, name, damage, range):
        self.Name = name
        self.Damage = damage
        self.Range = range

    def hit(self, actor, target):
        if not target.is_alive():
            print("Враг уже повержен")
            return

        ActorX, ActorY = actor.get_coords()
        TargetX, TargetY = target.get_coords()

        Distance = math.sqrt((TargetX - ActorX) ** 2 + (TargetY - ActorY) ** 2)

        if Distance > self.Range:
            print(f"Враг слишком далеко для оружия {self.Name}")
            return

        print(f"Врагу нанесен урон оружием {self.Name} в размере {self.Damage}")
        target.get_damage(self.Damage)

    def __str__(self):
        return self.Name

class BaseCharacter:
    def __init__(self, PosX, PosY, Hp):
        self.PosX = PosX
        self.PosY = PosY
        self.Hp = Hp

    def move(self, DeltaX, DeltaY):
        self.PosX += DeltaX
        self.PosY += DeltaY

    def is_alive(self):
        return self.Hp > 0

    def get_damage(self, Amount):
        self.Hp -= Amount

    def get_coords(self):
        return (self.PosX, self.PosY)

class BaseEnemy(BaseCharacter):
    def __init__(self, PosX, PosY, Weapon, Hp):
        super().__init__(PosX, PosY, Hp)
        self.Weapon = Weapon

    def hit(self, Target):
        if not isinstance(Target, MainHero):
            print("Могу ударить только Главного героя")
            return

        self.Weapon.hit(self, Target)

    def __str__(self):
        return f"Враг на позиции ({self.PosX}, {self.PosY}) с оружием {self.Weapon}"

class MainHero(BaseCharacter):
    def __init__(self, PosX, PosY, Name, Hp):
        super().__init__(PosX, PosY, Hp)
        self.Name = Name
        self.Weapons = []
        self.CurrentWeaponIndex = 0

    def hit(self, Target):
        if not self.Weapons:
            print("Я безоружен")
            return

        if not isinstance(Target, BaseEnemy):
            print("Могу ударить только Врага")
            return

        self.Weapons[self.CurrentWeaponIndex].hit(self, Target)

    def add_weapon(self, weapon):
        if not isinstance(weapon,Weapon):
            print("Это не оружие")
            return

        self.Weapons.append(weapon)
        print(f"Подобрал {weapon}")

        if len(self.Weapons) == 1:
            self.CurrentWeaponIndex = 0

    def next_weapon(self):
        if not self.Weapons:
            print("Я безоружен")
            return

        if len(self.Weapons) == 1:
            print("У меня только одно оружие")
            return

        self.CurrentWeaponIndex = (self.CurrentWeaponIndex + 1) % len(self.Weapons)
        print(f"Сменил оружие на {self.Weapons[self.CurrentWeaponIndex]}")

    def heal(self, Amount):
        self.Hp += Amount
        if self.Hp > 200:
            self.Hp = 200
        print(f"Полечился, теперь здоровья {self.Hp}")

# Пример
weapon1 = Weapon("Короткий меч", 5, 1)
weapon2 = Weapon("Длинный меч", 7, 2)
weapon3 = Weapon("Лук", 3, 10)
weapon4 = Weapon("Лазерная пушка", 1000, 1000)
princess = BaseCharacter(100, 100, 100)
archer = BaseEnemy(50, 50, weapon3, 100)
armored_swordsman = BaseEnemy(10, 10, weapon2, 500)
archer.hit(armored_swordsman)
armored_swordsman.move(10, 10)
print(armored_swordsman.get_coords())
main_hero = MainHero(0, 0, "Король Артур", 200)
main_hero.hit(armored_swordsman)
main_hero.next_weapon()
main_hero.add_weapon(weapon1)
main_hero.hit(armored_swordsman)
main_hero.add_weapon(weapon4)
main_hero.hit(armored_swordsman)
main_hero.next_weapon()
main_hero.hit(princess)
main_hero.hit(armored_swordsman)
main_hero.hit(armored_swordsman)