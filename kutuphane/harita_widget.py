from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import QPoint
from .veriler.koordinatlar import koordinatlar

class HaritaWidget(QWidget):
    def __init__(self, ebeveyn=None):
        super(HaritaWidget,self).__init__(ebeveyn)
        self.e = ebeveyn
        self.setFixedSize(900, 450)
        self.pin = QPixmap("./resimler/pin.png")
        self.pin_konum = QPoint(-50, -50)

        self.koordinat_pixelleri = {}
        for zone, koordinat in koordinatlar.items():
            pos = self.koordinat_pixel_tespiti(koordinat[1], koordinat[0], zone)
            self.koordinat_pixelleri[pos[0]] = pos[1]

    def ara(self, x, y):
        deger = 1000
        returner = ()
        for i in list(self.koordinat_pixelleri.keys()):
            deger_ = (i[0]-x)**2 + (i[1]-y)**2
            if deger_ < deger:
                deger = deger_
                returner = (i[0],i[1])

        return returner

    def koordinat_pixel_tespiti(self, longitude, latitude, time_zone=""):
        height = 450
        x = (self.width()/2)*(longitude/180)+(self.width()/2)
        y = (height/2)-((height/2)*(latitude/90))
        return ((x, y), time_zone)

    def mousePressEvent(self, event):
        self.pin_konum.setX(event.x()-(self.pin.width()//2))
        self.pin_konum.setY(event.y()-(self.pin.height()//2))
        bolge = self.ara(event.x(), event.y())
        if len(bolge):
            a = self.koordinat_pixelleri[bolge].split("/")
            b = "/".join(a[1:])
            self.e.harita_tiklandi((a[0], b))
        self.update()

    def pin_hareket_ettir(self, bolge_adi):
        pos = koordinatlar[bolge_adi]
        koordinat = self.koordinat_pixel_tespiti(pos[-1], pos[0])
        self.pin_konum.setX(koordinat[0][0] - (self.pin.width() // 2))
        self.pin_konum.setY(koordinat[0][1] - (self.pin.height() // 2))
        self.update()

    def paintEvent(self, event):
        boyayici = QPainter(self)
        boyayici.setRenderHints(QPainter.SmoothPixmapTransform|QPainter.Antialiasing|QPainter.HighQualityAntialiasing)

        boyayici.drawPixmap(QPoint(0, 0), QPixmap("./resimler/harita.png"))
        boyayici.drawPixmap(self.pin_konum, self.pin)