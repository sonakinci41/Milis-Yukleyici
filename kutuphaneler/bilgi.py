from gi.repository import Gtk, Gdk
from kutuphaneler import diller

class StBilgi(Gtk.Grid):
	def __init__(self,ebeveyn):
		Gtk.Window.__init__(self)
		self.ebeveyn = ebeveyn
		self.baslik = "Kurulum Bilgisi"
		self.ad = "Bilgi"

		self.sistem_dili_label = Gtk.Label()
		self.attach(self.sistem_dili_label,0,0,1,1)
		self.klavye__model_label = Gtk.Label()
		self.attach(self.klavye__model_label,0,1,1,1)

		self.klavye__duzen_label = Gtk.Label()
		self.attach(self.klavye__duzen_label,0,2,1,1)

		self.klavye__varyant_label = Gtk.Label()
		self.attach(self.klavye__varyant_label,0,3,1,1)

		self.konum_label = Gtk.Label()
		self.attach(self.konum_label,0,4,1,1)

		self.kullanici_adi_label = Gtk.Label()
		self.attach(self.kullanici_adi_label ,0,5,1,1)

		self.giris_adi_label = Gtk.Label()
		self.attach(self.giris_adi_label,0,6,1,1)

		self.bilgisayar_adi_label = Gtk.Label()
		self.attach(self.bilgisayar_adi_label,0,7,1,1)

		self.kullanici_sifre_label = Gtk.Label()
		self.attach(self.kullanici_sifre_label,0,8,1,1)

		self.yonetici_sifre_label = Gtk.Label()
		self.attach(self.yonetici_sifre_label,0,9,1,1)

		self.otomatik_giris_label = Gtk.Label()
		self.attach(self.otomatik_giris_label,0,10,1,1)

		self.sistem_diski_label = Gtk.Label()
		self.attach(self.sistem_diski_label,0,11,1,1)

		self.takas_diski_label = Gtk.Label()
		self.attach(self.takas_diski_label,0,12,1,1)

		self.uefi_diski_label = Gtk.Label()
		self.attach(self.uefi_diski_label,0,13,1,1)

		self.grub_kur_label = Gtk.Label()
		self.attach(self.grub_kur_label,0,14,1,1)


	def dil_ata(self,dil):
		self.baslik = diller.diller[dil]["t39"]
		self.sistem_dili_label.set_text(diller.diller[dil]["t40"]+self.ebeveyn.milis_ayarlari['dil'])
		self.klavye__model_label.set_text(" ".join(self.ebeveyn.milis_ayarlari['klavye_model']))
		self.klavye__duzen_label.set_text(" ".join(self.ebeveyn.milis_ayarlari['klavye_duzen']))
		self.klavye__varyant_label.set_text(" ".join(self.ebeveyn.milis_ayarlari['klavye_varyant']))
		self.konum_label.set_text(self.ebeveyn.milis_ayarlari['konum'])
		self.kullanici_adi_label.set_text(self.ebeveyn.milis_ayarlari['kullanici_adi'])
		self.giris_adi_label.set_text(self.ebeveyn.milis_ayarlari['giris_adi'])
		self.bilgisayar_adi_label.set_text(self.ebeveyn.milis_ayarlari['bilgisayar_adi'])
		self.kullanici_sifre_label.set_text(len(self.ebeveyn.milis_ayarlari['kullanici_sifre'])*"*")
		self.yonetici_sifre_label.set_text(len(self.ebeveyn.milis_ayarlari['yonetici_sifre'])*"*")
		self.otomatik_giris_label.set_text(str(self.ebeveyn.milis_ayarlari['oto_giris']))
		self.sistem_diski_label.set_text(self.ebeveyn.milis_ayarlari['sistem_disk'])
		self.takas_diski_label.set_text(self.ebeveyn.milis_ayarlari['takas_disk'])
		self.uefi_diski_label.set_text(self.ebeveyn.milis_ayarlari['uefi_disk'])
		self.grub_kur_label.set_text(str(self.ebeveyn.milis_ayarlari['grub_kur']))
		
		