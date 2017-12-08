from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QComboBox, QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
import webbrowser


class Hosgeldiniz(QWidget):
    def __init__(self, ebeveyn=None):
        super(Hosgeldiniz, self).__init__(ebeveyn)
        self.e = ebeveyn

        kutu = QGridLayout()
        self.setLayout(kutu)
        self.hosgeldiniz_te = QLabel()
        self.hosgeldiniz_te.setAlignment(Qt.AlignCenter)
        self.hosgeldiniz_te.setWordWrap(True)
        kutu.addWidget(self.hosgeldiniz_te,0,0,1,2)

        self.kurulum_belgesi = QPushButton()
        self.kurulum_belgesi.setIcon(QIcon("./resimler/belge.svg"))
        self.kurulum_belgesi.setIconSize(QSize(50,50))
        self.kurulum_belgesi.clicked.connect(self.kurulum_ac)
        kutu.addWidget(self.kurulum_belgesi,1,0,1,1)

        self.git = QPushButton()
        self.git.setIcon(QIcon("./resimler/git.svg"))
        self.git.setIconSize(QSize(50,50))
        self.git.clicked.connect(self.git_ac)
        kutu.addWidget(self.git,1,1,1,1)

        self.forum = QPushButton()
        self.forum.setIcon(QIcon("./resimler/forum.svg"))
        self.forum.setIconSize(QSize(50,50))
        self.forum.clicked.connect(self.forum_ac)
        kutu.addWidget(self.forum,2,0,1,1)

        self.irc = QPushButton()
        self.irc.setIcon(QIcon("./resimler/irc.svg"))
        self.irc.setIconSize(QSize(50,50))
        self.irc.clicked.connect(self.irc_ac)
        kutu.addWidget(self.irc,2,1,1,1)

        self.diller_resim = QLabel()
        self.diller_resim.setAlignment(Qt.AlignCenter)
        self.diller_resim.setPixmap(QPixmap("./resimler/diller.svg").scaled(250,250))
        kutu.addWidget(self.diller_resim,3,0,1,2)

        self.diller_label = QLabel()
        kutu.addWidget(self.diller_label,4,0,1,1)
        self.diller_combo = QComboBox()
        self.diller_combo.currentIndexChanged.connect(self.diller_combo_degisti)
        self.diller_combo.addItems(self.e.d.keys())
        self.diller_combo.setCurrentText("Türkçe")
        kutu.addWidget(self.diller_combo,4,1,1,1)


    def diller_combo_degisti(self):
        secilen = self.diller_combo.currentText()
        self.e.s_d = secilen
        self.yazi_ekle()
        self.e.milis_ayarlar["dil"] = self.e.d[self.e.s_d]["Dil_Kodu"]

    def kurulum_ac(self):
        webbrowser.open("https://milislinux.org/kategori/wiki/kurulum/")

    def git_ac(self):
        webbrowser.open("https://github.com/milisarge")

    def forum_ac(self):
        webbrowser.open("http://forum.milislinux.org/")

    def irc_ac(self):
        webbrowser.open("http://webchat.freenode.net/")

    def showEvent(self, event):
        self.yazi_ekle()

    def yazi_ekle(self):
        #Pencere başlığımızı ekleyelim
        self.e.setWindowTitle(self.e.d[self.e.s_d]["Milis-Yükleyiciye Hoşgeldiniz"])
        self.hosgeldiniz_te.setText(self.e.d[self.e.s_d]["Milis Linux (Milli İşletim Sistemi) sıfır kaynak koddan üretilen, kendine has paket yöneticisine sahip, bağımsız tabanlı yerli linux işletim sistemi projesidir. Genel felsefe olarak ülkemizdeki bilgisayar kullanıcıları için linuxu kolaylaştırıp Milis İşletim Sisteminin sorunsuz bir işletim sistemi olmasını sağlamayı ve yazılımsal olarak dışa bağımlı olmaktan kurtarmayı esas alır. Ayrıca her türlü katkıda bulunmak isteyenler için bulunmaz bir Türkçe açık kaynak projesidir."])
        self.diller_label.setText(self.e.d[self.e.s_d]["Lütfen bir dil seçiniz."])
        self.kurulum_belgesi.setText(self.e.d[self.e.s_d]["Kurulum Belgesi"])
        self.git.setText(self.e.d[self.e.s_d]["GitHub Adresi"])
        self.forum.setText(self.e.d[self.e.s_d]["Forum Adresi"])
        self.irc.setText(self.e.d[self.e.s_d]["freenode #milisarge"])
        self.e.ileri_dugme.setText(self.e.d[self.e.s_d]["İleri"])
        self.e.geri_dugme.setText(self.e.d[self.e.s_d]["Geri"])