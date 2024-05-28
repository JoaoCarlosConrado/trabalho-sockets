import os
import fileinput

class changeFiles:
    @staticmethod
    def readFile(name, line_number=1):
        try:
            # Define the path to the file in the /greenhouse directory
            file_path = os.path.join('greenhouse', f"{name}.txt")
            
            # Open the file in read mode (r)
            with open(file_path, 'r') as file:
                # Read the specified line of the file
                for i, line in enumerate(file):
                    if i + 1 == line_number:  # line_number - 1 to match the line indexing starting from 1
                        return line.strip()
                # If the specified line is not found, return an empty string
                return ""
        except FileNotFoundError:
            return f"Error: The file '{file_path}' was not found."
        except Exception as e:
            return f"Error while reading the file: {e}"

    @staticmethod
    def writeFile(name, text):
        try:
            # Define the path to the file in the /greenhouse directory
            file_path = os.path.join('greenhouse', f"{name}.txt")
            
            # Use fileinput to modify the first line
            with fileinput.FileInput(file_path, inplace=True) as file:
                for i, line in enumerate(file):
                    if i == 0:
                        print(text)
                    else:
                        print(line, end='')  # Print the other lines without modification

            return f"File '{file_path}' updated successfully."
        except Exception as e:
            return f"Error while writing to the file: {e}"
        
    @staticmethod
    def getID(name):
        return changeFiles.readFile(name, line_number=2)
        