#!/usr/bin/python
#########
# About #
#########

#Agua Riego Terraza (Irrigation Water Terrace)
# This script uses a Raspberry Pi to sense for the presense or absense of water. 
# If there ii no water a  email is sent.
# The status is store in a file



###########
# License #
###########
# Released under the WTFPL. 
#Full text and more information here: http://en.wikipedia.org/wiki/WTFPL

########################################
# Mosquitto broker                     #
########################################
mqtt_broker_ip="192.168.1.100"
mqtt_broker_port=1883
mqtt_client_id="MSRPI-terraza"
mqtt_topic_GPIO="/home/ter/ART/GPIO"       	# Topic with watering status in payload 
mqtt_topic_req_read="/home/ter/ART/req_read"     # Topic with request to read water repository state
mqtt_topic_req_water="/home/ter/ART/req_water" 	# Topic with request to water

# Log file
log_file = "/var/log/ART_MQTT.log"

#######################################
# import                              #
#######################################
import RPi.GPIO as GPIO
import string
import datetime
import time
import sys
import paho.mqtt.client as mqtt

# Function Definitions

#Tests whether water is present.
# returns 0 for dry
# returns 1 for wet
# tested to work on pin 18 
def RCtime (RCpin):
    reading = 0
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RCpin, GPIO.OUT)
    GPIO.output(RCpin, GPIO.LOW)
    time.sleep(0.1) 
    GPIO.setup(RCpin, GPIO.IN)
    # This takes about 1 millisecond per loop cycle
    while True:
        if (GPIO.input(RCpin) == GPIO.LOW):
            reading += 1
        
        # stops the reading if there is no current (the C not filling)     
        if reading >= 15000: # Increase this value if the capacitor is bigger or the R is bigger
#            print reading
            return 0  # dry
        if (GPIO.input(RCpin) != GPIO.LOW):
#            print reading
            return 1  # wet
	  
def water(order):	
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(4, GPIO.OUT)
  orderInt = 1  
  try:
    orderInt = int(order)
  except ValueError:
    orderInt = 1
  GPIO.output(4,orderInt)

def on_connect(mqttc, obj, flags, rc):
    log2file("Connected. rc: "+str(rc))

#  Whenever a message from request topic arrives a message with the status is published 
def on_message(mqttc, obj, msg):
    log2file("Message: "+msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    
    if msg.topic == mqtt_topic_req_read:
      mqttc.publish(mqtt_topic_GPIO, RCtime(18),2)
    if msg.topic == mqtt_topic_req_water:
      water(msg.payload)     

def on_publish(mqttc, obj, mid):
    log2file("Publish. mid: "+str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    log2file("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_log(mqttc, obj, level, string):
    log2file("Log: "+ string)

def log2file(log_str):
  
  str2w = str(datetime.datetime.now()).split('.')[0] + " - " + log_str
  f = open(log_file, 'a')
  print >>f, str2w
  
  f.close()
       

def main():
  if not len(sys.argv) == 2:
    print ('usage: ART_MQTTv3.py log_file  ')
    sys.exit(1)

  global log_file
  log_file = sys.argv[1]


  mqttc = mqtt.Client(mqtt_client_id,protocol=3)  
  mqttc.on_message = on_message
  mqttc.on_connect = on_connect
  mqttc.on_publish = on_publish
  mqttc.on_subscribe = on_subscribe                                                                                                                                                      

  mqttc.connect(mqtt_broker_ip, mqtt_broker_port, 60)

  mqttc.subscribe([(mqtt_topic_req_read,0),(mqtt_topic_req_water,0)])

	  
  mqttc.loop_forever()

  
if __name__ == '__main__':
  main()