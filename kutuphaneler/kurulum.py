from gi.repository import Gtk, Gio, Gdk, GLib
from kutuphaneler import diller
import os, subprocess, threading

class StKurulum(Gtk.Grid):
	def __init__(self,ebeveyn):
		Gtk.Window.__init__(self)
		self.ebeveyn = ebeveyn
		self.dosya_sayisi = 0
		self.kopyalanan_sayisi = 0
		self.baslik = "Milis Linux Kuruluyor"
		self.ad = "Kurulum"
		self.resim = Gtk.Image()
		self.resim.set_from_file("./resimler/resim_1.jpg")
		self.attach(self.resim,0,0,1,1)
		self.bilgi_label = Gtk.Label()
		self.attach(self.bilgi_label,0,1,1,1)
		self.pb = Gtk.ProgressBar()
		self.pb.set_fraction(100.0)
		self.attach(self.pb,0,2,1,1)
		self.resim_sayac = 7

	def kurulum_baslat(self,dialog):
		dialog.destroy()
		th = threading.Thread(target=self.kurulum)
		th.daemon = True
		th.start()

	def bilgi_guncelle(self,yuzde=0,yazi=""):
		self.pb.set_fraction(yuzde)
		self.bilgi_label.set_text(yazi)
		self.resim.set_from_file("./resimler/resim_{}.jpg".format(str((self.resim_sayac%7)+1)))
		self.resim_sayac += 1

	def kurulum(self):
		print("calisti")
		self.diskleri_coz()#Diskler Çözülüyor
		
		self.disk_bagla()#Diskler Bağlanıyor
		self.resim.set_from_file("./resimler/resim_2.jpg")
		self.chroot_olsutur()#Chroot Oluşturuluyor
		self.resim.set_from_file("./resimler/resim_3.jpg")
		self.resim.set_from_file("./resimler/resim_4.jpg")
		self.dosya_kopyala("/","/mnt/root/")#Dosyalar Kopyalanıyor
		self.resim.set_from_file("./resimler/resim_5.jpg")
		self.fstab_olustur()#Fstab Oluşturukuyor
		self.resim.set_from_file("./resimler/resim_6.jpg")
		self.konum_ata()#Konum Ayarlanıyor
		self.resim.set_from_file("./resimler/resim_7.jpg")
		#self.dil_ayar()#Dil Ayarlanıyor
		self.resim.set_from_file("./resimler/resim_1.jpg")
		self.host_ata()#Hast Ayarları Yapılıyor
		self.resim.set_from_file("./resimler/resim_2.jpg")
		self.klavye_ata()#Klavye Ayarlanıyor
		self.resim.set_from_file("./resimler/resim_3.jpg")
		self.live_kullanici_sil()#Geçici Kullanıcı Siliniyor
		self.resim.set_from_file("./resimler/resim_4.jpg")
		self.sudoers_ata()#Yetkili Kullanıcı Ayarlanıyor
		self.resim.set_from_file("./resimler/resim_5.jpg")
		self.initciop_ata()#Inıtciop Oluşturuluyor
		self.resim.set_from_file("./resimler/resim_6.jpg")
		self.kullanici_ekle()#Kullanıcı Ekleniyor
		self.resim.set_from_file("./resimler/resim_7.jpg")
		if self.ebeveyn.milis_ayarlari["oto_giris"]:
			self.lightdm_oto_giris()#Oto Matik Giriş Ayarlanıyor
		self.grub_ata()#Grup Ayarlanıyor
		self.resim.set_from_file("./resimler/resim_1.jpg")
		self.diskleri_coz()#Diskler Çözülüyor
		self.resim.set_from_file("./resimler/resim_2.jpg")
		#Kurulum Tamamlandı
		Gdk.threads_leave()

	def diskleri_coz(self):
		print("Diskler Çözülüyor")
		GLib.idle_add(self.bilgi_guncelle,0,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t49"])
		command = subprocess.Popen(["df", "-h"], stdout=subprocess.PIPE)
		output = command.stdout.read().decode("utf-8")
		for out in output.split("\n"):
			if out.startswith("/dev/sd"):
				mount_folder = out.split()[-1]
				if not mount_folder == "/bootmnt":
					os.system("umount --force {}".format(mount_folder))
		print("GELDİ")
		GLib.idle_add(self.bilgi_guncelle,100,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t49"])

	def disk_bagla(self):
		print("Disk bağlanıyor")
		GLib.idle_add(self.bilgi_guncelle,0,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t50"])
		os.makedirs("/mnt/root", exist_ok=True)
		GLib.idle_add(self.bilgi_guncelle,50,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t50"])
		os.system("mount {} {}".format(self.ebeveyn.milis_ayarlari["sistem_disk"], "/mnt/root"))
		GLib.idle_add(self.bilgi_guncelle,100,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t50"])

	def chroot_olsutur(self):
		GLib.idle_add(self.bilgi_guncelle,0,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t51"])
		os.makedirs("/mnt/root/dev/shm", exist_ok=True)
		GLib.idle_add(self.bilgi_guncelle,8,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t51"])
		os.makedirs("/mnt/root/dev/pts", exist_ok=True)
		GLib.idle_add(self.bilgi_guncelle,16,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t51"])
		os.makedirs("/mnt/root/sys", exist_ok=True)
		GLib.idle_add(self.bilgi_guncelle,24,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t51"])
		os.makedirs("/mnt/root/proc", exist_ok=True)
		GLib.idle_add(self.bilgi_guncelle,32,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t51"])
		os.system("mount --bind /dev/ /mnt/root/dev/")
		GLib.idle_add(self.bilgi_guncelle,40,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t51"])
		os.system("mount --bind /dev/shm /mnt/root/dev/shm")
		GLib.idle_add(self.bilgi_guncelle,48,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t51"])
		os.system("mount --bind /dev/pts /mnt/root/dev/pts")
		GLib.idle_add(self.bilgi_guncelle,56,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t51"])
		os.system("mount --bind /sys/ /mnt/root/sys/")
		GLib.idle_add(self.bilgi_guncelle,64,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t51"])
		os.system("mount --bind /proc/ /mnt/root/proc/")
		GLib.idle_add(self.bilgi_guncelle,72,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t51"])
		os.system("chmod 555 /mnt/root/sys/")
		GLib.idle_add(self.bilgi_guncelle,80,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t51"])
		os.system("chmod 555 /mnt/root/proc/")
		GLib.idle_add(self.bilgi_guncelle,88,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t51"])

		if self.ebeveyn.milis_ayarlari["uefi_disk"] != "":
			os.makedirs("/mnt/root/boot/efi", exist_ok=True)
			os.system("mount -vt vfat {} /mnt/root/boot/efi".format(self.ebeveyn.milis_ayarlari["uefi_disk"]))
			os.system("mount -vt efivarfs efivars /sys/firmware/efi/efivars")
		GLib.idle_add(self.bilgi_guncelle,100,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t51"])

	def dosya_hesapla(self,dizin="/"):
		print("Hesapla")
		GLib.idle_add(self.bilgi_guncelle,0,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t52"])
		dosyaninici = os.listdir(dizin)
		dosyaninici.sort()
		for i in dosyaninici:
			yol = os.path.join(dizin,i)
			try:
				if os.path.isdir(yol) and not os.path.islink(yol):
					self.dosya_hesapla(yol)
				else:
					self.dosya_sayisi += 1
					self.bilgi_label.set_text(diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t52"]+" "+str(self.dosya_sayisi))
			except:
				pass

	def dosya_kopyala(self,dizin,hedef):
		for diz in os.listdir(dizin):
			GLib.idle_add(self.bilgi_guncelle,0,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t53"]+diz)
			os.system("rsync --delete -axHAWX --numeric-ids /"+os.path.join(dizin,diz)+" "+hedef+" --exclude /proc")

	def fstab_olustur(self):
		print("Fstab")
		def fstab_parse():
			device_list = []
			blkid_output = subprocess.Popen("blkid", stdout=subprocess.PIPE)
			output = blkid_output.stdout.read().decode("utf-8")
			for o in output.split("\n"):
				device = []
				for i in o.split():
					if i.startswith("/dev"):
						device.append(i[:-1])
					elif i.startswith("UUID="):
						device.append(i[6:-1])
					elif i.startswith("TYPE="):
						device.append(i[6:-1])
				device_list.append(device)
			return device_list

		GLib.idle_add(self.bilgi_guncelle,0,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t54"])
		with open("/mnt/root/etc/fstab", "w") as fstab_file:
			for device in fstab_parse():
				try:
					if "/mnt" == device[0]:
						fstab_file.write('UUID={}\t / \t\t {} \t defaults\t0\t1\n'.format(device[1], device[2]))
					elif self.ebeveyn.milis_ayarlari["uefi_disk"] == device[0]:
						fstab_file.write('UUID={}\t /boot/efi \t\t {} \t umask=0077\t0\t1\n'.format(device[1], device[2]))
					elif self.ebeveyn.milis_ayarlari["takas_disk"] == device[0]:
						fstab_file.write('UUID={}\t swap \t swap \t defaults\t0\t0\n'.format(device[1], device[2]))
				except IndexError:
					print(device, "Bu ne?")
			if self.ebeveyn.milis_ayarlari["uefi_disk"] != "":
				fstab_file.write("efivarfs       /sys/firmware/efi/efivars  efivarfs  defaults  0      1\n")
		GLib.idle_add(self.bilgi_guncelle,100,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t54"])


	def chroot_komut(self, komut):
		print("Chroot")
		os.system("chroot {} /bin/sh -c \"{}\"".format("/mnt/root", komut))

	def konum_ata(self):
		print("Konum")
		GLib.idle_add(self.bilgi_guncelle,0,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t55"])
		self.chroot_komut("ln -s /usr/share/zoneinfo/{} /etc/localtime".format(self.ebeveyn.milis_ayarlari["konum"]))
		GLib.idle_add(self.bilgi_guncelle,100,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t55"])

	def dil_ayar(self):
		print("Dil")
		GLib.idle_add(self.bilgi_guncelle,0,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t56"])
		if self.ebeveyn.milis_ayarlari["dil"] == "Türkçe":
			self.locale = "tr_TR.UTF-8"
		else:
			self.locale = "en_US.UTF-8"
		with open("/mnt/root/etc/locale.conf", "w") as locale:
			locale.write("LANG={}\n".format(self.locale))
			locale.write("LC_COLLATE=C\n")
			locale.flush()
			locale.close()
		GLib.idle_add(self.bilgi_guncelle,20,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t56"])

		buffer = open("/mnt/root/etc/locale.gen").readlines()
		with open("/mnt/root/etc/locale.gen", "w") as locale:
			for i in buffer:
				if i.startswith("#{}".format(self.locale.split(".")[0])):
					locale.write(i[1:])
					locale.flush()
					locale.close()
		GLib.idle_add(self.bilgi_guncelle,40,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t56"])
		self.chroot_komut("export LANG={}".format(self.locale))
		GLib.idle_add(self.bilgi_guncelle,60,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t56"])
		self.chroot_komut("export LANGUAGE={}".format(self.locale))
		GLib.idle_add(self.bilgi_guncelle,80,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t56"])
		self.chroot_komut("locale-gen {}".format(self.locale))
		GLib.idle_add(self.bilgi_guncelle,100,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t56"])


	def host_ata(self):
		print("Host")
		GLib.idle_add(self.bilgi_guncelle,0,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t57"])
		hosts_text = "# /etc/hosts\n"\
				"#\n"\
				"# This file describes a number of hostname-to-address\n"\
				"# mappings for the TCP/IP subsystem.  It is mostly\n"\
				"# used at boot time, when no name servers are running.\n"\
				"# On small systems, this file can be used instead of a\n"\
				"# \"named\" name server.  Just add the names, addresses\n"\
				"# and any aliases to this file...\n"\
				"#\n"\
				"\n"\
				"127.0.0.1   localhost      {}\n"\
				"\n"\
				"# IPV6 versions of localhost and co\n"\
				"::1     localhost ip6-localhost ip6-loopback\n"\
				"fe00::0 ip6-localnet\n"\
				"ff00::0 ip6-mcastprefix\n"\
				"ff02::1 ip6-allnodes\n"\
				"ff02::2 ip6-allrouters\n"\
				"ff02::3 ip6-allhosts\n".format(self.ebeveyn.milis_ayarlari["bilgisayar_adi"])
		with open("/mnt/root/etc/hostname", "w") as hostname:
			hostname.write(self.ebeveyn.milis_ayarlari["bilgisayar_adi"])
			hostname.flush()
			hostname.close()
		GLib.idle_add(self.bilgi_guncelle,50,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t57"])

		with open("/mnt/root/etc/hosts", "w") as hosts:
			hosts.write(hosts_text)
			hosts.flush()
			hosts.close()
		GLib.idle_add(self.bilgi_guncelle,100,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t57"])


	def klavye_ata(self):
		print("Klavye")
		GLib.idle_add(self.bilgi_guncelle,0,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t58"])
		keyboard = "Section \"InputClass\"\n"\
				"\t\tIdentifier \"system-keyboard\"\n"\
				"\t\tMatchIsKeyboard \"on\"\n"\
				"\t\tOption \"XkbModel\" \"{}\"\n"\
				"\t\tOption \"XkbLayout\" \"{}\"\n"\
				"\t\tOption \"XkbVariant\" \"{}\"\n"\
				"EndSection\n".format(self.ebeveyn.milis_ayarlari["klavye_model"][0],
							self.ebeveyn.milis_ayarlari["klavye_duzen"][0],self.ebeveyn.milis_ayarlari["klavye_varyant"][0])
		with open("/mnt/root/etc/X11/xorg.conf.d/10-keyboard.conf", "w") as keyboard_conf:
			keyboard_conf.write(keyboard)
			keyboard_conf.flush()
			keyboard_conf.close()
		GLib.idle_add(self.bilgi_guncelle,100,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t58"])

	def live_kullanici_sil(self):
		print("Live")
		GLib.idle_add(self.bilgi_guncelle,0,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t59"])
		self.chroot_komut("userdel -r milis")
		GLib.idle_add(self.bilgi_guncelle,50,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t59"])
		if os.path.exists("/mnt/root/home/milis"):
			os.system("rm -rf /mnt/root/home/milis")
		GLib.idle_add(self.bilgi_guncelle,100,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t59"])

	def sudoers_ata(self):
		print("Sudoers")
		GLib.idle_add(self.bilgi_guncelle,0,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t60"])
		sudoers = "# to use special input methods. This may allow users to compromise  the root\n"\
				"# account if they are allowed to run commands without authentication.\n"\
				"#Defaults env_keep = \"LANG LC_ADDRESS LC_CTYPE LC_COLLATE LC_IDENTIFICATION LC_MEASUREMENT "\
				"LC_MESSAGES LC_MONETARY LC_NAME LC_NUMERIC LC_PAPER LC_TELEPHONE LC_TIME LC_ALL LANGUAGE LINGUAS "\
				"XDG_SESSION_COOKIE XMODIFIERS GTK_IM_MODULEQT_IM_MODULE QT_IM_SWITCHER\"\n"\
				"\n"\
				"# User privilege specification\n"\
				"root    ALL=(ALL) ALL\n"\
				"\n"\
				"# Uncomment to allow people in group wheel to run all commands\n"\
				"%wheel  ALL=(ALL)       ALL\n"\
				"\n"\
				"# Same thing without a password\n"\
				"#%wheel ALL=(ALL)       NOPASSWD: ALL\n"\
				"{}    ALL=(ALL)       ALL".format(self.ebeveyn.milis_ayarlari["kullanici_adi"])

		with open("/mnt/root/etc/sudoers", "w") as sudoers_file:
			sudoers_file.write(sudoers)
			sudoers_file.flush()
			sudoers_file.close()
		GLib.idle_add(self.bilgi_guncelle,100,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t60"])

	def initciop_ata(self):
		print("ınıtciop")
		GLib.idle_add(self.bilgi_guncelle,0,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t61"])
		self.chroot_komut("mkinitcpio -p linux")
		GLib.idle_add(self.bilgi_guncelle,100,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t61"])


	def kullanici_ekle(self):
		print("Kullanici Ekle")
		GLib.idle_add(self.bilgi_guncelle,0,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t62"])
		groups_user = "-G audio,video,cdrom,wheel,lpadmin"
		self.chroot_komut("useradd -s {} -c '{}' {} -m {}".format("/bin/bash", self.ebeveyn.milis_ayarlari["giris_adi"],
											groups_user, self.ebeveyn.milis_ayarlari["kullanici_adi"]))
		GLib.idle_add(self.bilgi_guncelle,30,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t62"])
		self.chroot_komut("yes {} | passwd {}".format(self.ebeveyn.milis_ayarlari["kullanici_sifre"], self.ebeveyn.milis_ayarlari["kullanici_adi"]))
		GLib.idle_add(self.bilgi_guncelle,70,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t62"])
		self.chroot_komut("yes {} | passwd root".format(self.ebeveyn.milis_ayarlari["yonetici_sifre"]))
		GLib.idle_add(self.bilgi_guncelle,100,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t62"])

	def lightdm_oto_giris(self):
		print("LightDm")
		GLib.idle_add(self.bilgi_guncelle,0,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t63"])
		conf_data = []
		with open("/mount/root/etc/lightdm/lightdm.conf") as conf:
			for text in conf.readlines():
				if text.startswith("autologin-user="):
					conf_data.append("autologin-user={}\n".format(self.ebeveyn.milis_ayarlari["kullanici_adi"]))
				else:
					conf_data.append(text)

		GLib.idle_add(self.bilgi_guncelle,50,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t63"])
		with open("/mount/root/etc/lightdm/lightdm.conf", "w") as conf:
			conf.write("".join(conf_data))
		GLib.idle_add(self.bilgi_guncelle,100,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t63"])

	def disk_numara_sil(self,disk):
		a = ""
		for i in disk:
			if not i.isnumeric():
				a += i
		return a


	def grub_ata(self):
		print("Grub")
		def boot_part(dev):
			asd = subprocess.Popen("blkid", stdout=subprocess.PIPE)
			qwe = asd.stdout.read().decode("utf-8")
			for o in qwe.split("\n"):
				i = o.split()
				try:
					if i[0][:-1] == dev:
						for j in i:
							if j.startswith("PARTUUID="):
								return j[10:-1]
				except IndexError as ex:
					print(ex)

		GLib.idle_add(self.bilgi_guncelle,0,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t64"])
		if self.ebeveyn.milis_ayarlari["uefi_disk"] == "":
			self.chroot_komut("grub-install --force {}".format(self.disk_numara_sil(self.ebeveyn.milis_ayarlari["sistem_disk"])))
			GLib.idle_add(self.bilgi_guncelle,30,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t64"])
		else:
			self.chroot_komut("grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=\"{0}\" "\
						"--recheck --debug --force".format("MilisLinux"))
			GLib.idle_add(self.bilgi_guncelle,60,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t64"])
			self.chroot_komut("efibootmgr --create --gpt --disk {1} --part {2} --write-signature "\
						"--loader \"/EFI/{0}/grubx64.efi\"".format("MilisLinux", self.ebeveyn.milis_ayarlari["uefi_disk"], boot_part(self.ebeveyn.milis_ayarlari["uefi_disk"])))
			GLib.idle_add(self.bilgi_guncelle,80,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t64"])
		self.chroot_komut("grub-mkconfig -o /boot/grub/grub.cfg")
		GLib.idle_add(self.bilgi_guncelle,100,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t64"])

	def diskleri_coz(self):
		print("Diskler Çözülüyor")
		GLib.idle_add(self.bilgi_guncelle,0,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t65"])
		os.system("umount --force /mnt/root/dev/")
		GLib.idle_add(self.bilgi_guncelle,15,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t65"])
		os.system("umount --force /mnt/root/dev/shm")
		GLib.idle_add(self.bilgi_guncelle,30,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t65"])
		os.system("umount --force /mnt/root/dev/pts")
		GLib.idle_add(self.bilgi_guncelle,45,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t65"])
		os.system("umount --force /mnt/root/sys/")
		GLib.idle_add(self.bilgi_guncelle,60,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t65"])
		os.system("umount --force /mnt/root/proc/")
		GLib.idle_add(self.bilgi_guncelle,75,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t65"])
		os.system("umount -lv /mnt/root")
		GLib.idle_add(self.bilgi_guncelle,100,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t65"])
		GLib.idle_add(self.bilgi_guncelle,100,diller.diller[self.ebeveyn.milis_ayarlari["dil"]]["t66"])

	def dil_ata(self,dil):
		self.baslik = diller.diller[dil]["t48"]
