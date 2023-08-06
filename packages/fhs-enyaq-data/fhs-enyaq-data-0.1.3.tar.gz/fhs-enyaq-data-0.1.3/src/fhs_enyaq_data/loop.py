""" Loop. """
import time
from pprint import pprint

from fhs_enyaq_data.mqtt import mqtt_connect, mqtt_publish_instruments

def data_loop(idle_wait=15, drive_wait=5, charge_wait=5, output=print):
    last_km = None
    from .fhs_enyaq_data import get_instruments_with_timeout
    from .config import get_config
    from .abrp_send import send_abrp
    config = get_config()
    # username = config['mqtt']['username'],
    if 'mqtt' in config:
        output('mqtt start')
        mqtt = mqtt_connect(
            host = config['mqtt']['host'],
            port = config['mqtt']['port'],
            tls = config['mqtt'].get('tls', False),
            username = config['mqtt'].get('username', None),
            password = config['mqtt'].get('password', None),
            info_output = output,
        )
    else:
        mqtt = None

    while True:
        # run
        output('get instruments information from skoda connect.')
        instruments = get_instruments_with_timeout(config)
        if instruments is not None:
            output(f"battery level: {instruments['Battery level']}   charging: {instruments['Charging']}")
            send_abrp(config, instruments, output=output)
            if mqtt is not None:
                mqtt_publish_instruments(mqtt, config['mqtt']['topic'], instruments)
                #pprint(instruments)
            sleep_time = idle_wait * 60
            if last_km is None:
                last_km = instruments['Electric range']
            if instruments['Charging'] == 1:
                sleep_time = charge_wait * 60
                output('charging.')
            elif last_km != instruments['Electric range']:
                sleep_time = drive_wait * 60
                output('driving.')
            else:
                output('parked or just starting to drive.')
            last_km = instruments['Electric range']
            output(f"going to sleep for {sleep_time} seconds.")
            time.sleep(sleep_time)
        else:
            output('no instruments returned, sleeping 120 seconds.')
            time.sleep(120)


