
from pysintegra.registros import Registro10


class ArquivoMagnetico(object):
    registros = []

    def __str__(self):
        return self.registros

    def add_registro_10(self, *args):
        """
            ### Registro 10
            Registro mestre do estabelecimento, destinado à identificação do estabelecimento
            informante;
        """
        self.registros.append(Registro10(*args))

    def gerar(self):
        sintegra_txt = ''
        for registro in self.registros:
            sintegra_txt += str(registro)
        return sintegra_txt
