# import a groupby() method
# from itertools module
from itertools import groupby
  
def datagroup(data, key):
    """Método para agrupar datos por una clave

    Args:
        data (list): Lista de datos a agrupar
        key (str): Clave por la cual se agruparán los datos

    Returns:
        list: Lista de datos agrupados por la clave
    """
    # sort the data on the basis of key    
    # define a fuction for key
    def key_func(k):
        return k[key]
    
    # sort data data by key key.
    data = sorted(data, key=key_func)

    res = []

    for key, value in groupby(data, key_func): 
        res.append(list(value))

    print(res)