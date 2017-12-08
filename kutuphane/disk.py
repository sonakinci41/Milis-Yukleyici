import parted
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QPushButton, QTreeWidget, QTreeWidgetItem, \
    QMessageBox, QDialog, QCheckBox, QGridLayout, QInputDialog, QHeaderView
from PyQt5.QtCore import Qt


class Disk(QWidget):
    def __init__(self, ebeveyn=None):
        super(Disk, self).__init__(ebeveyn)
        self.e = ebeveyn
        diskler_kutu = QGridLayout()
        self.setLayout(diskler_kutu)

        self.sistemDiski = ["", ""]
        self.takasDiski = ["", ""]
        self.seciliDisk = None
        self.diskler = parted.getAllDevices()
        self.disklerAcilirKutu = QComboBox()
        self.yenileButon = QPushButton()
        self.yenileButon.setIcon(QIcon("./resimler/yenile.svg"))
        self.yenileButon.pressed.connect(self.diskYenile)

        self.bolumListeKutu = QTreeWidget()
        self.bolumListeKutu.setColumnCount(4)
        self.bolumListeKutu.header().setStretchLastSection(False);
        self.bolumListeKutu.header().setSectionResizeMode(0, QHeaderView.Stretch);
        self.bolumListeKutu.header().setSectionResizeMode(1, QHeaderView.Stretch);
        self.bolumListeKutu.header().setSectionResizeMode(2, QHeaderView.Stretch);
        self.bolumListeKutu.header().setSectionResizeMode(3, QHeaderView.Stretch);

        self.disklerAcilirKutu.currentIndexChanged.connect(self.diskDegisti)

        diskler_kutu.addWidget(self.disklerAcilirKutu,0,0,1,6)
        diskler_kutu.addWidget(self.yenileButon,0,6,1,2)
        diskler_kutu.addWidget(self.bolumListeKutu,1,0,1,8)


        resim_label = QLabel()
        resim_label.setFixedSize(16,16)
        resim_label.setPixmap(QPixmap("./resimler/blank.svg"))
        diskler_kutu.addWidget(resim_label,2,0,1,1)
        self.blank_label = QLabel()
        diskler_kutu.addWidget(self.blank_label,2,1,1,1)
        resim_label = QLabel()
        resim_label.setFixedSize(16, 16)
        resim_label.setPixmap(QPixmap("./resimler/extended.svg"))
        diskler_kutu.addWidget(resim_label,2,2,1,1)
        self.extended_label = QLabel()
        diskler_kutu.addWidget(self.extended_label,2,3,1,1)
        resim_label = QLabel()
        resim_label.setFixedSize(16, 16)
        resim_label.setPixmap(QPixmap("./resimler/logical.svg"))
        diskler_kutu.addWidget(resim_label,2,4,1,1)
        self.logical_label = QLabel()
        diskler_kutu.addWidget(self.logical_label,2,5,1,1)
        resim_label = QLabel()
        resim_label.setFixedSize(16, 16)
        resim_label.setPixmap(QPixmap("./resimler/primary.svg"))
        diskler_kutu.addWidget(resim_label,2,6,1,1)
        self.primary_label = QLabel()
        diskler_kutu.addWidget(self.primary_label,2,7,1,1)

        self.bolumListeKutu.itemClicked.connect(self.bolumSecildiFonk)
        self.bolumListeKutu.itemDoubleClicked.connect(self.bolumFormatSecFonk)

        self.yeniBolumBtn = QPushButton()
        self.yeniBolumBtn.setIcon(QIcon("./resimler/yeni_bolum.svg"))
        self.yeniBolumBtn.pressed.connect(self.bolumEkleFonk)
        self.bolumSilBtn = QPushButton()
        self.bolumSilBtn.setIcon(QIcon("./resimler/bolum_sil.svg"))
        self.bolumSilBtn.pressed.connect(self.bolumSilFonk)
        diskler_kutu.addWidget(self.yeniBolumBtn,3,4,1,2)
        diskler_kutu.addWidget(self.bolumSilBtn,3,6,1,2)

        self.bolumSilBtn.setEnabled(False)
        self.diskYenile()

    def diskYenile(self):
        self.disklerAcilirKutu.clear()
        self.diskler = parted.getAllDevices()
        for disk in self.diskler:
            try:
                if parted.Disk(disk).type == "msdos" or parted.Disk(disk).type == "gpt" :
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
            self.e.disk = parted.Disk(self.aygit)
            self.bolumListeYenile()

    def bolumListeYenile(self):
        self.extended = None
        self.bolumListeKutu.clear()
        for bolum in self.e.disk.partitions:
            _bolum = self.bolumBilgi(bolum, "GB")
            if self.sistemDiski and bolum.path == self.sistemDiski[0]:
                if self.sistemDiski[1]:
                    item = self.treeWidgetItemOlustur(_bolum["yol"], self.e.d[self.e.s_d]["Sistem Diski"], _bolum["boyut"],
                                                      "ext4", _bolum["bayraklar"], _bolum["no"])
                else:
                    item = self.treeWidgetItemOlustur(_bolum["yol"], self.e.d[self.e.s_d]["Sistem Diski"], _bolum["boyut"],
                                                      _bolum["dosyaSis"], _bolum["bayraklar"], _bolum["no"])
            elif self.takasDiski and bolum.path == self.takasDiski[0]:
                item = self.treeWidgetItemOlustur(_bolum["yol"], self.e.d[self.e.s_d]["Takas Alanı"], _bolum["boyut"],
                                                  self.e.d[self.e.s_d]["takas"], _bolum["bayraklar"], _bolum["no"])
            else:
                item = self.treeWidgetItemOlustur(_bolum["yol"], "", _bolum["boyut"], _bolum["dosyaSis"],
                                                  _bolum["bayraklar"], _bolum["no"])

            if _bolum["tur"] == parted.PARTITION_NORMAL:
                item.setIcon(0, QIcon("./resimler/primary.svg"))
            elif _bolum["tur"] == parted.PARTITION_EXTENDED:
                item.setIcon(0, QIcon("./resimler/extended.svg"))
                self.extended = item
            elif _bolum["tur"] == parted.PARTITION_LOGICAL:
                item.setIcon(0, QIcon("./resimler/logical.svg"))
                self.extended.addChild(item)
                self.extended.setExpanded(True)
            self.bolumListeKutu.addTopLevelItem(item)

        for bosBolum in self.e.disk.getFreeSpacePartitions():
            _toplam = 0
            _bolum = self.bolumBilgi(bosBolum, "GB")
            if float(_bolum["boyut"]) > 1:
                if _bolum["tur"] == 5:
                    uzatilmisKalan = self.treeWidgetItemOlustur("", self.e.d[self.e.s_d]["Uzatılmış Bölüm Kalan"], _bolum["boyut"],
                                                                "", "", "ayrilmamis")
                    uzatilmisKalan.setIcon(0, QIcon("./resimler/blank.svg"))
                    self.extended.addChild(uzatilmisKalan)
                    self.extended.setExpanded(True)
                if _bolum["tur"] == parted.PARTITION_FREESPACE:
                    _toplam = _toplam + float(_bolum["boyut"])
                ayrilmamis = self.treeWidgetItemOlustur("", self.e.d[self.e.s_d]["Ayrılmamış Bölüm"], _toplam, "", "", "ayrilmamis")
                ayrilmamis.setIcon(0, QIcon("./resimler/blank.svg"))
                self.bolumListeKutu.addTopLevelItem(ayrilmamis)

    def treeWidgetItemOlustur(self, bolum, kullanim, boyut, format, islev, bolumno):
        item = QTreeWidgetItem()
        item.setText(0, str(bolum))
        item.setText(1, str(kullanim))
        item.setText(2, str(boyut) + " GB ")
        item.setText(3, str(format))
        item.setData(0,Qt.UserRole, bolumno)
        return item

    def bolumSecildiFonk(self, tiklanan):
        if tiklanan.data(0,Qt.UserRole) != "ayrilmamis":
            self.bolumSilBtn.setEnabled(True)
        else:
            self.bolumSilBtn.setEnabled(False)

    def bolumFormatSecFonk(self, tiklanan):
        if tiklanan.data(0,Qt.UserRole) != "ayrilmamis":
            self.seciliDisk = tiklanan
            diskOzellikPencere = diskOzellikleriSinif(self)
            diskOzellikPencere.exec_()
            if self.sistemDiski[0] != "":
                self.e.milis_ayarlar["disk_bolum"] = self.sistemDiski[0]
                self.e.milis_ayarlar["disk_format"] = self.sistemDiski[1]
            if self.takasDiski[0] != "":
                self.e.milis_ayarlar["disk_takasbolum"] = self.takasDiski[0]
            else:
                self.e.milis_ayarlar["disk_takasbolum"] = ""

            if self.sistemDiski[0] == "":
                pass
            elif self.sistemDiski[0] != "" and self.takasDiski[0] == "":
                QMessageBox.information(self, self.e.d[self.e.s_d]["Bilgi"], self.e.d[self.e.s_d]["Takas Alanı Belirtmediniz Takas alanı ram miktarınızın düşük olduğu durumlarda ram yerine disk kullanarak işlemlerin devam etmesini sağlar."])
                self.e.ileri_dugme.setDisabled(False)
                self.bolumListeYenile()
            elif self.sistemDiski[0] != "" and self.takasDiski[0] != "":
                if self.sistemDiski[0] == self.takasDiski[0]:
                    QMessageBox.warning(self, self.e.d[self.e.s_d]["Hata"], self.takasDiski[0] + self.e.d[self.e.s_d][" diskini hem sistem hem takas için seçtiniz. Aynı diski hem sistem hem takas olarak kullanmazsınız."])
                    self.e.ileri_dugme.setDisabled(True)
                else:
                    self.e.ileri_dugme.setDisabled(False)
                    self.bolumListeYenile()

    def bolumEkleFonk(self):
        if self._en_buyuk_bos_alan():
            alan = self._en_buyuk_bos_alan()
            birincilSayi = len(self.e.disk.getPrimaryPartitions())
            uzatilmisSayi = ext_count = 1 if self.e.disk.getExtendedPartition() else 0
            parts_avail = self.e.disk.maxPrimaryPartitionCount - (birincilSayi + uzatilmisSayi)
            if not parts_avail and not ext_count:
                QMessageBox.warning(self, self.e.d[self.e.s_d]["Uyarı"],self.e.d[self.e.s_d]["Eğer dörtten fazla disk bölümü oluşturmak istiyorsanız birincil bölümlerden birini silip uzatılmış bölüm oluşturun.Bu durumda oluşturduğunuz uzatılmış bölümleri işletim sistemi kurmak için kullanamayacağınızı aklınızda bulundurun."])
            else:
                if parts_avail:
                    if not uzatilmisSayi and parts_avail > 1:
                        self.bolumOlustur(alan, parted.PARTITION_NORMAL)
                        self.bolumListeYenile()
                    elif parts_avail == 1:
                        self.bolumOlustur(alan, parted.PARTITION_EXTENDED)
                        self.bolumListeYenile()
                if uzatilmisSayi:
                    ext_part = self.e.disk.getExtendedPartition()
                    try:
                        alan = ext_part.geometry.intersect(alan)
                    except ArithmeticError:
                        QMessageBox.critical(self, self.e.d[self.e.s_d]["Hata"], self.e.d[self.e.s_d]["Yeni disk bölümü oluşturmak için yeterli alan yok ! Uzatılmış bölümün boyutunu arttırmayı deneyiniz."])
                    else:
                        self.bolumOlustur(alan, parted.PARTITION_LOGICAL)
                        self.bolumListeYenile()

    def bolumSilFonk(self):
        if self.bolumListeKutu.currentItem().data(0,Qt.UserRole) != "ayrilmamis":
            bolumNo = int(self.bolumListeKutu.currentItem().data(0,Qt.UserRole))
            for bolum in self.e.disk.partitions:
                if bolum.number == bolumNo:
                    try:
                        self.e.disk.deletePartition(bolum)
                        self.bolumListeYenile()
                    except parted.PartitionException:
                        QMessageBox.warning(self, self.e.d[self.e.s_d]["Uyarı"], self.e.d[self.e.s_d]["Lütfen uzatılmış bölümleri silmeden önce mantıksal bölümleri siliniz."])
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

        for _alan in self.e.disk.getFreeSpaceRegions():
            if _alan.length > maks_boyut and _alan.length > alignment.grainSize:
                alan = _alan
                maks_boyut = _alan.length
        return alan

    def bolumOlustur(self, alan, bolumTur):
        if bolumTur == parted.PARTITION_NORMAL or bolumTur == parted.PARTITION_EXTENDED:
            for bosBolum in self.e.disk.getFreeSpacePartitions():
                _bolum = self.bolumBilgi(bosBolum, "GB")
                if _bolum["tur"] == parted.PARTITION_FREESPACE:
                    maksBoyut = float(_bolum["boyut"])
        elif bolumTur == bolumTur == parted.PARTITION_LOGICAL:
            for bosBolum in self.e.disk.getFreeSpacePartitions():
                _bolum = self.bolumBilgi(bosBolum, "GB")
                if _bolum["tur"] == 5:
                    maksBoyut = float(_bolum["boyut"])

        alignment = self.aygit.optimalAlignedConstraint
        constraint = self.aygit.getConstraint()
        data = {
            'start': constraint.startAlign.alignUp(alan, alan.start),
            'end': constraint.endAlign.alignDown(alan, alan.end),
        }

        boyut, ok = QInputDialog().getDouble(self, self.e.d[self.e.s_d]['Bölüm oluştur'], self.e.d[self.e.s_d]['GB cinsinden boyut'], min=0.001,
                                             value=1, max=maksBoyut, decimals=3)

        if ok:
            data["end"] = int(data["start"]) + int(parted.sizeToSectors(float(boyut), "GiB", self.aygit.sectorSize))
            try:
                geometry = parted.Geometry(device=self.aygit, start=int(data["start"]), end=int(data["end"]))
                partition = parted.Partition(
                    disk=self.e.disk,
                    type=bolumTur,
                    geometry=geometry,
                )

                self.e.disk.addPartition(partition=partition, constraint=constraint)
            except (parted.PartitionException, parted.GeometryException, parted.CreateException) as e:
                raise RuntimeError(e.message)

    def showEvent(self, event):
        self.e.setWindowTitle(self.e.d[self.e.s_d]["Disk Yapılandırma"])
        self.yenileButon.setText(self.e.d[self.e.s_d]["  Yenile"])
        self.bolumListeKutu.headerItem().setText(0, self.e.d[self.e.s_d]["Bölüm"])
        self.bolumListeKutu.headerItem().setText(1, self.e.d[self.e.s_d]["Kullanım Şekli"])
        self.bolumListeKutu.headerItem().setText(2, self.e.d[self.e.s_d]["Boyut"])
        self.bolumListeKutu.headerItem().setText(3, self.e.d[self.e.s_d]["Dosya Sistemi"])
        self.yeniBolumBtn.setText(self.e.d[self.e.s_d]["  Yeni Bölüm Ekle"])
        self.bolumSilBtn.setText(self.e.d[self.e.s_d]["  Bölümü Sil"])
        self.blank_label.setText(self.e.d[self.e.s_d]["Birincil Bölüm"])
        self.extended_label.setText(self.e.d[self.e.s_d]["Uzatılmış Bölüm"])
        self.logical_label.setText(self.e.d[self.e.s_d]["Mantıksal Bölüm"])
        self.primary_label.setText(self.e.d[self.e.s_d]["Ayrılmamış Bölüm"])
        self.e.ileri_dugme.setDisabled(True)


