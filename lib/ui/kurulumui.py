#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml, os, time
from PyQt5.QtCore import Qt, QTimer, QThread
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QProgressBar, QMessageBox, qApp
from PyQt5.QtGui import QPixmap

class KurulumPencere(QWidget):
    def __init__(self, ebeveyn=None):
        super(KurulumPencere, self).__init__(ebeveyn)
        self.ebeveyn = ebeveyn

        self.slaytnumarasi = 1
        kurulumKutu = QVBoxLayout()
        self.setLayout(kurulumKutu)
        inceleKutu = QHBoxLayout()
        kurulumKutu.addLayout(inceleKutu)
        inceleDugme = QPushButton("İncele")
        inceleDugme.setFixedHeight(25)
        inceleDugme.pressed.connect(self.kurulumBilgiFonksiyon)
        inceleKutu.addWidget(inceleDugme)
        self.kurulumBaslatDugme = QPushButton("Kurulumu Başlat")
        self.kurulumBaslatDugme.setFixedHeight(25)
        self.kurulumBaslatDugme.pressed.connect(self.kurulumFonksiyon)
        inceleKutu.addWidget(self.kurulumBaslatDugme)
        self.slaytci = QLabel(self.tr("Milis yükleyici kurulum için gerekli bilgileri topladı\nBaşlata tıklamanız halinde kurulum başlayacak\nve değişiklikler disklere uygulanacaktur."))
        self.slaytci.setAlignment(Qt.AlignCenter)
        self.slaytci.setFixedWidth(800)
        self.slaytci.setFixedHeight(190)
        kurulumKutu.addWidget(self.slaytci)
        self.kurulumBilgisiLabel = QLabel()
        self.kurulumBilgisiLabel.setFixedHeight(25)
        kurulumKutu.addWidget(self.kurulumBilgisiLabel)
        self.surecCubugu = QProgressBar()
        self.surecCubugu.setFixedHeight(25)
        kurulumKutu.addWidget(self.surecCubugu)

        self.zaman = QTimer(self)
        self.zaman.setInterval(30000)
        self.zaman.timeout.connect(self.slaytDegistir)


    def kurulumBilgiFonksiyon(self):
        QMessageBox.information(self, "Kurulum Bilgisi",yaml.dump(self.ebeveyn.kurparam, default_flow_style=False, explicit_start=True))


    def kurulumFonksiyon(self):
        self.kurulumBaslatDugme.setDisabled(True)
        self.ebeveyn.geriDugme.setDisabled(True)
        self.ebeveyn.ileriDugme.setDisabled(True)
        self.slaytDegistir()
        self.ebeveyn.kurulum_yaz(self.ebeveyn.kurparam, self.ebeveyn.kurulum_dosya)
        kurulum = self.ebeveyn.kurulum_oku(self.ebeveyn.kurulum_dosya)
        kbolum = kurulum["disk"]["bolum"]
        kformat = kurulum["disk"]["format"]
        kbaglam = kurulum["disk"]["baglam"]
        ktakas = kurulum["disk"]["takasbolum"]
        kisim = kurulum["kullanici"]["isim"]
        ksifre = kurulum["kullanici"]["sifre"]
        kgrubkur = kurulum["grub"]["kur"]
        kdil = kurulum["bolgesel"]["dil"]
        kzaman = kurulum["bolgesel"]["zaman"]

        self.kurulumBilgisiLabel.setText(self.tr("Değişiklikler Diske Uygulanıyor..."))
        if self.ebeveyn.disk:
            try:
                self.ebeveyn.disk.commit()
            except:
                pass

        if kformat == "evet":
            self.surecCubugu.setValue(0)
            self.kurulumBilgisiLabel.setText(self.tr("Diskler Formatlanıyor..."))
            self.bolumFormatla(kbolum)
        if ktakas != "":
            self.surecCubugu.setValue(0)
            self.kurulumBilgisiLabel.setText(self.tr("Takas Alanı Ayarlanıyor..."))
            self.takasAyarla(ktakas)

        self.surecCubugu.setValue(0)
        self.kurulumBilgisiLabel.setText(kbolum + self.tr(" bölümü ") + kbaglam + self.tr(" bağlamına bağlanıyor..."))
        self.bolumBagla(kbolum, kbaglam)

        self.surecCubugu.setValue(0)
        self.kurulumBilgisiLabel.setText(self.tr("Kullanıcı Oluşturuluyor..."))
        self.kullaniciOlustur(kisim, kisim, ksifre)

        self.surecCubugu.setValue(0)
        self.kurulumBilgisiLabel.setText(self.tr("Sistem Kopyalanıyor..."))
        self.sistemKopyala(kbaglam)

        self.surecCubugu.setValue(0)
        self.kurulumBilgisiLabel.setText(self.tr("kişisel ayarlar Oluşturuluyor..."))
        self.kisiselOlustur(kbaglam,kdil,kzaman)

        self.surecCubugu.setValue(0)
        self.kurulumBilgisiLabel.setText(self.tr("initrd Oluşturuluyor..."))
        self.initrdOlustur(kbaglam)
        
        

        if kgrubkur == "evet":
            self.surecCubugu.setValue(0)
            self.kurulumBilgisiLabel.setText(self.tr("Grub Kuruluyor..."))
            self.grubKur(kbolum, kbaglam)
        self.surecCubugu.setValue(0)
        self.bolumCoz(kbolum)
        self.ebeveyn.ileriDugmeFonksiyon()


    def slaytDegistir(self):
        self.slaytci.setPixmap(QPixmap(":/slaytlar/slayt_" + str(self.slaytnumarasi) + ".png").scaled(607, 190))
        if self.slaytnumarasi == 6:
            self.slaytnumarasi = 1
        else:
            self.slaytnumarasi += 1
        self.zaman.start()


    def bolumFormatla(self, hedef):
        komut = "umount -l " + hedef
        self.kurulumBilgisiLabel.setText(komut)
        if os.path.exists(hedef):
            os.system(komut)
            self.surecCubugu.setValue(50)
            komut2 = "mkfs.ext4 -F " + hedef
            try:
                os.system(komut2)
                self.surecCubugu.setValue(100)
            except OSError as e:
                QMessageBox.warning(self, self.tr("Hata"), str(e))
                qApp.closeAllWindows()
            self.kurulumBilgisiLabel.setText(hedef + self.tr(" disk bölümü formatlandı."))
        else:
            QMessageBox.warning(self, self.tr("Hata"), self.tr("Disk bulunamadı. Program kapatılacak."))
            qApp.closeAllWindows()


    def takasAyarla(self, bolum):
        self.kurulumBilgisiLabel.setText("mkswap " + bolum)
        os.system("mkswap " + bolum)
        self.kurulumBilgisiLabel.setText('echo "`lsblk -ln -o UUID ' + bolum + '` none swap sw 0 0" | tee -a /etc/fstab')
        os.system('echo "`lsblk -ln -o UUID ' + bolum + '` none swap sw 0 0" | tee -a /etc/fstab')


    def bolumBagla(self, hedef, baglam):
        komut = "mount " + hedef + " " + baglam
        try:
            os.system(komut)
            self.surecCubugu.setValue(100)
        except OSError as e:
            QMessageBox.warning(self, self.tr("Hata"), str(e))
            qApp.closeAllWindows()
        self.kurulumBilgisiLabel.setText(hedef + " " + baglam + self.tr(" altına bağlandı."))


    def toplamBoyutTespit(self,liste):
        self.toplamBoyut=[]
        for i in liste:
            if os.path.exists("/"+i):
                komut = "du -s /"+i
                donut_=self.ebeveyn.komutCalistirFonksiyon(komut)
                donut=donut_.split("\n")
                boyut_=donut[len(donut)-2]
                boyut=boyut_.split("\t")
                self.toplamBoyut.append(int(boyut[0]))


    def kullaniciOlustur(self, isim, kullisim, kullsifre):
        os.system("kopar milislinux-" + isim + " " + kullisim)
        self.surecCubugu.setValue(20)
        os.system('echo -e "' + kullsifre + '\n' + kullsifre + '" | passwd ' + kullisim)
        self.surecCubugu.setValue(40)
        ayar_komut = "cp -r /root/.config /home/" + kullisim + "/"
        os.system(ayar_komut)
        self.surecCubugu.setValue(60)
        ayar_komut2 = "cp -r /root/.xinitrc /home/" + kullisim + "/"
        os.system(ayar_komut2)
        self.surecCubugu.setValue(80)
        saat_komut = "saat_ayarla_tr"
        os.system(saat_komut)
        self.surecCubugu.setValue(100)
        self.kurulumBilgisiLabel.setText(kullisim + self.tr(" kullanıcısı başarıyla oluşturuldu."))


    def sistemKopyala(self, baglam):
        os.system("clear")
        self.kurulumBilgisiLabel.setText(self.tr("Kurulum .desktop siliniyor..."))
        komut1 = "rm -rf /root/Masaüstü/kurulum.desktop"
        komut2 = "rm -rf /root/Desktop/kurulum.desktop"
        os.system(komut1)
        os.system(komut2)
        self.kurulumBilgisiLabel.setText(self.tr("Dizinler kopyalanmaya başlanyor..."))
        dizinler = ["bin", "boot", "home", "lib", "sources", "usr", "depo", "etc", "lib64", "opt", "root", "sbin", "var"]
        yenidizinler = ["srv", "proc", "tmp", "mnt", "sys", "run", "dev", "media"]
        self.toplamBoyutTespit(dizinler)
        self.baglam = baglam

        self.progressDurum = True
        progresThread = progressAyarciSinif(self)
        progresThread.start()

        self.dizinSirasi = 0
        mikdiz = len(dizinler)
        for dizin in dizinler:
            self.kopyalanacakDizinAdi = dizin
            self.dizinSirasi += 1
            self.kurulumBilgisiLabel.setText(str(self.dizinSirasi) + "/" + str(mikdiz) + dizin + self.tr(" kopyalanıyor..."))
            komut = "rsync --delete -axHAWX --numeric-ids /" + dizin + " " + baglam + " --exclude /proc"
            os.system(komut)
            qApp.processEvents()

        self.surecCubugu.setValue(0)
        self.kurulumBilgisiLabel.setText(self.tr("Yeni Dizinler Oluşturuluyor..."))

        self.progressDurum = False
        i = 0
        mikdiz = len(yenidizinler)
        for ydizin in yenidizinler:
            i += 1
            komut = "mkdir -p " + baglam + "/" + ydizin
            os.system(komut)
            yuzde = str(round(i / mikdiz, 2))[2:]
            if len(yuzde) == 1:
                yuzde = yuzde + "0"
            self.surecCubugu.setValue(int(yuzde))
            self.kurulumBilgisiLabel.setText(dizin + self.tr(" kopyalandı."))
            qApp.processEvents()


    def kisiselOlustur(self, hedef,dil,zaman):
        bolge=zaman.split("/")[0]
        yer=zaman.split("/")[1]
        lokal_ayarlar=open("/tmp/locale.conf","w")
        lokal_ayarlar.write("LC_ALL="+dil+".UTF-8")
        lokal_ayarlar.write("LANG="+dil+".UTF-8")
        lokal_ayarlar.write("LANGUAGE="+dil+".UTF-8")
        os.system("cp -f /tmp/locale.conf " + hedef + "/etc/locale.conf")
        os.system("cp /usr/share/zoneinfo/"+bolge+"/"+yer+" " + hedef + "/etc/localtime")
        os.system("mount --bind /dev " + hedef + "/dev")
        self.surecCubugu.setValue(25)
        os.system("mount --bind /sys " + hedef + "/sys")
        self.surecCubugu.setValue(50)
        os.system("mount --bind /proc " + hedef + "/proc")
        os.system("mount --bind /run " + hedef + "/run")
        self.surecCubugu.setValue(75)
        os.system('chroot ' + hedef + ' rm -rf /home/atilla')
        os.system('chroot ' + hedef + ' rm -rf /root/bin/atilla.sh')
        os.system('chroot ' + hedef + ' userdel atilla')
        os.system('chroot ' + hedef + ' rm /etc/shadow- /etc/gshadow- /etc/passwd- /etc/group- ')
        os.system('chroot ' + hedef + ' sed -i "/^atilla/d" /etc/security/opasswd ')
        os.system('chroot ' + hedef + ' cp /etc/slim.conf.orj /etc/slim.conf ')
        self.surecCubugu.setValue(100)
        self.kurulumBilgisiLabel.setText(self.tr("kişisel ayarlar Oluşturuldu"))

    def initrdOlustur(self, hedef):
        self.surecCubugu.setValue(75)
        os.system('chroot ' + hedef + ' rm -f /boot/initramfs')
        os.system('chroot ' + hedef + ' rm -f /boot/kernel')
        os.system("cp /run/initramfs/live/boot/kernel "+hedef+"/boot/kernel-$(uname -r)")
        os.system('chroot ' + hedef + ' dracut --no-hostonly --add-drivers "ahci" -f /boot/initramfs')
        self.surecCubugu.setValue(100)
        self.kurulumBilgisiLabel.setText(self.tr("initrd Oluşturuldu"))

    def grubKur(self,hedef,baglam):
        hedef = hedef[:-1]
        if hedef == "/dev/mmcblk0": #SD kart'a kurulum fix
            os.system('chroot ' + baglam + 'grub-install /dev/mmcblk0')
            #os.system("grub-install --boot-directory="+baglam+"/boot /dev/mmcblk0")
            self.surecCubugu.setValue(100)
        else:
            #os.system("grub-install --boot-directory="+baglam+"/boot " + hedef)
            os.system('chroot ' + baglam + ' grub-install '+hedef)
            self.surecCubugu.setValue(50)
            os.system("chroot "+baglam+" grub-mkconfig -o /boot/grub/grub.cfg")
            self.surecCubugu.setValue(100)
        self.kurulumBilgisiLabel.setText(self.tr("Grub Kuruldu."))

    def bolumCoz(self,hedef):
        komut="umount -l "+hedef
        try:
           os.system(komut)
        except OSError as e:
            QMessageBox.warning(self,self.tr("Hata"),str(e))
            qApp.closeAllWindows()
        self.surecCubugu.setValue(100)
        self.kurulumBilgisiLabel.setText(hedef+self.tr(" çözüldü."))

