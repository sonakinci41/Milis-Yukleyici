#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit

class KullaniciPencere(QWidget):
    def __init__(self, ebeveyn=None):
        self.ebeveyn = ebeveyn

        super(KullaniciPencere, self).__init__(ebeveyn)
        kullaniciKutu = QGridLayout()
        self.setLayout(kullaniciKutu)

        kullaniciKutu.addWidget(QLabel(self.tr("Milis Linux Kullanabilmeniz İçin Bir Kullanıcı Oluşturmanız Gerekli")), 0, 0, 1, 2)
        self.kullaniciBilgiLabel = QLabel()
        kullaniciKutu.addWidget(self.kullaniciBilgiLabel, 1, 0, 1, 2)
        kullaniciKutu.addWidget(QLabel(self.tr("Kullanıcı Adı")), 2, 0, 1, 1)
        self.kullaniciAdi = QLineEdit()
        self.kullaniciAdi.textChanged.connect(self.kullaniciBilgiYaziGirildi)
        kullaniciKutu.addWidget(self.kullaniciAdi, 2, 1, 1, 1)
        kullaniciKutu.addWidget(QLabel(self.tr("Kullanıcı Şifresi")), 3, 0, 1, 1)
        self.kullaniciSifre = QLineEdit()
        self.kullaniciSifre.textChanged.connect(self.kullaniciBilgiYaziGirildi)
        self.kullaniciSifre.setEchoMode(QLineEdit.Password)
        kullaniciKutu.addWidget(self.kullaniciSifre, 3, 1, 1, 1)
        kullaniciKutu.addWidget(QLabel(self.tr("Kullanıcı Şifresi Tekrar")), 4, 0, 1, 1)
        self.kullaniciSifreTekrar = QLineEdit()
        self.kullaniciSifreTekrar.textChanged.connect(self.kullaniciBilgiYaziGirildi)
        self.kullaniciSifreTekrar.setEchoMode(QLineEdit.Password)
        kullaniciKutu.addWidget(self.kullaniciSifreTekrar, 4, 1, 1, 1)


    def kullaniciBilgiYaziGirildi(self):
        donut = ""
        ad = self.kullaniciAdi.text()
        sifre_1 = self.kullaniciSifre.text()
        sifre_2 = self.kullaniciSifreTekrar.text()
        if len(ad) > 0 and not ad[0].isalpha():
            donut += self.tr("Lütfen Karakter Adında Harf İle Başlanyın\n")
        if not ad.isalnum():
            donut += self.tr("Lütfen Karakter Adında Sadece Harf Ve Rakam Kullanın\n")
        if len(sifre_1) == 0 or len(sifre_2) == 0:
            donut += self.tr("Lütfen Bir Şifre Girin\n")
        if sifre_1 != sifre_2:
            donut += self.tr("Yazdığınız Şifreler Birbirinden Farklı\n")
        if donut == "":
            self.kullaniciBilgiLabel.setText(self.tr("Teşekkürler Lütfen Adınızı Ve Şifrenizi Unutmayınız"))
            self.ebeveyn.kurparam["kullanici"]["isim"] = ad
            self.ebeveyn.kurparam["kullanici"]["sifre"] = sifre_1
            self.ebeveyn.ileriDugme.setDisabled(False)
        else:
            self.ebeveyn.ileriDugme.setDisabled(True)
            self.kullaniciBilgiLabel.setText(donut)