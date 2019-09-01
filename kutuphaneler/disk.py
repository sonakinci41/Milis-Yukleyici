from gi.repository import Gtk, Gdk
from kutuphaneler import diller
import parted, subprocess

class StDisk(Gtk.Grid):
	def __init__(self,ebeveyn):
		Gtk.Window.__init__(self)
		self.ebeveyn = ebeveyn
		self.baslik = "Disk Ayarları"
		self.ad = "Disk"
		self.set_column_spacing(10)
		self.set_row_spacing(10)
		self.diskler_liste = {}
		self.disk_gecici = {"degisti":False}

		self.bilgi_label = Gtk.Label()
		self.bilgi_label.set_max_width_chars(70)
		self.bilgi_label.set_line_wrap(True)
		self.bilgi_label.set_use_markup(True)
		self.attach(self.bilgi_label,0,0,4,1)

		self.diskler_yazi = Gtk.Label()
		self.attach(self.diskler_yazi,0,1,1,1)

		self.diskler_combo = Gtk.ComboBoxText()
		self.diskler_combo.connect("changed", self.disk_secildi)
		self.attach(self.diskler_combo,1,1,1,1)

		self.disk_yenile = Gtk.Button()
		self.disk_yenile.connect("clicked", self.disk_doldur)
		self.disk_yenile.set_always_show_image(True)
		self.disk_yenile.set_image(Gtk.Image(stock=Gtk.STOCK_REFRESH))
		self.attach(self.disk_yenile,2,1,1,1)

		self.disk_duzenle = Gtk.Button()
		self.disk_duzenle.connect("clicked", self.disk_duzenle_surec)
		self.disk_duzenle.set_always_show_image(True)
		self.disk_duzenle.set_image(Gtk.Image(stock=Gtk.STOCK_EDIT))
		self.attach(self.disk_duzenle,3,1,1,1)

		self.disk_resim = Gtk.DrawingArea()
		self.attach(self.disk_resim,0,2,4,1)
		self.disk_resim.set_size_request(630, 100)
		self.disk_resim.connect("draw", self.expose)
		self.disk_resim.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
		self.disk_resim.connect("button_press_event", self.resim_tiklandi)

		self.grub_kur_radio = Gtk.RadioButton.new_with_label_from_widget(None,"")
		self.grub_kur_radio.connect("toggled", self.grub_kur_degisti, "kur")
		self.attach(self.grub_kur_radio,0,3,4,1)
		self.grub_kurma_radio = Gtk.RadioButton.new_with_label_from_widget(self.grub_kur_radio,"")
		self.grub_kurma_radio.connect("toggled", self.grub_kur_degisti, "kurma")
		self.attach(self.grub_kurma_radio,0,4,4,1)

		self.disk_doldur(None)

	def expose(self, widget, cr):
		# 10 10 dan başlayacak aralık 610 a 80 hesapları ona göre yapılacak
		cr.set_source_rgb(0.1,0.1,0.1)
		cr.rectangle(0,0,630,100)
		cr.fill()
		x_kor = 10
		if not self.disk_gecici["degisti"]:
			self.disk_gorunumu = {}
			for bolum in self.disk_gecici["secilen"]["bölüm"]:
				x_genislik = int(610*(float(bolum["boyut"])/float(self.disk_gecici["secilen"]["tum_boyut"])))
				yazi_konum = ((x_kor + x_kor + x_genislik) / 2 ) - 25
				self.disk_gorunumu[bolum["yol"]] = {"x_genislik":x_genislik,"x_kor":x_kor,"boyut":bolum["boyut"],"yazi_konum":yazi_konum}
				x_kor += x_genislik
			self.disk_gecici["degisti"] = True

		for bolum in self.disk_gorunumu.keys():
			ozel = False
			if bolum == self.ebeveyn.milis_ayarlari["sistem_disk"]:
				cr.set_source_rgb(0.5, 1, 0.5)
				cr.rectangle(self.disk_gorunumu[bolum]["x_kor"],10,self.disk_gorunumu[bolum]["x_genislik"],80)
				cr.fill()
				ozel = True
			if bolum == self.ebeveyn.milis_ayarlari["takas_disk"]:
				cr.set_source_rgb(1, 0.5, 0.5)
				cr.rectangle(self.disk_gorunumu[bolum]["x_kor"],10,self.disk_gorunumu[bolum]["x_genislik"],80)
				cr.fill()
				ozel = True
			if bolum == self.ebeveyn.milis_ayarlari["uefi_disk"]:
				cr.set_source_rgb(0.5, 0.5, 1)
				cr.rectangle(self.disk_gorunumu[bolum]["x_kor"],10,self.disk_gorunumu[bolum]["x_genislik"],80)
				cr.fill()
				ozel = True
			cr.set_line_width(3)
			if self.disk_gecici["tiklanan"] == bolum:
				cr.set_source_rgb(0.9, 1, 0)
			else:
				cr.set_source_rgb(1,1,1)
			cr.set_font_size(12)
			cr.rectangle(self.disk_gorunumu[bolum]["x_kor"],10,self.disk_gorunumu[bolum]["x_genislik"],80)
			cr.stroke()

			if ozel:
				cr.set_source_rgb(0.1,0.1,0.1)
			else:
				cr.set_source_rgb(1,1,1)
			cr.move_to(self.disk_gorunumu[bolum]["yazi_konum"],45)
			cr.show_text(bolum)
			cr.move_to(self.disk_gorunumu[bolum]["yazi_konum"],65)
			cr.show_text("   "+self.disk_gorunumu[bolum]["boyut"])
			cr.stroke()

	def menu_olustur(self,pos):
		menu = Gtk.Menu()
		if self.ebeveyn.milis_ayarlari["sistem_disk"] != self.disk_gecici["tiklanan"] and self.ebeveyn.milis_ayarlari["takas_disk"] != self.disk_gecici["tiklanan"] and self.ebeveyn.milis_ayarlari["uefi_disk"] != self.disk_gecici["tiklanan"]:
			if self.ebeveyn.milis_ayarlari["sistem_disk"] == "":
				sistem = Gtk.MenuItem(self.menu_text_sistem)
				sistem.connect("activate", self.sistem_diski_secildi)
				menu.append(sistem)
			if self.ebeveyn.milis_ayarlari["takas_disk"] == "":
				takas = Gtk.MenuItem(self.menu_text_takas)
				takas.connect("activate", self.takas_diski_secildi)
				menu.append(takas)
			if self.ebeveyn.milis_ayarlari["uefi_disk"] == "":
				uefi = Gtk.MenuItem('UEFI Bölümü')
				uefi.connect("activate", self.uefi_diski_secildi)
				menu.append(uefi)
			if self.ebeveyn.milis_ayarlari["sistem_disk"] == "" or self.ebeveyn.milis_ayarlari["takas_disk"] == "" or self.ebeveyn.milis_ayarlari["uefi_disk"] == "":
				menu.popup(None, None, None, None, 0, Gtk.get_current_event_time())
				menu.show_all()

	def sistem_diski_secildi(self,widget):
		self.ebeveyn.milis_ayarlari["sistem_disk"] = self.disk_gecici["tiklanan"]
		self.disk_resim.queue_draw()
		self.ebeveyn.ileri_dugme.set_sensitive(True)

	def takas_diski_secildi(self,widget):
		self.ebeveyn.milis_ayarlari["takas_disk"] = self.disk_gecici["tiklanan"]
		self.disk_resim.queue_draw()

	def uefi_diski_secildi(self,widget):
		self.ebeveyn.milis_ayarlari["uefi_disk"] = self.disk_gecici["tiklanan"]
		self.disk_resim.queue_draw()

	def disk_duzenle_surec(self,widget):
		surec = subprocess.Popen(['gparted'])
		surec.wait()
		self.disk_doldur(None)

	def resim_tiklandi(self,widget,pos):
		for disk in self.disk_gorunumu.keys():
			x_kor = self.disk_gorunumu[disk]["x_kor"]
			x_genislik = self.disk_gorunumu[disk]["x_genislik"]
			if x_kor <= pos.x <= x_kor+x_genislik:
				self.disk_gecici["tiklanan"] = disk
		self.disk_resim.queue_draw()
		self.menu_olustur(pos)

	def disk_doldur(self,widget):
		self.diskler_combo.remove_all()
		self.diskler = parted.getAllDevices()
		for disk in self.diskler:
			try:
				if parted.Disk(disk).type == "msdos" or parted.Disk(disk).type == "gpt":
					self.diskler_liste[disk.path] = {"parted":parted.Disk(disk),"tum_boyut":format(disk.getSize(unit="GB"), '.2f'),"bölüm":[]}
					self.diskler_combo.append_text(disk.path+" | "+disk.model+" | "+format(disk.getSize(unit="GB"), '.2f')+"GB")
			except parted.DiskLabelException:
				disk = parted.freshDisk(disk, "msdos")
				# CDROM Aygıtları için
				try:
					disk.commit()
				except parted.IOException:
					pass
				else:
					disk = disk.device
					self.diskler_liste[disk.path] = {"parted":parted.Disk(disk),"tum_boyut":format(disk.getSize(unit="GB"), '.2f'),"bölüm":[]}
					self.diskler_combo.append_text(disk.path+" | "+disk.model+" | "+format(disk.getSize(unit="GB"), '.2f')+"GB")
			for bolum in parted.Disk(disk).partitions:
				gelen = self.bolumBilgi(bolum)
				if gelen:
					self.diskler_liste[disk.path]["bölüm"].append(gelen)
		self.diskler_combo.set_active(0)

	def disk_secildi(self,widget):
		self.ebeveyn.milis_ayarlari["sistem_disk"] = ""
		self.ebeveyn.milis_ayarlari["takas_disk"] = ""
		self.ebeveyn.milis_ayarlari["uefi_disk"] = ""
		self.disk_gecici["degisti"] = False
		self.disk_gecici["tiklanan"] = ""
		if self.ebeveyn.stack_secili == 4:
			self.ebeveyn.ileri_dugme.set_sensitive(False)
		if self.diskler_combo.get_active_text():
			secilen = self.diskler_combo.get_active_text().split(" | ")[0]
			disk = self.diskler_liste[secilen]
			self.disk_gecici["secilen"] = disk
			self.disk_resim.queue_draw()

	def bolumBilgi(self, bolum):
		bilgi = {}
		bilgi["yol"] = bolum.path
		bilgi["boyut"] = format(bolum.getSize(unit="GB"), '.2f')
		bilgi["tip"] = "Bilinmeyen"
		if bolum.fileSystem:
			if bolum.fileSystem.type.startswith('linux-swap'):
				bilgi["tip"] = "Takas"
			else:
				bilgi["tip"] = bolum.fileSystem.type
		try:
			bilgi["bayraklar"] = bolum.getFlagsAsString()
		except:
			pass
		bilgi["no"] = bolum.number
		bilgi["tur"] = bolum.type
		if bilgi["tip"] == "Bilinmeyen":
			return False
		else:
			return bilgi

	def grub_kur_degisti(self,widget, islem):
		if self.grub_kur_radio.get_active():
			self.ebeveyn.milis_ayarlari["grub_kur"] = True
		elif self.grub_kurma_radio.get_active():
			self.ebeveyn.milis_ayarlari["grub_kur"] = False

	def dil_ata(self,dil):
		self.baslik = diller.diller[dil]["t29"]
		self.bilgi_label.set_markup(diller.diller[dil]["t30"])
		self.diskler_yazi.set_text(diller.diller[dil]["t31"])
		self.disk_yenile.set_label(diller.diller[dil]["t32"])
		self.menu_text_sistem = diller.diller[dil]["t33"]
		self.menu_text_takas = diller.diller[dil]["t34"]
		self.menu_text_uefi = diller.diller[dil]["t35"]
		self.disk_duzenle.set_label(diller.diller[dil]["t36"])
		self.grub_kur_radio.set_label(diller.diller[dil]["t37"])
		self.grub_kurma_radio.set_label(diller.diller[dil]["t38"])
