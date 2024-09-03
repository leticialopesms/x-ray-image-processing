# Medical-Image-Processing

Este repositório é dedicado à implementação de um pipeline para o processamento de imagens médicas em um ambiente hospitalar. O objetivo deste projeto é configurar e operar um PACS utilizando Docker, e processar arquivos DICOM para análise e classificação de achados médicos.



### Conceitos iniciais
Os conceitos a seguir foram fundamentais para entender melhor as ferramentas do desafio e como integrá-las.

* Um **PACS** (Picture Archiving and Communication System) é um sistema de arquivamento e comunicação de imagens médicas que permite o armazenamento, acesso e compartilhamento digital de imagens radiológicas e outros tipos de exames em uma rede hospitalar.

* Um arquivo **DICOM** (Digital Imaging and Communications in Medicine) é um formato padrão para armazenar e transmitir imagens médicas junto com informações associadas, permitindo a interoperabilidade entre diferentes sistemas de imagens médicas.

* **Docker**

* **OrthanC**

* A **API REST** do Orthanc permite que a interação com o servidor para realizar operações como upload, consulta e manipulação de imagens DICOM e outros dados relacionados.

* O **TorchXRayVision** é uma biblioteca de software de código aberto para trabalhar com conjuntos de dados de raios X do tórax e modelos de deep learning. Fornece uma interface e uma cadeia de pré-processamento para um vasto conjunto de tais dados publicamente disponíveis.



### Comentários sobre as tarefas

#### Tarefa 1
* Para iniciar, instalei o Docker Desktop e o configurei no ambiente virtual WSL2, com a ajuda do seguinte repositório: https://github.com/codeedu/wsl2-docker-quickstart.
* A partir disso, para baixar a imagem do OrthanC, utilizei o comando `docker pull jodogne/orthanc` e segui as instruções em https://orthanc.uclouvain.be/book/users/docker.html. O comando para rodar a versão do OrthanC com os plugins é: `docker run -p 4242:4242 -p 8042:8042 --rm jodogne/orthanc-plugins:1.12.4`.
* Para simplificar o gerenciamento do container do OrthanC, criei os arquivos `docker-compose.yaml` e `orthanc.json`, contendo todos as configurações e plugins necessários para rodar corretamente a aplicação. 
* Com isso, acessei http://localhost:8042 para interagir com o ambiente do OrthanC.
* Minha principal dificuldade nessa tarefa foi entender a função de cada ferramenta e como elas estariam integradas. Os links acima foram essenciais para ajudar nessa configuração.

#### Tarefa 2
* Com o auxílio do ChatGPT, criei um script (`send_dicom.py`) em python para enviar os arquivos na pasta `dicom_samples` para o OrthanC.
* A API REST do OrthanC foi utilizada para enviar arquivos DICOM para o servidor Orthanc por meio de uma requisição HTTP, utilizando a função `requests.post()` de python.
* Nessa tarefa, o principal desafio foi entender como funcionava a biblioteca `requests` e como utilizar a API REST a partir disso.
* Após finalizar e rodar o script, todos os arquivos `.dcm` foram enviados com sucesso para o OrthanC, como verifiquei acessando a interface web em http://localhost:8042.

#### Tarefa 3

#### Tarefa 4 (EXTRA)