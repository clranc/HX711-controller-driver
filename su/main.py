import picoweb
import acf_network as w
import coroutines as c
import tinyDB
import routes

wlan = w.connectToParent()

db = tiny.TinyDB()

r = routes.Route(db)

cr = c.Coroutines(db)

app = picoweb.WebApp(__name__,r.ROUTES)

app.run(debug=True, host=wlan.ifconfig()[0], func_list=funcs)
