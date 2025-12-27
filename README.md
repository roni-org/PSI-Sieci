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
cd zad1.1/server/
docker build -t z31_pserver1 .
docker run -it --rm --network-alias z31_pserver1 --hostname z31_pserver1 --network z31_network --name z31_pserver1 z31_pserver1 8001

```
### uruchomienie klienta do zad 1.1
dodajemy -v $(pwd):/output by zachować wykres z dockera na hoscie
```
cd zad1.1/client/
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
###

### Uruchomienie serwera do zad 2
```
cd zad2/server/
docker build -t z31_server2 .
docker run -d --name z31_server2 --network z31_network -p 5000:5000 z31_server2

```
### uruchomienie klienta do zad 2

```
cd zad2/client/
docker build -t z31_client2 .
docker run --rm --name z31_client --network z31_network z31_client2
```

### sprawdzenie wyników do zad 2
```
docker container cp z31_server2:/app/tree_preorder.txt -
```
###
### Przygotowanie plika do zad 1.2
```
cd zad12
head -c 10000 /dev/urandom > plik.bin
```

### Uruchomienie serwera do zad 1.2
```
cd zad12/server/
docker build -t z31_server12 .
docker run -d --name z31_server12 --network z31_network -p 5005:5005/udp z31_server12

```
### uruchomienie klienta do zad 1.2

```
cd zad2/client/
docker build -t z31_client12 .
cd ..
docker run --rm -it -v "$(pwd)/plik.bin:/app/plik.bin:ro" --network z31_network z31_cli
ent12 ./client /app/plik.bin z31_server12 5005
```

### sprawdzenie wyników do zad 1.2
```
docker cp z31_server12:/app/received.bin ./received.bin
sha256sum plik.bin received.bin
```

### ----------- uruchomienie projektu ------------
utworzenie sieci
```
docker network create z31_network
```
#### uruchomienie servera do projektu
```
cd project
docker build -f server/Dockerfile .
docker run -it --rm --name pserver1 --network z31_network mini_tls_server 4444 10

```
#### uruchomienie klienta do projektu
```
cd project
docker build -f client/Dockerfile .
docker run -it --rm --network z31_network mini_tls_client pserver1 4444

```
wyjście:
```
Ctr+C
lub
docker stop pserver1
```

### komendy na bigubu
ssh username@bigubu.ii.pw.edu.pl "mkdir -p ~/server"

scp server/Dockerfile username@bigubu.ii.pw.edu.pl:~/server/

scp -r username@bigubu.ii.pw.edu.pl:~/client/*.png .

### sprawozdanie
z zad 1.1 znajduje się w katalogu docs pod nazwą PSI_sprawozdanie_zad_1_1.pdf
#
z zad 2 znajduje się w katalogu zad2/docs pod nazwą PSI_sprawozdanie_zad_2.pdf