#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QCheckBox

class HosgeldinizPencere(QWidget):
    def __init__(self, ebeveyn=None):
        super(HosgeldinizPencere, self).__init__(ebeveyn)
        self.ebeveyn = ebeveyn

        hosgedinizKutu=QVBoxLayout()
        self.setLayout(hosgedinizKutu)

        hosgeldinizYazi=QLabel("Milis Linux Yükleyiciye Hoşgeldiniz")
        hosgedinizKutu.addWidget(hosgeldinizYazi)

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