from gi.repository import Gtk
from kutuphaneler import diller, klavyeler
import cairo, os, subprocess

class StKlavye(Gtk.Grid):
	def __init__(self,ebeveyn):
		Gtk.Window.__init__(self)
		self.ebeveyn = ebeveyn
		self.baslik = "Klavye Ayarları"
		self.ad = "Klavye"
		self.set_row_spacing(20)

		self.resim = Gtk.DrawingArea()
		self.resim.set_size_request (630, 200)
		self.resim.connect("draw", self.expose)
		self.attach(self.resim,0,0,4,1)

		self.model_yazi = Gtk.Label()
		self.attach(self.model_yazi,0,1,1,1)
		self.model_combo = Gtk.ComboBoxText()
		self.attach(self.model_combo,1,1,3,1)
		model = list(klavyeler.modeller.keys())
		model.sort()
		sayac = 0
		for mod_ in model:
			self.model_combo.append_text(klavyeler.modeller[mod_])
			if mod_ == "pc105":
				self.model_combo.set_active(sayac)
				self.ebeveyn.milis_ayarlari["klavye_model"] = mod_, klavyeler.modeller[mod_]
			sayac += 1

		self.ulke_yazi = Gtk.Label()
		self.attach(self.ulke_yazi,0,2,1,1)
		self.ulke_combo = Gtk.ComboBoxText()

		self.attach(self.ulke_combo,1,2,1,1)
		self.duzenler_doldur()

		self.tur_yazi = Gtk.Label()
		self.attach(self.tur_yazi,2,2,1,1)
		self.tur_combo = Gtk.ComboBoxText()
		self.attach(self.tur_combo,3,2,1,1)
		self.tur_combo.append_text("Default")
		for k in klavyeler.varyantlar[self.ebeveyn.milis_ayarlari["klavye_duzen"][0]]:
			self.tur_combo.append_text(list(k.values())[0])
		self.tur_combo.set_active(0)

		self.text_entry = Gtk.Entry()
		self.attach(self.text_entry,0,3,4,1)

		self.model_combo.connect("changed", self.klavye_modeli_secildi)
		self.ulke_combo.connect("changed", self.ulke_secildi)
		self.tur_combo.connect("changed", self.tur_secildi)

		self.cizim_baslangic(self.ebeveyn.milis_ayarlari["klavye_model"][0],
							self.ebeveyn.milis_ayarlari["klavye_duzen"][0],
							self.ebeveyn.milis_ayarlari["klavye_varyant"][0])


	def klavye_modeli_secildi(self,widget):
		model = list(klavyeler.modeller.keys())
		for mod_ in model:
			if klavyeler.modeller[mod_] == self.model_combo.get_active_text():
				self.ebeveyn.milis_ayarlari["klavye_model"] = mod_, klavyeler.modeller[mod_]
		self.cizim_baslangic(self.ebeveyn.milis_ayarlari["klavye_model"][0],
							self.ebeveyn.milis_ayarlari["klavye_duzen"][0],
							self.ebeveyn.milis_ayarlari["klavye_varyant"][0])


	def ulke_secildi(self,widget):
		for duzen in klavyeler.duzenler.keys():
			if klavyeler.duzenler[duzen] == self.ulke_combo.get_active_text():
				self.ebeveyn.milis_ayarlari["klavye_duzen"] = duzen, self.ulke_combo.get_active_text()

		self.tur_combo.remove_all()
		self.ebeveyn.milis_ayarlari["klavye_varyant"] = ("","")
		self.tur_combo.append_text("Default")
		try:
			for k in klavyeler.varyantlar[self.ebeveyn.milis_ayarlari["klavye_duzen"][0]]:
				self.tur_combo.append_text(list(k.values())[0])
		except:
			pass
		self.tur_combo.set_active(0)
		os.system("setxkbmap -layout {} -variant \"\"".format(self.ebeveyn.milis_ayarlari["klavye_duzen"][0]))

	def tur_secildi(self,widget):
		if self.tur_combo.get_active_text() == "Default":
			os.system("setxkbmap -variant \"\"")
			self.ebeveyn.milis_ayarlari["klavye_varyant"] = ("","")
			self.cizim_baslangic(self.ebeveyn.milis_ayarlari["klavye_model"][0],
								self.ebeveyn.milis_ayarlari["klavye_duzen"][0],
								self.ebeveyn.milis_ayarlari["klavye_varyant"][0])
		else:
			try:
				for k in klavyeler.varyantlar[self.ebeveyn.milis_ayarlari["klavye_duzen"][0]]:
					if list(k.values())[0] == self.tur_combo.get_active_text():
						self.ebeveyn.milis_ayarlari["klavye_varyant"] = list(k.keys())[0], list(k.values())[0]
						os.system("setxkbmap -layout {} -variant {}".format(self.ebeveyn.milis_ayarlari["klavye_duzen"][0],
																			self.ebeveyn.milis_ayarlari["klavye_varyant"][0]))
						self.cizim_baslangic(self.ebeveyn.milis_ayarlari["klavye_model"][0],
											self.ebeveyn.milis_ayarlari["klavye_duzen"][0],
											self.ebeveyn.milis_ayarlari["klavye_varyant"][0])
			except:
				pass


	def duzenler_doldur(self):
		self.ulke_combo.remove_all()
		keys = list(klavyeler.duzenler.keys())
		keys.sort()
		sayac = 0
		for key_ in keys:
			self.ulke_combo.append_text(klavyeler.duzenler[key_])
			if klavyeler.duzenler[key_] == "English (US)" and self.ebeveyn.milis_ayarlari["dil"] == "English":
				self.ulke_combo.set_active(sayac)
				self.ebeveyn.milis_ayarlari["klavye_duzen"] = "us", klavyeler.duzenler["us"]
			elif klavyeler.duzenler[key_] == "Turkish" and self.ebeveyn.milis_ayarlari["dil"] == "Türkçe":
				self.ulke_combo.set_active(sayac)
				self.ebeveyn.milis_ayarlari["klavye_duzen"] = "tr", klavyeler.duzenler["tr"]
			sayac += 1

	def dil_ata(self,dil):
		self.baslik = diller.diller[dil]["t11"]
		self.model_yazi.set_text(diller.diller[dil]["t12"])
		self.ulke_yazi.set_text(diller.diller[dil]["t13"])
		self.tur_yazi.set_text(diller.diller[dil]["t14"])

	def expose(self, widget, cr):
		klavye = cairo.ImageSurface.create_from_png("./resimler/klavye.png")
		cr.set_source_surface(klavye,0,0)
		cr.paint()
		koordinat_listesi = ((10, 20), (65, 65), (85, 105), (60, 150))
		sayac = 0
		if self.ebeveyn.milis_ayarlari["klavye_model"][0] in klavyeler.klavye_modeli.keys():
			for key_list in klavyeler.klavye_modeli[self.ebeveyn.milis_ayarlari["klavye_model"][0]]:
				coordinat = koordinat_listesi[sayac]
				sayac += 1
				for num, key in enumerate(key_list):
					try:
						cr.set_source_rgb(204, 255, 0)
						cr.select_font_face("Noto Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
						cr.set_font_size(10)
						cr.move_to(coordinat[0]+(42*num), coordinat[1])
						cr.show_text(self.tus_yerlesimi[key][1])

						cr.set_source_rgb(255, 255, 255)
						cr.set_font_size(12)
						cr.move_to(coordinat[0]+10+(42*num), coordinat[1]+15)
						cr.show_text(self.tus_yerlesimi[key][0])

					except KeyError as err:
						print(key)


	def cizim_baslangic(self,model, layout, variant):
		if model in klavyeler.klavye_modeli.keys():
			self.tus_yerlesimi = self.unicodeToString(model, layout, variant)
			if self.tus_yerlesimi:
				self.resim.queue_draw()

	def unicodeToString(self, model, layout, variant=""):
		try:
			keycodes = {}
			tus_yerlesimi_command = subprocess.Popen(["./betikler/ckbcomp", "-model", model, "-layout", layout, "-variant", variant],
													stdout=subprocess.PIPE)
			ciktilar = tus_yerlesimi_command.stdout.read()
			for cikti in ciktilar.decode("utf-8").split("\n"):
				if cikti.startswith("keycode") and cikti.count("="):
					cikti = cikti.split()
					if cikti[3].startswith("U+") or cikti[3].startswith("+U"):
						first = bytes("\\u" + cikti[3][2:].replace("+", ""), "ascii").decode("unicode-escape")
						second = bytes("\\u" + cikti[4][2:].replace("+", ""), "ascii").decode("unicode-escape")
						keycodes[int(cikti[1])] = [first, second]
			return keycodes
		except:
			return False

