#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import subprocess
import re
import crypt
import os
import sys
import site
import json

class merkezSinif(QMainWindow):
    def __init__(self,ebeveyn=None):
        super(merkezSinif,self).__init__(ebeveyn)
        #Merkez pencereyi 2 parçaya böleceğiz üst ve alt parça olarak
        #Bu bölümü merkze widget olarak atıyoruz
        #Pencereyi 800px 500px e sabitledik
        anaAyirici = QSplitter(Qt.Vertical)
        self.setCentralWidget(anaAyirici)
        self.setFixedWidth(800)
        self.setFixedHeight(500)
        #Üst ve alt parçaya birer widget atatyacağız
        ustParca=QWidget()
        altAyirici=QSplitter(Qt.Vertical)
        anaAyirici.addWidget(ustParca)
        anaAyirici.addWidget(altAyirici)
        yiginParca=QWidget()
        dugmeParca=QWidget()
        altAyirici.addWidget(yiginParca)
        altAyirici.addWidget(dugmeParca)
        #Üst parçamıza resmimizi ekliyoruz ve boyutlarını ayarlıyoruz
        #yiginParca ve dugmeParca nn yüksekliğini ayarlıyoruz
        ustParca.setStyleSheet("background-image: url(merkezArkaplan.png);")
        ustParca.setFixedWidth(800)
        ustParca.setFixedHeight(125)
        yiginParca.setFixedHeight(300)
        dugmeParca.setFixedHeight(75)

        self.yiginNumarasi=0
        self.sonyigin=0
        yiginKutusu=QHBoxLayout()
        yiginParca.setLayout(yiginKutusu)
        self.yiginWidget=QStackedWidget()
        yiginKutusu.addWidget(self.yiginWidget)
        self.yiginWidget.addWidget(self.hosgeldinizDestesi())
        self.yiginWidget.addWidget(self.baslangicKotrolDestesi())
        self.yiginWidget.addWidget(self.kullaniciBilgileriDestesi())
        self.yiginWidget.addWidget(self.diskisleriDestesi())

        dugmeKutusu=QHBoxLayout()
        dugmeParca.setLayout(dugmeKutusu)
        self.geriDugme=QPushButton("geri")
        self.geriDugme.setDisabled(True)
        self.geriDugme.pressed.connect(self.geriDugmeFonksiyon)
        self.ileriDugme=QPushButton("ileri")
        self.ileriDugme.setDisabled(True)
        self.ileriDugme.pressed.connect(self.ileriDugmeFonksiyon)
        dugmeKutusu.addWidget(self.geriDugme)
        dugmeKutusu.addWidget(self.ileriDugme)

    def hosgeldinizDestesi(self):
        hosgeldinizWidget=QWidget()
        hosgedinizKutu=QVBoxLayout()
        hosgeldinizWidget.setLayout(hosgedinizKutu)

        hosgeldinizYazi=QLabel("Milis Linux Yükleyiciye Hoşgeldiniz")
        hosgedinizKutu.addWidget(hosgeldinizYazi)

        kullanimSartlari = QTextEdit()
        hosgedinizKutu.addWidget(kullanimSartlari)
        kullanimSartlari.setText("""Milis Linux (Milli İşletim Sistemi) sıfır kaynak koddan üretilen,\n
kendine has paket yöneticisine sahip,\n
bağımsız tabanlı yerli linux işletim sistemi projesidir.\n
Genel felsefe olarak ülkemizdeki bilgisayar kullanıcıları için linuxu kolaylaştırıp\n
Milis İşletim Sisteminin sorunsuz bir işletim sistemi olmasını sağlamayı ve yazılımsal\n
olarak dışa bağımlı olmaktan kurtarmayı esas alır. Ayrıca her türlü katkıda bulunmak\n
isteyenler için bulunmaz bir Türkçe açık kaynak projesidir.\n""")

        self.sartKabulKutusu=QCheckBox("Kullanım Şartlarını Kabul Ediyorum.")
        self.sartKabulKutusu.stateChanged.connect(self.sartKabulFonksiyon)
        hosgedinizKutu.addWidget(self.sartKabulKutusu)

        return hosgeldinizWidget

    def baslangicKotrolDestesi(self):
        baslangicWidget=QWidget()
        baslangicKutu=QGridLayout()
        baslangicWidget.setLayout(baslangicKutu)

        bilgiLabel=QLabel("Milis yükleyicinin kurulumdan önce bazı kontoller gerçekleştirmesi gerekiyor")
        baslangicKutu.addWidget(bilgiLabel,0,0,1,1)
        self.baslaDugme=QPushButton("Başlat")
        self.baslaDugme.pressed.connect(self.baslangicKotrolFonksiyon)
        baslangicKutu.addWidget(self.baslaDugme,0,1,1,1)
        self.ciktiYazilari=QTextEdit()
        baslangicKutu.addWidget(self.ciktiYazilari,1,0,1,2)
        return baslangicWidget

    def kullaniciBilgileriDestesi(self):
        kullaniciWidget=QWidget()
        kullaniciKutu=QGridLayout()
        kullaniciWidget.setLayout(kullaniciKutu)

        kullaniciKutu.addWidget(QLabel("Milis Linux Kullanabilmeniz İçin Bir Kullanıcı Oluşturmanız Gerekli"),0,0,1,2)
        self.kullaniciBilgiLabel=QLabel()
        kullaniciKutu.addWidget(self.kullaniciBilgiLabel,1,0,1,2)
        kullaniciKutu.addWidget(QLabel("Kullanıcı Adı"),2,0,1,1)
        self.kullaniciAdi=QLineEdit()
        self.kullaniciAdi.textChanged.connect(self.kullaniciBilgiYaziGirildi)
        kullaniciKutu.addWidget(self.kullaniciAdi,2,1,1,1)
        kullaniciKutu.addWidget(QLabel("Kullanıcı Şifresi"),3,0,1,1)
        self.kullaniciSifre=QLineEdit()
        self.kullaniciSifre.textChanged.connect(self.kullaniciBilgiYaziGirildi)
        self.kullaniciSifre.setEchoMode(QLineEdit.Password)
        kullaniciKutu.addWidget(self.kullaniciSifre,3,1,1,1)
        kullaniciKutu.addWidget(QLabel("Kullanıcı Şifresi Tekrar"),4,0,1,1)
        self.kullaniciSifreTekrar=QLineEdit()
        self.kullaniciSifreTekrar.textChanged.connect(self.kullaniciBilgiYaziGirildi)
        self.kullaniciSifreTekrar.setEchoMode(QLineEdit.Password)
        kullaniciKutu.addWidget(self.kullaniciSifreTekrar,4,1,1,1)
        return kullaniciWidget

    def diskisleriDestesi(self):
        self.sistemDiski=""
        self.takasDiski=""
        self.seciliDisk=None
        disklerWidget=QWidget()
        disklerKutu=QGridLayout()
        disklerWidget.setLayout(disklerKutu)
        disklerKutu.addWidget(QLabel("Diskler"),0,0,1,1)
        self.disklerAcilirKutu=QComboBox()
        disklerKutu.addWidget(self.disklerAcilirKutu,0,1,1,1)
        self.disklerListe=QListWidget()
        disklerKutu.addWidget(self.disklerListe,1,0,1,2)
        self.diskler = self.disklerListesiSonuc()
        self.disklerListe.itemClicked.connect(self.disklerListeDegistiFonksiyon)
        self.disklerAcilirKutu.currentIndexChanged.connect(self.disklerAcilirDegistiFonksiyon)
        self.disklerAcilirDegistiFonksiyon()
        return disklerWidget

    def disklerAcilirDegistiFonksiyon(self):
        self.disklerListe.clear()
        for i in self.diskler:
            if i[0] == self.disklerAcilirKutu.currentText():
                sayac=0
                for x in i:
                    if sayac!=0:
                        self.disklerListe.addItem(x)
                    sayac+=1

    def disklerListeDegistiFonksiyon(self,tiklanan):
        self.seciliDisk=tiklanan.text()
        diskOzellikPencere=diskOzellikleriSinif(self)
        diskOzellikPencere.exec_()
        if self.sistemDiski!="":
