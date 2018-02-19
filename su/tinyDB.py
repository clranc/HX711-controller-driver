import btree

class TinyDB:
    def __init__(self):
        try:
            self.file = open("tiny.db", "r+b")
        except OSError:
            self.file = open("tiny.db", "w+b")

        self.db = btree.open(self.file)

    def getConfigs(self):
        return { b"id" : self.db[b"id"], b"host" : self.db[b"host"] }

    def setID(self, id):
        self.db[b"id"] = id
        self.db.flush()

    def setHost(self, host):
        self.db[b"host"] = host
        self.db.flush()
