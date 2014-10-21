Projekt z TAiO
==============

Generowanie pliku z nieprzetworzonymi danymi:
```sh
python gen.py 10 5 1000 > dane.csv
```

Generowanie pliku z danymi symbolicznymi:
```sh
python gen.py 10 5 1000 | python norm.py 10 > symboliczne.csv
```

Wypisywanie przykładowego rozkładu danych:
```sh
python gen.py 10 5 1000 | python norm.py 10 | python wypisz_rozklad.py 0
```

Zamiast pipe'ować wywołania, można też oczywiście zrobić:
```sh
python gen.py 10 5 1000 > dane.csv
python norm.py 10 < dane.csv > symboliczne.csv
python wypisz_rozklad.py 0 < symboliczne.csv
```

Każdy z plików informuje o swoich parametrach po uruchomieniu go z opcją -h.