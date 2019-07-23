from gi.repository import Gtk, Gdk
from kutuphaneler import koordinatlar, diller
import cairo, os


class StKonum(Gtk.Grid):
	def __init__(self,ebeveyn):
		Gtk.Window.__init__(self)
		self.ebeveyn = ebeveyn
		self.baslik = "Konum Ayarları"
		self.ad = "Konum"
		self.set_row_spacing(5)
		self.resim_secilen = ["",""]

		self.resim = Gtk.DrawingArea()
		self.resim.set_size_request (630, 315)
		self.resim.connect("draw", self.expose)
		self.resim.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
		self.resim.connect("button_press_event", self.resim_tiklandi)
		self.attach(self.resim,0,0,4,1)

		self.bolge_yazi = Gtk.Label()
		self.attach(self.bolge_yazi,0,1,1,1)
		self.bolge_combo = Gtk.ComboBoxText()
		self.attach(self.bolge_combo,1,1,1,1)
		self.sehir_yazi = Gtk.Label()
		self.attach(self.sehir_yazi,2,1,1,1)
		self.sehir_combo = Gtk.ComboBoxText()
		self.attach(self.sehir_combo,3,1,1,1)

		self.koordinat_hazirla()
		self.bolge_combo.connect("changed", self.bolge_combo_degisti)
		self.sehir_combo.connect("changed", self.sehir_combo_degisti)
		self.bolge_combo_degisti(None)

	def resim_tiklandi(self,widget,pos):
		deger = 2000
		koordinat = False
		for i in list(self.koordinat_pixelleri.keys()):
			deger_ = (i[0]-pos.x)**2 + (i[1]-pos.y)**2
			if deger_ < deger:
				deger = deger_
				koordinat = (i[0],i[1])
		if koordinat:
			bolge = self.koordinat_pixelleri[koordinat].split("/")
			sehir = "/".join(bolge[1:])
			self.resim_secilen = [bolge[0],sehir]
			self.bolge_combo_doldur()


	def koordinat_hazirla(self):
		self.koordinat_pixelleri = {}
		for zone, koordinat in koordinatlar.koordinatlar.items():
			pos = self.koordinat_pixel_tespiti(koordinat[1], koordinat[0], zone)
			self.koordinat_pixelleri[pos[0]] = pos[1]

		self.duzenli_ulke = {}
		for i in self.koordinat_pixelleri.items():
			degistir = i[1].split("/")
			if len(degistir) == 2:
				varmi = self.duzenli_ulke.get(degistir[0], "yok")
				if varmi == "yok":
					self.duzenli_ulke[degistir[0]] = [degistir[1]]
				else:
					self.duzenli_ulke[degistir[0]].append(degistir[1])
			elif len(degistir) == 3:
				varmi = self.duzenli_ulke.get(degistir[0], "yok")
				if varmi == "yok":
					self.duzenli_ulke[degistir[0]] = [degistir[1]+"/"+degistir[2]]
				else:
					self.duzenli_ulke[degistir[0]].append(degistir[1]+"/"+degistir[2])
		self.bolge_combo_doldur()

	def koordinat_pixel_tespiti(self, longitude, latitude, time_zone=""):
		width = 630
		height = 315
		x = (width/2)*(longitude/180)+(width/2)
		y = (height/2)-((height/2)*(latitude/90))
		return ((x, y), time_zone)

	def bolge_combo_doldur(self):
		sayac = 0
		kontrol = True
		for sehir in list(self.duzenli_ulke.keys()):
			self.bolge_combo.append_text(sehir)
			if self.resim_secilen[0] == sehir:
				if self.bolge_combo.get_active_text() == sehir:
					self.bolge_combo_degisti(None)
				else:
					self.bolge_combo.set_active(sayac)
				kontrol = False
			sayac += 1
		if self.resim_secilen[0] == "" and kontrol:
			self.bolge_combo.set_active(0)

	def sehir_combo_degisti(self,widget):
		if self.sehir_combo.get_active_text() != None:
			bolge_adi = self.bolge_combo.get_active_text()+"/"+self.sehir_combo.get_active_text()
			self.ebeveyn.milis_ayarlari["konum"] = bolge_adi
			self.resim.queue_draw()

	def bolge_combo_degisti(self, widget):
		self.sehir_combo.remove_all()
		sayac = 0
		var = False
		for ulke in self.duzenli_ulke[self.bolge_combo.get_active_text()]:
			self.sehir_combo.append_text(ulke)
			if ulke == self.resim_secilen[1]:
				self.sehir_combo.set_active(sayac)
				var = True
			elif ulke == "Istanbul" and self.resim_secilen[1] == "":
				self.sehir_combo.set_active(sayac)
				var = True
			sayac += 1
		if var == False:
			self.sehir_combo.set_active(0)
		self.resim_secilen = ["",""]

	def pin_hesapla(self):
		pos = koordinatlar.koordinatlar[self.ebeveyn.milis_ayarlari["konum"]]
		koordinat = self.koordinat_pixel_tespiti(pos[-1], pos[0])
		x = koordinat[0][0] - 5
		y = koordinat[0][1] - 5
		return (x,y)

	def dil_ata(self,dil):
		self.baslik = diller.diller[dil]["t15"]
		self.bolge_yazi.set_text(diller.diller[dil]["t16"])
		self.sehir_yazi.set_text(diller.diller[dil]["t17"])

	def expose(self, widget, cr):
		klavye = cairo.ImageSurface.create_from_png("./resimler/harita.png")
		cr.set_source_surface(klavye,0,0)
		cr.paint()
		if self.ebeveyn.milis_ayarlari["konum"]:
			pin = cairo.ImageSurface.create_from_png("./resimler/pin.png")
			pin_konum = self.pin_hesapla()
			cr.set_source_surface(pin,pin_konum[0],pin_konum[1])
			cr.paint()
