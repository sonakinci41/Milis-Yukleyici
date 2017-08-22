#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import parted
from PyQt5.QtGui import  QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox, QPushButton, QListWidget, QListWidgetItem, QVBoxLayout, QMessageBox, QDialog, QCheckBox, QGridLayout
from PyQt5.QtCore import Qt

class BolumlemePencere(QWidget):
    def __init__(self, ebeveyn=None):
        super(BolumlemePencere, self).__init__(ebeveyn)
        self.ebeveyn = ebeveyn


        self.sistemDiski = ""
        self.takasDiski = ""
        self.seciliDisk = None
        self.diskler = parted.getAllDevices()
        disklerWidget = QWidget()
        disklerLayout = QHBoxLayout()
        self.disklerAcilirKutu = QComboBox()
        self.yenileButon = QPushButton(self.tr("Yenile"))
        self.yenileButon.pressed.connect(self.diskYenile)

        self.bolumListeKutu = QListWidget()
        self.diskYenile()
        self.disklerAcilirKutu.currentIndexChanged.connect(self.diskDegisti)
        self.diskDegisti()

        disklerLayout.addWidget(self.disklerAcilirKutu)
        disklerLayout.addWidget(self.yenileButon)
        disklerWidget.setLayout(disklerLayout)
        layout = QVBoxLayout()
        layout.addWidget(disklerWidget)
        layout.addWidget(self.bolumListeKutu)
        lejant = QLabel()
        lejant.setPixmap(QPixmap(":/gorseller/lejant.png"))
        lejant.setAlignment(Qt.AlignCenter)
        layout.addWidget(lejant)
        self.bolumListeKutu.itemClicked.connect(self.bolumSecildiFonk)
        self.bolumListeKutu.itemDoubleClicked.connect(self.bolumFormatSecFonk)

        opWidget = QWidget()
        opButonlar = QHBoxLayout()
        self.yeniBolumBtn = QPushButton(self.tr("Yeni Bölüm Ekle"))
        self.yeniBolumBtn.pressed.connect(self.bolumEkleFonk)
        self.bolumSilBtn = QPushButton(self.tr("Bölümü Sil"))
        self.bolumSilBtn.pressed.connect(self.bolumSilFonk)
        opButonlar.addWidget(self.yeniBolumBtn)
        opButonlar.addWidget(self.bolumSilBtn)
        opWidget.setLayout(opButonlar)
        layout.addWidget(opWidget)

        self.bolumSilBtn.setEnabled(False)
        self.setLayout(layout)

    def diskYenile(self):
        self.disklerAcilirKutu.clear()
        self.diskler = parted.getAllDevices()
        for disk in self.diskler:
            try:
                if parted.Disk(disk).type == "msdos":
                    self.disklerAcilirKutu.addItem("{} {} GB ({})".format(disk.model, format(disk.getSize(unit="GB"), '.2f'), disk.path),userData=disk.path)
            except parted.DiskLabelException:
                disk = parted.freshDisk(disk, "msdos")
                # CDROM Aygıtları için
                try:
                    disk.commit()
                except parted.IOException:
                    pass
                else:
                    disk = disk.device
                    self.disklerAcilirKutu.addItem("{} {} GB ({})".format(disk.model, format(disk.getSize(unit="GB"), '.2f'), disk.path),userData=disk.path)

    def diskDegisti(self):
        if self.disklerAcilirKutu.currentData():
            self.aygit = parted.getDevice(self.disklerAcilirKutu.currentData())
            self.disk = parted.Disk(self.aygit)
            self.bolumListeYenile()

    def bolumListeYenile(self):
        self.bolumListeKutu.clear()
        for bolum in self.disk.partitions:
            _bolum = self.bolumBilgi(bolum, "GB")
            if self.sistemDiski and bolum.path == self.sistemDiski[0]:
                if self.sistemDiski[1] == self.tr("Evet"):
                    item = QListWidgetItem(self.tr("{}\t\t Sistem Diski \t\t {} GB \t\t {} \t\t {}").format(_bolum["yol"], _bolum["boyut"], "ext4",_bolum["bayraklar"]))
                else:
                    item = QListWidgetItem(self.tr("{}\t\t Sistem Diski \t\t {} GB \t\t {} \t\t {}").format(_bolum["yol"], _bolum["boyut"],_bolum["dosyaSis"], _bolum["bayraklar"]))
            elif self.takasDiski and bolum.path == self.takasDiski[0]:
                item = QListWidgetItem(self.tr("{}\t\t Takas Alanı \t\t {} GB \t\t {} \t\t {}").format(_bolum["yol"], _bolum["boyut"], "takas",_bolum["bayraklar"]))
            else:
                item = QListWidgetItem(self.tr("{}\t\t {} GB \t\t {} \t\t {}").format(_bolum["yol"], _bolum["boyut"], _bolum["dosyaSis"],_bolum["bayraklar"]))

            item.setData(Qt.UserRole, _bolum["no"])
            if _bolum["tur"] == parted.PARTITION_NORMAL:
                item.setIcon(QIcon("gorseller/primary.xpm"))
            elif _bolum["tur"] == parted.PARTITION_EXTENDED:
                item.setIcon(QIcon("gorseller/extended.xpm"))
            elif _bolum["tur"] == parted.PARTITION_LOGICAL:
                item.setIcon(QIcon("gorseller/logical.xpm"))
            self.bolumListeKutu.addItem(item)

            for bosBolum in self.disk.getFreeSpacePartitions():
                _toplam = 0
                _bolum = self.bolumBilgi(bosBolum, "GB")
                if float(_bolum["boyut"]) > 0:
                    if _bolum["tur"] == 5:
                        uzatilmisKalan = QListWidgetItem("{}\t{} GB".format(self.tr("Uzatılmış Bölüm Kalan"), _bolum["boyut"]))
                        uzatilmisKalan.setIcon(QIcon(":/gorseller/blank.xpm"))
                        uzatilmisKalan.setData(Qt.UserRole, "ayrilmamis")
                        self.bolumListeKutu.addItem(uzatilmisKalan)
                    if _bolum["tur"] == parted.PARTITION_FREESPACE:
                        _toplam = _toplam + float(_bolum["boyut"])
                    ayrilmamis = QListWidgetItem("{}\t{} GB".format(self.tr("Ayrılmamış Bölüm"), _toplam))
                    ayrilmamis.setIcon(QIcon(":/gorseller/blank.xpm"))
                    ayrilmamis.setData(Qt.UserRole, "ayrilmamis")
                    self.bolumListeKutu.addItem(ayrilmamis)

    def bolumSecildiFonk(self, tiklanan):
        if tiklanan.data(Qt.UserRole) != "ayrilmamis":
            self.bolumSilBtn.setEnabled(True)
        else:
            self.bolumSilBtn.setEnabled(False)


    def bolumFormatSecFonk(self, tiklanan):
        if tiklanan.data(Qt.UserRole) != "ayrilmamis":
            self.seciliDisk = tiklanan.text()
            diskOzellikPencere = diskOzellikleriSinif(self)
            diskOzellikPencere.exec_()
            if self.sistemDiski != "":
                self.ebeveyn.kurparam["disk"]["bolum"] = self.sistemDiski[0]
                self.ebeveyn.kurparam["disk"]["format"] = self.sistemDiski[1]
            if self.takasDiski != "":
                self.ebeveyn.kurparam["disk"]["takasbolum"] = self.takasDiski[0]
            else:
                self.ebeveyn.kurparam["disk"]["takasbolum"] = ""

            if self.sistemDiski == "":
                pass
            elif self.sistemDiski != "" and self.takasDiski == "":
                QMessageBox.information(self, self.tr("Bilgi"),self.tr("Takas Alanı Belirtmediniz\nTakas alanı ram miktarınızın düşük olduğu durumlarda\nram yerine disk kullanarak işlemlerin devam etmesini sağlar."))
                self.ebeveyn.ileriDugme.setDisabled(False)
                self.bolumListeYenile()
            elif self.sistemDiski != "" and self.takasDiski != "":
                if self.sistemDiski[0] == self.takasDiski[0]:
                    QMessageBox.warning(self, self.tr("Hata"), self.takasDiski[0] + self.tr(" diskini hem sistem hem takas için seçtiniz\nAynı diski hem sistem hem takas olarak kullanmazsınız"))
                    self.ebeveyn.ileriDugme.setDisabled(True)
                else:
                    self.ebeveyn.ileriDugme.setDisabled(False)
                    self.bolumListeYenile()

    def bolumEkleFonk(self):
        if self._en_buyuk_bos_alan():
            alan = self._en_buyuk_bos_alan()
            birincilSayi = len(self.disk.getPrimaryPartitions())
            uzatilmisSayi = ext_count = 1 if self.disk.getExtendedPartition() else 0
            parts_avail = self.disk.maxPrimaryPartitionCount - (birincilSayi + uzatilmisSayi)
            if not parts_avail and not ext_count:
                QMessageBox.warning(self,self.tr("Uyarı"),
                                    self.tr("""Eğer dörtten fazla disk bölümü oluşturmak istiyorsanız birincil bölümlerden birini silip uzatılmış bölüm oluşturun. 
                                    Bu durumda oluşturduğunuz uzatılmış bölümleri işletim sistemi kurmak için kullanamayacağınızı aklınızda bulundurun."""))
            else:
                if parts_avail:
                    if not uzatilmisSayi and parts_avail > 1:
                        self.bolumOlustur(alan, parted.PARTITION_NORMAL)
                        self.bolumListeYenile()
                    elif parts_avail == 1:
                        self.bolumOlustur(alan, parted.PARTITION_EXTENDED)
                        self.bolumListeYenile()
                if uzatilmisSayi:
                    ext_part = self.disk.getExtendedPartition()
                    try:
                        alan = ext_part.geometry.intersect(alan)
                    except ArithmeticError:
                        QMessageBox.critical(self,self.tr("Hata"),self.tr("Yeni disk bölümü oluşturmak için yeterli alan yok ! Uzatılmış bölümün boyutunu arttırmayı deneyiniz."))
                    else:
                        self.bolumOlustur(alan, parted.PARTITION_LOGICAL)
                        self.bolumListeYenile()

    def bolumSilFonk(self):
        bolumNo = self.bolumListeKutu.currentItem().data(Qt.UserRole)
        for bolum in self.disk.partitions:
            if bolum.number == bolumNo:
                try:
                    self.disk.deletePartition(bolum)
                    self.bolumListeYenile()
                except parted.PartitionException:
                    QMessageBox.warning(self,self.tr("Uyarı"),self.tr("Lütfen uzatılmış bölümleri silmeden önce mantıksal bölümleri siliniz."))
        self.bolumListeKutu.setCurrentRow(self.bolumListeKutu.count() - 2)


    def bolumBilgi(self, bolum, birim):
        _bolum = {}
        _bolum["yol"] = bolum.path
        if birim == "GB":
            _bolum["boyut"] = format(bolum.getSize(unit=birim), '.2f')
        else:
            _bolum["boyut"] = bolum.getSize(unit=birim)
        _bolum["dosyaSis"] = "Bilinmeyen"

        if bolum.fileSystem:
            if bolum.fileSystem.type.startswith('linux-swap'):
                _bolum["dosyaSis"] = "takas"
            else:
                _bolum["dosyaSis"] = bolum.fileSystem.type
        try:
            _bolum["bayraklar"] = bolum.getFlagsAsString()
        except:
            pass
        _bolum["no"] = bolum.number
        _bolum["tur"] = bolum.type
        return _bolum

    def _en_buyuk_bos_alan(self):
        maks_boyut = -1
        alan = None
        alignment = self.aygit.optimumAlignment

        for _alan in self.disk.getFreeSpaceRegions():
            if _alan.length > maks_boyut and _alan.length > alignment.grainSize:
                alan = _alan
                maks_boyut = _alan.length
        return alan


