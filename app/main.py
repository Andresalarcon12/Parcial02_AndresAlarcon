from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal

app = FastAPI(title="Servicio Factorial", version="1.0.0")

class CalcResponse(BaseModel):
    numero: int
    factorial: int
    etiqueta: Literal["par", "impar"]

def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("El factorial no está definido para negativos.")
    res = 1
    for i in range(2, n + 1):
        res *= i
    return res

@app.get("/calc/{n}", response_model=CalcResponse)
def calcular(n: int):
    
    if n < 0:
        raise HTTPException(status_code=400, detail="n debe ser >= 0")
    if n > 2000:
        raise HTTPException(status_code=413, detail="n demasiado grande para cálculo síncrono")

    fac = factorial(n)
    etiqueta = "par" if (n % 2 == 0) else "impar"

    return CalcResponse(numero=n, factorial=fac, etiqueta=etiqueta)
