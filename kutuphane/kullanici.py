from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QCheckBox, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap

class Kullanici(QWidget):
    def __init__(self, ebeveyn=None):
        super(Kullanici, self).__init__(ebeveyn)
        self.e = ebeveyn
        sol_kutu = QVBoxLayout()
        self.setLayout(sol_kutu)

        self.gercek_ad_ = None
        self.kullanici_adi_ = None
        self.bilgisayar_adi_ = None
        self.giris_sifresi_ = None
        self.admin_sifresi_ = None

        self.gercek_ad_label = QLabel()
        sol_kutu.addWidget(self.gercek_ad_label)

        satir_kutu = QHBoxLayout()
        satir_kutu.setAlignment(Qt.AlignLeft)
        sol_kutu.addLayout(satir_kutu)
        self.gercek_ad = QLineEdit()
        self.gercek_ad.textChanged.connect(self.otomatik_doldur)
        self.gercek_ad.textChanged.connect(self.gercek_ad_kontrol)
        self.gercek_ad.setFixedWidth(300)
        satir_kutu.addWidget(self.gercek_ad)
        self.gercek_ad_icon = QLabel()
        self.gercek_ad_icon.setFixedSize(24, 24)
        self.gercek_ad_icon.setScaledContents(True)
        satir_kutu.addWidget(self.gercek_ad_icon)

        self.gercek_ad_info = QLabel()
        self.gercek_ad_info.setFont(QFont('SansSerif', 10))
        sol_kutu.addWidget(self.gercek_ad_info)


        self.kullanici_adi_label = QLabel()
        sol_kutu.addWidget(self.kullanici_adi_label)

        satir_kutu = QHBoxLayout()
        satir_kutu.setAlignment(Qt.AlignLeft)
        sol_kutu.addLayout(satir_kutu)
        self.kullanici_adi = QLineEdit()
        self.kullanici_adi.textChanged.connect(self.kullanici_adi_kontrol)
        self.kullanici_adi.setFixedWidth(300)
        satir_kutu.addWidget(self.kullanici_adi)
        self.kullanici_adi_icon = QLabel()
        self.kullanici_adi_icon.setFixedSize(24, 24)
        self.kullanici_adi_icon.setScaledContents(True)
        satir_kutu.addWidget(self.kullanici_adi_icon)

        self.kullanici_adi_info = QLabel()
        sol_kutu.addWidget(self.kullanici_adi_info)

        self.bilgisayar_adi_label = QLabel()
        sol_kutu.addWidget(self.bilgisayar_adi_label)

        satir_kutu = QHBoxLayout()
        satir_kutu.setAlignment(Qt.AlignLeft)
        sol_kutu.addLayout(satir_kutu)
        self.bilgisayar_adi = QLineEdit()
        self.bilgisayar_adi.textChanged.connect(self.bilgisayar_adi_kontrol)
        self.bilgisayar_adi.setFixedWidth(300)
        satir_kutu.addWidget(self.bilgisayar_adi)
        self.bilgisayar_adi_icon = QLabel()
        self.bilgisayar_adi_icon.setFixedSize(24, 24)
        self.bilgisayar_adi_icon.setScaledContents(True)
        satir_kutu.addWidget(self.bilgisayar_adi_icon)

        self.bilgisayar_adi_info = QLabel()
        sol_kutu.addWidget(self.bilgisayar_adi_info)

        self.giris_sifresi_label = QLabel()
        sol_kutu.addWidget(self.giris_sifresi_label)

        self.giris_sifresi = QLineEdit()
        self.giris_sifresi.textChanged.connect(self.giris_sifresi_kontrol)
        self.giris_sifresi.setFixedWidth(300)
        self.giris_sifresi.setEchoMode(QLineEdit.Password)
        self.giris_sifresi_tekrar = QLineEdit()
        self.giris_sifresi_tekrar.textChanged.connect(self.giris_sifresi_kontrol)
        self.giris_sifresi_tekrar.setFixedWidth(300)
        self.giris_sifresi_tekrar.setEchoMode(QLineEdit.Password)
        self.giris_sifresi_icon = QLabel()
        self.giris_sifresi_icon.setFixedSize(24, 24)
        self.giris_sifresi_icon.setScaledContents(True)
        sifre_kutu = QHBoxLayout()
        sifre_kutu.setAlignment(Qt.AlignLeft)
        sol_kutu.addLayout(sifre_kutu)
        sifre_kutu.addWidget(self.giris_sifresi)
        sifre_kutu.addWidget(self.giris_sifresi_tekrar)
        sifre_kutu.addWidget(self.giris_sifresi_icon)

        self.giris_sifresi_info = QLabel()
        sol_kutu.addWidget(self.giris_sifresi_info)

        self.oto_giris_cb = QCheckBox()
        self.oto_giris_cb.stateChanged.connect(self.oto_giris_degisti)
        self.oto_giris_degisti()
        sol_kutu.addWidget(self.oto_giris_cb)
        self.admin_giris_ayni_cb = QCheckBox()
        self.admin_giris_ayni_cb.stateChanged.connect(self.admin_giris_degisti)
        sol_kutu.addWidget(self.admin_giris_ayni_cb)

        self.admin_sifresi_label = QLabel()
        sol_kutu.addWidget(self.admin_sifresi_label)

        self.admin_sifresi = QLineEdit()
        self.admin_sifresi.textChanged.connect(self.admin_sifresi_kontrol)
        self.admin_sifresi.setFixedWidth(300)
        self.admin_sifresi.setEchoMode(QLineEdit.Password)
        self.admin_sifresi_tekrar = QLineEdit()
        self.admin_sifresi_tekrar.textChanged.connect(self.admin_sifresi_kontrol)
        self.admin_sifresi_tekrar.setFixedWidth(300)
        self.admin_sifresi_tekrar.setEchoMode(QLineEdit.Password)
        self.admin_sifresi_icon = QLabel()
        self.admin_sifresi_icon.setFixedSize(24, 24)
        self.admin_sifresi_icon.setScaledContents(True)
        sifre_kutu = QHBoxLayout()
        sifre_kutu.setAlignment(Qt.AlignLeft)
        sol_kutu.addLayout(sifre_kutu)
        sifre_kutu.addWidget(self.admin_sifresi)
        sifre_kutu.addWidget(self.admin_sifresi_tekrar)
        sifre_kutu.addWidget(self.admin_sifresi_icon)

        self.admin_sifresi_info = QLabel()
        sol_kutu.addWidget(self.admin_sifresi_info)

        self.admin_giris_ayni_cb.setChecked(True)

    def gercek_ad_kontrol(self):
        if len(self.kullanici_adi.text()) > 2:
            self.gercek_ad_ = self.kullanici_adi.text()
            self.gercek_ad_icon.setPixmap(QPixmap("./resimler/oldu.svg"))
            self.gercek_ad_info.clear()
        else:
            self.gercek_ad_ = None
            self.gercek_ad_icon.setPixmap(QPixmap("./resimler/olmadi.svg"))
            self.gercek_ad_info.setText(self.e.d[self.e.s_d]["2 karakterden fazla olmalı"])
        self.ileri_kontrol()

    def kullanici_adi_kontrol(self):
        if self.kullanici_adi.text().isalnum() and len(self.kullanici_adi.text()) > 3:
            self.kullanici_adi_ = self.kullanici_adi.text()
            self.kullanici_adi_icon.setPixmap(QPixmap("./resimler/oldu.svg"))
            self.kullanici_adi_info.setText("")
        else:
            self.kullanici_adi_ = None
            self.kullanici_adi_icon.setPixmap(QPixmap("./resimler/olmadi.svg"))
            self.kullanici_adi_info.setText(self.e.d[self.e.s_d]["harf ve 3 karakterden fazla olmalı"])
        self.ileri_kontrol()

    def bilgisayar_adi_kontrol(self):
        if self.bilgisayar_adi.text().replace("-","").isalnum() and len(self.bilgisayar_adi.text()) > 3:
            self.bilgisayar_adi_ = self.bilgisayar_adi.text()
            self.bilgisayar_adi_icon.setPixmap(QPixmap("./resimler/oldu.svg"))
            self.bilgisayar_adi_info.setText("")
        else:
            self.bilgisayar_adi_ = None
            self.bilgisayar_adi_icon.setPixmap(QPixmap("./resimler/olmadi.svg"))
            self.bilgisayar_adi_info.setText(self.e.d[self.e.s_d]["harf ve 3 karakterden fazla olmalı"])
        self.ileri_kontrol()

    def giris_sifresi_kontrol(self):
        if len(self.giris_sifresi.text()) > 5 and self.giris_sifresi.text() == self.giris_sifresi_tekrar.text():
            self.giris_sifresi_ = self.giris_sifresi.text()
            self.giris_sifresi_icon.setPixmap(QPixmap("./resimler/oldu.svg"))
            self.giris_sifresi_info.setText("")
        else:
            self.giris_sifresi_ = None
            self.giris_sifresi_icon.setPixmap(QPixmap("./resimler/olmadi.svg"))
            self.giris_sifresi_info.setText(self.e.d[self.e.s_d]["5 karakterden fazla ve şifreler aynı olmalı"])
        self.ileri_kontrol()

    def admin_sifresi_kontrol(self):
        if len(self.admin_sifresi.text()) > 5 and self.admin_sifresi.text() == self.admin_sifresi_tekrar.text():
            self.admin_sifresi_ = self.admin_sifresi.text()
            self.admin_sifresi_icon.setPixmap(QPixmap("./resimler/oldu.svg"))
            self.admin_sifresi_info.setText("")
        else:
            self.admin_sifresi_ = None
            self.admin_sifresi_icon.setPixmap(QPixmap("./resimler/olmadi.svg"))
            self.admin_sifresi_info.setText(self.e.d[self.e.s_d]["5 karakterden fazla ve şifreler aynı olmalı"])
        self.ileri_kontrol()

    def admin_giris_degisti(self):
        if self.admin_giris_ayni_cb.isChecked():
            self.admin_sifresi.setHidden(True)
            self.admin_sifresi_tekrar.setHidden(True)
            self.admin_sifresi_icon.setHidden(True)
            self.admin_sifresi_label.setHidden(True)
            self.admin_sifresi_info.setHidden(True)
        else:
            self.admin_sifresi.setHidden(False)
            self.admin_sifresi_tekrar.setHidden(False)
            self.admin_sifresi_icon.setHidden(False)
            self.admin_sifresi_label.setHidden(False)
            self.admin_sifresi_info.setHidden(False)
        self.ileri_kontrol()

    def oto_giris_degisti(self):
        if self.oto_giris_cb.isChecked():
            self.e.milis_ayarlar["otomatik_giris"] = True
        else:
            self.e.milis_ayarlar["otomatik_giris"] = False

    def ileri_kontrol(self):
        if self.kullanici_adi_ != None and self.gercek_ad_ != None and self.bilgisayar_adi_ != None and self.giris_sifresi_ != None:
            if self.admin_sifresi_ != None:
                self.e.milis_ayarlar["gercek_ad"] = self.gercek_ad_
                self.e.milis_ayarlar["kullanici_adi"] = self.kullanici_adi_
                self.e.milis_ayarlar["bilgisayar_adi"] = self.bilgisayar_adi_
                self.e.milis_ayarlar["giris_sifresi"] = self.giris_sifresi_
                self.e.milis_ayarlar["admin_sifresi"] = self.admin_sifresi_
                self.e.ileri_dugme.setDisabled(False)
            elif self.admin_giris_ayni_cb.isChecked():
                self.e.milis_ayarlar["gercek_ad"] = self.gercek_ad_
                self.e.milis_ayarlar["kullanici_adi"] = self.kullanici_adi_
                self.e.milis_ayarlar["bilgisayar_adi"] = self.bilgisayar_adi_
                self.e.milis_ayarlar["giris_sifresi"] = self.giris_sifresi_
                self.e.milis_ayarlar["admin_sifresi"] = self.giris_sifresi_
                self.e.ileri_dugme.setDisabled(False)
            else:
                self.e.ileri_dugme.setDisabled(True)
        else:
            self.e.ileri_dugme.setDisabled(True)

    def otomatik_doldur(self):
        ad = self.gercek_ad.text()
        self.kullanici_adi.setText(ad.lower().replace(" ", ""))
        self.bilgisayar_adi.setText(ad.lower().replace(" ", "")+"-milis")

    def showEvent(self, event):
        self.e.setWindowTitle(self.e.d[self.e.s_d]["Kullanıcı Bilgileri"])
        self.gercek_ad_label.setText(self.e.d[self.e.s_d]["Adınız nedir?"])
        self.kullanici_adi_label.setText(self.e.d[self.e.s_d]["Giriş yapmak için hangi adı kullanmak istiyorsunuz?"])
        self.bilgisayar_adi_label.setText(self.e.d[self.e.s_d]["Bu bilgisayarın adı ne?"])
        self.giris_sifresi_label.setText(self.e.d[self.e.s_d]["Hesabınızı güvende tutmak için bir şifre seçin."])
        self.oto_giris_cb.setText(self.e.d[self.e.s_d]["Şifre istemeden otomatik giriş yapın"])
        self.admin_giris_ayni_cb.setText(self.e.d[self.e.s_d]["Yönetici hesabı için aynı şifreyi kullanın"])
        self.admin_sifresi_label.setText(self.e.d[self.e.s_d]["Yönetici hesabı için bir şifre seçin"])
        self.gercek_ad_kontrol()
        self.kullanici_adi_kontrol()
        self.bilgisayar_adi_kontrol()
        self.giris_sifresi_kontrol()
        self.admin_sifresi_kontrol()