# Medical-Image-Processing

Este repositório é dedicado à implementação de um pipeline para o processamento de imagens médicas em um ambiente hospitalar. O objetivo deste projeto é configurar e operar um PACS utilizando Docker, e processar arquivos DICOM para análise e classificação de achados médicos.

### Conceitos iniciais
* Um **PACS** (Picture Archiving and Communication System) é um sistema de arquivamento e comunicação de imagens médicas que permite o armazenamento, acesso e compartilhamento digital de imagens radiológicas e outros tipos de exames em uma rede hospitalar.

* Um arquivo **DICOM** (Digital Imaging and Communications in Medicine) é um formato padrão para armazenar e transmitir imagens médicas junto com informações associadas, permitindo a interoperabilidade entre diferentes sistemas de imagens médicas.

* **Docker**

* **OrthanC**

* **API REST**

* **TorchXRayVision**


### Comentários sobre as tarefas

#### Tarefa 1
* De início, instalei o Docker Desktop e o configurei no ambiente virtual WSL2, com a ajuda do seguinte repositório: https://github.com/codeedu/wsl2-docker-quickstart.
* A partir disso, para baixar a imagem do OrthanC, utilizei o comando `docker pull jodogne/orthanc` e segui as instruções presentes em https://orthanc.uclouvain.be/book/users/docker.html. Aprendi que, para simplificar o gerenciamento do container do OrthanC, pode-se criar os arquivos `docker-compose.yaml` e `orthanc.json`, contendo todos as configurações e plugins necessárias para rodar corretamente a aplicação. 
* Com isso, acessei http://localhost:8042 para interagir com o ambiente do OrthanC.
* Minha principal dificuldade nessa tarefa foi entender a função de cada ferramenta e como elas estariam integradas.