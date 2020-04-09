from gi.repository import Gtk, Gdk
from kutuphaneler import diller

class StKullanici(Gtk.Grid):
	def __init__(self,ebeveyn):
		Gtk.Window.__init__(self)
		self.ebeveyn = ebeveyn
		self.baslik = "Kullanıcı Ayarları"
		self.ad = "Kullanıcı"
		self.set_row_spacing(10)
		self.set_column_spacing(10)
		self.kontroller = [False,False,False,False,False]

		self.kirmizi = Gdk.RGBA(1.0, 0.15, 0.44, 1.0)
		self.yesil = Gdk.RGBA(0.65, 0.88, 0.18, 1.0)

		self.kul_yazi = Gtk.Label()
		self.attach(self.kul_yazi,0,0,1,1)
		self.kul_entry = Gtk.Entry()
		self.kul_entry.connect("changed", self.kul_entry_degisti)
		self.attach(self.kul_entry,1,0,1,1)
		self.kul_bilgi = Gtk.Label()
		self.kul_bilgi.override_color(Gtk.StateFlags.NORMAL, self.kirmizi)
		self.attach(self.kul_bilgi,2,0,1,1)

		self.gir_yazi = Gtk.Label()
		self.attach(self.gir_yazi,0,1,1,1)
		self.gir_entry = Gtk.Entry()
		self.gir_entry.connect("changed", self.gir_entry_degisti)
		self.attach(self.gir_entry,1,1,1,1)
		self.gir_bilgi = Gtk.Label()
		self.gir_bilgi.override_color(Gtk.StateFlags.NORMAL, self.kirmizi)
		self.attach(self.gir_bilgi,2,1,1,1)

		self.bil_yazi = Gtk.Label()
		self.attach(self.bil_yazi,0,2,1,1)
		self.bil_entry = Gtk.Entry()
		self.bil_entry.connect("changed", self.bil_entry_degisti)
		self.attach(self.bil_entry,1,2,1,1)
		self.bil_bilgi = Gtk.Label()
		self.bil_bilgi.override_color(Gtk.StateFlags.NORMAL, self.kirmizi)
		self.attach(self.bil_bilgi,2,2,1,1)

		self.sifre_yazi = Gtk.Label()
		self.attach(self.sifre_yazi,0,3,1,2)
		self.sifre_1_entry = Gtk.Entry()
		self.sifre_1_entry.set_visibility(False)
		self.sifre_1_entry.connect("changed", self.sifre_entry_degisti)
		self.attach(self.sifre_1_entry,1,3,1,1)
		self.sifre_2_entry = Gtk.Entry()
		self.sifre_2_entry.set_visibility(False)
		self.sifre_2_entry.connect("changed", self.sifre_entry_degisti)
		self.attach(self.sifre_2_entry,1,4,1,1)
		self.sifre_bilgi = Gtk.Label()
		self.sifre_bilgi.set_max_width_chars(25)
		self.sifre_bilgi.set_line_wrap(True)
		self.sifre_bilgi.set_use_markup(True)
		self.sifre_bilgi.override_color(Gtk.StateFlags.NORMAL, self.kirmizi)
		self.attach(self.sifre_bilgi,2,3,1,2)

		#self.oto_giris_yazi = Gtk.CheckButton()
		#self.attach(self.oto_giris_yazi,0,5,2,1)
		#self.oto_giris_yazi.connect("clicked", self.oto_giris_degisti)

		self.yon_kul_ayni_yazi = Gtk.CheckButton()
		self.yon_kul_ayni_yazi.set_active(True)
		self.attach(self.yon_kul_ayni_yazi,0,6,2,1)
		self.yon_kul_ayni_yazi.connect("clicked", self.yon_kul_ayni_yazi_degisti)

		self.yon_sifre_yazi = Gtk.Label()
		self.attach(self.yon_sifre_yazi,0,7,1,2)
		self.yon_sifre_1_entry = Gtk.Entry()
		self.yon_sifre_1_entry.set_visibility(False)
		self.yon_sifre_1_entry.connect("changed", self.yon_sifre_entry_degisti)
		self.attach(self.yon_sifre_1_entry,1,7,1,1)
		self.yon_sifre_2_entry = Gtk.Entry()
		self.yon_sifre_2_entry.set_visibility(False)
		self.yon_sifre_2_entry.connect("changed", self.yon_sifre_entry_degisti)
		self.attach(self.yon_sifre_2_entry,1,8,1,1)
		self.yon_sifre_bilgi = Gtk.Label()
		self.yon_sifre_bilgi.set_max_width_chars(25)
		self.yon_sifre_bilgi.set_line_wrap(True)
		self.yon_sifre_bilgi.set_use_markup(True)
		self.yon_sifre_bilgi.override_color(Gtk.StateFlags.NORMAL, self.kirmizi)
		self.attach(self.yon_sifre_bilgi,2,7,1,2)


	def kul_entry_degisti(self, widget):
		if self.kul_entry.get_text().isalnum() and len(self.kul_entry.get_text()) > 3:
			self.kul_bilgi.override_color(Gtk.StateFlags.NORMAL, self.yesil)
			self.ebeveyn.milis_ayarlari["kullanici_adi"] = self.kul_entry.get_text()
			self.kontroller[0] = True
		else:
			self.kontroller[0] = False
			self.kul_bilgi.override_color(Gtk.StateFlags.NORMAL, self.kirmizi)

		self.gir_entry.set_text(self.kul_entry.get_text())
		self.bil_entry.set_text(self.kul_entry.get_text()+"-makine")

	def gir_entry_degisti(self,widget):
		if self.gir_entry.get_text().replace("-","").isalnum() and len(self.gir_entry.get_text()) > 3:
			self.gir_bilgi.override_color(Gtk.StateFlags.NORMAL, self.yesil)
			self.ebeveyn.milis_ayarlari["giris_adi"] = self.gir_entry.get_text()
			self.kontroller[1] = True
		else:
			self.kontroller[1] = False
			self.gir_bilgi.override_color(Gtk.StateFlags.NORMAL, self.kirmizi)
		self.kontrol()

	def bil_entry_degisti(self,widget):
		if self.bil_entry.get_text().replace("-","").isalnum() and len(self.bil_entry.get_text()) > 3:
			self.bil_bilgi.override_color(Gtk.StateFlags.NORMAL, self.yesil)
			self.ebeveyn.milis_ayarlari["bilgisayar_adi"] = self.bil_entry.get_text()
			self.kontroller[2] = True
		else:
			self.kontroller[2] = False
			self.bil_bilgi.override_color(Gtk.StateFlags.NORMAL, self.kirmizi)
		self.kontrol()

	def sifre_entry_degisti(self,widget):
		if self.sifre_kontrol(self.sifre_1_entry.get_text(),self.sifre_2_entry.get_text()):
			self.sifre_bilgi.override_color(Gtk.StateFlags.NORMAL, self.yesil)
			self.ebeveyn.milis_ayarlari["kullanici_sifre"] = self.sifre_1_entry.get_text()
			self.kontroller[3] = True
			if self.yon_kul_ayni_yazi.get_active():
				self.kontroller[4] = self.kontroller[3]
				self.ebeveyn.milis_ayarlari["yonetici_sifre"] = self.sifre_1_entry.get_text()
		else:
			self.sifre_bilgi.override_color(Gtk.StateFlags.NORMAL, self.kirmizi)
			self.kontroller[3] = False
		self.kontrol()

	def yon_sifre_entry_degisti(self,widget):
		if self.sifre_kontrol(self.yon_sifre_1_entry.get_text(),self.yon_sifre_2_entry.get_text()):
			self.yon_sifre_bilgi.override_color(Gtk.StateFlags.NORMAL, self.yesil)
			self.ebeveyn.milis_ayarlari["yonetici_sifre"] = self.yon_sifre_1_entry.get_text()
			self.kontroller[4] = True
		else:
			self.yon_sifre_bilgi.override_color(Gtk.StateFlags.NORMAL, self.kirmizi)
			self.kontroller[4] = False
		self.kontrol()

	def kontrol(self):
		kontrol = False
		for i in self.kontroller:
			if i == False:
				kontrol = True
				break
		if kontrol == False:
			self.ebeveyn.ileri_dugme.set_sensitive(True)
			return True
		else:
			self.ebeveyn.ileri_dugme.set_sensitive(False)
			return False

	def sifre_kontrol(self,s_1,s_2):
		if len(s_1) > 5 and s_1 == s_2:
			return True

	def oto_giris_degisti(self,widget):
		if self.oto_giris_yazi.get_active():
			self.ebeveyn.milis_ayarlari["oto_giris"] = True
		else:
			self.ebeveyn.milis_ayarlari["oto_giris"] = False

	def yon_kul_ayni_yazi_degisti(self,widget):
		if self.yon_kul_ayni_yazi.get_active():
			self.yon_kul_ayni_gizle()
			self.ebeveyn.milis_ayarlari["yonetici_sifre"] = self.sifre_1_entry.get_text()
			self.kontroller[4] = self.kontroller[3]
			self.kontrol()
		else:
			self.yon_sifre_yazi.show()
			self.yon_sifre_1_entry.show()
			self.yon_sifre_2_entry.show()
			self.yon_sifre_bilgi.show()
			self.yon_sifre_entry_degisti(None)

	def yon_kul_ayni_gizle(self):
		self.yon_sifre_yazi.hide()
		self.yon_sifre_1_entry.hide()
		self.yon_sifre_2_entry.hide()
		self.yon_sifre_bilgi.hide()

	def dil_ata(self,dil):
		self.baslik = diller.diller[dil]["t18"]
		self.kul_yazi.set_text(diller.diller[dil]["t19"])
		self.gir_yazi.set_text(diller.diller[dil]["t20"])
		self.bil_yazi.set_text(diller.diller[dil]["t21"])
		self.kul_bilgi.set_text(diller.diller[dil]["t22"])
		self.gir_bilgi.set_text(diller.diller[dil]["t23"])
		self.bil_bilgi.set_text(diller.diller[dil]["t23"])
		self.sifre_yazi.set_text(diller.diller[dil]["t24"])
		self.sifre_bilgi.set_text(diller.diller[dil]["t25"])
		#self.oto_giris_yazi.set_label(diller.diller[dil]["t26"])
		self.yon_kul_ayni_yazi.set_label(diller.diller[dil]["t27"])
		self.yon_sifre_yazi.set_text(diller.diller[dil]["t28"])
		self.yon_sifre_bilgi.set_text(diller.diller[dil]["t25"])
