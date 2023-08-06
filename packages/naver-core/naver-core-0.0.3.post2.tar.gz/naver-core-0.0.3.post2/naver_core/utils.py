import json
import ast
import os
import pandas as pd
from .dto import *


def import_excel_to_db(root, file, sheet, table, nbd, test=True):

    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(root)))
    FILE_PATH = os.path.join(ROOT_DIR, f"imports\\{file}")
    current_excel = pd.read_excel(FILE_PATH, sheet_name=f"{sheet}").fillna(
        "").replace("\'", "", regex=True)
    current_dto = AnyListDto(current_excel.to_dict(orient='records'), False)
    # print(current_dto.__dict__)
    if not test:
        for child in current_dto.children:
            res = nbd.persistence.insertDto(child, f"{table}")
            res["session"].commit()


def any_module(file, max):
    import os
    import sys
    parent = os.path.dirname(os.path.abspath(file))
    for i in range(0, max):
        parent = os.path.dirname(parent)
        sys.path.insert(0, parent)


def jsonConvert(data):
    return json.loads(json.dumps(data, indent=4, sort_keys=True, default=str))


def replaceDictIf(data, key, replacement):
    """Método para remplazar un valor de un diccionario en caso de que coincida con una llave
    Args:
        data (dict): Diccionario con los datos de entrada
        key (str): Llave del diccionario
        replacement (any): Valor por defecto

    Returns:
        any: Valor del diccionario o el valor por defecto
    """
    assert isinstance(data, dict)
    return str(data.get(key)).replace(" ", "") or replacement


def replaceIf(value, key, replacement):
    """Método para remplazar un valor en caso de que coincida con una llave

    Args:
        value (any): Valor a comparar
        key (any): Llave a comparar
        replacement (any): Valor por defecto

    Returns:
        any: Valor por defecto o el valor de entrada
    """
    if value == key:
        return replacement
    return value


def prepareJsonData(data):
    """Prepara datos de  para convertir a JSON con double Quote debido que los atributos vienen con sigle quote

    Args:
        data (dict): data de ingreso

    Returns:
        dict: json procesado
    """
    replaced = json.dumps(str(data).replace("'", '"').replace('"s ', 's '))
    converted = json.loads(jsonConvert(replaced))
    jsondata = (ast.literal_eval(converted))
    return jsondata
