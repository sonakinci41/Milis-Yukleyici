from setuptools import setup, find_packages
from os import listdir, system

langs = []
for l in listdir('languages'):
    if l.endswith('ts'):
        system('lrelease languages/%s' % l)
        langs.append(('languages/%s' % l).replace('.ts', '.qm'))


system('pyrcc5 milis-kur.qrc -o lib/miliskurqrc.py')

datas = [('/usr/share/applications', ['milis-kur.desktop']),
         ('/usr/share/icons/hicolor/scalable/apps', ['slaytlar/miliskurlogo.svg']),
         ('/usr/share/milis-kur/languages', langs)]


setup(
    name = "milis-kur",
    scripts = ["milis-kur"],
    packages = find_packages(),
    version = "1.0",
    license = "GPL v3",
    description = "Milis GNU/Linux System Installer",
    author = "Fatih KAYA , Furkan KALKAN",
    author_email = "trlinux41@gmail.com",
    url = "https://github.com/sonakinci41/Milis-Yukleyici",
    keywords = ["PyQt5", "installer"],
    data_files = datas
)