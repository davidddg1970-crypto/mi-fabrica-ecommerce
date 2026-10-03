from fastapi import FastAPI, Request, HTTPException
import requests

app = FastAPI(title="Mi Fabrica E-commerce", version="1.0.0")

@app.get("/")
def health_check():
    return {"status": "online", "message": "¡Motor activo!"}

@app.post("/api/v1/generate-landing")
async def generate_landing(request: Request):
    try:
        data = await request.json()
        return {"status": "success", "received": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
