#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import parted
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox, QPushButton, QTreeWidget, QTreeWidgetItem, \
    QVBoxLayout, QMessageBox, QDialog, QCheckBox, QGridLayout, QInputDialog
from PyQt5.QtCore import Qt


class BolumlemePencere(QWidget):
    def __init__(self, ebeveyn=None):
        super(BolumlemePencere, self).__init__(ebeveyn)
        self.ebeveyn = ebeveyn

        self.sistemDiski = ["", ""]
        self.takasDiski = ["", ""]
        self.seciliDisk = None
        self.diskler = parted.getAllDevices()
        disklerWidget = QWidget()
        disklerLayout = QHBoxLayout()
        self.disklerAcilirKutu = QComboBox()
        self.yenileButon = QPushButton(self.tr("Yenile"))
        self.yenileButon.pressed.connect(self.diskYenile)

        self.bolumListeKutu = QTreeWidget()
        self.bolumListeKutu.setColumnCount(4)
        self.bolumListeKutu.headerItem().setText(0, self.tr("bölüm"))
        self.bolumListeKutu.headerItem().setText(1, self.tr("kullanım"))
        self.bolumListeKutu.headerItem().setText(2, self.tr("boyut"))
        self.bolumListeKutu.headerItem().setText(3, self.tr("format"))
        # self.bolumListeKutu.headerItem().setText(4, self.tr("bayraklar"))
        self.bolumListeKutu.headerItem().setText(4, self.tr("bölüm numarası"))

        self.disklerAcilirKutu.currentIndexChanged.connect(self.diskDegisti)

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
        self.diskYenile()

    def diskYenile(self):
        self.disklerAcilirKutu.clear()
        self.diskler = parted.getAllDevices()
        for disk in self.diskler:
            try:
                if parted.Disk(disk).type == "msdos":
                    self.disklerAcilirKutu.addItem(
                        "{} {} GB ({})".format(disk.model, format(disk.getSize(unit="GB"), '.2f'), disk.path),
                        userData=disk.path)
            except parted.DiskLabelException:
                disk = parted.freshDisk(disk, "msdos")
                # CDROM Aygıtları için
                try:
                    disk.commit()
                except parted.IOException:
                    pass
                else:
                    disk = disk.device
                    self.disklerAcilirKutu.addItem(
                        "{} {} GB ({})".format(disk.model, format(disk.getSize(unit="GB"), '.2f'), disk.path),
                        userData=disk.path)

    def diskDegisti(self):
        if self.disklerAcilirKutu.currentData():
            self.aygit = parted.getDevice(self.disklerAcilirKutu.currentData())
            self.ebeveyn.disk = parted.Disk(self.aygit)
            self.bolumListeYenile()

    def bolumListeYenile(self):
        self.extended = None
        self.bolumListeKutu.clear()
        for bolum in self.ebeveyn.disk.partitions:
            _bolum = self.bolumBilgi(bolum, "GB")
            if self.sistemDiski and bolum.path == self.sistemDiski[0]:
                if self.sistemDiski[1] == "evet":
                    item = self.treeWidgetItemOlustur(_bolum["yol"], self.tr("Sistem Diski"), _bolum["boyut"] + " GB",
                                                      "ext4", _bolum["bayraklar"], _bolum["no"])
                else:
                    item = self.treeWidgetItemOlustur(_bolum["yol"], self.tr("Sistem Diski"), _bolum["boyut"],
                                                      _bolum["dosyaSis"], _bolum["bayraklar"], _bolum["no"])
            elif self.takasDiski and bolum.path == self.takasDiski[0]:
                item = self.treeWidgetItemOlustur(_bolum["yol"], self.tr("Takas Alanı"), _bolum["boyut"],
                                                  self.tr("takas"), _bolum["bayraklar"], _bolum["no"])
            else:
                item = self.treeWidgetItemOlustur(_bolum["yol"], "", _bolum["boyut"], _bolum["dosyaSis"],
                                                  _bolum["bayraklar"], _bolum["no"])

            if _bolum["tur"] == parted.PARTITION_NORMAL:
                item.setIcon(0, QIcon("gorseller/primary.xpm"))
            elif _bolum["tur"] == parted.PARTITION_EXTENDED:
                item.setIcon(0, QIcon("gorseller/extended.xpm"))
                self.extended = item
            elif _bolum["tur"] == parted.PARTITION_LOGICAL:
                item.setIcon(0, QIcon("gorseller/logical.xpm"))
                self.extended.addChild(item)
                self.extended.setExpanded(True)
            self.bolumListeKutu.addTopLevelItem(item)

        for bosBolum in self.ebeveyn.disk.getFreeSpacePartitions():
            _toplam = 0
            _bolum = self.bolumBilgi(bosBolum, "GB")
            if float(_bolum["boyut"]) > 1:
                if _bolum["tur"] == 5:
                    uzatilmisKalan = self.treeWidgetItemOlustur("", self.tr("Uzatılmış Bölüm Kalan"), _bolum["boyut"],
                                                                "", "", "ayrilmamis")
                    uzatilmisKalan.setIcon(0, QIcon(":/gorseller/blank.xpm"))
                    self.extended.addChild(uzatilmisKalan)
                    self.extended.setExpanded(True)
                if _bolum["tur"] == parted.PARTITION_FREESPACE:
                    _toplam = _toplam + float(_bolum["boyut"])
                ayrilmamis = self.treeWidgetItemOlustur("", self.tr("Ayrılmamış Bölüm"), _toplam, "", "", "ayrilmamis")
                ayrilmamis.setIcon(0, QIcon(":/gorseller/blank.xpm"))
                self.bolumListeKutu.addTopLevelItem(ayrilmamis)
        self.bolumListeKutu.resizeColumnToContents(0)
        self.bolumListeKutu.resizeColumnToContents(1)
        self.bolumListeKutu.resizeColumnToContents(2)
        self.bolumListeKutu.resizeColumnToContents(3)

    def treeWidgetItemOlustur(self, bolum, kullanim, boyut, format, islev, bolumno):
        item = QTreeWidgetItem()
        item.setText(0, str(bolum))
        item.setText(1, str(kullanim))
        item.setText(2, str(boyut) + " GB ")
        item.setText(3, str(format))
        # item.setText(4, str(islev))
        item.setText(4, str(bolumno))
        return item

    def bolumSecildiFonk(self, tiklanan):
        if tiklanan.text(5) != "ayrilmamis":
            self.bolumSilBtn.setEnabled(True)
        else:
            self.bolumSilBtn.setEnabled(False)

    def bolumFormatSecFonk(self, tiklanan):
        if tiklanan.text(5) != "ayrilmamis":
            self.seciliDisk = tiklanan
            diskOzellikPencere = diskOzellikleriSinif(self)
            diskOzellikPencere.exec_()
            if self.sistemDiski[0] != "":
                self.ebeveyn.kurparam["disk"]["bolum"] = self.sistemDiski[0]
                self.ebeveyn.kurparam["disk"]["format"] = self.sistemDiski[1]
            if self.takasDiski[0] != "":
                self.ebeveyn.kurparam["disk"]["takasbolum"] = self.takasDiski[0]
            else:
                self.ebeveyn.kurparam["disk"]["takasbolum"] = ""

            if self.sistemDiski[0] == "":
                pass
            elif self.sistemDiski[0] != "" and self.takasDiski[0] == "":
                QMessageBox.information(self, self.tr("Bilgi"), self.tr(
                    "Takas Alanı Belirtmediniz\nTakas alanı ram miktarınızın düşük olduğu durumlarda\nram yerine disk kullanarak işlemlerin devam etmesini sağlar."))
                self.ebeveyn.ileriDugme.setDisabled(False)
                self.bolumListeYenile()
            elif self.sistemDiski[0] != "" and self.takasDiski[0] != "":
                if self.sistemDiski[0] == self.takasDiski[0]:
                    QMessageBox.warning(self, self.tr("Hata"), self.takasDiski[0] + self.tr(
                        " diskini hem sistem hem takas için seçtiniz\nAynı diski hem sistem hem takas olarak kullanmazsınız"))
                    self.ebeveyn.ileriDugme.setDisabled(True)
                else:
                    self.ebeveyn.ileriDugme.setDisabled(False)
                    self.bolumListeYenile()

    def bolumEkleFonk(self):
        if self._en_buyuk_bos_alan():
            alan = self._en_buyuk_bos_alan()
            birincilSayi = len(self.ebeveyn.disk.getPrimaryPartitions())
            uzatilmisSayi = ext_count = 1 if self.ebeveyn.disk.getExtendedPartition() else 0
            parts_avail = self.ebeveyn.disk.maxPrimaryPartitionCount - (birincilSayi + uzatilmisSayi)
            if not parts_avail and not ext_count:
                QMessageBox.warning(self, self.tr("Uyarı"),
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
                    ext_part = self.ebeveyn.disk.getExtendedPartition()
                    try:
                        alan = ext_part.geometry.intersect(alan)
                    except ArithmeticError:
                        QMessageBox.critical(self, self.tr("Hata"), self.tr(
                            "Yeni disk bölümü oluşturmak için yeterli alan yok ! Uzatılmış bölümün boyutunu arttırmayı deneyiniz."))
                    else:
                        self.bolumOlustur(alan, parted.PARTITION_LOGICAL)
                        self.bolumListeYenile()

    def bolumSilFonk(self):
        bolumNo = int(self.bolumListeKutu.currentItem().text(4))
        for bolum in self.ebeveyn.disk.partitions:
            if bolum.number == bolumNo:
                try:
                    self.ebeveyn.disk.deletePartition(bolum)
                    self.bolumListeYenile()
                except parted.PartitionException:
                    QMessageBox.warning(self, self.tr("Uyarı"), self.tr(
                        "Lütfen uzatılmış bölümleri silmeden önce mantıksal bölümleri siliniz."))
        self.bolumSilBtn.setDisabled(True)

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

        for _alan in self.ebeveyn.disk.getFreeSpaceRegions():
            if _alan.length > maks_boyut and _alan.length > alignment.grainSize:
                alan = _alan
                maks_boyut = _alan.length
        return alan

    def bolumOlustur(self, alan, bolumTur):
        if bolumTur == parted.PARTITION_NORMAL or bolumTur == parted.PARTITION_EXTENDED:
            for bosBolum in self.ebeveyn.disk.getFreeSpacePartitions():
                _bolum = self.bolumBilgi(bosBolum, "GB")
                if _bolum["tur"] == parted.PARTITION_FREESPACE:
                    maksBoyut = float(_bolum["boyut"])
        elif bolumTur == bolumTur == parted.PARTITION_LOGICAL:
            for bosBolum in self.ebeveyn.disk.getFreeSpacePartitions():
                _bolum = self.bolumBilgi(bosBolum, "GB")
                if _bolum["tur"] == 5:
                    maksBoyut = float(_bolum["boyut"])

        alignment = self.aygit.optimalAlignedConstraint
        constraint = self.aygit.getConstraint()
        data = {
            'start': constraint.startAlign.alignUp(alan, alan.start),
            'end': constraint.endAlign.alignDown(alan, alan.end),
        }

        boyut, ok = QInputDialog().getDouble(self, self.tr('Bölüm oluştur'), self.tr('GB cinsinden boyut:'), min=0.001,
                                             value=1, max=maksBoyut, decimals=3)

        if ok:
            data["end"] = int(data["start"]) + int(parted.sizeToSectors(float(boyut), "GiB", self.aygit.sectorSize))
            try:
                geometry = parted.Geometry(device=self.aygit, start=int(data["start"]), end=int(data["end"]))
                partition = parted.Partition(
                    disk=self.ebeveyn.disk,
                    type=bolumTur,
                    geometry=geometry,
                )

                self.ebeveyn.disk.addPartition(partition=partition, constraint=constraint)
            except (parted.PartitionException, parted.GeometryException, parted.CreateException) as e:
                # GeometryException accounts for incorrect start/end values (e.g. start < end),
                # CreateException is raised e.g. when the partition doesn't fit on the disk.
                # PartedException is a generic error (e.g. start/end values out of range)
                raise RuntimeError(e.message)


class diskOzellikleriSinif(QDialog):
    def __init__(self, ebeveyn=None):
        super(diskOzellikleriSinif, self).__init__(ebeveyn)
        self.ebeveyn = ebeveyn
        disk_ = self.ebeveyn.seciliDisk
        self.baslik_ = disk_.text(0)
        format_ = disk_.text(3)
        self.setWindowTitle(self.baslik_)
        diskOzellikKutu = QGridLayout()
        self.setLayout(diskOzellikKutu)
        self.secenekAcilirListe = QComboBox()
        self.secenekAcilirListe.addItem(self.tr("Sistem Diski"))
        self.secenekAcilirListe.addItem(self.tr("Takas Alanı"))
        diskOzellikKutu.addWidget(self.secenekAcilirListe, 0, 0, 1, 1)
        self.diskBicimlendirKutu = QCheckBox(self.tr("Diski Biçimlendir"))
        if format_ != "ext4":
            self.diskBicimlendirKutu.setChecked(True)
            self.diskBicimlendirKutu.setDisabled(True)
        diskOzellikKutu.addWidget(self.diskBicimlendirKutu, 1, 0, 1, 1)
        tamamDugme = QPushButton(self.tr("Tamam"))
        tamamDugme.pressed.connect(self.tamamBasildiFonk)
        diskOzellikKutu.addWidget(tamamDugme, 2, 0, 1, 1)

    def tamamBasildiFonk(self):
        if self.secenekAcilirListe.currentText() == self.tr("Sistem Diski"):
            self.ebeveyn.sistemDiski = [self.baslik_]
            if self.diskBicimlendirKutu.isChecked():
                self.ebeveyn.sistemDiski.append("evet")
            else:
                self.ebeveyn.sistemDiski.append("hayir")
        elif self.secenekAcilirListe.currentText() == self.tr("Takas Alanı"):
            self.ebeveyn.takasDiski = [self.baslik_]
            if self.diskBicimlendirKutu.isChecked():
                self.ebeveyn.takasDiski.append("evet")
            else:
                self.ebeveyn.takasDiski.append("hayir")
        QDialog.accept(self)
