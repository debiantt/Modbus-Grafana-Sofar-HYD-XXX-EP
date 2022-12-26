import os,time,logging
from datetime import datetime
from const import *
from logging.handlers import RotatingFileHandler

import minimalmodbus#pip3 install minimalmodbus
import paho.mqtt.client as mqtt #pip3 install paho-mqtt
from influxdb_client.client.write_api import SYNCHRONOUS#pip3 install influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision


#####LOGGING CONFIG##########
logger = logging.getLogger(LOGGER_TEXT)
logger.setLevel(level=eval(LOG_LEVEL))
handler = logging.FileHandler(LOG_FILE)
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=int(LOG_ROTATE_SIZE_BYTES), backupCount=int(LOG_ROTATE_COUNT_FILES))
handler.setLevel(eval(LOG_LEVEL))
formatter = logging.Formatter(LOG_FORMATTER)
handler.setFormatter(formatter)
logger.addHandler(handler)
############################



def connectMQTT():
  clientmqtt = mqtt.Client("", True, None, mqtt.MQTTv31)  
  clientmqtt.connect(MQTT_IP,MQTT_PORT,MQTT_KEEP_ALIVE)
  return clientmqtt

#Conexión modbus
def connectModBus():
  instrument = minimalmodbus.Instrument(MODBUS_USB_PORT, 1)  # port name, slave address (in decimal)
  instrument.serial.baudrate = MODBUS_BAUDIOS  
  instrument.serial.timeout  = int(MODBUS_SERIAL_TIMEOUT)
  instrument.close_port_after_each_call = MODBUS_CLOSE_PORT_AFTER
  return instrument
def writeInflux(item, value):
  try:       
    with InfluxDBClient(url=DDBB_URL, token=DDBB_TOKEN, org=DDBB_ORG) as client:
      write_api = client.write_api(write_options=SYNCHRONOUS)        
      point = Point(item) \
        .tag(item, item) \
        .field(item, value) \
        .time(datetime.utcnow(), WritePrecision.MS)

      write_api.write(DDBB_BUCKET, DDBB_ORG, point)
  except Exception as e:
    logger.error("Error connecting Database: %s " % e)
    logger.error("Trying again in 10 seg")
    time.sleep(10)
    writeInflux(item, value)
  client.close()

#Función inicial  
def initProcess():
  if MQTT is True:  
    clientmqtt=connectMQTT()

  #conectamos con el inversor
  instrument=connectModBus()
  
  values_t = {}
  registers_t=eval(REGISTERS)

  #Construimos un buble infinito para leer cada x seg los valores de modbus, procesarlos e introducirlos en MQTT y/o InfluxDB
  while True:        
    for key in registers_t:    
      register = registers_t[key][0]
      decimal = registers_t[key][1]
      signed = registers_t[key][2]
      try:
        values_t.update({key : instrument.read_register(register, decimal, signed=signed)})
      except IOError as e:      
          logger.error("READ MODBUS - Error reading registry %s" % (e))
      time.sleep(float(DELAY_MODBUS_VALUES_SECONDS))
    instrument.serial.close()  
    
    #Calculamos el total_stream
    values_t.update( { "total_stream" : values_t['stream1'] + values_t['stream2'] } )
    #Modificamos los valores listados en ABS_VALUES a valores absolutos
    for val in ABS_VALUES:    
      values_t.update({val : abs(values_t[val])})
    #Recorremos los valores y los anotamos en MQTT y/o InfluxDB
    for item in values_t.keys():
      if MQTT is True:
        clientmqtt.publish(MQTT_PUBLISH_QUEUE+item, str(values_t[item]))
      if INFLUX is True: 
        writeInflux(item,float(values_t[item]))  
              
    time.sleep(int(READ_SECONDS))
    logger.debug("-->"+str(values_t))


if __name__ == "__main__":
  logger.info('main - Init')  
  logger.info("MQTT: "+str(MQTT)+" <-> INFLUX: "+str(INFLUX))
  initProcess()