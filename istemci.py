import sys
import os
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QVBoxLayout
from PyQt5 import uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D

class MplCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure()

        self.axes = self.fig.add_subplot(111, projection='3d')

        super().__init__(self.fig)
        

class UcusUygulamasi(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('tasarim.ui', self)

        self.layout = QVBoxLayout()
        self.widget_grafik.setLayout(self.layout)

        self.grafik_tuvali = MplCanvas()
        self.layout.addWidget(self.grafik_tuvali)

        self.btn_sorgula.clicked.connect(self.sorgula_tiklandi)

    def sorgula_tiklandi(self):
        girilen_id = self.txt_ucus_id.text()

        if girilen_id == "":
            QMessageBox.warning(self, "Hata", "Lütfen ID giriniz!")
            return
        
        url = "http://127.0.0.1:5000/ucus-sorgula?id=" + girilen_id

        try:
            cevap = requests.get(url)

            if cevap.status_code == 200:
                veri = cevap.json()

                pilot = veri["pilot"]
                nokta_sayisi = len(veri["rota"])

                mesaj = f"Pilot: {pilot}\nRota Noktası: {nokta_sayisi}"
                self.lbl_sonuc.setText(mesaj)

                x_listesi = []
                y_listesi = []
                z_listesi = []
                
                for nokta in veri["rota"]:
                    x_listesi.append(nokta["x"])
                    y_listesi.append(nokta["y"])
                    z_listesi.append(nokta["z"])

                self.grafik_tuvali.axes.clear()

                self.grafik_tuvali.axes.plot3D(x_listesi, y_listesi, z_listesi, 'blue')

                self.grafik_tuvali.axes.scatter(x_listesi, y_listesi, z_listesi, c='red', marker='o')

                self.grafik_tuvali.axes.set_xlabel('Enlem', labelpad=15)
                self.grafik_tuvali.axes.set_ylabel('Boylam', labelpad=15)
                self.grafik_tuvali.axes.set_zlabel('İrtifa (m)', labelpad=10)

                self.grafik_tuvali.axes.ticklabel_format(useOffset=False, style='plain')

                self.grafik_tuvali.draw()

            else:
                self.lbl_sonuc.setText("Uçuş bulunamadı!")
                self.grafik_tuvali.axes.clear() 
                self.grafik_tuvali.draw()

        except:
            self.lbl_sonuc.setText("Sunucuya bağlanılamadı!")

if __name__ == "__main__":

    os.environ["QT_QPA_PLATFORM"] = "xcb"

    app = QApplication(sys.argv)
    pencere = UcusUygulamasi()
    pencere.show()
    sys.exit(app.exec_())