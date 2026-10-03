from fastapi import FastAPI

app = FastAPI(title="Mi Fabrica E-commerce", version="1.0.0")

@app.get("/")
def read_root():
    return {"status": "online", "message": "¡Robot listo y conectado!"}
