from gi.repository import Gtk, Gdk, GdkPixbuf
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
		self.ayarli_diskler = {}

		#self.bilgi_label = Gtk.Label()
		#self.bilgi_label.set_max_width_chars(70)
		#self.bilgi_label.set_line_wrap(True)
		#self.bilgi_label.set_use_markup(True)
		#self.attach(self.bilgi_label,0,0,4,1)

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
		self.set_baseline_row(2)

		self.disk_duzenle = Gtk.Button()
		self.disk_duzenle.connect("clicked", self.disk_duzenle_surec)
		self.disk_duzenle.set_always_show_image(True)
		self.disk_duzenle.set_image(Gtk.Image(stock=Gtk.STOCK_EDIT))
		self.attach(self.disk_duzenle,3,1,1,1)

		self.disk_liste_store = Gtk.ListStore(GdkPixbuf.Pixbuf(),str,str,str,str,str)
		self.disk_liste = Gtk.TreeView(model = self.disk_liste_store)
		self.disk_liste.connect("row-activated",self.disk_liste_tiklandi)

		sutun_icon = Gtk.CellRendererPixbuf()
		sutun_icon.set_fixed_size(32,32)
		self.sutun_icon = Gtk.TreeViewColumn("Simge",sutun_icon, gicon = 0)
		self.disk_liste.append_column(self.sutun_icon)

		sutun_text = Gtk.CellRendererText()
		self.sutun_ad = Gtk.TreeViewColumn("Ad",sutun_text, text = 1)
		self.disk_liste.append_column(self.sutun_ad)

		sutun_text = Gtk.CellRendererText()
		self.sutun_format = Gtk.TreeViewColumn("Format",sutun_text, text = 2)
		self.disk_liste.append_column(self.sutun_format)

		sutun_text = Gtk.CellRendererText()
		self.sutun_boyut = Gtk.TreeViewColumn("Boyut",sutun_text, text = 3)
		self.disk_liste.append_column(self.sutun_boyut)

		sutun_text = Gtk.CellRendererText()
		self.sutun_kullanim = Gtk.TreeViewColumn("Kullanım",sutun_text, text = 4)
		self.disk_liste.append_column(self.sutun_kullanim)

		sutun_text = Gtk.CellRendererText()
		self.sutun_bayrak = Gtk.TreeViewColumn("Bayraklar",sutun_text, text = 5)
		self.disk_liste.append_column(self.sutun_bayrak)

		scroll = Gtk.ScrolledWindow()
		scroll.set_min_content_width(630)
		scroll.set_min_content_height(250)
		scroll.set_policy(Gtk.PolicyType.AUTOMATIC,Gtk.PolicyType.AUTOMATIC)
		scroll.add(self.disk_liste)

		self.attach(scroll,0,2,4,1)

		self.grub_kur_radio = Gtk.RadioButton.new_with_label_from_widget(None,"")
		self.grub_kur_radio.connect("toggled", self.grub_kur_degisti, "kur")
		self.attach(self.grub_kur_radio,0,3,4,1)
		self.grub_kurma_radio = Gtk.RadioButton.new_with_label_from_widget(self.grub_kur_radio,"")
		self.grub_kurma_radio.connect("toggled", self.grub_kur_degisti, "kurma")
		self.attach(self.grub_kurma_radio,0,4,4,1)

		self.disk_doldur(None)

	def disk_liste_tiklandi(self,widget,path,coloumn):
		satir = self.disk_liste_store[path]
		print(satir)


	def disk_duzenle_surec(self,widget):
		surec = subprocess.Popen(['gparted'])
		surec.wait()
		self.disk_doldur(None)

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
		disk = self.diskler_combo.get_active_text()
		if disk != None:
			disk = disk.split(" | ")[0]
			self.disk_liste_store.clear()
			sayac = 0
			for bolum in self.diskler_liste[disk]["bölüm"]:
				if sayac > 9:
					icon_name = str(sayac)[-1]
				else:
					icon_name = str(sayac)
				icon_name = "./resimler/"+icon_name + ".svg"
				icon = GdkPixbuf.Pixbuf.new_from_file(icon_name)
				self.disk_liste_store.append([icon,bolum["yol"],bolum["tip"],bolum["boyut"],"",bolum["bayraklar"]])
				sayac += 1
			

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
		#self.bilgi_label.set_markup(diller.diller[dil]["t30"])
		self.diskler_yazi.set_text(diller.diller[dil]["t31"])
		self.disk_yenile.set_label(diller.diller[dil]["t32"])
		self.menu_text_sistem = diller.diller[dil]["t33"]
		self.menu_text_takas = diller.diller[dil]["t34"]
		self.menu_text_uefi = diller.diller[dil]["t35"]
		self.disk_duzenle.set_label(diller.diller[dil]["t36"])
		self.grub_kur_radio.set_label(diller.diller[dil]["t37"])
		self.grub_kurma_radio.set_label(diller.diller[dil]["t38"])
		self.sutun_icon.set_title(diller.diller[dil]["t67"])
		self.sutun_ad.set_title(diller.diller[dil]["t68"])
		self.sutun_format.set_title(diller.diller[dil]["t69"])
		self.sutun_boyut.set_title(diller.diller[dil]["t70"])
		self.sutun_kullanim.set_title(diller.diller[dil]["t71"])
		self.sutun_bayrak.set_title(diller.diller[dil]["t72"])