class diskOzellikleriSinif(QDialog):
    def __init__(self, ebeveyn=None):
        super(diskOzellikleriSinif, self).__init__(ebeveyn)
        self.e = ebeveyn
        disk_ = self.e.seciliDisk
        self.baslik_ = disk_.text(0)
        self.boyut_ = float(disk_.text(2).replace(" GB",""))
        format_ = disk_.text(3)
        self.setWindowTitle(self.baslik_)
        diskOzellikKutu = QGridLayout()
        self.setLayout(diskOzellikKutu)
        self.secenekAcilirListe = QComboBox()
        self.secenekAcilirListe.addItem(self.e.e.d[self.e.e.s_d]["Sistem Diski"])
        self.secenekAcilirListe.addItem(self.e.e.d[self.e.e.s_d]["Takas Alanı"])
        diskOzellikKutu.addWidget(self.secenekAcilirListe, 0, 0, 1, 1)
        self.diskBicimlendirKutu = QCheckBox(self.e.e.d[self.e.e.s_d]["Diski Biçimlendir"])
        if format_ != "ext4":
            self.diskBicimlendirKutu.setChecked(True)
            self.diskBicimlendirKutu.setDisabled(True)
        diskOzellikKutu.addWidget(self.diskBicimlendirKutu, 1, 0, 1, 1)
        tamamDugme = QPushButton(self.e.e.d[self.e.e.s_d]["Tamam"])
        tamamDugme.pressed.connect(self.tamamBasildiFonk)
        diskOzellikKutu.addWidget(tamamDugme, 2, 0, 1, 1)

    def tamamBasildiFonk(self):
        if self.secenekAcilirListe.currentText() == self.e.e.d[self.e.e.s_d]["Sistem Diski"]:
            komut = "LC_ALL=C df -h / | awk '{ print $3 }' | tail -n 1 | sed 's/G//'g"
            boyut = self.e.e.komutCalistirFonksiyon(komut)
            if self.boyut_ >= round(float(boyut)):
                self.e.sistemDiski = [self.baslik_]
                if self.diskBicimlendirKutu.isChecked():
                    self.e.sistemDiski.append(True)
                else:
                    self.e.sistemDiski.append(False)
            else:
                    QMessageBox.critical(self, self.e.e.d[self.e.e.s_d]["Hata"], self.e.e.d[self.e.e.s_d]["Bu bölüm sistem diski oluşturmak için çok küçük ! Sistem diski seçilecek bölüm en azından {} GB boyutunda olmalıdır."].format(round(float(boyut))))
        elif self.secenekAcilirListe.currentText() == self.e.e.d[self.e.e.s_d]["Takas Alanı"]:
            self.e.takasDiski = [self.baslik_]
            if self.diskBicimlendirKutu.isChecked():
                self.e.takasDiski.append(True)
            else:
                self.e.takasDiski.append(False)
        QDialog.accept(self)