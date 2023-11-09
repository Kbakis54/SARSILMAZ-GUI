from dronekit import Command, connect, VehicleMode, LocationGlobalRelative, LocationLocal,__init__

# print("Simülatör başlatılıyor (SITL)")
connection_string = "tcp:127.0.0.1:5762"

print("Araç şurada bağlanıyor: %s" % (connection_string,))
vehicle = connect(connection_string, wait_ready=False)
# print(vehicle.gimbal.rotate(roll=int(vehicle.attitude.roll),pitch=int(vehicle.attitude.pitch), yaw=int(vehicle.attitude.yaw)))
lat = vehicle.location.global_relative_frame.lat
lon = vehicle.location.global_relative_frame.lon


# #        self.ui.pushButton.clicked.connect(self.connect)
#     def connect(self, string) :
#         connection_string = self.ui.comboBox.currentText()
#         string = connection_string
#         connect(connectsdef mainmain() :
#     map()
#     arayuz()
#     p1 = Process(target=main)
#     p2 = Process(target=root_tk)

#     p1.start()
#     p2.start()
#     p1.join()
#     p2.join()
# mainmain()ion_string, wait_ready=False)
