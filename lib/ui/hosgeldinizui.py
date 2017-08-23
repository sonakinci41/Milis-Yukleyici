#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QCheckBox, QComboBox, QHBoxLayout

class HosgeldinizPencere(QWidget):
    def __init__(self, ebeveyn=None):
        super(HosgeldinizPencere, self).__init__(ebeveyn)
        self.ebeveyn = ebeveyn

        self.diller = {"Afghani" : "af", "Albanian" : "al", "Armenian" : "am", "Arabic" : "ara", "German (Austria)" : "at",
                       "Azerbaijani" : "az", "Bosnian" : "ba", "Bangla" : "bd", "Belgian" : "be", "Bulgarian" : "bg",
                       "Portuguese (Brazil)": "br", "Braille": "brai", "Dzongkha":  "bt", "Tswana" : "bw", "Belarusian": "by",
                       "French (Canada)":"ca", "French (Democratic Republic of the Congo)":"cd", "German (Switzerland)":"ch",
                       "English (Cameroon)":"cm", "Chinese":"cn", "Czech":"cz", "German": "de", "Danish":"dk", "Estonian":"ee",
                       "Esperanto":"epo", "Spanish":"es", "Amharic":"et", "Finnish":"fi","Faroese": "fo", "French":"fr",
                       "English (UK)":"gb", "Georgian":"ge", "English (Ghana)":"gh", "French (Guinea)":"gn", "Greek":"gr",
                       "Croatian":"hr", "Hungarian":"hu", "Irish":"ie", "Hebrew":"il", "Indian":"in", "Iraqi":"iq",
                       "Persian":"ir", "Icelandic":"is", "Italian":"it", "Japanese":"jp", "Swahili (Kenya)":"ke",
                       "Kyrgyz":"kg", "Khmer (Cambodia)":"kh", "Korean":"kr", "Kazakh":"kz", "Lao":"la",
                       "Spanish (Latin American)":"latam", "Sinhala (phonetic)":"lk", "Lithuanian":"lt", "Latvian":"lv",
                       "Arabic (Morocco)":"ma", "Maori":"mao", "Moldavian":"md", "Montenegrin":"me", "Macedonian":"mk",
                       "Bambara":"ml", "Burmese":"mm", "Mongolian":"mn", "Maltese":"mt", "Dhivehi":"mv",
                       "Japanese (PC-98xx Series)":"nec_vndr/jp", "English (Nigeria)":"ng", "Dutch":"nl", "Norwegian":"no",
                       "Nepali":"np", "Filipino":"ph", "Urdu (Pakistan)":"pk", "Polish":"pl", "Portuguese":"pt",
                       "Romanian":"ro", "Serbian": "rs", "Russian":"ru", "Swedish":"se", "Slovenian":"si", "Slovak":"sk",
                       "Wolof":"sn", "Arabic (Syria)":"sy", "Thai":"th", "Tajik":"tj", "Turkmen":"tm","Turkish": "tr",
                       "Taiwanese":"tw", "Swahili (Tanzania)":"tz", "Ukrainian":"ua", "English (US)":"us", "Uzbek":"uz",
                       "Vietnamese":"vn","English (South Africa)":"za"}

        hosgedinizKutu=QVBoxLayout()
        self.setLayout(hosgedinizKutu)

        hosgeldinizYazi=QLabel(self.tr("<h1>Milis Linux Yükleyiciye Hoşgeldiniz</h1>"))
        hosgeldinizYazi.setAlignment(Qt.AlignCenter)
        hosgedinizKutu.addWidget(hosgeldinizYazi)

        dillerKutu=QHBoxLayout()
        hosgedinizKutu.addLayout(dillerKutu)

        dillerKutu.addWidget(QLabel(self.tr("Lütfen Sistem Ve Yükleyici İçin Bir Dil Seçiniz")))

        self.dillerCombo = QComboBox()
        dillerKutu.addWidget(self.dillerCombo)
        self.dillerCombo.currentTextChanged.connect(self.dillerComboDegisti)
        self.dillerComboDoldur()

        kullanimSartlari = QTextEdit()
        hosgedinizKutu.addWidget(kullanimSartlari)
        kullanimSartlari.setText(self.tr("""Milis Linux (Milli İşletim Sistemi) sıfır kaynak koddan üretilen,\n
        kendine has paket yöneticisine sahip,\n
        bağımsız tabanlı yerli linux işletim sistemi projesidir.\n
        Genel felsefe olarak ülkemizdeki bilgisayar kullanıcıları için linuxu kolaylaştırıp\n
        Milis İşletim Sisteminin sorunsuz bir işletim sistemi olmasını sağlamayı ve yazılımsal\n
        olarak dışa bağımlı olmaktan kurtarmayı esas alır. Ayrıca her türlü katkıda bulunmak\n
        isteyenler için bulunmaz bir Türkçe açık kaynak projesidir.\n"""))

        self.sartKabulKutusu=QCheckBox("Kullanım Şartlarını Kabul Ediyorum.")
        self.sartKabulKutusu.stateChanged.connect(self.sartKabulFonksiyon)
        hosgedinizKutu.addWidget(self.sartKabulKutusu)

    def sartKabulFonksiyon(self):
        if self.sartKabulKutusu.isChecked():
            self.ebeveyn.ileriDugme.setDisabled(False)
        else:
            self.ebeveyn.ileriDugme.setDisabled(True)

    def dillerComboDoldur(self):
        liste = list(self.diller.keys())
        liste.sort()
        self.dillerCombo.addItems(liste)
        self.dillerCombo.setCurrentText("Turkish")

    def dillerComboDegisti(self,dil):
        self.ebeveyn.sistemDili = self.diller[dil]