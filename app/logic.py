from typing import List

from app.core.database import get_engine


QUERY_STATISTICS_GROUP = """
    with estadisticas as (
        select
            g.nombre as grupo,
            e.id as equipo_id,
            e.nombre,
            sum(
                case when e.id = p.local_id then
                    -- partidos local
                    case
                        when p.goles_local > p.goles_visitante then 3
                        when p.goles_local = p.goles_visitante then 1
                        else 0
                    end
                else
                    -- partidos visitante
                    case
                        when p.goles_visitante > p.goles_local then 3
                        when p.goles_visitante = p.goles_local then 1
                        else 0
                    end
                end
            ) as pts,
            sum(
                case when e.id = p.local_id then p.goles_local else p.goles_visitante end
            ) as goles_favor,
            sum(
                case when e.id != p.local_id then p.goles_local else p.goles_visitante end
            ) as goles_contra 
        from
            equipos e
            join equipos_grupos eg on e.id = eg.equipo_id
            join grupos g on eg.grupo_id = g.id
            join partidos p on e.id = p.local_id or e.id = p.visitante_id
        where eg.grupo_id = {grupo_id}
        group by
            e.id,
            e.nombre
    )
    select
        e.*,
        e.goles_favor - e.goles_contra as diferencia
    from estadisticas e
    order by e.pts desc, (e.goles_favor - e.goles_contra) desc
"""


def gral_statistics(teams_list: List[int]):
    pass


def group_statistics(teams_list: List[int]):
    pass