#            self.kurparam["disk"]["bolum"]="/dev/"+self.sistemDiski[0]
#            self.kurparam["disk"]["format"]=self.sistemDiski[1]
            pass
        elif self.takasDiski!="":
#            self.kurparam["disk"]["takasbolum"]="/dev/"+self.takasDiski[0]
            pass
        if self.sistemDiski=="":
            pass
        elif self.sistemDiski!="" and self.takasDiski=="":
            QMessageBox.information(self,"Bilgi","Takas Alanı Belirtmediniz\nTakas alanı ram miktarınızın düşük olduğu durumlarda\nram yerine disk kullanarak işlemlerin devam etmesini sağlar.")
            self.ileriDugme.setDisabled(False)
        elif self.sistemDiski!="" and self.takasDiski!="":
            if self.sistemDiski[0]==self.takasDiski[0]:
                QMessageBox.warning(self,"Hata",self.takasDiski[0]+" diskini hem sistem hem takas için seçtiniz\nAynı diski hem sistem hem takas olarak kullanmazsınız")
                self.ileriDugme.setDisabled(True)
            else:
                self.ileriDugme.setDisabled(False)

    def disklerListesiSonuc(self):
        sonuc = []
        diskler = self.bagliDisklerFonksiyon()
        bolumler = self.bagliDiskBolumleriFonksiyon()
        for i in diskler:
            if i[0]!="" or i[1]!="":
                liste = [i[1]]
                for x in bolumler:
                    if i[0] == x[0][:3] and len(x[0])>3:
                        liste.append(x[0]+x[1])
                sonuc.append(liste)
        for i in sonuc:
            self.disklerAcilirKutu.addItem(i[0])
        return sonuc

    def bagliDisklerFonksiyon(self):
        diskSecimler = []
        diskIsımler  = self.komutCalistirFonksiyon("lsblk -nS -o NAME").split('\n')
        diskModeller = self.komutCalistirFonksiyon("lsblk -nS -o MODEL").split('\n')
        for i in range(len(diskIsımler)):
            diskSecimler.append((diskIsımler[i],diskModeller[i]))
        return diskSecimler

    def bagliDiskBolumleriFonksiyon(self):
        bolumSecimler=[]
        uygunBolumler=['sd','hd','mmcblk0p']
        diskBolumler =self.komutCalistirFonksiyon("lsblk -ln -o  NAME    | awk '{print $1}'").split('\n')
        bolumBoyutlar=self.komutCalistirFonksiyon("lsblk -ln -o  SIZE    | awk '{print $1}'").split('\n')
        bolumDs=self.komutCalistirFonksiyon("lsblk -ln -o  FSTYPE  | awk '{print $1}'").split('\n')
        bolumMajmin=self.komutCalistirFonksiyon("lsblk -ln -o  MAJ:MIN | awk '{print $1}'").split('\n')
        bolumEtiket=self.komutCalistirFonksiyon("lsblk -ln -o  LABEL").split('\n') #Bunda awk yok çünkü arada boşluk olabilir.
        for i in range(len(diskBolumler)-1):
            if bolumMajmin[i].split(":")[1] != "0": # partition olmayanları ele (sda/sdb seçince grub bozuluyor.)
                for uygunBolum in uygunBolumler:
                    if uygunBolum in diskBolumler[i]:
                        bolumSecimler.append((diskBolumler[i],bolumEtiket[i]+ "\t" +bolumBoyutlar[i]+"\t"+bolumDs[i]))
        return bolumSecimler

    def kullaniciBilgiYaziGirildi(self):
        donut=""
        ad = self.kullaniciAdi.text()
        sifre_1 = self.kullaniciSifre.text()
        sifre_2 = self.kullaniciSifreTekrar.text()
        if len(ad)>0 and not ad[0].isalpha():
            donut += "Lütfen Karakter Adında Harf İle Başlanyın\n"
        if not ad.isalnum():
            donut += "Lütfen Karakter Adında Sadece Harf Ve Rakam Kullanın\n"
        if len(sifre_1) == 0 or len(sifre_2)==0:
            donut += "Lütfen Bir Şifre Girin"
        if sifre_1 != sifre_2:
            donut += "Yazdığınız Şifreler Birbirinden Farklı\n"
        if donut == "":
            self.kullaniciBilgiLabel.setText("Teşekkürler Lütfen Adınızı Ve Şifrenizi Unutmayınız")
