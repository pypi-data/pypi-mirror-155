import json
from .utils import jsonConvert
from psycopg2 import DataError



def checkErrorLenght(e, code):
    if len(e.args) > 1:
        return {'data': None, 'state': False, 'code': e.args[0], 'message': e.args[1]}
    else:
        return {'data': None, 'state': False, 'code': code, 'message': e.args[0]}


def ErrorResponse(e):
    if isinstance(e, Exception):
        return checkErrorLenght(e,500)
    if isinstance(e, ValueError):
         return checkErrorLenght(e,500)
    if isinstance(e, TypeError):
         return checkErrorLenght(e,500)
    if isinstance(e, DataError):
        return checkErrorLenght(e,500)
    if isinstance(e, dict):
        return e
    print(str(e))
    error = eval(str(e))
    data = {'data': None, 'state': False,
            'code': error[0], 'message': error[1]}
    res = jsonConvert(data)
    return res


def Ok(e):
    if isinstance(e, dict):
        return {'data': e, 'state': True, 'code': None, 'message': None}
    if isinstance(e, list):
        l = []
        for i in e:
            l.append((i))
        return {'data': l, 'state': True, 'code': None, 'message': None}
    data = e
    data = {'data': data, 'state': True, 'code': None, 'message': None}
    res = jsonConvert(data)
    return res


def getValue(input, key):
    data = input.get('data')
    if isinstance(data, dict):
        if key in data:
            return data[key]
        else:
            return None
    else:
        return None


if __name__ == '__main__':
    pass
