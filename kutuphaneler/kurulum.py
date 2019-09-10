from gi.repository import Gtk
from kutuphaneler import diller
import os

class StKurulum(Gtk.Grid):
	def __init__(self,ebeveyn):
		Gtk.Window.__init__(self)
		self.ebeveyn = ebeveyn
		self.baslik = "Milis Linux Kuruluyor"
		self.ad = "Kurulum"
		self.pb = Gtk.ProgressBar()
		self.pb.set_fraction(100.0)
		self.attach(self.pb,0,0,1,1)


	def kurulum(self):
		#self.sistem_diski_ayarla(self.ebeveyn.milis_ayarlari["sistem_disk"])
		if self.ebeveyn.milis_ayarlari["takas_disk"] != "":
			pass
			#self.takas_diski_ayarla(self.ebeveyn.milis_ayarlari["takas_disk"])
		if self.ebeveyn.milis_ayarlari["uefi_disk"] != "":
			pass
			#self.uefi_diski_ayarla(self.ebeveyn.milis_ayarlari["uefi_disk"])
		#self.sistem_diski_bagla(self.ebeveyn.milis_ayarlari["sistem_disk"],BAĞLANACAK YERİ BİLMİYORUM)
		#self.kullanici_olustur(BURAYA NELER GELECEĞİ HENÜZ BELİRLİ DEĞİL)
		#self.sistem_kopyala()
		#self.initrd_olustur(self.ebeveyn.milis_ayarlari["sistem_disk"])
		#grub_kur

	def sistem_diski_ayarla(self,bolum):
		komut="umount -l "+bolum
		if os.path.exists(hedef):
			print("Diski ayırırlıyor")
			os.system(komut)
			komut2="mkfs.ext4 -F " + hedef
			try:
				print("Disk biçimlendiriliyor")
				os.system(komut2)
			except OSError as e:
				print("Disk biçimlendirilirken bir hatayla karşılaşıdı",str(e))#################HATA
		else:
			print("Disk bulunamadı")#################HATA


	def takas_diski_ayarla(self,bolum):
		print("Takas Diski Ayarlanıyor")
		os.system("mkswap "+"/dev/"+bolum)
		os.system('echo "`lsblk -ln -o UUID /dev/' + bolum + '` none swap sw 0 0" | tee -a /etc/fstab')

	def uefi_diski_ayarla(self,bolum):
		print("UEFİ Diski Ayarlanıyor")
		pass

	def sistem_diski_bagla(hedef,baglam):
		print("Disk hedefe bağlandı")
		komut="mount "+hedef+" "+baglam
		try:
			os.system(komut)
		except OSError as e:
			print("Disk bağlanamadı",str(e))##################HATA

	def kullanici_olustur(self,isim,kullisim,kullsifre):
		os.system("kopar milislinux-"+isim+" "+kullisim)
		os.system('echo -e "'+kullsifre+'\n'+kullsifre+'" | passwd '+kullisim)
		os.system("cp -r /root/.config /home/"+kullisim+"/")
		os.system("cp -r /root/.xinitrc /home/"+kullisim+"/")
		os.system("saat_ayarla_tr")

	def sistem_kopyala(self):
		pass

	def initrd_olustur(self,hedef):
		os.system("mount --bind /dev "+hedef+"/dev")
		os.system("mount --bind /sys "+hedef+"/sys")
		os.system("mount --bind /proc "+hedef+"/proc")
		os.system('chroot '+hedef+' dracut --no-hostonly --add-drivers "ahci" -f /boot/initramfs')

	def grub_kur(self,hedef,baglam):
		hedef = hedef[:-1]
		if hedef == "/dev/mmcblk0": #SD kart'a kurulum fix
			os.system("grub-install --boot-directory="+baglam+"/boot /dev/mmcblk0")
		else:
			os.system("grub-install --boot-directory="+baglam+"/boot " + hedef)
			os.system("chroot "+baglam+" grub-mkconfig -o /boot/grub/grub.cfg")

	def dil_ata(self,dil):
		self.baslik = diller.diller[dil]["t48"]
		self.pb.set_text("Yani Kuracaz Silecez")