# ART
Agua Riego Terraza (Irrigation Water Terrace)

##	Historia
Riego automático comercial -> todos los días 10 min
Añadido enchufe programador-> al encender se enciende la bomba-> riego cuando quiero
Problema: no sé cuando se acaba agua. Primeros intentos: [detector de nivel de agua con atmega](http://mc-platforms.blogspot.com.es/2012/01/detector-de-nivel-de-agua-con-atmega.html)

Raspberry en la terraza como servidor de impresión red y airprint y backup de disco. Infrautilizada ->  convertirla en sensor/actuador??

##	Riego con RaspberryPi
###		Raspberry terraza: 
GPIO para leer si hay agua y encender el motor .
Hay un script corriendo en python [ART_MQTTv3.py](https://github.com/jmartinz/ART/blob/master/ART_MQTTv3.py) que se suscribe a dos mensajes el broker MQTT del salón:
* mqtt_topic_req_read="/home/ter/ART/req_read"     # Topic with request to read water repository state-> Usa circuito RC como indica en https://learn.adafruit.com/basic-resistor-sensor-reading-on-raspberry-pi 
* mqtt_topic_req_water="/home/ter/ART/req_water" 	# Topic with request to water -> Enciende/apaga relé. regleta modificada siguiendo pasos en http://diwo.bq.com/regleta-telecontrolada-por-voz/

###	Raspberry salón: 
*	Mosquito (MQTT)
*	Node-RED:
![ART Node red flow](https://github.com/jmartinz/ART/blob/master/img/node-red_jmmp_20150201.png)
