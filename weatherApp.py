import sys
import requests
from PyQt5.QtWidgets import (QApplication,QLabel,QWidget,QLineEdit,QPushButton,QVBoxLayout)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ",self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get weather",self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)

        vbox.addWidget(self.description_label)
        
        self.setLayout(vbox)
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.description_label.setObjectName("description_label")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.get_weather_button.setObjectName("get_weather_button")

        self.setStyleSheet("""
                           QLabel,QPushButton{
                           font-family:calibri;
                           }
                           QLabel#city_label{
                               font-size: 40px;
                               font-family:italic;
                           }
                           QLineEdit#city_input{
                           font-size:40px;
                           }
                           QPushButton#get_weather_button{
                           font-size: 30px;
                           font-weight:bold;
                           }
                            QLabel#temperature_label,#description_label{
                           font-size:75px;}

                           QLabel#emoji_label{
                           font-size:100px;
                           font-family:segoe UI emoji;}
                                                      """)
        
        self.get_weather_button.clicked.connect(self.get_weather)
    def get_weather(self):
        api_key = "26d52bfa3538dd42fa9829a8eb01f1a8"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request!\n please enter a valid input.")
                case 401:
                    self.display_error("Not Authorised!\nInvalid API key.")
                case 403:
                    self.display_error("forbidden!\n please enter a valid input.")
                case 404:
                    self.display_error("not found!\nPlase enter a vaild city.")
                case 500:
                    self.display_error("server error!\n please enter a valid input.")
                case 502:
                    self.display_errort("Bad gateway!\n please enter a valid input.")
                case 503:
                    self.display_error("service unavailable!\n please enter a valid input.")
                case 504:
                    self.display_error("gateway timeout!\n please enter a valid input.")
                case _:
                    self.display_error(f"HTTP error!\n{http_error}")
                
        except requests.exceptions.RequestException as  req_error:
            self.display_error(f"Request Error!\n{req_error}")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects!\nCheck the URL.")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error!\nplease check your internet connection.")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error!\nThe request timed out.")
        

        

    def display_error(self,message):
        self.temperature_label.setStyleSheet("Font-size:30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self,data):
        self.temperature_label.setStyleSheet("Font-size:75px;")
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]
        
        
        
        self.temperature_label.setText(f"{temperature_c:.1f}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "🌧"
        elif 300 <= weather_id <= 321:
            return "🌦"
        elif  500 <= weather_id <= 531:
            return "🌨"
        elif 600 <= weather_id <= 622:
            return "❄"
        elif weather_id == 800:
            return "☀"
        

if __name__=='__main__':
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())