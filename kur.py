import gi
gi.require_version('Gtk', '3.0')
from kutuphaneler import diller, klavyeler, hosgeldiniz, klavye, konum, kullanici, disk, bilgi, kurulum, bitti
#gi.require_version('GtkSource', '3.0')

from gi.repository import Gtk


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
		self.stack_liste = [hosgeldiniz.StHosgeldiniz(self),klavye.StKlavye(self),konum.StKonum(self),kullanici.StKullanici(self),disk.StDisk(self),bilgi.StBilgi(self),kurulum.StKurulum(self),bitti.StBitti(self)]
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
		elif self.stack_secili == 5:
			self.stack_liste[self.stack_secili].dil_ata(self.milis_ayarlari["dil"])
		elif self.stack_secili == 7:
			self.ileri_dugme.set_sensitive(False)
			self.geri_dugme.set_sensitive(False)


	def geri_basildi(self,widget):
		self.stack_secili -= 1
		self.baslik_ekle(self.stack_liste[self.stack_secili])
		self.ileri_dugme.set_sensitive(True)
		if self.stack_secili == 0:
			self.geri_dugme.set_sensitive(False)

	def baslik_ekle(self,stack):
		if self.stack_secili == 6:
			baslik = diller.diller[self.milis_ayarlari["dil"]]["t73"]
			soru = Gtk.MessageDialog(self,0,Gtk.MessageType.QUESTION, Gtk.ButtonsType.OK_CANCEL,baslik)
			soru.set_title(diller.diller[self.milis_ayarlari["dil"]]["t73"])
			soru.format_secondary_text(diller.diller[self.milis_ayarlari["dil"]]["t45"])
			cevap = soru.run()
			if cevap == Gtk.ResponseType.OK:
				soru.destroy()
				self.hb.props.title = stack.baslik
				self.stack.set_visible_child_name(stack.ad)
				#self.stack.kurulum_baslat(self)
				yazilacak = ""
				keymap = self.milis_ayarlari['klavye_duzen'][0] + self.milis_ayarlari['klavye_varyant'][0]
				yazilacak += "KEYMAP {}\n".format(keymap)
				yazilacak += "HOSTNAME {}\n".format(self.milis_ayarlari['bilgisayar_adi'])
				if self.milis_ayarlari['dil'] == "Türkçe":
					yazilacak += "LOCALE tr_TR.utf8\n"
				elif self.milis_ayarlari['dil'] == "English":
					yazilacak += "LOCALE en_US.utf8\n"
				zone = self.milis_ayarlari['konum']
				if zone == 'Europe/Istanbul':
					zone = 'Turkey'
				yazilacak += "TIMEZONE {}\n".format(zone)
				yazilacak += "ROOTPASSWORD {}\n".format(self.milis_ayarlari['yonetici_sifre'])
				yazilacak += "USERLOGIN {}\n".format(self.milis_ayarlari['giris_adi'])
				yazilacak += "USERNAME {}\n".format(self.milis_ayarlari['kullanici_adi'])
				yazilacak += "USERPASSWORD {}\n".format(self.milis_ayarlari['kullanici_sifre'])
				yazilacak += "USERGROUPS tty,floppy,disk,lp,audio,video,cdrom,adm,wheel,users,pulse-access\n"
				yazilacak += "BOOTLOADER {}\n".format(self.milis_ayarlari['grub_kur'])
				yazilacak += "TEXTCONSOLE 0\n"
				if self.milis_ayarlari["sistem_disk"] != "":
					yazilacak += "MOUNTPOINT {}\n".format(self.milis_ayarlari["sistem_disk"])
				if self.milis_ayarlari["takas_disk"] != "":
					yazilacak += "MOUNTPOINT {}\n".format(self.milis_ayarlari["takas_disk"])
				if self.milis_ayarlari["uefi_disk"] != "":
					yazilacak += "MOUNTPOINT {}\n".format(self.milis_ayarlari["uefi_disk"])
				f = open("/tmp/milis_kur_ayar.txt","w")
				f.write(yazilacak)
				f.close()
				self.ileri_dugme.set_sensitive(False)
				self.geri_dugme.set_sensitive(False)
				stack.terminal.komutlar.append("milis-kur2 /tmp/milis_kur_ayar.txt text")
				stack.terminal.komut_calistir()
			else:
				self.stack_secili = 5
				soru.destroy()
		else:
			self.hb.props.title = stack.baslik
			self.stack.set_visible_child_name(stack.ad)

if __name__ == '__main__':
	pen = MerkezPencere()
	pen.connect("destroy", Gtk.main_quit)
	pen.show_all()
	Gtk.main()
