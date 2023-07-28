from typing import List
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker

from app.core.database import engine, get_session
from app import queries


Base = declarative_base()


class EstadisticasGral(Base):
    __tablename__ = "estadisticas_gral"
    equipo_id = Column(Integer, primary_key=True)
    pts = Column(Integer)
    goles_favor = Column(Integer)
    goles_contra = Column(Integer)
    diferencia = Column(Integer)


class EstadisticasGrupo(Base):
    __tablename__ = "estadisticas_grupo"
    equipo_id = Column(Integer, primary_key=True)
    grupo_id = Column(Integer, primary_key=True)
    pts = Column(Integer)
    goles_favor = Column(Integer)
    goles_contra = Column(Integer)
    diferencia = Column(Integer)


def get_statistics(teams_list: List[int], only_group_statistics=False):
    """
    Obtener el cálculo.
    """
    if only_group_statistics:
        query = queries.QUERY_STATISTICS_TEAM_ONLY_GROUP_MATCHS
    else:
        query = queries.QUERY_STATISTICS_TEAM

    query = text(query.format(teams_id=",".join(str(t) for t in teams_list)))
    statistic = []

    with get_session() as db:
        result = db.execute(query).fetchall()

    for row in result:
        dict_row = dict(zip(row._mapping.keys(), row))
        statistic.append(dict_row)

    return statistic


def insert_or_update_statistic(statistic: List[dict], for_group=False):
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    if for_group:
        statistic = EstadisticasGrupo(**statistic)
    else:
        statistic = EstadisticasGral(**statistic)

    session.merge(statistic)
    session.commit()
    session.close()


def gral_statistics(teams_list: List[int]):
    statistics = get_statistics(teams_list)

    for statistic in statistics:
        # quito campo que no se usa en EstadisticasGral
        # Esto debería hacerse a partir de un schema en el select!
        statistic.pop("grupo_id")
        insert_or_update_statistic(statistic)

    return {"message": "ok"}


def group_statistics(teams_list: List[int]):
    statistics = get_statistics(teams_list, True)

    for statistic in statistics:
        insert_or_update_statistic(statistic, True)

    return {"message": "ok"}
