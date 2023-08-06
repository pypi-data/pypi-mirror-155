
class DataDto(object):
    """Clase de respuesta de la capa de Fachada Web

    Attributes:
        data (dict): Diccionario con los datos de la respuesta
        message (str): Mensaje de la respuesta
        code (int): Codigo de la respuesta
        state (bool): Estado de la respuesta
    """

    def __init__(self, **kwargs):
        self.data = kwargs.get('data', None)
        self.message = kwargs.get('message', None)
        self.code = kwargs.get('code', None)
        self.state = kwargs.get('state', None)

    def __dict__(self):
        return {
            'data': self.data,
            'message': self.message,
            'code': self.code,
            'state': self.state
        }


class AnyDto(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class AnyListDto(object):
    def __init__(self, data, pure=True):
        self.children = list()
        for item in data:
            if pure:
                self.children.append(AnyDto(**item).__dict__)
            else:
                self.children.append(AnyDto(**item))