class diskOzellikleriSinif(QDialog):
    def __init__(self,ebeveyn=None):
        super(diskOzellikleriSinif,self).__init__(ebeveyn)
        self.ebeveyn = ebeveyn
        disk_=self.ebeveyn.seciliDisk.split("\t")
        self.baslik_=disk_[0]
        format_=disk_[3]
        self.setWindowTitle(self.baslik_)
        diskOzellikKutu=QGridLayout()
        self.setLayout(diskOzellikKutu)
        self.secenekAcilirListe=QComboBox()
        self.secenekAcilirListe.addItem(self.tr("Sistem Diski"))
        self.secenekAcilirListe.addItem(self.tr("Takas Alanı"))
        diskOzellikKutu.addWidget(self.secenekAcilirListe,0,0,1,1)
        self.diskBicimlendirKutu = QCheckBox(self.tr("Diski Biçimlendir"))
        if format_ != "ext4":
            self.diskBicimlendirKutu.setChecked(True)
            self.diskBicimlendirKutu.setDisabled(True)
        diskOzellikKutu.addWidget(self.diskBicimlendirKutu,1,0,1,1)
        tamamDugme=QPushButton(self.tr("Tamam"))
        tamamDugme.pressed.connect(self.tamamBasildiFonk)
        diskOzellikKutu.addWidget(tamamDugme,2,0,1,1)

    def tamamBasildiFonk(self):
        if self.secenekAcilirListe.currentText() == self.tr("Sistem Diski"):
            self.ebeveyn.sistemDiski = [self.baslik_]
            if self.diskBicimlendirKutu.isChecked():
                self.ebeveyn.sistemDiski.append(self.tr("Evet"))
            else:
                self.ebeveyn.sistemDiski.append(self.tr("Hayır"))
        elif self.secenekAcilirListe.currentText() == self.tr("Takas Alanı"):
            self.ebeveyn.takasDiski = [self.baslik_]
            if self.diskBicimlendirKutu.isChecked():
                self.ebeveyn.takasDiski.append(self.tr("Evet"))
            else:
                self.ebeveyn.takasDiski.append(self.tr("Hayır"))
        QDialog.accept(self)