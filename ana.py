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
import yaml

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
        ustParca.setStyleSheet("background-image: url("+yol+"/slaytlar/merkezArkaplan.png);")
        ustParca.setFixedWidth(800)
        ustParca.setFixedHeight(125)
        yiginParca.setFixedHeight(325)
        dugmeParca.setFixedHeight(50)

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
        self.yiginWidget.addWidget(self.grubKurulacakmiDestesi())
        self.yiginWidget.addWidget(self.kurulumEkraniDestesi())
        self.yiginWidget.addWidget(self.kurulumSonuclandiDestesi())

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

    def grubKurulacakmiDestesi(self):
        grubWidget=QWidget()
        grubKutu=QGridLayout()
        grubWidget.setLayout(grubKutu)

        grubKutu.addWidget(QLabel("""Sisteme Grub kurmak istiyormusunuz?\n Grub bir linux önyükleyicisidir\n
Eğer sisteminizde kurulu bir linux dağıtımı var ise ve disk biçimlendirilmemişse grub kurmayabilirsiniz.\n
Eğer sisteminizde kurulu bir linux dağıtımı yok veya disk biçimlendirilmişse grub kurmadığınız takdirde\n
sistem başlamayacaktır."""),0,0,1,2)
        self.grubKurDugme=QPushButton("Grub Kur")
        self.grubKurDugme.pressed.connect(self.grubKurFonksiyon)
        grubKutu.addWidget(self.grubKurDugme,1,0,1,1)
        self.grubKurmaDugme=QPushButton("Grub Kurma")
        self.grubKurmaDugme.pressed.connect(self.grubKurmaFonksiyon)
        grubKutu.addWidget(self.grubKurmaDugme,1,1,1,1)
        return grubWidget

    def kurulumEkraniDestesi(self):
        self.slaytnumarasi=1
        kurulumWidget=QWidget()
        kurulumKutu=QGridLayout()
        kurulumWidget.setLayout(kurulumKutu)
        inceleDugme=QPushButton("İncele")
        inceleDugme.setFixedHeight(25)
        inceleDugme.pressed.connect(self.kurulumBilgiFonksiyon)
        kurulumKutu.addWidget(inceleDugme,0,0,1,1)
        self.kurulumBaslatDugme=QPushButton("Kurulumu Başlat")
        self.kurulumBaslatDugme.setFixedHeight(25)
        self.kurulumBaslatDugme.pressed.connect(self.kurulumFonksiyon)
        kurulumKutu.addWidget(self.kurulumBaslatDugme,0,1,1,1)
        self.slaytci=QLabel("Milis yükleyici kurulum için gerekli bilgileri topladı\nBaşlata tıklamanız halinde kurulum başlayacak\nve değişiklikler disklere uygulanacaktur.")
        self.slaytci.setAlignment(Qt.AlignCenter)
        self.slaytci.setFixedWidth(800)
        self.slaytci.setFixedHeight(250)
        kurulumKutu.addWidget(self.slaytci,1,0,1,2)
        self.kurulumBilgisiLabel=QLabel()
        self.kurulumBilgisiLabel.setFixedHeight(25)
        kurulumKutu.addWidget(self.kurulumBilgisiLabel,2,0,1,2)
        self.surecCubugu = QProgressBar()
        self.surecCubugu.setFixedHeight(25)
        kurulumKutu.addWidget(self.surecCubugu,3,0,1,2)

        self.zaman = QTimer(self)
        self.zaman.setInterval(30000)
        self.zaman.timeout.connect(self.slaytDegistir)

        return kurulumWidget

    def kurulumSonuclandiDestesi(self):
        kurulumSonucWidget=QWidget()
        kurulumSonucKutu=QGridLayout()
        kurulumSonucWidget.setLayout(kurulumSonucKutu)
        milisLogo=QLabel()
        milisLogo.setPixmap(QPixmap(yol+"/slaytlar/Milis-logo.svg").scaled(230,168))
        milisLogo.setAlignment(Qt.AlignCenter)
        kurulumSonucKutu.addWidget(milisLogo,0,0,1,1)
        milisTesekkurYazi=QLabel("Milis Linux Başarıyla Kurulmuştur.\nMilis Linux Kurduğunuz İçin Teşekkür Ederiz.\nİsterseniz sistemi denemeye devam edebilirsiniz\nYada tekrar başlatıp sisteminizi kullanbilirsiniz.")
        kurulumSonucKutu.addWidget(milisTesekkurYazi,1,0,1,1)
        milisTesekkurYazi.setAlignment(Qt.AlignCenter)
        deneDugme=QPushButton("Milis Linux'u denemeye devam et")
        deneDugme.pressed.connect(self.deneDugmeFonksiyon)
        kurulumSonucKutu.addWidget(deneDugme,2,0,1,1)
        tekrarBaslatDugme=QPushButton("Tekrar Başlat")
        tekrarBaslatDugme.pressed.connect(self.tekrarBaslatDugmeFonksiyon)
        kurulumSonucKutu.addWidget(tekrarBaslatDugme,3,0,1,1)

        return kurulumSonucWidget

    def deneDugmeFonksiyon(self):
        sys.exit()

    def tekrarBaslatDugmeFonksiyon(self):
        os.system("shutdown -r now")

    def slaytDegistir(self):
        self.slaytci.setPixmap(QPixmap(yol+"/slaytlar/slayt_"+str(self.slaytnumarasi)+".png").scaled(700,219))
        if self.slaytnumarasi==6:
            self.slaytnumarasi=1
        else:
            self.slaytnumarasi+=1
        self.zaman.start()

    def kurulumFonksiyon(self):
        self.kurulumBaslatDugme.setDisabled(True)
        self.geriDugme.setDisabled(True)
        self.ileriDugme.setDisabled(True)
        self.slaytDegistir()
        self.kurulum_yaz(self.kurparam,self.kurulum_dosya)
        kurulum=self.kurulum_oku(self.kurulum_dosya)
        kbolum=kurulum["disk"]["bolum"]
        kformat=kurulum["disk"]["format"]
        kbaglam=kurulum["disk"]["baglam"]
        ktakas=kurulum["disk"]["takasbolum"]
        kisim=kurulum["kullanici"]["isim"]
        ksifre=kurulum["kullanici"]["sifre"]
        kgrubkur=kurulum["grub"]["kur"]

        if kformat == "evet":
            self.surecCubugu.setValue(0)
            self.kurulumBilgisiLabel.setText("Diskler Formatlanıyor...")
            self.bolumFormatla(kbolum)
        if ktakas !="":
            self.surecCubugu.setValue(0)
            self.kurulumBilgisiLabel.setText("Takas Alanı Ayarlanıyor...")
            self.takasAyarla(ktakas)

        self.surecCubugu.setValue(0)
        self.kurulumBilgisiLabel.setText(kbolum+" bölümü "+kbaglam+" bağlamına bağlanıyor...")
        self.bolumBagla(kbolum,kbaglam)

        self.surecCubugu.setValue(0)
        self.kurulumBilgisiLabel.setText("Kullanıcı Oluşturuluyor...")
        self.kullaniciOlustur(kisim,kisim,ksifre)

        self.surecCubugu.setValue(0)
        self.kurulumBilgisiLabel.setText("Sistem Kopyalanıyor...")
        self.sistemKopyala(kbaglam)

        self.surecCubugu.setValue(0)
        self.kurulumBilgisiLabel.setText("initrd Oluşturuluyor...")
        self.initrdOlustur(kbaglam)

        if kgrubkur == "evet":
            self.surecCubugu.setValue(0)
            self.kurulumBilgisiLabel.setText("Grub Kuruluyor...")
            self.grubKur(kbolum,kbaglam)
        self.surecCubugu.setValue(0)
        self.bolumCoz(kbolum)
        self.ileriDugmeFonksiyon()


    def bolumCoz(self,hedef):
        komut="umount -l "+hedef
        try:
            os.system(komut)
        except OSError as e:
            QMessageBox.warning(self,"Hata",str(e))
            sys.exit()
        self.surecCubugu.setValue(100)
        self.kurulumBilgisiLabel.setText(hedef+" çözüldü.")

    def grubKur(self,hedef,baglam):
        hedef = hedef[:-1]
        if hedef == "/dev/mmcblk0": #SD kart'a kurulum fix
            os.system("grub-install --boot-directory="+baglam+"/boot /dev/mmcblk0")
            self.surecCubugu.setValue(100)
        else:
            os.system("grub-install --boot-directory="+baglam+"/boot " + hedef)
            self.surecCubugu.setValue(50)
            os.system("chroot "+baglam+" grub-mkconfig -o /boot/grub/grub.cfg")
            self.surecCubugu.setValue(100)
        self.kurulumBilgisiLabel.setText("Grub Kuruldu.")

    def initrdOlustur(self,hedef):
        os.system("mount --bind /dev "+hedef+"/dev")
        self.surecCubugu.setValue(25)
        os.system("mount --bind /sys "+hedef+"/sys")
        self.surecCubugu.setValue(50)
        os.system("mount --bind /proc "+hedef+"/proc")
        self.surecCubugu.setValue(75)
        os.system('chroot '+hedef+' dracut --no-hostonly --add-drivers "ahci" -f /boot/initramfs')
        self.surecCubugu.setValue(100)
        self.kurulumBilgisiLabel.setText("initrd Oluşturuldu")

    def sistemKopyala(self,baglam):
        os.system("clear")
        komut=""
        self.kurulumBilgisiLabel.setText("Kurulum .desktop siliniyor...")
        komut1="rm /root/Masaüstü/kurulum.desktop"
        komut2="rm /root/Desktop/kurulum.desktop"
        os.system(komut1)
        os.system(komut2)
        self.kurulumBilgisiLabel.setText("Dizinler kopyalanmaya başlanyor...")
        dizinler=["bin","boot","home","lib","sources","usr","depo","etc","include","lib64","opt","root","sbin","var"]
        yenidizinler=["srv","proc","tmp","mnt","sys","run","dev","media"]
        i=0
        mikdiz=len(dizinler)
        for dizin in dizinler:
            i+=1
            self.kurulumBilgisiLabel.setText(str(i)+"/"+str(mikdiz)+dizin+" kopyalanıyor...")
            komut="rsync --delete -a --info=progress2 /"+dizin+" "+baglam+" --exclude /proc"
            os.system(komut)
            yuzde = str(round(i/mikdiz,2))[2:]
            if len(yuzde) == 1:
                yuzde = yuzde + "0"
            self.surecCubugu.setValue(int(yuzde))
            self.kurulumBilgisiLabel.setText(dizin+" kopyalandı.")
            qApp.processEvents()
        self.surecCubugu.setValue(0)
        self.kurulumBilgisiLabel.setText("Yeni Dizinler Oluşturuluyor...")
        i=0
        mikdiz=len(yenidizinler)
        for ydizin in yenidizinler:
            i+=1
            self.kurulumBilgisiLabel.setText(ydizin+" oluşturuluyor...")
            komut="mkdir -p "+baglam+"/"+ydizin
            os.system(komut)
            yuzde = str(round(i/mikdiz,2))[2:]
            if len(yuzde) == 1:
                yuzde = yuzde + "0"
            self.surecCubugu.setValue(int(yuzde))
            self.kurulumBilgisiLabel.setText(ydizin+" oluşturuldu.")
            qApp.processEvents()

    def kullaniciOlustur(self,isim,kullisim,kullsifre):
        os.system("kopar milislinux-"+isim+" "+kullisim)
        self.surecCubugu.setValue(20)
        os.system('echo -e "'+kullsifre+'\n'+kullsifre+'" | passwd '+kullisim)
        self.surecCubugu.setValue(40)
        ayar_komut="cp -r /root/.config /home/"+kullisim+"/"
        os.system(ayar_komut)
        self.surecCubugu.setValue(60)
        ayar_komut2="cp -r /root/.xinitrc /home/"+kullisim+"/"
        os.system(ayar_komut2)
        self.surecCubugu.setValue(80)
        saat_komut="saat_ayarla_tr"
        os.system(saat_komut)
        self.surecCubugu.setValue(100)
        self.kurulumBilgisiLabel.setText(kullisim+" kullanıcısı başarıyla oluşturuldu.")

    def bolumBagla(self,hedef,baglam):
        komut="mount "+hedef+" "+baglam
        try:
            os.system(komut)
            self.surecCubugu.setValue(100)
        except OSError as e:
            QMessageBox.warning(self,"Hata",str(e))
            sys.exit()
        self.kurulumBilgisiLabel.setText(hedef+" "+baglam+" altına bağlandı.")

    def takasAyarla(self,bolum):
        self.kurulumBilgisiLabel.setText("mkswap "+"/dev/"+bolum)
        os.system("mkswap "+"/dev/"+bolum)
        self.kurulumBilgisiLabel.setText('echo "`lsblk -ln -o UUID /dev/' + bolum + '` none swap sw 0 0" | tee -a /etc/fstab')
        os.system('echo "`lsblk -ln -o UUID /dev/' + bolum + '` none swap sw 0 0" | tee -a /etc/fstab')

    def bolumFormatla(self,hedef):
        komut="umount -l "+hedef
        self.kurulumBilgisiLabel.setText(komut)
        if os.path.exists(hedef):
            os.system(komut)
            self.surecCubugu.setValue(50)
            komut2="mkfs.ext4 -F " + hedef
            try:
                os.system(komut2)
                self.surecCubugu.setValue(100)
            except OSError as e:
                QMessageBox.warning(self,"Hata",str(e))
                sys.exit()
            self.kurulumBilgisiLabel.setText(hedef+" disk bölümü formatlandı.")
        else:
            QMessageBox.warning(self,"Hata","Disk bulunamadı. Program kapatılacak.")
            sys.exit()

    def kurulumBilgiFonksiyon(self):
        QMessageBox.information(self,"Kurulum Bilgisi",yaml.dump(self.kurparam, default_flow_style=False, explicit_start=True))

    def grubKurFonksiyon(self):
        self.kurparam["grub"]["kur"]="evet"
        self.grubKurDugme.setDisabled(True)
        self.grubKurmaDugme.setDisabled(False)
        self.ileriDugme.setDisabled(False)

    def grubKurmaFonksiyon(self):
        self.kurparam["grub"]["kur"]="hayir"
        self.grubKurDugme.setDisabled(False)
        self.grubKurmaDugme.setDisabled(True)
        self.ileriDugme.setDisabled(False)

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
            self.kurparam["disk"]["bolum"]="/dev/"+self.sistemDiski[0]
            self.kurparam["disk"]["format"]=self.sistemDiski[1]
        if self.takasDiski!="":
            self.kurparam["disk"]["takasbolum"]="/dev/"+self.takasDiski[0]
        else:
            self.kurparam["disk"]["takasbolum"]=""

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
            self.kurparam["kullanici"]["isim"]=ad
            self.kurparam["kullanici"]["sifre"]=sifre_1
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
        cikti+="#Log dosyası oluşturuluyor...\n"
        f = open("/tmp/kurulum.log","w")
        _kurulum_dosya="/root/ayarlar/kurulum.yml"
        self.kurulum_dosya=""
        if not os.path.exists(_kurulum_dosya):
            QMessageBox.warning(self,"Hata","Milis kurulumu için gerekli olan /root/ayarlar/kurulum.yml\n dosyası bulunamadı. Milis yükleyici sonladırılacak!")
            sys.exit()
        else:
            cikti+="#Yml dosyası kopyalanıyor...\n"
            cikti+= self.komutCalistirFonksiyon("cp "+_kurulum_dosya+" /opt/kurulum.yml")
            self.ciktiYazilari.setText(cikti)
            self.kurulum_dosya="/opt/kurulum.yml"
            self.kurparam=self.kurulum_oku(self.kurulum_dosya)
            cikti+="============================\nİşlem tamamlandı devam edebilirsiniz"
            self.ciktiYazilari.setText(cikti)
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

    def kurulum_yaz(self,param,kurulumdos):
        with open(kurulumdos, 'w') as outfile:
            yaml.dump(param, outfile, default_flow_style=False,allow_unicode=True)







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
    yol=os.getcwd()
    baslatFonk()
