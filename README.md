# Testna naloga AI / Autonomous drones / Tracking

## Opis rešitve
Program je napisan v Pythonu in razdeljen na štiri datoteke.
V `controller.py` je koda, ki generira ukaze za drona.

V `tracker.py` je koda, za sledenje objekta. Odločil sem se za algoritem
redkega optičnega pretoka, specifično Lucas-Kanade, saj smo podobno nalogo sledenja objektu
že imeli na fakulteti in smo takrat to rešili s pomočjo optičnega pretoka.

V `debug_info.py` je koda, ki v levi zgornji kot slike izpiše pomembne podatke,
kot so trenutni center objekta, oddaljenost objekta od centra slike, relativna velikost objekta in ukaz dronu.

V `main.py` pa je narejen workflow.
In sicer najprej se naloži video posnetek. Sledi izbira objekta opisana v poglavju Zagon.
Nato pa se pretvori frame v grayscale in se znotraj ROI naredi
feature extraction. Te točke potem grejo v Lucas-Kanade kot točke za spremljanje premika objekta.

Potem pa se v zanki frame by frame izvaja Lucas-Kanade za spremljanje objektu in
se sproti tudi izpisujejo podatki iz debug_info.

Prav tako se na sliki vidi:
- center slike, kot rumena pika,
- center objekta, kot modra pika,
- vijolična črta, ki povezuje oba centra,
- bounding box okoli dejanskih feature pikslov, kot roza okvir,
- feature piksli, kot rdeče pike,
- in zeleni okvir, ki predstavlja kje bi se naj nahajal objekt na sliki.

## Zagon
Za zagon rešitve je potrebno repozitorij klonirati in dodati
datoteko `video.mp4` na enak nivo kot je datoteka `main.py`. Prav tako je potrebno
namestiti knjižnico openCV in numpy.
```
pip install opencv-python numpy
```
Potem pa se zažene funkcija main.
```
python main.py
```
Prikaže se prvi frame videa, na katerem uporabnik izbere
objekt z miško (click and drag). Po izbiri mora uporabnik pritisniti tipko `SPACE` ali `ENTER`.


## Težave, s katerimi sem se srečal
Najprej sem poskušal rešiti problem premika bounding boxa preko seštevanja
spremembe dx, dy pikslov in prištevek sprememb k trenutni pozicija okvirja. Ta pristop
se je izkazal za nezaneslivega zaradi seštevanja ocenitvenih napak oz. okvir je postopoma začel iti v drugo
smer kot pa zazne feature točke (drifting). 

Potem pa sistem ponovne izbire feature pikslov, če jih imamo premalo ali pa na vsakih x framov.
To sem sicer poskusil, tako da sem vse feature piksle, ki gredo izven zelenega okvirja odstranil, vendar se je potem zgodilo to, da so se našli napačni
piksli znotraj zelenega okvirja, kar je slabo vplivalo na nadaljno sledenje objektu. Zaradi tega sem to odstranil iz končne rešitve.

## Možne izboljšave
Definitivno bi bilo smiselno imeti možnost ponovne izbire feature pikslov, če
se trenutni zgubijo, ampak na dober način oz. boljši kot poskušen. Prav tako bi lahko uporabil več točk / preveril ali bi bila uporaba
gostega optičnega pretoka boljša (ne preveč računsko zahtevna za realtime).