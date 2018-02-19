import picoweb as pw
import ujson as uj

class Route:
    def __init__(self,db):
        self.ROUTES = [
                 ("/config",self.configs),
             ]
        self.db = db

    def configs(req, resp):
        yield from picoweb.start_response(resp)

        if req.method == "GET":
            config = self.db.getConfigs()
            yield from resp.awrite(uj.dumps(config))

        elif req.method == "POST":
            id = req.reader().read()
            id = uj.loads(id)
            self.db.setID(id[b"id"])
        yield from resp.awrite(


