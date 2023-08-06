import molspecutils.alchemy.meta as meta
from molspecutils.happier import CH3Cl_gq_to_dict, CH3Cl_lq_to_dict, HITRANRow
from sqlalchemy import (Column, Float, ForeignKey, Integer, MetaData, String,
                        Table)


def local_state_convert(llq: str, luq: str):
    return CH3Cl_lq_to_dict(llq), CH3Cl_lq_to_dict(luq)


def global_state_convert(glq: str, guq: str):
    return CH3Cl_gq_to_dict(glq), CH3Cl_gq_to_dict(guq) 


def state_dicts(row: HITRANRow):
    """Return state dicts for insertion into db."""
    statepp, statep = local_state_convert(row.llq, row.luq)
    glq, guq = global_state_convert(row.glq, row.guq)
    statepp.update(glq)
    statepp['g'] = row.gpp
    statepp['energy'] = row.elower
    statep.update(guq)
    statep['g'] = row.gp
    statep['energy'] = row.elower+row.nu

    return statepp, statep


def skip_func(statepp: dict, statep: dict) -> bool:
    """Take only nu3 data."""
    nus = ['nu'+str(i) for i in (1, 2, 4, 5, 6)]
    pp = [statepp[nu]==0 for nu in nus]
    p = [statep[nu]==0 for nu in nus]

    return not all(pp + p)


metadata = MetaData()

states = Table(
    "states", metadata,
    Column('id', Integer, primary_key=True),
    Column('energy', Float),    # general
    Column('g', Float),
    Column('J', Integer),     # rotational
    Column('K', Integer),
    Column('l', Integer),
    Column('f', Float),

    Column('rovib', String(2)),

    Column('nu1', Integer),   # vibrational
    Column('nu2', Integer),
    Column('nu3', Integer),
    Column('nu4', Integer),
    Column('nu5', Integer),
    Column('nu6', Integer),
)

line_parameters = meta.line_parameters.to_metadata(metadata)
