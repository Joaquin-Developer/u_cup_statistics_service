from typing import List
from fastapi import FastAPI, Request, Query
from fastapi.responses import JSONResponse

from app import logic


app = FastAPI()


@app.exception_handler(Exception)
def custom_exception_handler(_: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content={"message": "Error inesperado. " + str(exc)},
    )


@app.post("/estadisticas/grupo")
def estadisticas_grupo(equipos_id: List[int] = Query(None)):
    return logic.group_statistics(equipos_id)


@app.post("/estadisticas/general")
def estadisticas_gral(equipos_id: List[int] = Query(None)):
    return logic.gral_statistics(equipos_id)
