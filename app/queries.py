
QUERY_STATISTICS_TEAM = """
    with estadisticas as (
        select
            e.id as equipo_id,
            eg.grupo_id,
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
            join partidos p on e.id = p.local_id or e.id = p.visitante_id
        where e.id in ({teams_id})
        group by
            e.id
        union
        select
            e.id as equipo_id,
            eg.grupo_id,
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
            join enfrentamientos p on e.id = p.local_id or e.id = p.visitante_id
        where e.id in ({teams_id})
        group by
            e.id
    )
    select
        e.equipo_id,
        e.grupo_id,
        sum(e.pts) as pts,
        sum(goles_favor) as goles_favor,
        sum(goles_contra) as goles_contra,
        sum(goles_favor) - sum(goles_contra) as diferencia
    from estadisticas e
    group by e.equipo_id
    order by
        sum(e.pts) desc,
        sum(goles_favor) - sum(goles_contra) desc
"""


QUERY_STATISTICS_TEAM_ONLY_GROUP_MATCHS = """
    with estadisticas as (
        select
            e.id as equipo_id,
            eg.grupo_id,
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
            join partidos p on e.id = p.local_id or e.id = p.visitante_id
        where e.id in ({teams_id})
        group by
            e.id
    )
    select
        e.equipo_id,
        e.grupo_id,
        e.pts as pts,
        e.goles_favor as goles_favor,
        e.goles_contra as goles_contra,
        e.goles_favor - e.goles_contra as diferencia
    from estadisticas e
    group by e.equipo_id
    order by
        e.pts desc,
        e.goles_favor - e.goles_contra desc
"""