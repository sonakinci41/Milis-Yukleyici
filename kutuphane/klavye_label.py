from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt5.QtCore import QPoint, pyqtSignal
import subprocess


klavye_modeli = {
"pc104" : [
    [0x29, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xa, 0xb, 0xc, 0xd],
    [0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b, 0x2b],
    [0x1e, 0x1f, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28],
    [0x2c, 0x2d, 0x2e, 0x2f, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35]
],

"pc105" : [
    [0x29, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xa, 0xb, 0xc, 0xd],
    [0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b],
    [0x1e, 0x1f, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x2b],
    [0x56, 0x2c, 0x2d, 0x2e, 0x2f, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35]
],

"pc106" : [
    [0x29, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xa, 0xb, 0xc, 0xd, 0xe],
    [0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b],
    [0x1e, 0x1f, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29],
    [0x2c, 0x2d, 0x2e, 0x2f, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36]
]
}


class KlavyeLabel(QLabel):

    klavye_bilgi = pyqtSignal(str, str, str) # model, layout, variant = pc105, tr, f

    ciziliyor = False
    tus_yerlesimi = None
    klavye_modeli = None

    def __init__(self, ebeveyn=None):
        super().__init__()
        self.e = ebeveyn
        self.setFixedSize(900, 253)


        self.klavye_bilgi.connect(self.proc)

    def proc(self, model, layout, variant):
        if model in klavye_modeli:
            self.ciziliyor = True
            self.tus_yerlesimi = self.unicodeToString(model, layout, variant)
            self.klavye_modeli = model
        else:
            self.ciziliyor = False

        self.update()

    def unicodeToString(self, model, layout, variant=""):
        keycodes = {}
        tus_yerlesimi_command = subprocess.Popen(["ckbcomp", "-model", model, "-layout", layout, "-variant", variant],
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

    def paintEvent(self, event):
        boyayici = QPainter(self)
        boyayici.setRenderHints(QPainter.SmoothPixmapTransform|QPainter.Antialiasing|QPainter.HighQualityAntialiasing)

        boyayici.drawPixmap(QPoint(0, 0), QPixmap("./resimler/klavye.png"))

        koordinat_listesi = ((10, 30), (90, 90), (115, 150), (80, 215))
        sayac = 0
        if self.ciziliyor:
            for key_list in klavye_modeli[self.klavye_modeli]:
                coordinat = koordinat_listesi[sayac]
                sayac += 1
                for num, key in enumerate(key_list):
                    try:
                        font = boyayici.font()
                        font.setPointSize(12)
                        boyayici.setFont(font)

                        big = QPen(QColor("#ccff00"))
                        boyayici.setPen(big)
                        boyayici.drawText(coordinat[0]+(60*num), coordinat[1], self.tus_yerlesimi[key][1])

                        font = boyayici.font()
                        font.setPointSize(14)
                        boyayici.setFont(font)

                        little = QPen(QColor(255, 255, 255))
                        boyayici.setPen(little)
                        boyayici.drawText(coordinat[0]+15+(60*num), coordinat[1]+20, self.tus_yerlesimi[key][0])

                    except KeyError as err:
                        print(self.tus_yerlesimi, key)
