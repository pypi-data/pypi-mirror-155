import os
import csv
from datetime import datetime
from prettytable import PrettyTable


class Log:
    file = "logs.csv"

    def __init__(self, file_name=""):
        if file_name == "":
            print(
                f"[INFO] Generating logs file with default name '{self.file}'")
            self.file = self.file
        else:
            print(
                f"[INFO] Generating logs file with custom name '{file_name}'")
            self.file = file_name
        print("[INFO] Pass logs parameter in List or String format only.\n")

    def write(self, content):
        try:
            with open(os.path.join(os.getcwd() + os.sep + self.file), 'a', encoding="utf-8", newline='') as logging:
                writer = csv.writer(logging)
                _now = datetime.now()
                if type(content) == str:
                    writer.writerow([_now, content])
                elif type(content) == list:
                    content.insert(0, _now)
                    writer.writerow(content)
        
        except:
            print("[INFO] Pass logs parameter in String or List or Tuple format only.")

    def _convert(self, _list):
        _str = ""
        for i in _list:
            _str += i + " "
        return _str

    def show(self):
        try:
            _logTable = PrettyTable(["DATETIME", "LOG DATA"])
            with open(os.path.join(os.getcwd() + os.sep + self.file), 'r', encoding="utf-8", newline='') as logging:
                reader = csv.reader(logging)
                for i in reader:
                    _logTable.add_row([i[0], self._convert(i[1:])])

            print(_logTable)
        
        except FileNotFoundError:
            print("[INFO] Log file does not exists.\n[INFO] Please write the logs before showing the data.")
