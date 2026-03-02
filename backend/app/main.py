from fastapi import FastAPI

app = FastAPI(title="Conference Attendees API")


@app.get("/health")
def health():
    return {"status": "ok"}