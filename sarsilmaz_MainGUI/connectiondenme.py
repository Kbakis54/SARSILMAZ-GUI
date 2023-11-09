import threading
import sarsilmaz_MainGUI.mainarayüz as mainarayüz  # PyQt5 uygulamanızın adını buraya ekleyin
import sarsilmaz_MainGUI.mainMap as mainMap  # Tkinter uygulamanızın adını buraya ekleyin

def run_pyqt():
    app = mainarayüz.create_app()  # PyQt5 uygulamanızı başlatın
    app.exec_()

def run_tkinter():
    root = mainMap.create_root()  # Tkinter uygulamanızı başlatın
    root.mainloop()

if __name__ == "__main__":
    # İki farklı thread oluşturarak her bir GUI uygulamasını çalıştırın
    pyqt_thread = threading.Thread(target=run_pyqt)
    tkinter_thread = threading.Thread(target=run_tkinter)

    pyqt_thread.start()
    tkinter_thread.start()

    pyqt_thread.join()
    tkinter_thread.join()
