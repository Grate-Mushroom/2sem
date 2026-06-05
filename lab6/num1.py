class BigBell:
    def __init__(self):
        self.IsDing = True

    def sound(self):
        if self.IsDing:
            print("ding")
            self.IsDing = False
        else:
            print("dong")
            self.IsDing = True

bell = BigBell()
bell.sound()
bell.sound()
bell.sound()
bell.sound()
