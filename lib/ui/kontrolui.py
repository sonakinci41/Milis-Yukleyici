#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QTextEdit, QMessageBox, qApp

class KontrolPencere(QWidget):
    def __init__(self, ebeveyn=None):
        self.ebeveyn = ebeveyn

        super(KontrolPencere, self).__init__(ebeveyn)
        baslangicKutu = QGridLayout()
        self.setLayout(baslangicKutu)

        bilgiLabel = QLabel(self.tr("Milis yükleyicinin kurulumdan önce bazı kontoller gerçekleştirmesi gerekiyor"))
        baslangicKutu.addWidget(bilgiLabel, 0, 0, 1, 1)
        self.baslaDugme = QPushButton(self.tr("Başlat"))
        self.baslaDugme.clicked.connect(self.baslangicKotrolFonksiyon)
        baslangicKutu.addWidget(self.baslaDugme, 0, 1, 1, 1)
        self.ciktiYazilari = QTextEdit()
        baslangicKutu.addWidget(self.ciktiYazilari, 1, 0, 1, 2)

    def baslangicKotrolFonksiyon(self):
        self.baslaDugme.setDisabled(True)
        cikti = self.tr("#Log dosyası oluşturuluyor...\n")
        self.ciktiYazilari.setText(cikti)
        f = open("/tmp/kurulum.log", "w")
        kurulum_dosya = "/root/ayarlar/kurulum.yml"
        if not os.path.exists(kurulum_dosya):
            QMessageBox.warning(self, "Hata",
                                self.tr(""""Milis kurulumu için gerekli olan /root/ayarlar/kurulum.yml \n
                                dosyası bulunamadı. Milis yükleyici sonladırılacak!"""))
            qApp.closeAllWindows()
        else:
            cikti += self.tr("#Yml dosyası kopyalanıyor...\n")
            cikti += self.ebeveyn.komutCalistirFonksiyon("cp " + kurulum_dosya + " /opt/kurulum.yml")
            self.ciktiYazilari.setText(cikti)
            self.ebeveyn.kurulum_oku(self.ebeveyn.kurulum_dosya)
            cikti += "============================\n"+self.tr("İşlem tamamlandı devam edebilirsiniz")
            self.ciktiYazilari.setText(cikti)
            self.ebeveyn.ileriDugme.setDisabled(False)