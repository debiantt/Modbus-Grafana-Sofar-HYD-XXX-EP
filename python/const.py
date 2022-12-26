import configparser
config = configparser.ConfigParser()
# Desde python funciona bien esta linea, pero creando un exe la ruta no es la correcta
# config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '.', 'main.ini'))
#main_config=os.environ.get('SOLAR_CONFIG')
main_config="./main.ini"
config.read(main_config)

#OPTIONS
MQTT = eval(config.get('OPTIONS', 'MQTT'))
INFLUX = eval(config.get('OPTIONS', 'INFLUX'))
READ_SECONDS=config.get('OPTIONS', 'READ_SECONDS', fallback=10)
DELAY_MODBUS_VALUES_SECONDS=config.get('OPTIONS', 'DELAY_MODBUS_VALUES_SECONDS')
ABS_VALUES=eval(config.get('OPTIONS', 'ABS_VALUES'))
REGISTERS=config.get('OPTIONS', 'REGISTERS')
#LOGS
LOG_FORMATTER='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL=config.get('LOG', 'LOG_LEVEL')
LOGGER_TEXT=config.get('LOG', 'LOGGER_TEXT')
LOG_FILE=config.get('LOG', 'LOG_FILE')
LOG_ROTATE_SIZE_BYTES=config.get('LOG', 'LOG_ROTATE_SIZE_BYTES')
LOG_ROTATE_COUNT_FILES=config.get('LOG', 'LOG_ROTATE_COUNT_FILES')

#DDBB
DDBB_TOKEN=config.get('DDBB', 'DDBB_TOKEN')
DDBB_ORG=config.get('DDBB', 'DDBB_ORG')
DDBB_BUCKET=config.get('DDBB', 'DDBB_BUCKET')
DDBB_URL=config.get('DDBB', 'DDBB_URL')
#MQTT
MQTT_USER=config.get('MQTT', 'MQTT_USER')
MQTT_PWD=config.get('MQTT', 'MQTT_PWD')
MQTT_IP=config.get('MQTT', 'MQTT_IP')
MQTT_PORT=config.get('MQTT', 'MQTT_PORT')
MQTT_KEEP_ALIVE=config.get('MQTT', 'MQTT_KEEP_ALIVE')
MQTT_PUBLISH_QUEUE=config.get('MQTT', 'MQTT_PUBLISH_QUEUE')

#MODBUS
MODBUS_USB_PORT=config.get('MODBUS', 'MODBUS_USB_PORT')
MODBUS_BAUDIOS=config.get('MODBUS', 'MODBUS_BAUDIOS')
MODBUS_SERIAL_TIMEOUT=config.get('MODBUS', 'MODBUS_SERIAL_TIMEOUT')
MODBUS_CLOSE_PORT_AFTER=config.get('MODBUS', 'MODBUS_CLOSE_PORT_AFTER')

