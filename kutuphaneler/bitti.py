from gi.repository import Gtk
from kutuphaneler import diller
import os



class StBitti(Gtk.Grid):
	def __init__(self,ebeveyn):
		Gtk.Window.__init__(self)
		self.ebeveyn = ebeveyn
		self.baslik = "Kurulum Tamamlandi"
		self.ad = "Bitti"

		self.set_column_spacing(5)
		self.set_row_spacing(25)

		icon = Gtk.Image.new_from_file("./resimler/milis_son.svg")
		self.attach(icon,0,0,2,1)
		self.yazi = Gtk.Label()
		self.yazi.set_max_width_chars(70)
		self.yazi.set_line_wrap(True)
		self.yazi.set_justify(Gtk.Justification.LEFT)
		self.attach(self.yazi,0,1,2,1)

		self.deneme_devam = Gtk.Button()
		self.deneme_devam.connect("clicked",self.deneme_basildi)
		self.attach(self.deneme_devam,0,2,1,1)

		self.yeniden_baslat = Gtk.Button()
		self.yeniden_baslat.connect("clicked",self.yeniden_basildi)
		self.attach(self.yeniden_baslat,1,2,1,1)


	def deneme_basildi(self,widget):
		self.ebeveyn.destroy()


	def yeniden_basildi(self,widget):
		os.system("reboot")


	def dil_ata(self,dil):
		self.baslik = diller.diller[dil]["t66"]
		self.yazi.set_text(diller.diller[dil]["t74"])
		self.deneme_devam.set_label(diller.diller[dil]["t76"])
		self.yeniden_baslat.set_label(diller.diller[dil]["t75"])