from fastapi import FastAPI 
 
app = FastAPI(title="MVP DataOps Docente") 
 
@app.get("/") 
def root(): 
    return {"message": "API MVP DataOps Docente activa"} 
 
@app.get("/health") 
def health(): 
    return {"status": "ok"} 