#            self.kurparam["kullanici"]["isim"]=ad
#            self.kurparam["kullanici"]["sifre"]=sifre_1
            self.ileriDugme.setDisabled(False)
        else:
            self.kullaniciBilgiLabel.setText(donut)

    def sartKabulFonksiyon(self):
        if self.sartKabulKutusu.isChecked():
            self.ileriDugme.setDisabled(False)
        else:
            self.ileriDugme.setDisabled(True)

    def baslangicKotrolFonksiyon(self):
        self.baslaDugme.setDisabled(True)
        cikti=""
        cikti+="Paket Güncellemeleri Kontrol Ediliyor\n=================================\n"
        self.ciktiYazilari.setText(cikti)
#        cikti+=self.komutCalistirFonksiyon("mps -GG")+"\n"
#        self.ciktiYazilari.setText(cikti)
#        cikti+=self.komutCalistirFonksiyon("mps -G")+"\n"
#        self.ciktiYazilari.setText(cikti)
        cikti+="LSB Relase Tamiri Yapılıyor\n=================================\n"
        self.ciktiYazilari.setText(cikti)
#        cikti+=self.komutCalistirFonksiyon("mps -g lsb-release")+"\n"
#        self.ciktiYazilari.setText(cikti)
        cikti+="Gereçlerin Kontrolü Yapılıyor\n=================================\n"
        self.ciktiYazilari.setText(cikti)
