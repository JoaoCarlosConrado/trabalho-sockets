from sdtp.sdtpClient import *
import client.globalVars as gv


def setupDataScreen(type):
    print(f"setting the {type}")
    print("Set Min Value: ")
    min_ = input()
    print("Set Max Value: ")
    max_ = input()

    if type == "temperature":
        unit_of_measurement = "CELSIUS"
    elif type == "humidity":
        unit_of_measurement = "PERCENTAGE"
    elif type == "co2":
        unit_of_measurement = "PPM"
    

    try:
        message = SettingsRequestMessage(gv.KEY, "SET", type, min_, max_, unit_of_measurement)
        response = send_request("127.0.0.1", 65433, message)
        response = json.loads(response)
        if response["status"] == "OK":
            print("Settings updated successfully")
        else:
            raise Exception(response["message"])
    except Exception as e:
        print("Error setting data:", e)   
    input("Press Enter to continue...")
    return