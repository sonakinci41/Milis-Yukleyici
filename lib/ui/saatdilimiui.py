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

        self.kitalarCombo = QComboBox()
        comboLayout.addWidget(self.kitalarCombo)

        self.sehirlerCombo = QComboBox()
        comboLayout.addWidget(self.sehirlerCombo)
        self.kitalarCombo.currentTextChanged.connect(self.sehirlerComboDoldur)
        self.kitalarComboDoldur()
        self.sehirlerCombo.currentTextChanged.connect(self.saatDilimiSecildi)
        self.kitalarCombo.setCurrentText("Europe")


    def saatDilimiSecildi(self,sehir):
        if self.ebeveyn.kurparam != None:
            saatDilimi = self.kitalarCombo.currentText()+"/"+sehir			
            self.ebeveyn.kurparam["bolgesel"]["zaman"] = saatDilimi.replace(" ","_")
            self.ebeveyn.kurparam["bolgesel"]["dil"] = self.ebeveyn.sistemDili
            self.ebeveyn.ileriDugme.setDisabled(False)

    def saatDilimiSozlukOlustur(self):
        self.saatDilimiSozluk = {}
        saatDilimiListe = pytz.all_timezones
        for saatDilimi in saatDilimiListe:
            saatDilimi = saatDilimi.replace("_"," ")
            saatDilimi = saatDilimi.split("/")
            if len(saatDilimi) >= 2:					
                varmi = self.saatDilimiSozluk.get(saatDilimi[0],"yok")
                if varmi == "yok":			
                    self.saatDilimiSozluk[saatDilimi[0]] = [saatDilimi[1]]
                else:
                    if len(saatDilimi) == 2:
                        varmi.append(saatDilimi[1])
                    elif len(saatDilimi) == 3:
                        varmi.append(saatDilimi[1] + "/" + saatDilimi[2])

    def kitalarComboDoldur(self):
        liste = list(self.saatDilimiSozluk.keys())
        liste.sort()
        self.kitalarCombo.addItems(liste)

    def sehirlerComboDoldur(self,ulke):
        self.sehirlerCombo.clear()
        self.sehirlerCombo.addItem("------")
        liste = self.saatDilimiSozluk[ulke]
        liste.sort()
        self.sehirlerCombo.addItems(liste)
