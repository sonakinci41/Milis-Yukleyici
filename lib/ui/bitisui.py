#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, qApp

class BitisPencere(QWidget):
    def __init__(self, ebeveyn=None):
        self.ebeveyn = ebeveyn

        super(BitisPencere, self).__init__(ebeveyn)
        kurulumSonucKutu = QGridLayout()
        self.setLayout(kurulumSonucKutu)
        milisLogo = QLabel()
        milisLogo.setPixmap(QPixmap(":/slaytlar/Milis-logo.svg").scaled(230, 168))
        milisLogo.setAlignment(Qt.AlignCenter)
        kurulumSonucKutu.addWidget(milisLogo, 0, 0, 1, 1)
        milisTesekkurYazi = QLabel(self.tr("Milis Linux Başarıyla Kurulmuştur.\nMilis Linux Kurduğunuz İçin Teşekkür Ederiz.\nİsterseniz sistemi denemeye devam edebilirsiniz\nYada tekrar başlatıp sisteminizi kullanbilirsiniz."))
        kurulumSonucKutu.addWidget(milisTesekkurYazi, 1, 0, 1, 1)
        milisTesekkurYazi.setAlignment(Qt.AlignCenter)
        deneDugme = QPushButton(self.tr("Milis Linux'u denemeye devam et"))
        deneDugme.pressed.connect(self.deneDugmeFonksiyon)
        kurulumSonucKutu.addWidget(deneDugme, 2, 0, 1, 1)
        tekrarBaslatDugme = QPushButton("Tekrar Başlat")
        tekrarBaslatDugme.pressed.connect(self.tekrarBaslatDugmeFonksiyon)
        kurulumSonucKutu.addWidget(tekrarBaslatDugme, 3, 0, 1, 1)

    def deneDugmeFonksiyon(self):
        qApp.closeAllWindows()

    def tekrarBaslatDugmeFonksiyon(self):
        os.system("shutdown -r now")