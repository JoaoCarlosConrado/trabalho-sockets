# PORTAS DE COMUNICAÇÃO
TCPSERVERPORT = 65432        
UDPSERVERPORT = 65433      
TCPACTUATORPORT = 65434

# id dos atuadores
HEATERID = None
COOLERID = None
IRRIGATIONSYSTEMID = None
CO2INJECTORID = None

#status dos atuadores
HEATERSTATUS = "DISABLED"
COOLERSTATUS = "DISABLED"
IRRIGATIONSYSTEMSTATUS = "DISABLED"
CO2INJECTORSTATUS = "DISABLED"

# id dos sensores
TEMPERATUREID = None
HUMIDITYID = None
CO2LEVELID = None

#Unidades de medida dos sensores
TEMPERATUREUM = ["CELSIUS"]
HUMIDITYUM = ["PERCENTAGE"]
CO2LEVELUM = ["PPM"]

# valores dos sensores
TEMPERATURE = 0
HUMIDITY = 0
CO2LEVEL = 0

# minimo e maximo configurados para os sensores
# os valores começam assim por padrão, mas podem ser alterados
TEMPERATUREMIN = 29
TEMPERATUREMAX = 31
HUMIDITYMIN = 50
HUMIDITYMAX = 70
CO2LEVELMIN = 1300
CO2LEVELMAX = 1700

KEY = "chavepix"