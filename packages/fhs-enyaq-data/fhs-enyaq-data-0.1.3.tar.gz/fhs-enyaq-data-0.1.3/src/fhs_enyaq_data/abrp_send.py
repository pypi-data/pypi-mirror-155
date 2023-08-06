"""Send abrp."""

from .abrp.abrp_class import abrp_class
from pprint import pprint

def send_abrp(config, data, output=None):
    abrp = abrp_class(token=config['abrp']['token'], car_type=config['abrp'].get('car_type', "skoda:enyaq:21:77:meb"))
    result = abrp.send_data(data)
    if output is not None:
        output(f"abrp send, result: {result}")
    return result
