class Registro():

    def __init__(self, *args):
        # Valida se todos os valures atribuídos são válidos.
        i = 0
        for valor in self.__dir__():
            if(valor[0:2] != '__'):
                at = getattr(self, valor)
                at.value = args[i]
                try:
                    at.validar()
                except ValueError as e:
                    raise ValueError(
                        "Erro no " + self.__class__.__name__ + ": " + str(e) + '. Valor: ' + str(args[i]))
                i += 1


class Formato():
    size = 0
    value = 0
    description = 'Nenhuma descrição fornecida'

    def __init__(self, description, size, value):
        self.value = value
        self.size = size
        self.description = description

    def pre_validate(self):
        if(len(str(self.value)) > self.size):
            raise ValueError('O campo ' + self.description +
                             ' excede o tamanho de ' + str(self.size))


class FormatoN(Formato):
    def validar(self):
        super().pre_validate()
        return True


class FormatoX(Formato):
    def validar(self):
        super().pre_validate()
        return True
