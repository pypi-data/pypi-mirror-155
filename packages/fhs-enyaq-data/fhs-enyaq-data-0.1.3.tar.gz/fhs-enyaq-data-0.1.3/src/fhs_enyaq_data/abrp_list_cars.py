"""list abrp."""

from .abrp.abrp_class import abrp_class
from pprint import pprint

def list_cars():
    car_types={}
    abrp = abrp_class(token="")
    result = abrp.get_car_types()
    if result is None:
        print('error getting car types.')
        exit(1)
    for i in result['result']:
        for k in i:
            if 'ENYAQ' in k.upper():
                car_types[k] = i[k]
    return car_types
