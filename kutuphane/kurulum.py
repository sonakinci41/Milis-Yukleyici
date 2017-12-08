from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QMessageBox, qApp
from PyQt5.QtCore import QTimer, QThread
from PyQt5.QtGui import QPixmap
import os, time

class Kurulum(QWidget):
    def __init__(self, ebeveyn=None):
        super(Kurulum, self).__init__(ebeveyn)
        self.e = ebeveyn
        kutu = QVBoxLayout()
        kutu.setContentsMargins(0,0,0,0)
        self.setLayout(kutu)

        self.slayt_label = QLabel()
        self.slayt_label.setFixedSize(950,475)
        kutu.addWidget(self.slayt_label)
        self.bilgi_label = QLabel()
        kutu.addWidget(self.bilgi_label)
        self.surec_cubugu = QProgressBar()
        kutu.addWidget(self.surec_cubugu)

    def slaytci(self):
        self.slaytlar = os.listdir("slaytlar")
        self.slaytlar.sort()
        self.bulunulan_slayt = 1
        self.slayt_sayisi = len(self.slaytlar)
        self.slayt_label.setPixmap(QPixmap("slaytlar/" + self.slaytlar[0]))
        self.zaman = QTimer(self)
        self.zaman.setInterval(30000)
        self.zaman.timeout.connect(self.slay_degistir)
        self.zaman.start()

    def slay_degistir(self):
        self.bulunulan_slayt += 1
        if self.bulunulan_slayt > self.slayt_sayisi:
            self.bulunulan_slayt = 1
        self.slayt_label.setPixmap(QPixmap("slaytlar/"+self.slaytlar[self.bulunulan_slayt-1]))


    def showEvent(self, event):
        self.e.setWindowTitle(self.e.d[self.e.s_d]["Milis Linux Yükleniyor"])
        self.slaytci()
        kurulum = kurulumThread(self)
        kurulum.start()

