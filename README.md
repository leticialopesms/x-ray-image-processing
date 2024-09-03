# Medical Image Processing - Desafio MICLab

Este repositório é dedicado ao estudo de processamento de imagens médicas em um ambiente hospitalar. Dentre os desafios deste projeto, estão configurar e operar um PACS, realizar o processamento de arquivos DICOM e entender o uso do modelo pré-treinado TorchXRayVision para análise e classificação de achados médicos.



### Conceitos iniciais
Os conceitos a seguir foram fundamentais para entender melhor as ferramentas e as aplicações do desafio, e como elas se relacionam.

* Um **PACS** (Picture Archiving and Communication System) é um sistema de arquivamento e comunicação de imagens médicas que permite o armazenamento, acesso e compartilhamento digital de imagens radiológicas e outros tipos de exames em uma rede hospitalar.

* Um arquivo **DICOM** (Digital Imaging and Communications in Medicine) é um formato padrão para armazenar e transmitir imagens médicas junto com informações associadas, permitindo a interoperabilidade entre diferentes sistemas de imagens médicas.

* **[Docker](https://www.docker.com/)** é uma plataforma open source que possibilita o empacotamento de uma aplicação dentro de um container, para que ela possa se adequar e rodar em qualquer máquina que tenha essa tecnologia instalada.

* **[OrthanC](https://www.orthanc-server.com/)** é um PACS que permite melhorar os fluxos DICOM nos hospitais e possibilita análises automatizadas de imagens médicas. A **API REST** do Orthanc permite que a interação com o servidor para realizar operações como upload, consulta, manipulação de imagens DICOM e outros dados relacionados.

* O **[TorchXRayVision](https://github.com/mlmed/torchxrayvision)** é uma biblioteca de software de código aberto para trabalhar com conjuntos de dados de raios X do tórax e modelos de deep learning. Fornece uma interface e uma cadeia de pré-processamento para um vasto conjunto de dados disponíveis publicamente.



### Comentários sobre o desafio

#### Tarefa 1: Configurar e rodar um PACs OrthanC, utilizando Docker.
* Para iniciar, o Docker Desktop foi instalado e o configurado para o ambiente virtual WSL2, com a ajuda do seguinte repositório: https://github.com/codeedu/wsl2-docker-quickstart.
* A partir disso, para baixar a imagem do OrthanC, utilizei o comando `docker pull jodogne/orthanc-plugins` e segui as instruções em https://orthanc.uclouvain.be/book/users/docker.html.
* Para simplificar o gerenciamento do container do OrthanC, criei os arquivos `docker-compose.yaml` e `orthanc.json`, contendo todas as configurações personalizadas e os plugins necessários para rodar corretamente a aplicação.
* Com isso, foi possível interagir com o ambiente do OrthanC a partir do endereço http://localhost:8042.
* A principal dificuldade nessa tarefa foi entender a função de cada ferramenta e como elas estariam integradas. Os links acima foram essenciais para ajudar nessa configuração.

#### Tarefa 2: Utilizar um script Python para enviar arquivos DICOM.
* Com o auxílio do ChatGPT, criei um script (`send_dicom.py`) em python para enviar os arquivos na pasta `dicom_samples` para o OrthanC.
* A API REST do OrthanC foi utilizada para enviar arquivos DICOM para o servidor Orthanc por meio de uma requisição HTTP, utilizando a função `requests.post()` de python.
* Nessa tarefa, o principal desafio foi entender como funcionava a biblioteca `requests` e como utilizar a API REST a partir disso.

#### Tarefa 3: Computar os resultados de classificação de achados utilizando o TorchXRayVision. 
* A partir do repositório https://github.com/mlmed/torchxrayvision, foi possível compreender melhor como aplicar o modelo pré-treinado do TorchRayVision para analisar e detectar patologias em imagens de raio-X.
* Para gerar o script para computar os resultados, utilizei como base os arquivos `process_image.py`, que processa uma única imagem, e `process_batch.py`, que processa várias amostras em um diretório.
* Aqui, a principal dificuldade foi adaptar o código de leitura de imagens para a leitura de arquivos DICOM, já que o modelo de predição exige formatos e tamanhos específicos para gerar os resultados. Por exemplo, alguns arquivos armazenavam imagens com um tamanho maior que o limite de pixels esperado pela função `xrv.utils.read_xray_dcm`, o que exigiu um ajuste nos parâmetros. Além disso, a função `xrv.models` espera que as imagens possuam uma resolução específica (224x224), sendo necessário, então, realizar um resize. Essas, dentre outras especificações, demandaram várias adaptações no código para que as predições fossem realizadas corretamente.
* Os resultados gerados pelo TorchRayVision estão presentes em `resultados_torchxrayvision.json`.

#### Tarefa 4: Criar um DICOM SR (Structured Report) para cada arquivo DICOM com os resultados do modelo, e enviá-los para o PACS local OrthanC.