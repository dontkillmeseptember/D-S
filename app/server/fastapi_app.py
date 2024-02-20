from misc.libraries import FastAPI, Thread, uvicorn

app = FastAPI()

@app.get("/")
def read_root():
	return {"🪷 D & S - V1.0.5"}

def run():
    uvicorn.run(app, port = 8000, host = "127.0.0.1")

def keep_alive():
	t = Thread(target = run)
	t.start()