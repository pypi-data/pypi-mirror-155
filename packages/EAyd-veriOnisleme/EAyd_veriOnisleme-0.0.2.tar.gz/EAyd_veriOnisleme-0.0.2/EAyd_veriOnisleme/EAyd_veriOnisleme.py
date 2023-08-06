import os

def dosyaOku(dosyaAdi):
    f = open(dosyaAdi,"r", encoding='utf8')
    metin = f.read()
    f.close()
    return metin

def dosyayaEklemeYap(dosyaAdi, metin):
    f = open(dosyaAdi,"a", encoding='utf8')
    f.write(metin + "\n")
    f.close()

def dosyayaSilerekYaz(dosyaAdi, metin):
    f = open(dosyaAdi,"w", encoding='utf8')
    f.write(metin)
    f.close()
