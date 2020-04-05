from gi.repository import Gtk
from kutuphaneler import diller
import webbrowser

class StHosgeldiniz(Gtk.Grid):
	def __init__(self,ebeveyn):
		Gtk.Window.__init__(self)
		self.ebeveyn = ebeveyn
		self.baslik = "Milis Linux Kurulumuna Hoşgeldiniz"
		self.ad = "Hosgeldin"
		self.set_column_spacing(5)
		self.set_row_spacing(5)

		self.dil_yazi = Gtk.Label()
		self.add(self.dil_yazi)

		self.dil_combo = Gtk.ComboBoxText()
		for dil in diller.diller.keys():
			self.dil_combo.append_text(dil)
		self.dil_combo.set_active(0)
		self.dil_combo.connect("changed", self.dil_degisti)
		self.attach(self.dil_combo,1,0,1,1)

		icon = Gtk.Image.new_from_file("./resimler/milis_yuvarlak.svg")
		self.attach(icon,0,1,2,1)
		self.yazi = Gtk.Label()
		self.yazi.set_max_width_chars(70)
		self.yazi.set_line_wrap(True)
		self.yazi.set_justify(Gtk.Justification.LEFT)
		self.attach(self.yazi,0,2,2,1)

		self.belge_dugme = Gtk.Button()
		self.belge_dugme.set_always_show_image(True)
		belge_resim = Gtk.Image.new_from_file("./resimler/belge.svg")
		self.belge_dugme.set_image(belge_resim)
		self.belge_dugme.connect("clicked",self.belge_tiklandi)
		self.attach(self.belge_dugme,0,3,1,1)

		self.forum_dugme = Gtk.Button()
		self.forum_dugme.set_always_show_image(True)
		forum_resim = Gtk.Image.new_from_file("./resimler/forum.svg")
		self.forum_dugme.set_image(forum_resim)
		self.forum_dugme.connect("clicked",self.forum_tiklandi)
		self.attach(self.forum_dugme,1,3,1,1)

		self.git_dugme = Gtk.Button()
		self.git_dugme.set_always_show_image(True)
		git_resim = Gtk.Image.new_from_file("./resimler/git.svg")
		self.git_dugme.set_image(git_resim)
		self.git_dugme.connect("clicked",self.git_tiklandi)
		self.attach(self.git_dugme,0,4,1,1)

		self.iletisim_dugme = Gtk.Button()
		self.iletisim_dugme.set_always_show_image(True)
		iletisim_resim = Gtk.Image.new_from_file("./resimler/iletisim.svg")
		self.iletisim_dugme.set_image(iletisim_resim)
		self.iletisim_dugme.connect("clicked",self.iletisim_tiklandi)
		self.attach(self.iletisim_dugme,1,4,1,1)

	def dil_ata(self,dil):
		self.yazi.set_text(diller.diller[dil]["t4"])
		self.belge_dugme.set_label(diller.diller[dil]["t5"])
		self.forum_dugme.set_label(diller.diller[dil]["t6"])
		self.git_dugme.set_label(diller.diller[dil]["t7"])
		self.iletisim_dugme.set_label(diller.diller[dil]["t8"])
		self.dil_yazi.set_text(diller.diller[dil]["t9"])
		self.baslik = diller.diller[dil]["t10"]

	def dil_degisti(self,widget):
		self.ebeveyn.dil_ata(self.dil_combo.get_active_text())
		self.ebeveyn.milis_ayarlari["dil"] = self.dil_combo.get_active_text()
		self.ebeveyn.stack_liste[1].duzenler_doldur()

	def belge_tiklandi(self,widget):
		webbrowser.open("https://mls.akdeniz.edu.tr/belgeler/")

	def forum_tiklandi(self,widget):
		webbrowser.open("https://forum.milislinux.org/")

	def git_tiklandi(self,widget):
		webbrowser.open("https://mls.akdeniz.edu.tr/git/")

	def iletisim_tiklandi(self,widget):
		webbrowser.open("https://mls.akdeniz.edu.tr/mm/")
