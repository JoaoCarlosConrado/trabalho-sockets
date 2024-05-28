from sdtp.sdtpClient import *
from client.setupData import setupDataScreen
import client.globalVars as gv
import json


def setupScreen():
    print("Setup Greenhouse")
    print("1. Configure Temperature")
    print("2. Configure Humidity Percentage")
    print("3. Configure CO2 Level")
    print("4. View current settings")
    print("0. Back to Main Screen")
    choice = input("Enter your choice: ")
    if choice == "1":
        setupDataScreen("temperature")
    elif choice == "2":
        setupDataScreen("humidity")
    elif choice == "3":
        setupDataScreen("co2")
    elif choice == "4":
        viewCurrentSettings()
    elif choice == "0":
        return
    else:
        print("Invalid choice")
        return
    return
    
def viewCurrentSettings():
    try:
        message = SettingsRequestMessage(gv.KEY, "GET", "temperature", 0, 0, "CELSIUS")
        response = send_request("127.0.0.1", 65433, message)
        response = json.loads(response)
        if response["status"] == "OK":
            print(f"Temperature: Min: {response['min']}°C, Max: {response['max']}°C")
        else:
            raise Exception(response["message"])
        
        message = SettingsRequestMessage(gv.KEY, "GET", "humidity", 0, 0, "PERCENTAGE")
        response = send_request("127.0.0.1", 65433, message)
        response = json.loads(response)
        if response["status"] == "OK":
            print(f"Humidity: Min: {response['min']}%, Max: {response['max']}%")
        else:
            raise Exception(response["message"])
        
        message = SettingsRequestMessage(gv.KEY, "GET", "co2", 0, 0, "PPM")
        response = send_request("127.0.0.1", 65433, message)
        response = json.loads(response)
        if response["status"] == "OK":
            print(f"CO2 Level: Min: {response['min']}PPM, Max: {response['max']}PPM")
        else:
            raise Exception(response["message"])
        
    except Exception as e:
        print("Error getting settings:", e)
        return
