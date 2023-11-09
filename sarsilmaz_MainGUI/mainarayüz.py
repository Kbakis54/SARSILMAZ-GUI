from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from sarsgui_taslak import Ui_MainWindow
import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import QTimer
from geopy.geocoders import OpenCage
from PyQt5.QtGui import QFont,  QColor
from connecBaglanti import connect, connection_string, vehicle , VehicleMode, LocationLocal
from attitude_indicator import AttitudeIndicator
import datetime
import time
import math

# print("Simülatör başlatılıyor (SITL)")
# connection_string = "tcp:127.0.0.1:5762"

# print("Araç şurada bağlanıyor: %s" % (connection_string,))
# vehicle = connect(connection_string, wait_ready=False)
# # lat = vehicle.lsocation.global_relative_frame.lat
# lon = vehicle.location.global_relative_frame.lon

opencage_api_key = "52a94988093548da915e5528202b0290"

class MainPage(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # if had is None:
        #     from gyrosanirim import HUDWindow
        #     self.had = HUDWindow(self)
        # else:
        #     self.had = had

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("SarsGUI")
        print("Opening SARSGui..")
        self.ai_widget = AttitudeIndicator(self)
        
        # frame_ai'ye bir QVBoxLayout ekleyin
        frame_layout = QVBoxLayout(self.ui.frame_ai)
        frame_layout.addWidget(self.ai_widget)
                      
   
        # self.init_layout()  # Yeni eklediğimiz fonksiyonu çağırın

        #self.frame_map = self.ui.frame_map


        #invicible connect text
        warn = "Warning: You must be connected to the vehicle"
        self.ui.label_warn.setText(warn)
        font = QFont()
        self.ui.label_warn.setFont(font)   
        font_color = QColor(82, 99, 145) #invicible rgb code
        self.ui.label_warn.setStyleSheet(f"color: {font_color.name()};")

    # #     self.ui.pushButton.clicked.connect(self.connected)
    # # def connected(self) :
    # #     if "tcp:127.0.0.1:5762" == self.ui.comboBox.currentText() :
    # #         self.ui.label_warn.setText("Vehicle Connected")
    # #         font = QFont()
    # #         font.setPointSize(18) 
    # #         self.ui.label_warn.setFont(font)   
    # #         font_color = QColor(0, 200, 0)  # Kırmızı bir font rengi
    # #         self.ui.label_warn.setStyleSheet(f"color: {font_color.name()};")

        self.timer = QTimer()
        self.timer.start(500)
        self.timer.timeout.connect(self.update_location_and_marker)
        self.timer.timeout.connect(self.update)
        self.armtimer = QTimer()
        self.armtimer.timeout.connect(self.updatearm)
        # self.timer=QTimer()
        # self.timer.timeout.connect(self.update)
        # self.timer.start(500)
        self.arm = False
        self.counter = 0
        
        self.ui.pushButton_arm.clicked.connect(self.armcom)
        self.ui.pushButton_disarm.clicked.connect(self.disarmcom)
        self.ui.pushButton_reboot.clicked.connect(self.rebootcom)
        self.ui.pushButton_modeSelect.clicked.connect(self.modechange)
        self.ui.pushButton_back.clicked.connect(self.go_backward)
        self.ui.pushButton_forwrd.clicked.connect(self.go_forward)
        self.ui.pushButton_left.clicked.connect(self.go_left)
        self.ui.pushButton_right.clicked.connect(self.go_right)
    def modechange(self, nowmode) :
        nowmode = self.ui.comboBox_mode.currentText()
        vehicle.mode = VehicleMode(str(nowmode))

    def rebootcom(self) :
        vehicle.reboot()
    def armcom(self) :
        vehicle.arm()
    def disarmcom(self) :
        vehicle.disarm()
    def updatearm(self) :
        self.counter += 1
        self.ui.label_atime.setText(str(self.counter))

    
    def go_right(self) :
        vehicle.channels.overrides['1'] = 1800
        time.sleep(0.5)
        vehicle.channels.overrides['1'] = 1500

    def go_left(self) :
        vehicle.channels.overrides['1'] = 1200
        time.sleep(0.5)
        vehicle.channels.overrides['1'] = 1500

    def go_forward(self) :
        vehicle.channels.overrides['2'] = 1200
        time.sleep(0.5)
        vehicle.channels.overrides['2'] = 1500

    def go_backward(self) :
        vehicle.channels.overrides['2'] = 1800
        time.sleep(0.5)
        vehicle.channels.overrides['2'] = 1500




    def update_location_and_marker(self):
        # self.armtimer = QTimer()
        # self.armtimer.start(1000)
        # self.armtimer.timeout.connect(self.armUpdate)  
        lat = vehicle.location.global_relative_frame.lat
        lon = vehicle.location.global_relative_frame.lon
        geolocator = OpenCage(api_key= opencage_api_key)
        location = geolocator.reverse((lat, lon), exactly_one=True)

        if location:
            address = location.raw.get('formatted')
        else:
            address = "Bilinmeyen Adres"
        warn = "Warning: You must be connected to the vehicle"
        self.ui.label_warn.setText(warn)
        font = QFont()
        self.ui.label_warn.setFont(font)   
        font_color = QColor(82, 99, 145) #invicible rgb code
        self.ui.label_warn.setStyleSheet(f"color: {font_color.name()};")
        #home location
        homeloc = vehicle.home_location
        self.ui.label_homeloc.setText(str(homeloc))
        font.setPointSize(14)  # Yazı büyüklüğünü ayarlayın
        self.ui.label_adress.setFont(font)
        #home distance
        homedis = round(LocationLocal.distance_home(vehicle.location.local_frame),2)
        self.ui.label_homedistance.setText(str(homedis))
        font.setPointSize(14)  # Yazı büyüklüğünü ayarlayın
        self.ui.label_adress.setFont(font)
        #datatime
        now = datetime.datetime.now()
        self.ui.label_dtime.setText(now.strftime("%H:%M:%S"))
        #adress
        self.ui.label_adress.setText(str(address))
        font = QFont()
        font.setPointSize(14)  # Yazı büyüklüğünü ayarlayın
        self.ui.label_adress.setFont(font)
        #gps
        self.ui.label_gps.setText(str(vehicle.gps_0))
        font.setPointSize(14) 
        self.ui.label_gps.setFont(font)
        #air speed
        arr = vehicle.airspeed
        rounded_arr = round(arr, 3)
        airsped = str(rounded_arr) + ' m/s'
        self.ui.label_as.setText(str(airsped))
        font.setPointSize(14) 
        self.ui.label_as.setFont(font)
        #batterycurrent,level,voltage
        self.ui.label_batterycur.setText(str(vehicle.battery.current))
        font.setPointSize(14) 
        self.ui.label_batterycur.setFont(font)
        self.ui.label_batterylev.setText(str(vehicle.battery.level))
        font.setPointSize(14) 
        self.ui.label_batterylev.setFont(font)
        self.ui.label_batteryvol.setText(str(vehicle.battery.voltage))
        font.setPointSize(14) 
        self.ui.label_batteryvol.setFont(font)        
        #longtitude
        self.ui.label_lon.setText(str(vehicle.location.global_relative_frame.lon))
        font.setPointSize(14) 
        self.ui.label_lon.setFont(font)
        #latitude
        self.ui.label_lat.setText(str(vehicle.location.global_relative_frame.lat))
        font.setPointSize(14) 
        self.ui.label_lat.setFont(font)
        #velocity
        self.ui.label_velo.setText(str(vehicle.velocity))
        font.setPointSize(14) 
        self.ui.label_velo.setFont(font)
        #altitude
        altidude = str(vehicle.location.global_relative_frame.alt) + ' m'
        self.ui.label_alt.setText(str(altidude))
        font.setPointSize(14) 
        self.ui.label_alt.setFont(font)
        #ground speed
        grr = vehicle.groundspeed
        rounded_grr = round(grr, 3)
        grsped = str(rounded_grr) + ' m/s'
        self.ui.label_gs.setText(str(grsped))
        font.setPointSize(14) 
        self.ui.label_gs.setFont(font)
        #ekf
        if vehicle.ekf_ok == True:
            ekfok = "EKF"
            self.ui.label_ekf.setText(ekfok)
            font = QFont()
            font.setPointSize(14) 
            self.ui.label_ekf.setFont(font)   
            font_color = QColor(0, 200, 0)  # Kırmızı bir font rengi
            self.ui.label_ekf.setStyleSheet(f"color: {font_color.name()};")
        else :
            ekfok = "EKF"
            self.ui.label_ekf.setText(ekfok)
            font = QFont()
            font.setPointSize(11) 
            self.ui.label_ekf.setFont(font)   
            font_color = QColor(200, 0, 0)  # Kırmızı bir font rengi
            self.ui.label_ekf.setStyleSheet(f"color: {font_color.name()};")
        #arm
        if vehicle.armed == True: 

            armyazi = "ARM"          
            self.ui.label_ARM.setText(armyazi)
            font = QFont()
            font.setPointSize(24) 
            self.ui.label_ARM.setFont(font)   
            font_color = QColor(0, 200, 0)  # Yeşil bir font rengi
            self.ui.label_ARM.setStyleSheet(f"color: {font_color.name()};")
            
        elif vehicle.armed == False:
            if self.arm == False:
                self.armtimer.start(1000)
                self.arm == True   
                self.counter = 0         
            armyazi = "ARM"          
            self.ui.label_ARM.setText(armyazi)
            font = QFont()
            font.setPointSize(24) 
            self.ui.label_ARM.setFont(font)   
            font_color = QColor(200, 0, 0)  # Kırmızı bir font rengi
            self.ui.label_ARM.setStyleSheet(f"color: {font_color.name()};")
        #İsArmable       
        if vehicle.is_armable == True:
            isarm = "Yes"
            self.ui.label_isarmable.setText(isarm)
            font = QFont()
            font.setPointSize(14) 
            self.ui.label_isarmable.setFont(font)   
            font_color = QColor(0, 200, 0)  # Kırmızı bir font rengi
            self.ui.label_isarmable.setStyleSheet(f"color: {font_color.name()};")
        else :
            isarm = "No"
            self.ui.label_isarmable.setText(isarm)
            font = QFont()
            font.setPointSize(14) 
            self.ui.label_ekf.setFont(font)   
            font_color = QColor(200, 0, 0)  # Kırmızı bir font rengi
            self.ui.label_isarmable.setStyleSheet(f"color: {font_color.name()};")        





        #mode
        self.ui.label_mode_out.setText(str(vehicle.mode.name))
        font.setPointSize(14) 
        self.ui.label_gps.setFont(font)
        # print(vehicle.attitude.roll)
        # print(vehicle.attitude.pitch)

#######################################
        
    def updatePitch(self, pitch):
        pitch = math.degrees(vehicle.attitude.pitch)
        self.ai_widget.setRoll(pitch)

    def updateRoll(self, roll):
        roll = math.degrees(vehicle.attitude.roll)
        self.ai_widget.setPitch((roll))
    
    def update(self):
        self.updateRoll(float(math.degrees(vehicle.attitude.roll)))
        self.updatePitch(float(math.degrees(vehicle.attitude.pitch)))
    
def main():
    uygulama = QApplication([])
    pencere = MainPage()
    pencere.show()
    sys.exit(uygulama.exec_())

if __name__ == "__main__":
    # from mainMap import root_tk
    # root_tk.mainloop()
    main()
    # root_tk.mainloop()
# def arayuz() :
#     p1 = Process(target= main())
#     p2 = Process(root_tk.mainloop())
    
#     p1.start
#     p2.start
# if __name__ == '__main__' :
#     arayuz()
