from datetime import datetime

class Logger:
    def __init__(self, filename):
        self.filename = filename
        self.log('Init')

    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.filename, "a", encoding='utf-8') as file:
            file.write(f"[{timestamp}] {message}\n")