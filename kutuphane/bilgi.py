from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QCheckBox
from PyQt5.QtGui import QPixmap


class Bilgi(QWidget):
    def __init__(self, ebeveyn=None):
        super(Bilgi, self).__init__(ebeveyn)
        self.e = ebeveyn

        kutu = QGridLayout()
        self.setLayout(kutu)
        self.dil_resim = QLabel()
        self.dil_resim.setPixmap(QPixmap("./resimler/diller_32_32.svg"))
        self.dil_resim.setFixedSize(32,32)
        kutu.addWidget(self.dil_resim,0,0,1,1)
        self.dil_label = QLabel()
        kutu.addWidget(self.dil_label,0,1,1,1)
        self.dil_info = QLabel()
        kutu.addWidget(self.dil_info,1,0,1,2)

        self.klavye_resim = QLabel()
        self.klavye_resim.setPixmap(QPixmap("./resimler/klavye_.svg"))
        self.klavye_resim.setFixedSize(32,32)
        kutu.addWidget(self.klavye_resim,2,0,1,1)
        self.klavye_label = QLabel()
        kutu.addWidget(self.klavye_label,2,1,1,1)
        self.klavye_info = QLabel()
        kutu.addWidget(self.klavye_info,3,0,1,2)

        self.konum_resim = QLabel()
        self.konum_resim.setPixmap(QPixmap("./resimler/konum.svg"))
        self.konum_resim.setFixedSize(32,32)
        kutu.addWidget(self.konum_resim,4,0,1,1)
        self.konum_label = QLabel()
        kutu.addWidget(self.konum_label,4,1,1,1)
        self.konum_info = QLabel()
        kutu.addWidget(self.konum_info,5,0,1,2)

        self.kullanici_resim = QLabel()
        self.kullanici_resim.setPixmap(QPixmap("./resimler/kullanici.svg"))
        self.kullanici_resim.setFixedSize(32,32)
        kutu.addWidget(self.kullanici_resim,6,0,1,1)
        self.kullanici_label = QLabel()
        kutu.addWidget(self.kullanici_label,6,1,1,1)
        self.kullanici_info = QLabel()
        kutu.addWidget(self.kullanici_info,7,0,1,2)

        self.disk_resim = QLabel()
        self.disk_resim.setPixmap(QPixmap("./resimler/disk.svg"))
        self.disk_resim.setFixedSize(32,32)
        kutu.addWidget(self.disk_resim,8,0,1,1)
        self.disk_label = QLabel()
        kutu.addWidget(self.disk_label,8,1,1,1)
        self.disk_info = QLabel()
        kutu.addWidget(self.disk_info,9,0,1,2)

        self.grub_resim = QLabel()
        self.grub_resim.setPixmap(QPixmap("./resimler/grub.svg"))
        self.grub_resim.setFixedSize(32,32)
        kutu.addWidget(self.grub_resim,10,0,1,1)
        self.grub_label = QLabel()
        kutu.addWidget(self.grub_label,10,1,1,1)
        self.grub_cb = QCheckBox()
        self.grub_cb.stateChanged.connect(self.grub_kur)
        self.grub_cb.setChecked(True)
        kutu.addWidget(self.grub_cb,11,0,1,2)

    def grub_kur(self):
        if self.grub_cb.isChecked():
            self.e.milis_ayarlar["grub-kur"] = True
        else:
            self.e.milis_ayarlar["grub-kur"] = False

    def showEvent(self, event):
        self.e.setWindowTitle(self.e.d[self.e.s_d]["Kurulum Bilgileri"])
        self.dil_label.setText(self.e.d[self.e.s_d]["Sistem Dili"])
        self.dil_info.setText(self.e.milis_ayarlar["dil"])
        self.klavye_label.setText(self.e.d[self.e.s_d]["Klavye Bilgileri"])
        self.klavye_info.setText(self.e.d[self.e.s_d]["Klavye Modeli"]+":"+" ".join(self.e.milis_ayarlar["klavye_model"])+"\n"+self.e.d[self.e.s_d]["Klavye Düzeni"]+":"+" ".join(self.e.milis_ayarlar["klavye_duzeni"])+"\n"+self.e.d[self.e.s_d]["Klavye Varyantı"]+":"+str(self.e.milis_ayarlar["klavye_varyantı"]))
        self.konum_label.setText(self.e.d[self.e.s_d]["Konum"])
        self.konum_info.setText(self.e.milis_ayarlar["konum"])
        self.kullanici_label.setText(self.e.d[self.e.s_d]["Kullanıcı Bilgileri"])
        self.kullanici_info.setText(self.e.d[self.e.s_d]["Ad"]+":"+self.e.milis_ayarlar["gercek_ad"]+"\n"+self.e.d[self.e.s_d]["Kullanıcı Adı"]+":"+self.e.milis_ayarlar["kullanici_adi"]+"\n"+self.e.d[self.e.s_d]["Bilgisayar Adı"]+":"+self.e.milis_ayarlar["bilgisayar_adi"]+"\n"+self.e.d[self.e.s_d]["Şifre istemeden otomatik giriş yapın"]+":"+str(self.e.milis_ayarlar["otomatik_giris"]))
        self.disk_label.setText(self.e.d[self.e.s_d]["Disk Bilgileri"])
        self.disk_info.setText(self.e.d[self.e.s_d]["Sistem Diski"]+":"+self.e.milis_ayarlar["disk_bolum"]+"\n"+self.e.d[self.e.s_d]["Disk Biçimlenecekmi"]+":"+str(self.e.milis_ayarlar["disk_format"])+"\n"+self.e.d[self.e.s_d]["Takas Alanı"]+":"+str(self.e.milis_ayarlar["disk_takasbolum"]))
        self.grub_label.setText(self.e.d[self.e.s_d]["Grub Kurmak İstiyormusunuz?"])
        self.grub_cb.setText(self.e.d[self.e.s_d]["Grub bilgisayarınızın açılmasını sağlayan bir önyükleyicidir. Kurmak istermisiniz?"])