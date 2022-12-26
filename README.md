# Modbus-Grafana-Sofar-HYD-XXX-EP

Aplicación python de comunicación vía modbus RTU con inversores SOFAR HYD-XXXX-EP y panel grafana+influxdb de visualización de resultados. Requiere dispositivo de comunicación RTU USB (p.e DSD Tech SH-U10). La aplicación es compatible con Raspberry Pi o similar. Escritura de datos en MQTT (mosquitto) opcional.

![alt text](https://github.com/debiantt/Modbus-Grafana-Sofar-HYD-XXX-EP/tree/main/grafana/sc.png?raw=true)


## Dependencias

| Python  | Grafana | Influx  | Mosquitto |
|---------|---------|---------|-----------|
| >= 3.10 |>= 9.3.x | >=2.5   | =>2.0.15  |

## Instalación

git clone https://github.com/debiantt/Modbus-Grafana-Sofar-HYD-XXX-EP.git


## Configuración

**Step 1:** Antes de lanzar la aplicación es necesario configurar la URL de la base de datos InfluxDB.

python/main.ini --> Establecer el valor de las siguiente variable:
        
        DDBB_URL --> InfluxDB URL (p.e http://X.X.X.X:8086)

Opcional (requiere descomentar el bloque MQTT del docker-compose y establecer a True la variable MQTT del archivo python/main.ini):

        MQTT_IP --> <MQTT Server IP>
        MQTT_PUBLISH_QUEUE --> <MQTT_queue>

## Customizar la seguridad (opcional)

El usuario y password por defecto, tanto de Grafana como de InfluxDB es:

    user: admin
    Pass: password

Se puede modificar desde las respectivas consolas de administración (Grafana/InfluxDB):
    
    Grafana --> http://x.x.x.x:3000    
    InfluxDB --> http://x.x.x.x:8086    

El token de acceso a InfluxDB ya está generado y configurado tanto en el archivo python/main.ini como en Grafana.
Si quiere actualizar el token, genérelo desde la consola de administración de InfluxDB (http://x.x.x.x:8086) y realice los siguientes pasos:

python/main.ini --> Establecer el nuevo token en la variable DDBB_TOKEN

Grafana:
    
    Ir a Data Sources/InfluxDB > Settings    
    En "Custom HTTP Headers" hacer clic en el botón "Reset" del Header "Authorization"
    Asignar como value el nuevo token añadiendole "Token " --> "Token hd7eBy4QwOIH8bkAJuZ6cw..."
    Hacer clic en el botón "Save & test"

## Uso

cd /path_to_repository/Modbus-Grafana-Sofar-HYD-XXX-EP

docker-compose up -d

**Acceso Grafana**

    http://x.x.x.x:3000

**Acceso InfluxDB**

    http://x.x.x.x:8086


**Python main.py**

Conectar dispositivo (p.e Raspberry pi) al inversor SOFAR HYD-XXXX-EP a través del conversor USB-RS485 (p.e DSD Tech SH-U10) y lanzar el proceso:
    
    cd /path_to_repository/Modbus-Grafana-Sofar-HYD-XXX-EP/python

    python3 main.py


Si el archivo python/main.ini está correctamente configurado comenzará a escribir en la base de datos InfluxDB toda la información que obtenga vía modbus del
inversor SOFAR.

## Notas

En el directorio info/ existe un documento (SOFAR_HYD_XXXX_EP_modbus.xlsx) con las opciones a consultar del inversor sofar y su código correspondiente. Esas opciones se pueden agregar y/o modificar en el archivo python/main.ini

Modificar la variable MODBUS_USB_PORT (valor por defecto /dev/ttyUSB0) del archivo python/main.ini si fuese necesario para adaptarlo al valor de su dispositivo.







