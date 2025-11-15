# PSI -Sieci

### zespół: z31
* Weronika Maślana
* Alesia Filinkova
* Diana Pelin

### Komendy
#### UWAGA, używaj network create TYLKO lokalnie
```
docker network create z31_network
```
### Uruchomienie serwera do zad 1.1
```
cd server/
docker build -t z31_pserver1 .
docker run -it --rm --network-alias z31_pserver1 --hostname z31_pserver1 --network z31_network --name z31_pserver1 z31_pserver1 8001

```
### uruchomienie klienta do zad 1.1
dodajemy -v $(pwd):/output by zachować wykres z dockera na hoscie
```
cd client/
docker build -t z31_pclient1 .
docker run -it --rm -v $(pwd):/output  --network z31_network     z31_pclient1 z31_pserver1 8001
```

wyjście:
```
Ctr+C
lub
docker stop z31_pserver1
```
### uruchomienie klienta bez zachowywania wykresu z dockera na hoscie
```
cd client/
docker build -t z31_pclient1 .
docker run -it --rm --network z31_network z31_pclient1 z31_pserver1 8001

```

### komendy na bigubu
ssh username@bigubu.ii.pw.edu.pl "mkdir -p ~/server"

scp server/Dockerfile username@bigubu.ii.pw.edu.pl:~/server/

scp -r username@bigubu.ii.pw.edu.pl:~/client/*.png .

### sprawozdanie
z zad 1.1 znajduje się w katalogu docs pod nazwą PSI_sprawozdanie_zad_1_1.pdf