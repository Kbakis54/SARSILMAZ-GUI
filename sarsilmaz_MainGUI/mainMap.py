import tkinter
import tkintermapview
import time
import threading
import os
from PIL import Image, ImageTk
from connecBaglanti import connect, connection_string, vehicle, lat, lon
lat = vehicle.location.global_relative_frame.lat
lon = vehicle.location.global_relative_frame.lon
# create tkinter window
root_tk = tkinter.Tk()
root_tk.geometry(f"{1000}x{700}")
root_tk.title("SarsGUI Map")

# create map widget
map_widget = tkintermapview.TkinterMapView(root_tk, width=1000, height=700, corner_radius=0)
map_widget.pack(fill="both", expand=True)
print("Opening Map..")
# connection_string = "tcp:127.0.0.1:5762"

# from dsronekit import connect, VehicleMode

# print("Araç şurada bağlanıyor: %s" % (connection_string,))
# vehicle = connect(connection_string, wait_ready=False)
# lat = vehicle.location.global_relative_frame.lat
# lon = vehicle.location.global_relative_frame.lon

# set other tile server (standard is OpenStreetMap)
map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=21)  # google satellite

# set current position and zoom
map_widget.set_position(lat, lon, marker=False)
map_widget.set_zoom(17)

# Önceki marker'ı temizleme işlevini tanımla
def clear_previous_marker():
    map_widget.delete_all_marker()

# Konum güncelleme iş parçacığını başlatın
def update_position():
                          #####1. YOL#######
    #     # Load the image
    # image=Image.open('/home/baki/Desktop/bakiss/images/sarso.png')

    # # Resize the image in the given (width, height)
    # img=image.resize((40, 40))

    # # Conver the image in TkImage
    # plane_image=ImageTk.PhotoImage(img)
                        #####2. YOL#######
    current_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    plane_image = ImageTk.PhotoImage(Image.open(os.path.join(current_path, "images", "sarso.png")).resize((40, 40)))
    

    global lat, lon
    while True:
        lat = vehicle.location.global_relative_frame.lat
        lon = vehicle.location.global_relative_frame.lon
        
        # Her güncelleme işleminden önce önceki marker'ı temizle
        clear_previous_marker()
        
        # Yeni marker'ı ekle
        map_widget.set_marker(lat, lon, text="VTOL", text_color="white", icon=plane_image)
        time.sleep(0.5)

update_thread = threading.Thread(target=update_position)
update_thread.daemon = True
update_thread.start()

root_tk.mainloop()
