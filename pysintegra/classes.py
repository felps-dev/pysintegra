import datetime
from decimal import Decimal
import copy


class Registro():
    """
        Classe Genérica de Registro
    """

    def __str__(self):
        # Serializa o Registro para STR
        i = 0
        final = ''
        for valor in self.__dir__():
            if(valor[0:2] != '__'):
                at = getattr(self, valor)
                final += str(at).ljust(at.size, ' ')
                i += 1
        return final

    def __init__(self, *args):
        # Valida se todos os valures atribuídos são válidos.
        i = 0
        for variavel in self.__dir__():
            if(variavel[0:2] != '__'):
                registro = getattr(self, variavel)
                # Cria uma cópia do registro, caso contrário o python associa ao endereço de memória
                new_registro = copy.copy(registro)
                if(registro.changeable):
                    if(i >= len(args)):
                        raise ValueError(
                            "Erro no " + self.__class__.__name__ + ": Faltando valor para " + registro.description)
                    new_registro.value = args[i]
                    try:
                        new_registro.validar()
                        setattr(self, variavel, new_registro)
                    except ValueError as e:
                        raise ValueError(
                            "Erro no " + self.__class__.__name__ + ": " + str(e) + '. Valor: ' + str(args[i]))
                    i += 1
                else:
                    setattr(self, variavel, new_registro)


class Formato():
    """
        Classe Genérica de Formato
    """
    size = 0
    value = 0
    description = 'Nenhuma descrição fornecida'
    changeable = True
    decimal_places = 2

    def __init__(self, description, size, value, changeable=True, decimal_places=2):
        self.value = value
        self.size = size
        self.description = description
        self.changeable = changeable
        self.decimal_places = decimal_places

    def __str__(self):
        return str(self.value)

    def pre_validate(self):
        if(len(str(self)) > self.size):
            self.raise_error('excede o tamanho de ' + str(self.size))

    def raise_error(self, erro):
        raise ValueError('O campo ' + self.description + ' ' + erro)


class FormatoN(Formato):
    """
        Formato do tipo N, numérico genérico
    """

    def __str__(self):
        return str(self.value).replace('.', '').rjust(self.size, '0')

    def validar(self):
        super().pre_validate()
        return True


class FormatoNData(Formato):
    """
        Formato do tipo N, numérico tipo DATA
    """

    def __str__(self):
        return datetime.datetime.strftime(self.value, '%Y%m%d')

    def validar(self):
        super().pre_validate()
        if(not isinstance(self.value, datetime.date)):
            self.raise_error(' não é do tipo date')
        return True


class FormatoNValor(Formato):
    """
        Formato do tipo N, numérico tipo Valor
    """

    def __str__(self):
        return str("{0:." + str(self.decimal_places) +
                   "}").format(self.value).replace('.', '').rjust(self.size, '0')

    def validar(self):
        super().pre_validate()
        if(not isinstance(self.value, float) and not isinstance(self.value, Decimal)):
            self.raise_error(' não é do tipo float ou Decimal.')
        return True


class FormatoX(Formato):
    """
        Formato do tipo X, string
    """

    def validar(self):
        super().pre_validate()
        return True
