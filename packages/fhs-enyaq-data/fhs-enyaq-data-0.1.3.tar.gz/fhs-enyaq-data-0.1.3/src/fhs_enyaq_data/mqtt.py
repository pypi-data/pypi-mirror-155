import paho.mqtt.client as mqtt

client = None
output = None

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        if output is not None:
            output("mqtt: Connected successfully")
    else:
        if output is not None:
            output("mqtt: Connect returned result code: " + str(rc))
        else:
            print("mqtt: Connect returned result code: " + str(rc))


def on_publish(client, userdata, result):             #create function for callback
    #print("mqtt: data published \n")
    pass


def mqtt_connect(host, port, tls = False, username=None, password=None, info_output=None):
    global client
    global output
    output = info_output
    client = mqtt.Client()
    client.on_publish = on_publish
    client.on_connect = on_connect

    if tls is True:
        client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)

    if password is not None:
        client.username_pw_set(username, password)

    client.connect(host, port)
    client.loop_start()
    return client

def mqtt_publish(client, topic, value):
    result = client.publish(topic, value)


def mqtt_publish_instruments(client, topic, instruments):
    mqtt_publish(client, f"{topic}/battery_level", instruments['Battery level'])
    mqtt_publish(client, f"{topic}/charging", instruments['Charging'])
    mqtt_publish(client, f"{topic}/charging_power", instruments['Charging power'])
    mqtt_publish(client, f"{topic}/charging_rate", instruments['Charging rate'])
    mqtt_publish(client, f"{topic}/climatisation_target_temperature", instruments['Climatisation target temperature'])
    mqtt_publish(client, f"{topic}/electric_range", instruments['Electric range'])
    mqtt_publish(client, f"{topic}/minimum_charge_level", instruments['Minimum charge level'])


