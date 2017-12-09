#
#
#  Copyright 2017 Metehan Özbek <mthnzbk@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QLabel, QLineEdit, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from .klavye_label import KlavyeLabel
import os
from .veriler.klavye_veri import duzenler,modeller,varyantlar


class Klavye(QWidget):
    def __init__(self, ebeveyn=None):
        super(Klavye,self).__init__(ebeveyn)
        self.e = ebeveyn
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignCenter)

        merkez_layout = QHBoxLayout()
        self.layout().addLayout(merkez_layout)

        self.klavye_resim = KlavyeLabel(self)
        merkez_layout.addWidget(self.klavye_resim)

        self.layout().addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.MinimumExpanding))

        hlayoutx = QHBoxLayout()
        self.layout().addLayout(hlayoutx)

        self.model_label = QLabel()
        #self.model_label.setFixedWidth(150)
        hlayoutx.addWidget(self.model_label)

        self.model_combo = QComboBox()
        hlayoutx.addWidget(self.model_combo)

        hlayout = QHBoxLayout()
        self.layout().addLayout(hlayout)

        self.ulke_label = QLabel()
        hlayout.addWidget(self.ulke_label)

        self.ulke_combo = QComboBox()
        #self.ulke_combo.setFixedWidth(325)
        hlayout.addWidget(self.ulke_combo)

        hlayout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Expanding))

        self.klavye_label = QLabel()
        hlayout.addWidget(self.klavye_label)

        self.keyboardVList = QComboBox()
        #self.keyboardVList.setFixedWidth(325)
        hlayout.addWidget(self.keyboardVList)

        self.text_le = QLineEdit()
        #self.text_le.setFixedWidth(800)
        self.layout().addWidget(self.text_le)

        self.layout().addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.MinimumExpanding))

        self.klavye_listesi = modeller
        self.layout_list = duzenler
        self.variant_list = varyantlar

        model = list(self.klavye_listesi.keys())
        model.sort()
        for i in model:
            self.model_combo.addItem(self.klavye_listesi[i])
            if i == "pc105":
                self.model_combo.setCurrentText(self.klavye_listesi[i])
                self.e.milis_ayarlar["klavye_model"] = i, self.klavye_listesi[i]

        keys = list(self.layout_list.keys())
        keys.sort()
        for i in keys:
            self.ulke_combo.addItem(self.layout_list[i])

        default = self.layout_list.get(self.e.milis_ayarlar["dil"][:2], "us")
        if default == "us":
            self.ulke_combo.setCurrentText(self.layout_list[default])
            self.e.milis_ayarlar["klavye_duzeni"] = default, self.layout_list[default]

        else:
            self.ulke_combo.setCurrentText(default)
            self.e.milis_ayarlar["klavye_duzeni"] = self.e.milis_ayarlar["dil"][:2], default

        self.keyboardVList.addItem("Default")
        for k, v in self.variant_list.items():
            if k == self.e.milis_ayarlar["klavye_duzeni"][0]:
                for i in v:
                    self.keyboardVList.addItems(i.values())
        self.e.milis_ayarlar["klavye_varyantı"] = None

        self.model_combo.currentTextChanged.connect(self.klaye_modeli_secildi)
        self.ulke_combo.currentTextChanged.connect(self.ulke_secildi)
        self.keyboardVList.currentTextChanged.connect(self.klavye_tipi_secildi)

        self.klavye_resim.klavye_bilgi.emit(self.e.milis_ayarlar["klavye_model"][0],
                                        self.e.milis_ayarlar["klavye_duzeni"][0],
                                        self.e.milis_ayarlar["klavye_varyantı"])

    def showEvent(self, event):
        self.e.setWindowTitle(self.e.d[self.e.s_d]["Klavye Ayarları"])
        self.model_label.setText(self.e.d[self.e.s_d]["Klavye Modeli"])
        self.ulke_label.setText(self.e.d[self.e.s_d]["Ülke"])
        self.klavye_label.setText(self.e.d[self.e.s_d]["Klavye Türü"])
        self.text_le.setPlaceholderText(self.e.d[self.e.s_d]["Klavyenizi test edin"])

    def klaye_modeli_secildi(self, value):
        for model in self.klavye_listesi.keys():
            if self.klavye_listesi[model] == value:
                self.e.milis_ayarlar["klavye_model"] = model, value

        self.klavye_resim.klavye_bilgi.emit(self.e.milis_ayarlar["klavye_model"][0],
                                        self.e.milis_ayarlar["klavye_duzeni"][0],
                                        self.e.milis_ayarlar["klavye_varyantı"])

    def ulke_secildi(self, value):
        for layout in self.layout_list.keys():
            if self.layout_list[layout] == value:
                self.e.milis_ayarlar["klavye_duzeni"] = layout, value

        self.keyboardVList.clear()
        self.e.milis_ayarlar["klavye_varyantı"] = None
        self.keyboardVList.addItem("Default")
        for k, v in self.variant_list.items():
            if k == self.e.milis_ayarlar["klavye_duzeni"][0]:
                for i in v:
                    self.keyboardVList.addItems(i.values())

        os.system("setxkbmap -layout {} -variant \"\"".format(self.e.milis_ayarlar["klavye_duzeni"][0]))
        self.klavye_resim.klavye_bilgi.emit(self.e.milis_ayarlar["klavye_model"][0],
                                        self.e.milis_ayarlar["klavye_duzeni"][0],
                                        self.e.milis_ayarlar["klavye_varyantı"])

    def klavye_tipi_secildi(self, value):
        if value == "Default":
            os.system("setxkbmap -variant \"\"")
            self.e.milis_ayarlar["klavye_varyantı"] = None
            self.klavye_resim.klavye_bilgi.emit(self.e.milis_ayarlar["klavye_model"][0],
                                            self.e.milis_ayarlar["klavye_duzeni"][0],
                                            self.e.milis_ayarlar["klavye_varyantı"])

        else:
            for variant in self.variant_list.keys():
                if variant in self.e.milis_ayarlar["klavye_duzeni"]:
                    for key in self.variant_list[variant]:
                        if key[list(key.keys())[0]] == value:
                            self.e.milis_ayarlar["klavye_varyantı"] = list(key.keys())[0], list(key.values())[0]
                            print("setxkbmap -variant {}".format(self.e.milis_ayarlar["klavye_varyantı"][0]))
                            os.system("setxkbmap -variant {}".format(self.e.milis_ayarlar["klavye_varyantı"][0]))

            varyant = self.e.milis_ayarlar["klavye_varyantı"]
            if varyant == None:
                varyant = [""]
            self.klavye_resim.klavye_bilgi.emit(self.e.milis_ayarlar["klavye_model"][0],
                                            self.e.milis_ayarlar["klavye_duzeni"][0],
                                            varyant[0])
