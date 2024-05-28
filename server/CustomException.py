
class CustomException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return f"{self.message}"
    
    def getCode(self):
        return f"{self.code}"