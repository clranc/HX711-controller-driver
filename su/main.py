import picoweb
import acf_network as w
import coroutines as c

wlan = w.connectToParent()

funcs = [c.testRoutine, c.testRoutine2]

app = picoweb.WebApp(__name__)


@app.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite("Yo bro, got your message")


app.run(debug=True, host=wlan.ifconfig()[0], func_list=funcs)
