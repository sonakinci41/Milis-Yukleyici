import gi, os
from gi.repository import Vte, GLib, Gdk, Gio, Gtk
from kutuphaneler import diller

class StKurulum(Gtk.Grid):
	def __init__(self,ebeveyn):
		Gtk.Window.__init__(self)
		self.ebeveyn = ebeveyn
		self.baslik = "Milis Linux Kuruluyor"
		self.ad = "Kurulum"
		self.terminal = Terminal(self)
		scroll = Gtk.ScrolledWindow()
		scroll.set_min_content_width(630)
		scroll.set_min_content_height(350)
		scroll.set_policy(Gtk.PolicyType.AUTOMATIC,Gtk.PolicyType.AUTOMATIC)
		scroll.add(self.terminal)
		self.attach(scroll,0,0,1,1)

	def dil_ata(self,dil):
		self.baslik = diller.diller[dil]["t48"]

class Terminal(Vte.Terminal):
	def __init__(self,ebeveyn):
		Vte.Terminal.__init__(self)
		#Ebeveyndeki değişkenlere ulaşmak için
		self.ebeveyn = ebeveyn
		#Komutları ebeveyn buraya dolduracak bitene kadar dönecek
		self.komutlar = []
		#Spawn sync ile terminali oluşturuyoruz
		self.spawn_sync(Vte.PtyFlags.DEFAULT,
						os.path.expanduser('~'),
						["/bin/bash"],
						[],
						GLib.SpawnFlags.DO_NOT_REAP_CHILD,
						None,
						None)
		#Renkler için bir paket oluşturacağız
		palet = [
			Gdk.RGBA(),
			Gdk.RGBA(),
			Gdk.RGBA(),
			Gdk.RGBA(),
			Gdk.RGBA(),
			Gdk.RGBA(),
			Gdk.RGBA(),
			Gdk.RGBA(),
			Gdk.RGBA(),
			Gdk.RGBA(),
			Gdk.RGBA(),
			Gdk.RGBA(),
			Gdk.RGBA(),
			Gdk.RGBA(),
			Gdk.RGBA(),
			Gdk.RGBA(),
			Gdk.RGBA(),
			Gdk.RGBA(),
			]
		#Renklerimizi bir listeye veriyoruz
		renkler = [
			"#f8f8f2",
			"#272822",
			"#000000",
			"#f92672",
			"#a6e22e",
			"#e6db74",
			"#66d9ef",
			"#ae81ff",
			"#a1efe4",
			"#f8f8f2",
			"#000000",
			"#c61e5b",
			"#80af24",
			"#b3aa5a",
			"#50abbc",
			"#8b67cc",
			"#7fbcb3",
			"#cbcdc8",
			]
		#Paletlere renkleri ekleyelim
		for sayi in range(0,16):
			oldu_mu = palet[sayi].parse(renkler[sayi])
			if not oldu_mu:
				print("Renk okunamadı :: {}".format(renkler[sayi]))

		#Renkleri terminale ekleyelim
		self.set_colors(palet[0],palet[1],palet[2:])
		#Scroll hareket ettiğinde sinyal yayılacak bizde bittimi anlayacağız
		self.connect("contents-changed", self.komut_bitti)

	def komut_bitti(self,term):
		"""Komutun bitip bitmediğini anlamaya çalışacağız"""
		#Scroll hareket edince ekrandaki texti almalıyız
		text = self.get_text_include_trailing_spaces(None,None)[0]
		#Satırlara bölelim
		bol = text.split("\n")
		#Son satırı almaya çalışacağız
		son = ""
		bol = bol[::-1]
		for satir in bol:
			if satir != '':
				son = satir
				break
		#Bu son satır root[ arada birşeyler ]# ise o zaman tamam bitmiş
		if son[:6] == "root [" and son[-3:] == "]# " and len(self.komutlar) != 0:
			#Bittiyse dosya yazımı tamamlanmıştı dosyayı okuyalım
			okunan = self.takip_oku()
			#Çalışan komut komutların 0. arkadaşı
			calisan_komut = self.komutlar[0]
			#Her komut çalıştığında farklı sonuçlar olacak bu yüzden
			self.komutlar.pop(0)
			#Çalıştıracak komut bitmediyse tekrardan komutu siliyoruz
			if len(self.komutlar) != 0:
				self.komut_calistir()
			else:
				okunan = okunan.split("\n")
				if okunan[-1] == "OK" or okunan[-2] == "OK":
					print("KURULUM BAŞARILI")
					self.ebeveyn.ebeveyn.ileri_basildi(None)
				else:
					baslik = diller.diller[self.ebeveyn.ebeveyn.milis_ayarlari["dil"]]["t77"]
					soru = Gtk.MessageDialog(self.ebeveyn.ebeveyn,0,Gtk.MessageType.WARNING, Gtk.ButtonsType.OK,baslik)
					soru.set_title(diller.diller[self.ebeveyn.ebeveyn.milis_ayarlari["dil"]]["t77"])
					soru.format_secondary_text(diller.diller[self.ebeveyn.ebeveyn.milis_ayarlari["dil"]]["t78"])
					cevap = soru.run()
					if cevap == Gtk.ResponseType.OK:
						soru.destroy()
					self.ebeveyn.ebeveyn.stack_secili = 1
					self.ebeveyn.ebeveyn.geri_basildi(None)
					print("KURULUM BAŞARISIZ")


	def takip_oku(self):
		"""Takip ettiğimiz dosyayı okumaya çalışacağız"""
		try:
			f = open("/tmp/t_takip.txt")
			okunan = f.read()
			f.close()
		except:
			print("/tmp/t_takip.txt OKUNAMADI")
			okunan = ""
		return okunan


	def komut_calistir(self):
		"""Komut çalıştırılmak için bu fonksiyonu yazacağız"""
		#Terminali tekrardan güncelelyelim birşeyler yazan olur falan
		a = self.spawn_sync(Vte.PtyFlags.DEFAULT,
						"/",
						["/bin/bash"],
						[],
						GLib.SpawnFlags.DO_NOT_REAP_CHILD,
						None,
						None)
		#Yürütülen komutu print edelim
		print("Komut yürütülüyor :: {} - id :: {}".format(self.komutlar[0],a))
		#Komutun çıktısını alabilmek için çıktıyı tmp altında t_takip.txt ye
		#Yazdıracağız o yüzden gelen komutu güncelliyoruz
		komut = "{} 2>&1 | tee /tmp/t_takip.txt\n".format(self.komutlar[0])
		# /tmp/t_takip.txt dosyasının silinince durumun düzelidiği söylendiğinden
		# Dosyayı silelim
		if os.path.exists("/tmp/t_takip.txt"):
			os.remove("/tmp/t_takip.txt")
		# Feed Child versiyonu sıkıntı bu yüzden 2 farklı yöntem deniyoruz
		try:
			a = self.feed_child_binary(bytes(komut,"utf-8"))
		except:
			a = self.feed_child(komut,len(komut)+2)