class progressAyarciSinif(QThread):
    def __init__(self,ebeveyn=None):
        super(progressAyarciSinif,self).__init__(ebeveyn)
        self.ebeveyn = ebeveyn
        self.ebeveyn.zaman.stop()
        self.ebeveyn.zaman.start()

    def run(self):
        while self.ebeveyn.progressDurum:
            self.guncelle()
            time.sleep(1)

    def guncelle(self):
        boyut=self.boyutTespit()
        toplamBoyut=self.ebeveyn.toplamBoyut[self.ebeveyn.dizinSirasi-1]
        print(boyut)
        print(toplamBoyut)
        if boyut<toplamBoyut:
            yuzde = str(round(boyut/toplamBoyut,2))[2:]
            if len(yuzde) == 1:
                yuzde = yuzde + "0"
            self.ebeveyn.surecCubugu.setValue(int(yuzde))
        else:
            self.ebeveyn.surecCubugu.setValue(100)

    def boyutTespit(self):
        try:
            komut = "du -s "+self.ebeveyn.baglam+"/"+self.ebeveyn.kopyalanacakDizinAdi
            donut_=self.ebeveyn.ebeveyn.komutCalistirFonksiyon(komut)
            donut=donut_.split("\n")
            boyut_=donut[len(donut)-2]
            boyut=boyut_.split("\t")
            return int(boyut[0])
        except:
            return 0
