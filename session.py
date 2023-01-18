class Session:
    def __init__(self):
        self.user = None

    def set(self, user):
        self.user = user

    def clear(self):
        self.user = None


session = Session()