#        paketd=site.getsitepackages()
#        yukluler=os.listdir(paketd[0])
#        kur="pip3 install "
#        mpskur="mps kur "
#        kontrol=[""]
#        mpskontrol=["python3-pip","python-yaml","python3-yaml","python3-pythondialog"]
#
#        for mpsk in mpskontrol:
#            if os.path.exists("/var/lib/pkg/DB/"+mpsk) is False:
#                cikti+=self.komutCalistirFonksiyon("mps kur "+mpsk)+"\n"
#                self.ciktiYazilari.setText(cikti)
#            else:
#                cikti+="mpsk,zaten kurulu\n"
#                self.ciktiYazilari.setText(cikti)
#
#            for yuklu in yukluler:
#                for kont in kontrol:
#                    if kont in yuklu:
#                        cikti+=kont+"kurulu\n"
#                        self.ciktiYazilari.setText(cikti)
#                        kontrol.remove(kont)
#            for kont in kontrol:
#                cikti+=self.komutCalistirFonksiyon(kur+kont)+"\n"
#                self.ciktiYazilari.setText(cikti)
#
#        f = open("/tmp/kurulum.log","w")
#        _kurulum_dosya="/root/ayarlar/kurulum.yml"
#        kurulum_dosya=""
#        if not os.path.exists(_kurulum_dosya):
#            QMessageBox.warning(self,"Hata","Milis kurulumu için gerekli olan /root/ayarlar/kurulum.yml\n dosyası bulunamadı. Milis yükleyici sonladırılacak!")
#            sys.exit()
#        else:
#            self.ciktiYazilari.setText(self.komutCalistirFonksiyon("cp "+_kurulum_dosya+" /opt/kurulum.yml"))
#            self.kurulum_dosya="/opt/kurulum.yml"
#            self.kurparam=self.kurulum_oku(kurulum_dosya)
        self.ileriDugme.setDisabled(False)

    def ileriDugmeFonksiyon(self):
        self.yiginNumarasi+=1
        if self.yiginNumarasi !=0:
            self.geriDugme.setDisabled(False)
        if self.sonyigin<self.yiginNumarasi:
            self.sonyigin+=1
            self.ileriDugme.setDisabled(True)
        elif self.sonyigin==self.yiginNumarasi:
            self.ileriDugme.setDisabled(True)
        self.yiginWidget.setCurrentIndex(self.yiginNumarasi)

    def geriDugmeFonksiyon(self):
        self.yiginNumarasi-=1
        if self.yiginNumarasi ==0:
            self.geriDugme.setDisabled(True)
        if self.sonyigin>self.yiginNumarasi:
            self.ileriDugme.setDisabled(False)
        self.yiginWidget.setCurrentIndex(self.yiginNumarasi)

    def komutCalistirFonksiyon(self,komut):
        out = subprocess.check_output(komut,stderr=subprocess.STDOUT,shell=True,universal_newlines=True)
        return out.replace("\b","")

    def kurulum_oku(self,kurulumdos):
        with open(kurulumdos, 'r') as f:
            param = yaml.load(f)
        return param

