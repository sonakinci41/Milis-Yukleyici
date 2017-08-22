#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton

class GrubPencere(QWidget):
    def __init__(self, ebeveyn=None):
        super(GrubPencere, self).__init__(ebeveyn)
        self.ebeveyn = ebeveyn

        grubKutu=QGridLayout()
        self.setLayout(grubKutu)
        grubKutu.addWidget(QLabel(self.tr("""Sisteme Grub kurmak istiyormusunuz?\n Grub bir linux önyükleyicisidir\n
        Eğer sisteminizde kurulu bir linux dağıtımı var ise ve disk biçimlendirilmemişse grub kurmayabilirsiniz.\n
        Eğer sisteminizde kurulu bir linux dağıtımı yok veya disk biçimlendirilmişse grub kurmadığınız takdirde\n
        sistem başlamayacaktır.""")),0,0,1,2)
        self.grubKurDugme=QPushButton("Grub Kur")
        self.grubKurDugme.clicked.connect(self.grubKurFonksiyon)
        grubKutu.addWidget(self.grubKurDugme,1,0,1,1)
        self.grubKurmaDugme=QPushButton("Grub Kurma")
        self.grubKurmaDugme.clicked.connect(self.grubKurmaFonksiyon)
        grubKutu.addWidget(self.grubKurmaDugme,1,1,1,1)

    def grubKurFonksiyon(self):
        self.ebeveyn.kurparam["grub"]["kur"] = "evet"
        self.grubKurDugme.setDisabled(True)
        self.grubKurmaDugme.setDisabled(False)
        self.ebeveyn.ileriDugme.setDisabled(False)

    def grubKurmaFonksiyon(self):
        self.ebeveyn.kurparam["grub"]["kur"] = "hayir"
        self.grubKurDugme.setDisabled(False)
        self.grubKurmaDugme.setDisabled(True)
        self.ebeveyn.ileriDugme.setDisabled(False)