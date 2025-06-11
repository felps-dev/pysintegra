"""
PySintegra - SINTEGRA magnetic file generator and parser.

A modern Python library for generating and parsing SINTEGRA magnetic files
with Pydantic models for robust validation and type safety.
"""

from .models import (
    BaseRecord,
    Registro10,
    Registro11,
    Registro50,
    Registro51,
    Registro53,
    Registro54,
    Registro55,
    Registro60A,
    Registro60I,
    Registro60M,
    Registro61,
    Registro61R,
    Registro70,
    Registro71,
    Registro74,
    Registro75,
    Registro76,
    Registro85,
    Registro86,
    Registro90,
)
from .processor import ArquivoMagnetico, SintegraProcessor


def get_version() -> str:
    """Get the current version of PySintegra."""
    return "1.0.0"


__version__ = get_version()
__author__ = "Felipe Correa Pereira da Silva"
__license__ = "GNU Lesser General Public License (LGPL)"
__url__ = "https://github.com/felps-dev/pysintegra"

__all__ = [
    "BaseRecord",
    "Registro10",
    "Registro11",
    "Registro50",
    "Registro51",
    "Registro53",
    "Registro54",
    "Registro55",
    "Registro60A",
    "Registro60I",
    "Registro60M",
    "Registro61",
    "Registro61R",
    "Registro70",
    "Registro71",
    "Registro74",
    "Registro75",
    "Registro76",
    "Registro85",
    "Registro86",
    "Registro90",
    "SintegraProcessor",
    "ArquivoMagnetico",
    "get_version",
]
