from fastapi import FastAPI

app = FastAPI(title="Pi Platform Demo API", version="1.0.0")

@app.get("/")
def root():
    return {"service": "pi-demo-api", "message": "Deployed with GitHub Actions and Argo CD"}

@app.get("/healthz")
def healthz():
    return {"status": "ok"}
