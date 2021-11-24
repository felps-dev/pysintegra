
from pysintegra.registros import Registro10


class ArquivoMagnetico(object):
    registros = []

    def __str__(self):
        return self.registros

    def add_registro_10(self, *args):
        self.registros.append(Registro10(*args))
