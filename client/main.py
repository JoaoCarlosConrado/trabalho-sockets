from sdtp.sdtpClient import *
from client.setupGreenhouse import setupScreen
import client.globalVars as gv
import json

def mainScreen():
    print("Main Screen")
    print("1. View Temperature")
    print("2. View Humidity Percentage")
    print("3. View CO2 Level")
    print("4. Setting up Greenhouse")
    print("0. Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        getTemperature()
    elif choice == "2":
        getHumidity()
    elif choice == "3":
        getCO2Level()
    elif choice == "4":
        setupScreen()
    elif choice == "0":
        print("Exiting...")
        exit()
    else:
        print("Invalid choice")

def getTemperature():
    try:
        message = ValueRequestMessage(gv.KEY, "temperature", "CELSIUS")
        response = send_request("127.0.0.1", 65433, message)
        response = json.loads(response)
        if response["status"] == "OK":
            print(f"Temperature: {response["value"]}°C")
        else:
            raise Exception(response["message"])  # Aqui você levanta uma exceção caso o status não seja "OK"
    except Exception as e:
        print("Error getting:", e)
        return

def getHumidity():
    try:
        message = ValueRequestMessage(gv.KEY, "humidity", "PERCENTAGE")
        response = send_request("127.0.0.1", 65433, message)
        response = json.loads(response)
        if response["status"] == "OK":
            print(f"Humidity: {response['value']}%")
        else:
            raise Exception(response["message"])
    except Exception as e:
        print("Error getting:", e)
        return

def getCO2Level():
    try:
        message = ValueRequestMessage(gv.KEY, "co2", "PPM")
        response = send_request("127.0.0.1", 65433, message)
        response = json.loads(response)
        if response["status"] == "OK":
            print(f"CO2 Level: {response['value']}PPM")
        else:
            raise Exception(response["message"])
    except Exception as e:
        print("Error getting:", e)
        return
    
if __name__ == "__main__":
    while True:
        mainScreen()