from PyQt5.QtGui import QImage,QPainter,QPen, QBrush , QColor

def asama_ciz(asama,tum_asama):
    #Amacımız pencerenin üzerinde gözüken adım kısmı için gerekli resmi oluşturmak
    resim = QImage(950,10,QImage.Format_RGB32)
    boyayici = QPainter()
    boyayici.begin(resim)
    mavi_kalem = QPen(QColor("#00bbf2"))
    mavi_firca = QBrush(QColor("#00bbf2"))
    beyaz_kalem = QPen(QColor("#ffffff"))
    beyaz_firca = QBrush(QColor("#ffffff"))
    boyayici.setPen(beyaz_kalem)
    boyayici.setBrush(beyaz_firca)
    boyayici.drawRect(0,0,950,10)
    boyayici.setPen(mavi_kalem)
    boyayici.setBrush(mavi_firca)
    en_hesabi = (asama/tum_asama)*950
    boyayici.drawRect(0,0,int(en_hesabi),10)
    boyayici.end()
    return resim