class diskOzellikleriSinif(QDialog):
    def __init__(self,ebeveyn=None):
        super(diskOzellikleriSinif,self).__init__(ebeveyn)
        self.ebeveyn = ebeveyn
        disk_=self.ebeveyn.seciliDisk.split("\t")
        self.baslik_=disk_[0]
        format_=disk_[2]

        self.setWindowTitle(self.baslik_)
        diskOzellikKutu=QGridLayout()
        self.setLayout(diskOzellikKutu)
        self.secenekAcilirListe=QComboBox()
        self.secenekAcilirListe.addItem("Sistem Diski")
        self.secenekAcilirListe.addItem("Takas Alanı")
        diskOzellikKutu.addWidget(self.secenekAcilirListe,0,0,1,1)
        self.diskBicimlendirKutu = QCheckBox("Diski Biçimlendir")
        if format_ != "ext4":
            self.diskBicimlendirKutu.setChecked(True)
            self.diskBicimlendirKutu.setDisabled(True)
        diskOzellikKutu.addWidget(self.diskBicimlendirKutu,1,0,1,1)
        tamamDugme=QPushButton("Tamam")
        tamamDugme.pressed.connect(self.tamamBasildiFonk)
        diskOzellikKutu.addWidget(tamamDugme,2,0,1,1)

    def tamamBasildiFonk(self):
        if self.secenekAcilirListe.currentText() == "Sistem Diski":
            self.ebeveyn.sistemDiski=[self.baslik_]
            if self.diskBicimlendirKutu.isChecked():
                self.ebeveyn.sistemDiski.append("evet")
            else:
                self.ebeveyn.sistemDiski.append("hayır")
        elif self.secenekAcilirListe.currentText() == "Takas Alanı":
            self.ebeveyn.takasDiski=[self.baslik_]
            if self.diskBicimlendirKutu.isChecked():
                self.ebeveyn.takasDiski.append("evet")
            else:
                self.ebeveyn.takasDiski.append("hayır")
        QDialog.accept(self)

def baslatFonk():
    uygulama_ = QApplication(sys.argv)
    uygulama_.setOrganizationName('Milis Linux')
    uygulama_.setApplicationName('Milis Yukleyici')
    merkezPencere_ = merkezSinif()
    merkezPencere_.show()
    sys.exit(uygulama_.exec_())

if __name__ == "__main__":
    baslatFonk()
