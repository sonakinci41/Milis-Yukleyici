from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QComboBox
from .harita_widget import HaritaWidget
from PyQt5.QtCore import Qt

class Konum(QWidget):
    def __init__(self, ebeveyn=None):
        super(Konum, self).__init__(ebeveyn)
        self.e = ebeveyn
        kutu = QGridLayout()
        kutu.setAlignment(Qt.AlignCenter)
        self.setLayout(kutu)
        self.bigli_label = QLabel()
        kutu.addWidget(self.bigli_label,0,0,1,2)

        self.harita = HaritaWidget(self)
        kutu.addWidget(self.harita,1,0,1,2)

        self.bolge_label = QLabel()
        kutu.addWidget(self.bolge_label,2,0,1,1)

        self.sehir_label = QLabel()
        kutu.addWidget(self.sehir_label,2,1,1,1)

        self.bolge_combo = QComboBox()
        self.bolge_combo.currentTextChanged.connect(self.sehir_combo_doldur)
        kutu.addWidget(self.bolge_combo,3,0,1,1)
        self.sehir_combo = QComboBox()
        self.sehir_combo.currentTextChanged.connect(self.sehir_combo_degisti)
        kutu.addWidget(self.sehir_combo,3,1,1,1)
        self.bolge_combo_doldur()
        self.bolge_combo.setCurrentText("Europe")
        self.sehir_combo.setCurrentText("Istanbul")

    def bolge_combo_doldur(self):
        self.duzenli_ulke = {}
        for i in self.harita.koordinat_pixelleri.items():
            degistir = i[1].split("/")
            if len(degistir) == 2:
                varmi = self.duzenli_ulke.get(degistir[0], "yok")
                if varmi == "yok":
                    self.duzenli_ulke[degistir[0]] = [degistir[1]]
                else:
                    self.duzenli_ulke[degistir[0]].append(degistir[1])
            elif len(degistir) == 3:
                varmi = self.duzenli_ulke.get(degistir[0], "yok")
                if varmi == "yok":
                    self.duzenli_ulke[degistir[0]] = [degistir[1]+"/"+degistir[2]]
                else:
                    self.duzenli_ulke[degistir[0]].append(degistir[1]+"/"+degistir[2])
        self.bolge_combo.addItems(self.duzenli_ulke.keys())

    def sehir_combo_doldur(self):
        self.sehir_combo.clear()
        self.sehir_combo.addItems(self.duzenli_ulke[self.bolge_combo.currentText()])

    def sehir_combo_degisti(self):
        if self.sehir_combo.currentText() != "":
            bolge_adi = self.bolge_combo.currentText()+"/"+self.sehir_combo.currentText()
            self.harita.pin_hareket_ettir(bolge_adi)
            self.e.milis_ayarlar["konum"] = bolge_adi

    def harita_tiklandi(self,tiklanan):
        self.bolge_combo.setCurrentText(tiklanan[0])
        self.sehir_combo.setCurrentText(tiklanan[1])

    def showEvent(self, event):
        self.e.setWindowTitle(self.e.d[self.e.s_d]["Saat Dilimi"])
        self.bigli_label.setText(self.e.d[self.e.s_d]["Lütfen saat dilimini ayarlayabilmemiz için harita üzerinden konumunuzu seçiniz."])
        self.bolge_label.setText(self.e.d[self.e.s_d]["Bölge"])
        self.sehir_label.setText(self.e.d[self.e.s_d]["Şehir"])