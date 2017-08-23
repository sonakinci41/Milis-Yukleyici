#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QComboBox, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
import pytz

class SaatDilimiPencere(QWidget):
    def __init__(self, ebeveyn=None):
        super(SaatDilimiPencere, self).__init__(ebeveyn)
        self.ebeveyn = ebeveyn

        self.saatDilimiSozlukOlustur()

        merkezLayout = QVBoxLayout()
        dunyaResmi = QLabel()
        dunyaResmi.setPixmap(QPixmap(":/slaytlar/dunya.svg").scaled(504,250))
        dunyaResmi.setAlignment(Qt.AlignCenter)
        merkezLayout.addWidget(dunyaResmi)
        merkezLayout.addWidget(QLabel(self.tr("Bir zaman dilimi seçiniz.")))
        self.setLayout(merkezLayout)
        comboLayout = QHBoxLayout()
        merkezLayout.addLayout(comboLayout)

        self.ulkelerCombo = QComboBox()
        comboLayout.addWidget(self.ulkelerCombo)

        self.sehirlerCombo = QComboBox()
        comboLayout.addWidget(self.sehirlerCombo)
        self.ulkelerCombo.currentTextChanged.connect(self.sehirlerComboDoldur)
        self.ulkelerComboDoldur()
        self.sehirlerCombo.currentTextChanged.connect(self.saatDilimiSecildi)


    def saatDilimiSecildi(self,sehir):
        if sehir == "------":
            self.ebeveyn.ileriDugme.setDisabled(True)
        else:
            self.ebeveyn.ileriDugme.setDisabled(False)
            self.ebeveyn.kurparam["bolgesel"]["zaman"] = self.ulkelerCombo.currentText()+"/"+sehir
            self.ebeveyn.kurparam["bolgesel"]["dil"] = self.ebeveyn.sistemDili


    def saatDilimiSozlukOlustur(self):
        self.saatDilimiSozluk = {}
        saatDilimiListe = pytz.all_timezones
        for saatDilimi in saatDilimiListe:
            saatDilimi = saatDilimi.split("/")
            if len(saatDilimi) == 2:
                varmi = self.saatDilimiSozluk.get(saatDilimi[0],"yok")
                if varmi == "yok":
                    self.saatDilimiSozluk[saatDilimi[0]] = [saatDilimi[1]]
                else:
                    varmi.append(saatDilimi[1])

    def ulkelerComboDoldur(self):
        liste = list(self.saatDilimiSozluk.keys())
        liste.sort()
        self.ulkelerCombo.addItems(liste)

    def sehirlerComboDoldur(self,ulke):
        self.sehirlerCombo.clear()
        self.sehirlerCombo.addItem("------")
        liste = self.saatDilimiSozluk[ulke]
        liste.sort()
        self.sehirlerCombo.addItems(liste)