
from pysintegra.registros import Registro10, Registro11, Registro50


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

    def add_registro_11(self, *args):
        """
            ### Registro 11
            Dados Complementares do Informante;
        """
        self.registros.append(Registro11(*args))

    def add_registro_50(self, *args):
        """
            ### Registro 50
            Registro de total de Nota Fiscal modelos 1 e 1 A, Nota Fiscal/Conta de Energia Elétrica,
            modelo 6, Nota Fiscal de Serviço de Comunicação, modelo 21, e Nota Fiscal de Serviço
            de Telecomunicações, modelo 22, destinado a especificar as informações de totalização
            do documento fiscal, relativamente ao ICMS. No caso de documentos com mais de uma
            alíquota de ICMS e/ou mais de um Código Fiscal de Operação ou Prestação - CFOP,
            deve ser gerado para cada combinação de "alíquota" e "CFOP" um registro tipo 50, com
            valores nos campos monetários (11, 12, 13, 14 e 15) correspondendo à soma dos itens
            que compõe o mesmo, de tal forma que as somas dos valores dos campos monetários
            dos diversos registros que representam uma mesma nota fiscal, corresponderão aos
            valores totais da mesma;
        """
        self.registros.append(Registro50(*args))

    def gerar(self):
        sintegra_txt = ''
        for registro in self.registros:
            sintegra_txt += str(registro)
        return sintegra_txt
