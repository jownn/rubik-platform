# rubik-platform

Este é um projeto de um kit educacional utilizando um cubo mágico (Rubik).

### Pré-requisitos

Para utilização do kit é necessario

```
Python
O Kit educacional (robô)
```

### Instalação

Obs.: É necessário antes de instalar este projeto, ter instalado: 
* Docker e o Docker-compose

Para instalá-lo em sua máquina plugue a camêra e faça os comandos a seguir:

``` bash
  git clone https://github.com/jownn/rubik-platform.git
  cd rubik-platform
  xhost +local:root
  docker-compose build
  docker-compose up
```

Para resetar o docker com o banco:

``` bash
    docker-compose down --rmi all -v --remove-orphans
```

### Utilização

    Link para acesso: http://0.0.0.0:5000/
    O usuario padrão é o admin:admin
    As demais utilizações são explicadas na tela inicial