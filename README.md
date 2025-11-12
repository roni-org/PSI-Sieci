# PSI -Sieci

### zespół: Z31
* Weronika Maślana
* Alesia Filinkova
* Diana Pelin

### Komendy
#### UWAGA, używaj network create TYLKO lokalnie
docker network create Z31_network


```
cd server/
docker build -t pserver1 .
docker run -it --network-alias pserver1 --hostname pserver1 --network Z31_network --name pserver1 pserver1 8001

lub

docker run -it --rm \
  --network Z31_network \
  --name pserver1 \
  pserver1 8001
```

```
cd client/
docker build -t pclient1 .
docker run -it --network Z31_network pclient1 pserver1 8001

lub

docker run -it --rm \
  --network Z31_network \
  pclient1 pserver1 8001

```