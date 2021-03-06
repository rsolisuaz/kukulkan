#!/usr/bin/python

import paho.mqtt.client as paho
import signal
import sys
import time

from random import randint
from threading import Thread

def functionDataActuator(status):
    print "Data Actuator Status %s" % status

def functionDataActuatorMqttOnMessage(mosq, obj, msg):
    print "Data Sensor Mqtt Subscribe Message!"
    functionDataActuator(msg.payload)

def functionDataActuatorMqttSubscribe():
    mqttclient = paho.Client()
    mqttclient.on_message = functionDataActuatorMqttOnMessage
    mqttclient.connect("iot.eclipse.org", 1883, 60)
    mqttclient.subscribe("Xcambo/Kukulkan/DataActuator", 0)
    while mqttclient.loop() == 0:
        pass

def functionDataSensor():
    data = randint(0, 65535)
    return data

def functionDataSensorMqttOnPublish(mosq, obj, msg):
    print "Data Sensor Mqtt Published!"

def functionDataSensorMqttPublish():
    mqttclient = paho.Client()
    mqttclient.on_publish = functionDataSensorMqttOnPublish
    mqttclient.connect("iot.eclipse.org", 1883, 60)
    while True:
        data = functionDataSensor()
        topic = "Xcambo/Kukulkan/DataSensor"
        mqttclient.publish(topic, data)
        time.sleep(1)

def functionSignalHandler(signal, frame):
    sys.exit(0)

if __name__ == '__main__':

    signal.signal(signal.SIGINT, functionSignalHandler)

    threadmqttpublish = Thread(target=functionDataSensorMqttPublish)
    threadmqttpublish.start()

    threadmqttsubscribe = Thread(target=functionDataActuatorMqttSubscribe)
    threadmqttsubscribe.start()

    while True:
        print "Hello Xcambo"
        print "Data Sensor: %s " % functionDataSensor()
        time.sleep(5)

# End of File
