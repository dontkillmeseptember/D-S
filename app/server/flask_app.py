from misc.libraries import Flask, Thread

app = Flask(__name__)

@app.route('/')
def home():
  return "🪷 D & S - V1.0.0"

def run():
  app.run(host='0.0.0.0', port=80)

def keep_alive():
  t = Thread(target=run)
  t.start()