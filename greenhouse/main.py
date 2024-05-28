from time import sleep
from greenhouse.changeFiles import changeFiles as cf
import random

def calculateTemperature():
    temperature_str = cf.readFile("temperature")
    try:
        temperature = float(temperature_str)
    except ValueError:
        print(f"Error: Could not convert '{temperature_str}' to float. Initializing to 25.0.")
        temperature = 25.0
        cf.writeFile("temperature", temperature)

    heater = cf.readFile("heater")
    cooler = cf.readFile("cooler")
    if heater == "ACTIVE":
        temperature += 0.2
    if cooler == "ACTIVE":
        temperature -= 0.2
    if heater == "DISABLED" and cooler == "DISABLED":
        temperature += random.uniform(-0.1, 0.1)
    temperature = round(temperature, 2)
    cf.writeFile("temperature", temperature)

def calculateHumidity():
    humidity_str = cf.readFile("humidity")
    try:
        humidity = float(humidity_str)
    except ValueError:
        print(f"Error: Could not convert '{humidity_str}' to float. Initializing to 50.0.")
        humidity = 50.0
        cf.writeFile("humidity", humidity)

    irrigationsystem = cf.readFile("irrigationsystem")
    if irrigationsystem == "ACTIVE":
        humidity += 0.5
    else:
        humidity -= 0.01
    humidity = round(humidity, 2)
    cf.writeFile("humidity", humidity)

def calculateCO2Level():
    co2level_str = cf.readFile("co2level")
    try:
        co2level = float(co2level_str)
    except ValueError:
        print(f"Error: Could not convert '{co2level_str}' to float. Initializing to 500.0.")
        co2level = 500.0
        cf.writeFile("co2level", co2level)

    co2injector = cf.readFile("co2injector")
    if co2injector == "ACTIVE":
        co2level += 3
    else:
        co2level -= 0.02
    co2level = round(co2level, 2)
    cf.writeFile("co2level", co2level)

# Initial setup
cf.writeFile("temperature", "25") # Celsius
cf.writeFile("humidity", "50") # Percentage
cf.writeFile("co2level", "500") # PPM
cf.writeFile("heater", "DISABLED")
cf.writeFile("cooler", "DISABLED")
cf.writeFile("irrigationsystem", "DISABLED")
cf.writeFile("co2injector", "DISABLED")

while True:
    sleep(1)
    calculateTemperature()
    calculateHumidity()
    calculateCO2Level()
    
    print("Temperature:", cf.readFile("temperature"), "°C")
    print("Humidity:", cf.readFile("humidity"), "%")
    print("CO2 Level:", cf.readFile("co2level"), "ppm")