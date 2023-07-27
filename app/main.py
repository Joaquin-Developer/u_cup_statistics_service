from typing import List
from fastapi import Query, FastAPI

from app import logic


app = FastAPI()


@app.post("/estadisticas/grupo")
def estadisticas_grupo(equipos_id: List[int] = Query(None)):
    return logic.group_statistics(equipos_id)


@app.post("/estadisticas/general")
def estadisticas_gral(equipos_id: List[int] = Query(None)):
    return logic.gral_statistics(equipos_id)
