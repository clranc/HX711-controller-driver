import btree

newkey_key = "CanIHasCheezBurger"

class TinyDB:
    def __init__(self):
        try:
            self.file = open("tiny.db", "r+b")
            self.db = btree.open(self.file)
        except OSError:
            self.file = open("tiny.db", "w+b")
            self.db = btree.open(self.file)
            self.db[b"key"] = newkey_key
            self.db

    def getKey(self):
        return self.db[b"key"]

    def setKey(self, key):
        self.db[b"key"] = key
        self.db.flush()
