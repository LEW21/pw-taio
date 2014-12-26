Projekt z TAiO
==============

##### Wymagania systemowe potrzebne do uruchomienia programu

* Python 3
* numpy (pakiet do Pythona)

##### Pozostałe zależności są dostarczone razem z kodem programu (nie ma potrzeby ich osobnego instalowania):

* pyswarm  - funkcja PSO
* openpyxl - import/eksport formatu Excel

##### Uruchamianie programu

* `python TAIO2014.py`
* lub alternatywnie w Bashu Linuksa: `./TAIO2014.py`

##### Parametry uruchomieniowe

Wywołanie programu z parametrem `-h` spowoduje wypisanie wszystkich dostępnych parametrów, wraz z ich opisami.
Nazwy parametrów powinny być poprzedzane jednym znakiem "-", np. `-etap a1`

##### Przykład uruchomienia z parametrami
`python TAIO2014.py -etap a1 -dyskretyzacja 4 -iloscKlas 10 -iloscCech 5 -iloscPowtorzenWKlasie 50`

Wynik zostanie wypisany na ekran. Można go także zapisać do pliku, korzystając z parametru `sciezkaOutputKlas`.