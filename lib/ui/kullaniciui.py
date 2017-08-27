#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QCheckBox

class KullaniciPencere(QWidget):
    def __init__(self, ebeveyn=None):
        self.ebeveyn = ebeveyn

        super(KullaniciPencere, self).__init__(ebeveyn)
        kullaniciKutu = QGridLayout()
        self.setLayout(kullaniciKutu)

        kullaniciKutu.addWidget(QLabel(self.tr("Milis Linux Kullanabilmeniz İçin Bir Kullanıcı Oluşturmanız Gerekli")), 0, 0, 1, 2)
        self.kullaniciBilgiLabel = QLabel()
        kullaniciKutu.addWidget(self.kullaniciBilgiLabel, 1, 0, 1, 2)

        kullaniciKutu.addWidget(QLabel(self.tr("Ad Soyad")),2,0,1,1)
        self.adSoyad = QLineEdit()
        self.adSoyad.textChanged.connect(self.kullaniciBilgiYaziGirildi)
        kullaniciKutu.addWidget(self.adSoyad)
        kullaniciKutu.addWidget(QLabel(self.tr("Kullanıcı Adı")), 3, 0, 1, 1)
        self.kullaniciAdi = QLineEdit()
        self.kullaniciAdi.textChanged.connect(self.kullaniciBilgiYaziGirildi)
        kullaniciKutu.addWidget(self.kullaniciAdi, 3, 1, 1, 1)
        kullaniciKutu.addWidget(QLabel(self.tr("Kullanıcı Şifresi")), 4, 0, 1, 1)
        self.kullaniciSifre = QLineEdit()
        self.kullaniciSifre.textChanged.connect(self.kullaniciBilgiYaziGirildi)
        self.kullaniciSifre.setEchoMode(QLineEdit.Password)
        kullaniciKutu.addWidget(self.kullaniciSifre, 4, 1, 1, 1)
        kullaniciKutu.addWidget(QLabel(self.tr("Kullanıcı Şifresi Tekrar")), 5, 0, 1, 1)
        self.kullaniciSifreTekrar = QLineEdit()
        self.kullaniciSifreTekrar.textChanged.connect(self.kullaniciBilgiYaziGirildi)
        self.kullaniciSifreTekrar.setEchoMode(QLineEdit.Password)
        kullaniciKutu.addWidget(self.kullaniciSifreTekrar, 5, 1, 1, 1)

        self.rootSifresiCheckBox = QCheckBox(self.tr("Root şifresi kullanıcı şifresiyle aynı olsun"))
        self.rootSifresiCheckBox.setChecked(True)
        self.rootSifresiCheckBox.stateChanged.connect(self.rootSifresiDurumDegisti)
        kullaniciKutu.addWidget(self.rootSifresiCheckBox,6,0,1,2)

        self.otomatikGiris = QCheckBox(self.tr("Oluşturulan kullanıcıya otomatik giriş yapılsın"))
        self.otomatikGiris.clicked.connect(self.otogirisCheckBoxDegisti)
        kullaniciKutu.addWidget(self.otomatikGiris,9,0,1,2)

        self.rootLabel = QLabel(self.tr("Root Şifresi"))
        self.rootLabel.setHidden(True)
        kullaniciKutu.addWidget(self.rootLabel,7,0,1,1)
        self.rootTekrarLabel = QLabel(self.tr("Root Şifresi Tekrar"))
        self.rootTekrarLabel.setHidden(True)
        kullaniciKutu.addWidget(self.rootTekrarLabel,8,0,1,1)
        self.rootSifresi_1 = QLineEdit()
        self.rootSifresi_1.setEchoMode(QLineEdit.Password)
        self.rootSifresi_1.textChanged.connect(self.kullaniciBilgiYaziGirildi)
        kullaniciKutu.addWidget(self.rootSifresi_1,7,1,1,1)
        self.rootSifresi_1.setHidden(True)
        self.rootSifresi_2 = QLineEdit()
        self.rootSifresi_2.setEchoMode(QLineEdit.Password)
        self.rootSifresi_2.textChanged.connect(self.kullaniciBilgiYaziGirildi)
        kullaniciKutu.addWidget(self.rootSifresi_2,8,1,1,1)
        self.rootSifresi_2.setHidden(True)


    def rootSifresiDurumDegisti(self):
        if self.rootSifresiCheckBox.isChecked():
            self.rootSifresi_1.setHidden(True)
            self.rootSifresi_2.setHidden(True)
            self.rootLabel.setHidden(True)
            self.rootTekrarLabel.setHidden(True)
        else:
            self.rootSifresi_1.setHidden(False)
            self.rootSifresi_2.setHidden(False)
            self.rootLabel.setHidden(False)
            self.rootTekrarLabel.setHidden(False)

    def otogirisCheckBoxDegisti(self):
        if self.otomatikGiris.isChecked():
            self.ebeveyn.kurparam["kullanici"]["otogiris"] = "evet"
        else:
            self.ebeveyn.kurparam["kullanici"]["otogiris"] = "hayir"

    def kullaniciBilgiYaziGirildi(self):
        ad = self.kullaniciAdi.text()
        self.donut = ""

        #Ad Soyad kontrolü
        if self.adSoyad.text() == "":
            self.donut += self.tr("Ad Soyad Boş bırakılamaz\n")
        elif not self.adSoyad.text().replace(" ","").isalpha():
            self.donut += self.tr("Ad Soyad Bölümün Harf Ve Boşluk Kullanınız")

        #Kullanıcı Adı Kontrolü
        if not ad.islower():
            self.donut += self.tr("Lütfen Kullanıcı Adında Büyük Harf Kullanmayınız\n")
        kontrol = ad.replace("-","")
        kontrol = kontrol.replace("_","")
        if len(ad) > 0 and not ad[0].isalpha():
            self.donut += self.tr("Lütfen Kullanıcı Adında Harf İle Başlanyın\n")
        if not kontrol.isalnum():
            self.donut += self.tr("Lütfen Kullanıcı Adında Sadece Harf Ve Rakam Kullanın\n")

        sifre_1 = self.kullaniciSifre.text()
        sifre_2 = self.kullaniciSifreTekrar.text()
        self.donutOlustur(sifre_1,sifre_2)
        if not self.rootSifresiCheckBox.isChecked():
            root_1 = self.rootSifresi_1.text()
            root_2 = self.rootSifresi_2.text()
            self.donutOlustur(root_1,root_2)

        if self.donut == "":
            self.kullaniciBilgiLabel.setText(self.tr("Teşekkürler Lütfen Kullanıcı Adınızı Ve Şifrenizi Unutmayınız"))
            self.ebeveyn.kurparam["kullanici"]["isim"] = ad
            self.ebeveyn.kurparam["kullanici"]["sifre"] = sifre_1
            self.ebeveyn.kurparam["kullanici"]["uzunisim"] = self.adSoyad.text()
            if self.rootSifresiCheckBox.isChecked():
                self.ebeveyn.kurparam["kullanici"]["root"] = sifre_1
            else:
                self.ebeveyn.kurparam["kullanici"]["root"] = root_1
            self.ebeveyn.ileriDugme.setDisabled(False)
        else:
            self.ebeveyn.ileriDugme.setDisabled(True)
            self.kullaniciBilgiLabel.setText(self.donut)

    def donutOlustur(self,sifre_1,sifre_2):
        kontrol = sifre_1.replace("-","")
        kontrol = kontrol.replace("_","")
        if not kontrol.isalnum():
            self.donut += self.tr("Lütfen Şifrelerde Sadece Rakam Ve Harf Kullanınız\n")
        if len(sifre_1) == 0 or len(sifre_2) == 0:
            self.donut += self.tr("Lütfen Bir Şifre Girin\n")
        if sifre_1 != sifre_2:
            self.donut += self.tr("Yazdığınız Şifreler Birbirinden Farklı\n")