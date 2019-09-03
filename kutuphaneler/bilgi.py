from gi.repository import Gtk, Gdk
from kutuphaneler import diller

class StBilgi(Gtk.Grid):
	def __init__(self,ebeveyn):
		Gtk.Window.__init__(self)
		self.ebeveyn = ebeveyn
		self.baslik = "Kurulum Bilgisi"
		self.ad = "Bilgi"

		self.sistem_dili_label = Gtk.Label()
		self.sistem_dili_label.set_hexpand(True)
		self.attach(self.sistem_dili_label,0,0,1,1)

		self.klavye_model_label = Gtk.Label()
		self.klavye_model_label.set_hexpand(True)
		self.attach(self.klavye_model_label,0,1,1,1)

		self.klavye_duzen_label = Gtk.Label()
		self.klavye_duzen_label.set_hexpand(True)
		self.attach(self.klavye_duzen_label,0,2,1,1)

		self.klavye_varyant_label = Gtk.Label()
		self.klavye_varyant_label.set_hexpand(True)
		self.attach(self.klavye_varyant_label,0,3,1,1)

		self.konum_label = Gtk.Label()
		self.konum_label.set_hexpand(True)
		self.attach(self.konum_label,0,4,1,1)

		self.kullanici_adi_label = Gtk.Label()
		self.kullanici_adi_label.set_hexpand(True)
		self.attach(self.kullanici_adi_label ,0,5,1,1)

		self.giris_adi_label = Gtk.Label()
		self.giris_adi_label.set_hexpand(True)
		self.attach(self.giris_adi_label,0,6,1,1)

		self.bilgisayar_adi_label = Gtk.Label()
		self.bilgisayar_adi_label.set_hexpand(True)
		self.attach(self.bilgisayar_adi_label,0,7,1,1)

		self.kullanici_sifre_label = Gtk.Label()
		self.kullanici_sifre_label.set_hexpand(True)
		self.attach(self.kullanici_sifre_label,0,8,1,1)

		self.yonetici_sifre_label = Gtk.Label()
		self.yonetici_sifre_label.set_hexpand(True)
		self.attach(self.yonetici_sifre_label,0,9,1,1)

		self.otomatik_giris_label = Gtk.Label()
		self.otomatik_giris_label.set_hexpand(True)
		self.attach(self.otomatik_giris_label,0,10,1,1)

		self.sistem_diski_label = Gtk.Label()
		self.sistem_diski_label.set_hexpand(True)
		self.attach(self.sistem_diski_label,0,11,1,1)

		self.takas_diski_label = Gtk.Label()
		self.takas_diski_label.set_hexpand(True)
		self.attach(self.takas_diski_label,0,12,1,1)

		self.uefi_diski_label = Gtk.Label()
		self.uefi_diski_label.set_hexpand(True)
		self.attach(self.uefi_diski_label,0,13,1,1)

		self.grub_kur_label = Gtk.Label()
		self.grub_kur_label.set_hexpand(True)
		self.attach(self.grub_kur_label,0,14,1,1)


	def dil_ata(self,dil):
		self.baslik = diller.diller[dil]["t39"]
		self.sistem_dili_label.set_text(diller.diller[dil]["t40"]+" : "+self.ebeveyn.milis_ayarlari['dil'])
		self.klavye_model_label.set_text(diller.diller[dil]["t41"]+" : "+" ".join(self.ebeveyn.milis_ayarlari['klavye_model']))
		self.klavye_duzen_label.set_text(diller.diller[dil]["t42"]+" : "+" ".join(self.ebeveyn.milis_ayarlari['klavye_duzen']))
		self.klavye_varyant_label.set_text(diller.diller[dil]["t43"]+" : "+" ".join(self.ebeveyn.milis_ayarlari['klavye_varyant']))
		self.konum_label.set_text(diller.diller[dil]["t44"]+" : "+self.ebeveyn.milis_ayarlari['konum'])
		self.kullanici_adi_label.set_text(diller.diller[dil]["t19"]+" : "+self.ebeveyn.milis_ayarlari['kullanici_adi'])
		self.giris_adi_label.set_text(diller.diller[dil]["t20"]+" : "+self.ebeveyn.milis_ayarlari['giris_adi'])
		self.bilgisayar_adi_label.set_text(diller.diller[dil]["t21"]+" : "+self.ebeveyn.milis_ayarlari['bilgisayar_adi'])
		self.kullanici_sifre_label.set_text(diller.diller[dil]["t24"]+" : "+len(self.ebeveyn.milis_ayarlari['kullanici_sifre'])*"*")
		self.yonetici_sifre_label.set_text(diller.diller[dil]["t28"]+" : "+len(self.ebeveyn.milis_ayarlari['yonetici_sifre'])*"*")
		self.otomatik_giris_label.set_text(diller.diller[dil]["t26"]+" : "+str(self.ebeveyn.milis_ayarlari['oto_giris']))
		self.sistem_diski_label.set_text(diller.diller[dil]["t33"]+" : "+self.ebeveyn.milis_ayarlari['sistem_disk'])
		self.takas_diski_label.set_text(diller.diller[dil]["t34"]+" : "+self.ebeveyn.milis_ayarlari['takas_disk'])
		self.uefi_diski_label.set_text(diller.diller[dil]["t35"]+" : "+self.ebeveyn.milis_ayarlari['uefi_disk'])
		self.grub_kur_label.set_text(diller.diller[dil]["t37"]+" : "+str(self.ebeveyn.milis_ayarlari['grub_kur']))
		
		