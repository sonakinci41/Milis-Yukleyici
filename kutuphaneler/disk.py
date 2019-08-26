from gi.repository import Gtk, Gdk
from kutuphaneler import diller
import parted, random

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
		self.bilgi_label.set_max_width_chars(90)
		self.bilgi_label.set_line_wrap(True)
		self.bilgi_label.set_use_markup(True)
		self.attach(self.bilgi_label,0,0,3,1)

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

		self.disk_resim = Gtk.DrawingArea()
		self.attach(self.disk_resim,0,2,3,1)
		self.disk_resim.set_size_request(630, 100)
		self.disk_resim.connect("draw", self.expose)
		self.disk_resim.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
		self.disk_resim.connect("button_press_event", self.resim_tiklandi)

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
				yazi_konum = ((x_kor + x_kor + x_genislik) / 2 ) - 10
				self.disk_gorunumu[bolum["yol"]] = {"x_genislik":x_genislik,"x_kor":x_kor,"boyut":bolum["boyut"],"yazi_konum":yazi_konum,"secim":"yok"}
				x_kor += x_genislik
			self.disk_gecici["degisti"] = True

		for bolum in self.disk_gorunumu.keys():
			cr.set_line_width(3)
			if self.disk_gecici["tiklanan"] == bolum:
				cr.set_source_rgb(204, 255, 0)
			else:
				cr.set_source_rgb(1,1,1)
			cr.rectangle(self.disk_gorunumu[bolum]["x_kor"],10,self.disk_gorunumu[bolum]["x_genislik"],80)
			cr.stroke()
			cr.move_to(self.disk_gorunumu[bolum]["yazi_konum"],45)
			cr.show_text(bolum)
			cr.move_to(self.disk_gorunumu[bolum]["yazi_konum"],65)
			cr.show_text("   "+self.disk_gorunumu[bolum]["boyut"])
			cr.stroke()

	def menu_olustur(self,pos):
		menu = Gtk.Menu()
		sistem = Gtk.MenuItem('Sistem Diski Yap')
		takas = Gtk.MenuItem('Takas Diski Yap')
		uefi = Gtk.MenuItem('UEFI Diski Yap')
		menu.append(sistem)
		menu.append(takas)
		menu.append(uefi)
		menu.popup(None, None, None, None, 0, Gtk.get_current_event_time())
		menu.show_all()

	def resim_tiklandi(self,widget,pos):
		self.menu_olustur(pos)
		for disk in self.disk_gorunumu.keys():
			x_kor = self.disk_gorunumu[disk]["x_kor"]
			x_genislik = self.disk_gorunumu[disk]["x_genislik"]
			if x_kor <= pos.x <= x_kor+x_genislik:
				self.disk_gecici["tiklanan"] = disk
		self.disk_resim.queue_draw()

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
		self.disk_gecici["degisti"] = False
		self.disk_gecici["tiklanan"] = ""
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

	def dil_ata(self,dil):
		self.baslik = diller.diller[dil]["t29"]
		self.bilgi_label.set_markup(diller.diller[dil]["t30"])
		self.diskler_yazi.set_text(diller.diller[dil]["t31"])
		self.disk_yenile.set_label(diller.diller[dil]["t32"])
