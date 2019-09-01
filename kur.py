import gi
gi.require_version('Gtk', '3.0')
from kutuphaneler import diller, klavyeler, hosgeldiniz, klavye, konum, kullanici, disk
#gi.require_version('GtkSource', '3.0')

from gi.repository import Gtk#GtkSource, GObject, Gio, Gdk

class MerkezPencere(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self)
		self.set_border_width(5)
		self.set_resizable(False)
		self.set_default_size(640, 350)
		self.milis_ayarlari = {"dil":"Türkçe",
								"klavye_model":("",""),
								"klavye_duzen":("",""),
								"klavye_varyant":("",""),
								"konum":False,
								"kullanici_adi":"",
								"giris_adi":"",
								"bilgisayar_adi":"",
								"kullanici_sifre":"",
								"yonetici_sifre":"",
								"oto_giris":False,
								"sistem_disk":"",
								"takas_disk":"",
								"uefi_disk":"",
								"grub_kur":True}

		self.hb = Gtk.HeaderBar()
		self.hb.set_show_close_button(True)
		self.set_titlebar(self.hb)

		self.geri_dugme = Gtk.Button()
		self.geri_dugme.connect("clicked",self.geri_basildi)
		self.geri_dugme.set_always_show_image(True)
		self.geri_dugme.set_image(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
		self.hb.pack_start(self.geri_dugme)

		self.ileri_dugme = Gtk.Button()
		self.ileri_dugme.connect("clicked",self.ileri_basildi)
		self.ileri_dugme.set_always_show_image(True)
		self.ileri_dugme.set_image_position(Gtk.Justification.RIGHT)
		self.ileri_dugme.set_image(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
		self.hb.pack_end(self.ileri_dugme)

		self.stack_secili = 0
		self.stack_liste = [hosgeldiniz.StHosgeldiniz(self),klavye.StKlavye(self),konum.StKonum(self),kullanici.StKullanici(self),disk.StDisk(self)]
		self.stack = Gtk.Stack()
		self.add(self.stack)
		self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
		self.stack.set_transition_duration(1000)
		for sta in self.stack_liste:
			self.stack.add_titled(sta, sta.ad, sta.baslik)

		####### ilk stacketi ekliyoruz ######
		self.baslik_ekle(self.stack_liste[0])
		self.geri_dugme.set_sensitive(False)
		self.dil_ata("Türkçe")

	def dil_ata(self,dil):
		self.set_title(diller.diller[dil]["t1"])
		self.geri_dugme.set_label(diller.diller[dil]["t2"])
		self.ileri_dugme.set_label(diller.diller[dil]["t3"])
		for sta in self.stack_liste:
			sta.dil_ata(dil)
		self.hb.props.title = self.stack_liste[self.stack_secili].baslik

	def ileri_basildi(self,widget):
		self.stack_secili += 1
		self.geri_dugme.set_sensitive(True)
		self.baslik_ekle(self.stack_liste[self.stack_secili])
		if self.stack_secili == 3:
			if self.stack_liste[self.stack_secili].kontrol() == False:
				self.stack_liste[self.stack_secili].yon_kul_ayni_gizle()
			else:
				self.ileri_dugme.set_sensitive(True)
		elif self.stack_secili == 4 and self.milis_ayarlari["sistem_disk"] == "":
				self.ileri_dugme.set_sensitive(False)

	def geri_basildi(self,widget):
		self.stack_secili -= 1
		self.baslik_ekle(self.stack_liste[self.stack_secili])
		self.ileri_dugme.set_sensitive(True)
		if self.stack_secili == 0:
			self.geri_dugme.set_sensitive(False)

	def baslik_ekle(self,stack):
		self.hb.props.title = stack.baslik
		self.stack.set_visible_child_name(stack.ad)

if __name__ == '__main__':
	pen = MerkezPencere()
	pen.connect("destroy", Gtk.main_quit)
	pen.show_all()
	Gtk.main()
