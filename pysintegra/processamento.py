
from pysintegra.registros import Registro10, Registro11, Registro50, Registro51, Registro53, Registro54, Registro55, Registro60A, Registro60I, Registro60M, Registro61, Registro70, Registro71, Registro74, Registro75, Registro76, Registro85, Registro86, Registro90


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

    def add_registro_51(self, *args):
        """
            ### Registro 51
            Registro de total de Nota Fiscal, modelos 1 e 1-A, destinado a especificar as
            informações de totalização do documento fiscal, relativamente ao IPI; 
        """
        self.registros.append(Registro51(*args))

    def add_registro_53(self, *args):
        """
            ### Registro 53
            Registro de total de documento fiscal, quanto à substituição tributária; 
        """
        self.registros.append(Registro53(*args))

    def add_registro_54(self, *args):
        """
            ### Registro 54
            Registro de Mercadoria / Produto (classificação fiscal);
            #### Quem deve apresentar o registro 54?
            Apenas os contribuintes que emitem documento fiscal por processamento de dados (Nota Fiscal Modelo 1
            e 1A). Os contribuintes que apenas escrituram os livros fiscais por processamento estão dispensados de
            apresentar o registro 54, ou a critério de sua Unidade Federada. 
        """
        self.registros.append(Registro54(*args))

    def add_registro_55(self, *args):
        """
            ### Registro 55
            Registro de Guia Nacional de Recolhimentos de Tributos Estaduais - GNRE; 
        """
        self.registros.append(Registro55(*args))

    def add_registro_60M(self, *args):
        """
            ### Registro 60M
            Registro destinado a informar as operações e prestações realizadas com os
            documentos fiscais emitidos por equipamento emissor de cupom fiscal os quais são:
            Cupom Fiscal, Cupom Fiscal - PDV , Bilhete de Passagem Rodoviário, modelo 13,
            Bilhete de Passagem Aquaviário, modelo 14, Bilhete de Passagem e Nota de Bagagem,
            modelo 15, Bilhete de Passagem Ferroviário, modelo 16 e Nota Fiscal de Venda a
            Consumidor, modelo 2; 
        """
        self.registros.append(Registro60M(*args))

    def add_registro_60A(self, *args):
        """
            ### Registro 60A
            Identificador de cada Situação Tributária no final do dia de cada
            equipamento emissor de cupom fiscal; 
        """
        self.registros.append(Registro60A(*args))

    def add_registro_60I(self, *args):
        """
            ### Registro 60I
            Item do documento fiscal emitido por Terminal Ponto de Venda (PDV)
            ou equipamento Emissor de Cupom Fiscal (ECF); 
        """
        self.registros.append(Registro60I(*args))

    def add_registro_61(self, *args):
        """
            ### Registro 61
            Para os documentos fiscais descritos a seguir, quando não emitidos por equipamento
            emissor de cupom fiscal: Bilhete de Passagem Rodoviário, modelo 13, Bilhete de
            Passagem Aquaviário, modelo 14, Bilhete de Passagem e Nota de Bagagem, modelo
            15, Bilhete de Passagem Ferroviário, modelo 16, Nota Fiscal de Venda a Consumidor,
            modelo 2, e Nota Fiscal de Produtor, modelo 4;  
        """
        self.registros.append(Registro61(*args))

    def add_registro_70(self, *args):
        """
            ### Registro 70
            Registro de total de Nota Fiscal de Serviço de Transporte, modelo 7, de Conhecimento
            de Transporte Rodoviário de Cargas, modelo 8, de Conhecimento de Transporte
            Aquaviário de Cargas, modelo 9, de Conhecimento Aéreo, modelo 10, e de
            Conhecimento de Transporte Ferroviário de Cargas, modelo 11, destinado a especificar
            as informações de totalização do documento fiscal, relativamente ao ICMS;  
        """
        self.registros.append(Registro70(*args))

    def add_registro_71(self, *args):
        """
            ### Registro 71
            Registro de Informações da carga transportada referente a Conhecimento de Transporte
            Rodoviário de Cargas, modelo 8, Conhecimento de Transporte Aquaviário de Cargas,
            modelo 9, de Conhecimento Aéreo, modelo 10, e de Conhecimento de Transporte
            Ferroviário de Cargas, modelo 11;  
            #### Quem deve gerar o Registro 71?
            Apenas os prestadores de serviços de transporte. 
        """
        self.registros.append(Registro71(*args))

    def add_registro_74(self, *args):
        """
            ### Registro 74
            Registro de Inventário;
        """
        self.registros.append(Registro74(*args))

    def add_registro_75(self, *args):
        """
            ### Registro 75
            Registro de Código de Produto e Serviço;;
        """
        self.registros.append(Registro75(*args))

    def add_registro_76(self, *args):
        """
            ### Registro 76
            Registro de total de Nota Fiscal de Serviço de Comunicação (modelo 21) e Nota Fiscal de Telecomunicações (modelo 22) nas prestações de serviços.
        """
        self.registros.append(Registro76(*args))

    def add_registro_85(self, *args):
        """
            ### Registro 85
            Informações de Exportações
        """
        self.registros.append(Registro85(*args))

    def add_registro_86(self, *args):
        """
            ### Registro 86
            Informações Complementares de Exportações
        """
        self.registros.append(Registro86(*args))

    def add_registro_90(self, *args):
        """
            ### Registro 90
            Registro de totalização do arquivo, destinado a fornecer dados indicando a quantidade de registros. 
        """
        self.registros.append(Registro90(*args))

    def gerar(self):
        sintegra_txt = ''
        for registro in self.registros:
            sintegra_txt += str(registro)
        return sintegra_txt
