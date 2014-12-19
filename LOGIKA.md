### Automat deterministyczny

Postać macierzy litery: Najwyżej jedna jedynka w każdej kolumnie.  
Postać słowa: lista liter

Startuje w stanie początkowym, zapisanym w postaci wektora [1, 0, ..., 0].

Iteruje po literach słowa, i w każdej iteracji ustala nowy stan na wynik mnożenia macierzy przypisanej danej literze przez stary wektor stanu.

Zmienna ze stanem ma cały czas formę wektora z jedną jedynką i resztą zer. Numerem stanu jest indeks tej jedynki.

### Automat niedeterministyczny

Postać macierzy litery: Kilka jedynek w każdej kolumnie.  
Postać słowa: lista liter

Startuje w stanie początkowym, zapisanym w postaci wektora [1, 0, ..., 0].

Iteruje po literach słowa analogicznie do automatu deterministycznego. Po wykonaniu mnożenia stan ma jednak formę wektora z kilkoma jedynkami - więc na końcu każdej iteracji 
losuje z wektora stanu jedną jedynkę (tj. wybiera jeden stan), a resztę zeruje.

### Automat rozmyty

Postać macierzy litery: Najwyżej jedna jedynka w każdej kolumnie.  
Postać słowa: lista wektorów pewności liter

Startuje w stanie początkowym, zapisanym w postaci wektora [x, x, ..., x], gdzie x to 1/liczba_stanów.

Iteruje po słowie. W pętli wewnętrznej iteruje po pewnościach liter i mnoży macierz danej litery przez stary wektor stanu (analogicznie do deterministycznego - otrzymując 
wektor), a potem jeszcze przez pewność tej litery. Sumuje wyniki działań pętli wewnętrznej, otrzymując nowy wektor stanu.

Zmienna ze stanem ma formę wektora liczb rzeczywistych, z których każda opisuje pewność że znajdujemy się w danym stanie.
