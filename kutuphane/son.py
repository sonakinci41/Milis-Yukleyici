from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QCheckBox, QRadioButton


class Son(QWidget):
    def __init__(self, ebeveyn=None):
        super(Son, self).__init__(ebeveyn)
        self.e = ebeveyn
        self.kapanacak_mi =False

        kutu = QGridLayout()
        self.setLayout(kutu)

        milis_logo = QLabel()
        milis_logo.setAlignment(Qt.AlignCenter)
        milis_logo.setPixmap(QPixmap("./resimler/milis-logo.svg"))
        kutu.addWidget(milis_logo,0,0,1,2)

        self.veda_label = QLabel()
        self.veda_label.setAlignment(Qt.AlignCenter)
        self.veda_label.setWordWrap(True)
        kutu.addWidget(self.veda_label,1,0,1,2)

        self.denemeye_devam = QRadioButton()
        self.denemeye_devam.setIcon(QIcon("./resimler/cik.svg"))
        self.denemeye_devam.setIconSize(QSize(50,50))
        self.denemeye_devam.toggled.connect(self.degisti)
        kutu.addWidget(self.denemeye_devam,2,0,1,1)
        self.kapat = QRadioButton()
        self.kapat.setIcon(QIcon("./resimler/yeniden-baslat.svg"))
        self.kapat.setIconSize(QSize(50,50))
        self.kapat.toggled.connect(self.degisti)
        kutu.addWidget(self.kapat,2,1,1,1)

        self.denemeye_devam.setChecked(True)

    def degisti(self):
        if self.kapat.isChecked():
            self.kapanacak_mi = True
        else:
            self.kapanacak_mi = False

    def showEvent(self, event):
        self.e.setWindowTitle(self.e.d[self.e.s_d]["Yükleme Tamamlandı"])
        self.veda_label.setText(self.e.d[self.e.s_d]["Milis Linux başarıyla yüklendi. Milis Linux yüklediğiniz için teşekkür ederiz. İsterseniz sistemi denemeye devam edebilirsiniz. Veya tekrar başlatıp sisteminizi kullanbilirsiniz."])
        self.denemeye_devam.setText(self.e.d[self.e.s_d]["Denemeye devam et"])
        self.kapat.setText(self.e.d[self.e.s_d]["Tekrar başlat"])