class kurulumThread(QThread):
    def __init__(self, ebeveyn=None):
        super(kurulumThread, self).__init__(ebeveyn)
        self.f = ebeveyn
        self.e = self.f.e

    def run(self):
        self.e.geri_dugme.setDisabled(True)
        self.e.ileri_dugme.setDisabled(True)
        kbolum = self.e.milis_ayarlar["disk_bolum"]
        kformat = self.e.milis_ayarlar["disk_format"]
        kbaglam = "/mnt"
        ktakas = self.e.milis_ayarlar["disk_takasbolum"]
        kisim = self.e.milis_ayarlar["kullanici_adi"]
        kuisim = self.e.milis_ayarlar["gercek_ad"]
        ksifre = self.e.milis_ayarlar["giris_sifresi"]
        krootsifre = self.e.milis_ayarlar["admin_sifresi"]
        kotogiris = self.e.milis_ayarlar["otomatik_giris"]
        kgrubkur = self.e.milis_ayarlar["grub-kur"]
        kdil = self.e.milis_ayarlar["dil"]
        kzaman = self.e.milis_ayarlar["konum"]

        self.f.bilgi_label.setText(self.e.d[self.e.s_d]["Değişiklikler Diske Uygulanıyor..."])
        if self.e.disk:
            try:
                self.e.disk.commit()
            except:
                pass

        if kformat:
            self.f.surec_cubugu.setValue(0)
            self.f.bilgi_label.setText(self.e.d[self.e.s_d]["Diskler Formatlanıyor..."])
            self.bolumFormatla(kbolum)
        if ktakas != "":
            self.f.surec_cubugu.setValue(0)
            self.f.bilgi_label.setText(self.e.d[self.e.s_d]["Takas Alanı Ayarlanıyor..."])
            self.takasAyarla(ktakas)

        self.f.surec_cubugu.setValue(0)
        self.f.bilgi_label.setText(kbolum + self.e.d[self.e.s_d][" bölümü "] + kbaglam + self.e.d[self.e.s_d][" bağlamına bağlanıyor..."])
        self.bolumBagla(kbolum, kbaglam)

        self.f.surec_cubugu.setValue(0)
        self.f.bilgi_label.setText(self.e.d[self.e.s_d]["Kullanıcı Oluşturuluyor..."])
        self.kullaniciOlustur(kuisim, kisim, ksifre, krootsifre)

        self.f.surec_cubugu.setValue(0)
        self.f.bilgi_label.setText(self.e.d[self.e.s_d]["Sistem Kopyalanıyor..."])
        self.sistemKopyala(kbaglam)

        self.f.surec_cubugu.setValue(0)
        self.f.bilgi_label.setText(self.e.d[self.e.s_d]["kişisel ayarlar oluşturuluyor..."])
        self.kisiselOlustur(kbaglam, kdil, kzaman, kotogiris, kisim)

        self.f.surec_cubugu.setValue(0)
        self.f.bilgi_label.setText(self.e.d[self.e.s_d]["initrd oluşturuluyor..."])
        self.initrdOlustur(kbaglam)

        if kgrubkur:
            self.f.surec_cubugu.setValue(0)
            self.f.bilgi_label.setText(self.e.d[self.e.s_d]["Grub Kuruluyor..."])
            self.grubKur(kbolum, kbaglam)
        self.f.surec_cubugu.setValue(0)
        self.bolumCoz(kbolum)
        self.e.asama_degistir(8)

    def bolumFormatla(self, hedef):
        komut = "umount -l " + hedef
        self.f.bilgi_label.setText(komut)
        if os.path.exists(hedef):
            os.system(komut)
            self.f.surec_cubugu.setValue(50)
            komut2 = "mkfs.ext4 -F " + hedef
            try:
                os.system(komut2)
                self.f.surec_cubugu.setValue(100)
            except OSError as e:
                QMessageBox.warning(self, self.e.d[self.e.s_d]["Hata"], str(e))
                qApp.closeAllWindows()
                self.f.bilgi_label.setText(hedef + self.e.d[self.e.s_d][" disk bölümü formatlandı."])
        else:
            QMessageBox.warning(self, self.e.d[self.e.s_d]["Hata"], self.e.d[self.e.s_d]["Disk bulunamadı. Program kapatılacak."])
            qApp.closeAllWindows()

    def takasAyarla(self, bolum):
        self.f.bilgi_label.setText("mkswap " + bolum)
        os.system("mkswap " + bolum)
        self.f.bilgi_label.setText(
            'echo "UUID=`lsblk -ln -o UUID ' + bolum + '` none swap sw 0 0" | tee -a /etc/fstab')
        os.system('echo "UUID=`lsblk -ln -o UUID ' + bolum + '` none swap sw 0 0" | tee -a /etc/fstab')

    def bolumBagla(self, hedef, baglam):
        komut = "mount " + hedef + " " + baglam
        try:
            os.system(komut)
            self.f.surec_cubugu.setValue(100)
        except OSError as e:
            QMessageBox.warning(self, self.e.d[self.e.s_d]["Hata"], str(e))
            qApp.closeAllWindows()
            self.f.bilgi_label.setText(hedef + " " + baglam + self.e.d[self.e.s_d][" altına bağlandı."])

    def toplamBoyutTespit(self, liste):
        self.toplamBoyut = []
        for i in liste:
            if os.path.exists("/" + i):
                komut = "du -s /" + i
                donut_ = self.e.komutCalistirFonksiyon(komut)
                donut = donut_.split("\n")
                boyut_ = donut[len(donut) - 2]
                boyut = boyut_.split("\t")
                self.toplamBoyut.append(int(boyut[0]))

    def kullaniciOlustur(self, uzun_isim, kullisim, kullsifre, rootsifre):
        uzun_isim = uzun_isim.replace(' ', '_')
        os.system("kopar " + uzun_isim + " " + kullisim)
        self.f.surec_cubugu.setValue(20)
        os.system('echo -e "' + kullsifre + '\n' + kullsifre + '" | passwd ' + kullisim)
        os.system('echo -e "' + rootsifre + '\n' + rootsifre + '" | passwd root')
        self.f.surec_cubugu.setValue(40)
        ayar_komut = "cp -r /home/atilla/.config /home/" + kullisim + "/"
        os.system(ayar_komut)
        self.f.surec_cubugu.setValue(60)
        ayar_komut2 = "cp -r /root/.xinitrc /home/" + kullisim + "/"
        os.system(ayar_komut2)
        self.f.surec_cubugu.setValue(80)
        saat_komut = "saat_ayarla_tr"
        os.system(saat_komut)
        self.f.surec_cubugu.setValue(100)
        self.f.bilgi_label.setText(kullisim + self.e.d[self.e.s_d][" kullanıcısı başarıyla oluşturuldu."])

    def sistemKopyala(self, baglam):
        os.system("clear")
        komut1 = "rm -rf /root/Masaüstü/kurulum.desktop"
        komut2 = "rm -rf /root/Desktop/kurulum.desktop"
        os.system(komut1)
        os.system(komut2)
        self.f.bilgi_label.setText(self.e.d[self.e.s_d]["Dizinler kopyalanmaya başlanıyor..."])
        dizinler = ["bin", "boot", "home", "lib", "sources", "usr", "depo", "etc", "lib64", "opt", "root", "sbin",
                    "var"]
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
            self.f.bilgi_label.setText(
                str(self.dizinSirasi) + "/" + str(mikdiz) + dizin + self.e.d[self.e.s_d][" kopyalanıyor..."])
            komut = "rsync --delete -axHAWX --numeric-ids /" + dizin + " " + baglam + " --exclude /proc"
            os.system(komut)
            qApp.processEvents()

        self.f.surec_cubugu.setValue(0)
        self.f.bilgi_label.setText(self.e.d[self.e.s_d]["Yeni Dizinler Oluşturuluyor..."])

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
            self.f.surec_cubugu.setValue(int(yuzde))
            self.f.bilgi_label.setText(dizin + self.e.d[self.e.s_d][" kopyalandı."])
            qApp.processEvents()

    def kisiselOlustur(self, hedef, dil, zaman, otogiris, isim):
        bolge = zaman.split("/")[0]
        yer = zaman.split("/")[1]
        lokal_ayarlar = open("/tmp/locale.conf", "w")
        icerik = "LC_ALL=" + dil + ".UTF-8 \n"
        icerik += "LANG=" + dil + ".UTF-8 \n"
        icerik += "LANGUAGE=" + dil + ".UTF-8"
        lokal_ayarlar.write(icerik)
        lokal_ayarlar.close()
        os.system("cp /usr/share/zoneinfo/" + bolge + "/" + yer + " " + hedef + "/etc/localtime")
        os.system("mount --bind /dev " + hedef + "/dev")
        self.f.surec_cubugu.setValue(25)
        os.system("mount --bind /sys " + hedef + "/sys")
        self.f.surec_cubugu.setValue(50)
        os.system("mount --bind /proc " + hedef + "/proc")
        os.system("mount --bind /run " + hedef + "/run")
        self.f.surec_cubugu.setValue(75)
        os.system("cp -rf /tmp/locale.conf " + hedef + "/etc/")
        os.system("cp -rf /run/initramfs/live/updates/home/atilla/.* " + hedef + "/etc/skel/")
        os.system("cp -rf /run/initramfs/live/updates/home/atilla/.* " + hedef + "/home/" + isim + "/")
        os.system('chroot ' + hedef + ' rm -rf /home/atilla')
        os.system('chroot ' + hedef + ' rm -rf /root/bin/atilla.sh')
        os.system('chroot ' + hedef + ' rm -rf /opt/Milis-Yukleyici')
        os.system('chroot ' + hedef + ' rm -rf /root/Desktop/kurulum.desktop')
        os.system('chroot ' + hedef + ' rm -rf /home/' + isim + '/Desktop/kurulum.desktop')
        os.system('chroot ' + hedef + ' rm -rf /root/Masaüstü/kurulum.desktop')
        os.system('chroot ' + hedef + ' rm -rf /home/' + isim + '/Masaüstü/kurulum.desktop')
        os.system('chroot ' + hedef + ' rm -rf /root/Masaüstü/milis-kur.desktop')
        os.system('chroot ' + hedef + ' userdel atilla')
        os.system('chroot ' + hedef + ' rm /etc/shadow- /etc/gshadow- /etc/passwd- /etc/group- ')
        os.system('chroot ' + hedef + ' sed -i "/^atilla/d" /etc/security/opasswd ')
        os.system('chroot ' + hedef + ' cp /etc/slim.conf.orj /etc/slim.conf ')
        os.system('chroot ' + hedef + ' rm -rf /home/' + isim + '/Desktop')
        os.system('chroot ' + hedef + ' su - ' + isim + ' -c "xdg-user-dirs-update" ')
        os.system('chroot ' + hedef + ' chown ' + isim + ':' + isim + ' -R /home/' + isim)
        os.system('chroot ' + hedef + ' setfacl -m u:' + isim + ':rw /dev/snd/* ')

        if otogiris:
            os.system('chroot ' + hedef + ' sed -i s/"#default_user .*"/"default_user ' + isim + '/" /etc/slim.conf')
            os.system('chroot ' + hedef + ' sed -i s/"#auto_login .*"/"auto_login  yes/" /etc/slim.conf')

        self.f.surec_cubugu.setValue(100)
        self.f.bilgi_label.setText(self.e.d[self.e.s_d]["kişisel ayarlar oluşturuldu"])

    def initrdOlustur(self, hedef):
        self.f.surec_cubugu.setValue(75)
        os.system('chroot ' + hedef + ' rm -f /boot/initramfs')
        os.system('chroot ' + hedef + ' rm -f /boot/kernel')
        os.system("cp /run/initramfs/live/boot/kernel " + hedef + "/boot/kernel-$(uname -r)")
        os.system('chroot ' + hedef + ' dracut --no-hostonly --add-drivers "ahci" -f /boot/initramfs')
        self.f.surec_cubugu.setValue(100)
        self.f.bilgi_label.setText(self.e.d[self.e.s_d]["initrd oluşturuldu"])

    def grubKur(self, hedef, baglam):
        hedef = hedef[:-1]
        if hedef == "/dev/mmcblk0":  # SD kart'a kurulum fix
            os.system('chroot ' + baglam + 'grub-install /dev/mmcblk0')
            # os.system("grub-install --boot-directory="+baglam+"/boot /dev/mmcblk0")
            self.f.surec_cubugu.setValue(100)
        else:
            # os.system("grub-install --boot-directory="+baglam+"/boot " + hedef)
            os.system('chroot ' + baglam + ' grub-install ' + hedef)
            self.f.surec_cubugu.setValue(50)
            os.system("chroot " + baglam + " grub-mkconfig -o /boot/grub/grub.cfg")
            self.f.surec_cubugu.setValue(100)
            self.f.bilgi_label.setText(self.e.d[self.e.s_d]["Grub Kuruldu."])

    def bolumCoz(self, hedef):
        komut = "umount -l " + hedef
        try:
            os.system(komut)
        except OSError as e:
            QMessageBox.warning(self, self.e.d[self.e.s_d]["Hata"], str(e))
            qApp.closeAllWindows()
        self.f.surec_cubugu.setValue(100)
        self.f.bilgi_label.setText(hedef + self.e.d[self.e.s_d][" çözüldü."])




class progressAyarciSinif(QThread):
    def __init__(self, ebeveyn=None):
        super(progressAyarciSinif, self).__init__(ebeveyn)
        self.e = ebeveyn
        self.f = self.e.f

    def run(self):
        while self.e.progressDurum:
            self.guncelle()
            time.sleep(1)

    def guncelle(self):
        boyut = self.boyutTespit()
        toplamBoyut = self.e.toplamBoyut[self.e.dizinSirasi - 1]
        print(boyut)
        print(toplamBoyut)
        if boyut < toplamBoyut:
            yuzde = str(round(boyut / toplamBoyut, 2))[2:]
            if len(yuzde) == 1:
                yuzde = yuzde + "0"
            self.f.surec_cubugu.setValue(int(yuzde))
        else:
            self.f.surec_cubugu.setValue(100)

    def boyutTespit(self):
        try:
            komut = "du -s " + self.e.baglam + "/" + self.e.kopyalanacakDizinAdi
            donut_ = self.e.e.komutCalistirFonksiyon(komut)
            donut = donut_.split("\n")
            boyut_ = donut[len(donut) - 2]
            boyut = boyut_.split("\t")
            return int(boyut[0])
        except:
            return 0
