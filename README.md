# Processamento de Imagens de Raio-X

Este repositório é dedicado ao estudo de organização e processamento de imagens de raio-x. Neste projeto, pretende-se configurar e operar um PACS, realizar o processamento de arquivos DICOM e entender o uso do modelo pré-treinado da biblioteca TorchXRayVision para análise e classificação de achados médicos.

## Conceitos iniciais

Os conceitos a seguir foram fundamentais para entender melhor as ferramentas e as aplicações do desafio:

* Um **PACS** (Picture Archiving and Communication System) é um sistema de arquivamento e comunicação de imagens médicas que permite o armazenamento, acesso e compartilhamento digital de imagens radiológicas e outros tipos de exames em uma rede hospitalar.

* Um arquivo **DICOM** (Digital Imaging and Communications in Medicine) é um formato padrão para armazenar e transmitir imagens médicas junto com informações associadas, permitindo a interoperabilidade entre diferentes sistemas de imagens médicas.

* **[Docker](https://www.docker.com/)** é uma plataforma open source que possibilita o empacotamento de uma aplicação dentro de um container, para que ela possa se adequar e rodar em qualquer máquina que tenha essa tecnologia instalada.

* **[Orthanc](https://www.orthanc-server.com/)** é um PACS que permite melhorar os fluxos de arquivos DICOM nos hospitais e possibilita análises automatizadas de imagens médicas. A **API REST** do Orthanc permite a interação com o servidor para realizar operações como upload, consulta e manipulação de imagens DICOM.

* **[TorchXRayVision](https://github.com/mlmed/torchxrayvision)** é uma biblioteca open source que permite integrar conjuntos de dados de raios-x do tórax e modelos de deep learning. O modelo utilizado aqui permite identificar e classificar diversas condições patológicas presentes nas imagens de radiografia.

A partir desses conceitos, segui uma série de tarefas para alcançar os objetivos do estudo.

## 1. Configurar e rodar um PACs Orthanc, utilizando Docker.

Para iniciar, o Docker Desktop foi instalado e configurado para o ambiente virtual WSL2, com a ajuda do repositório [wsl2-docker-quickstart](https://github.com/codeedu/wsl2-docker-quickstart).

A imagem utilizada foi `jodogne/orthanc-python`, seguindo as instruções em [Orthanc Book](https://orthanc.uclouvain.be/book/users/docker.html).

Para simplificar o gerenciamento do container do OrthacC, criei os arquivos `docker-compose.yaml` e `orthanc.json`, contendo todas as configurações personalizadas e os plugins necessários para rodar corretamente a aplicação. Mais tarde, de acordo com os scripts criados, adicionei um `Dockerfile` para incluir todas as dependências necessárias.

Para construir a nova imagem:
```sh
docker-compose build
```

Para iniciar o container em segundo plano (modo _detached_):
```sh
docker-compose up -d
```

Para abrir um terminal bash no container:
```sh
docker-compose exec orthanc bash
```

Para sair da sessão atual dentro do container:
```sh
exit
```

Para parar e remover os containers, volumes e redes criados:
```sh
docker-compose down
```

Com isso, foi possível interagir com o ambiente do Orthanc pelo endereço http://localhost:8042. A principal dificuldade nessa tarefa foi entender o ambiente Docker e como utilizá-lo para rodar o PACS isoladamente. Os links acima foram essenciais para ajudar nessa configuração.

## 2. Utilizar um script Python para enviar arquivos DICOM.

O script `send_dicom.py` envia os arquivos DICOM na pasta `dicom_samples` para o Orthanc. A API REST do Orthanc foi utilizada para enviar arquivos DICOM para o servidor por meio de uma requisição HTTP, utilizando a função `requests.post()`.

## 3. Computar os resultados de classificação de achados utilizando o TorchXRayVision. 

A partir do repositório [TorchXRayVision](https://github.com/mlmed/torchxrayvision), foi possível aplicar o modelo pré-treinado da biblioteca para analisar e detectar patologias em imagens de raio-x do tórax. As previsões geradas pelo modelo correspondem a probabilidades associadas à presença de cada patologia em uma imagem de radiografia.

Para gerar o `process_dicom.py` e computar os resultados, utilizei como base o código da sessão _getting started_ do repositório. Aqui, a principal dificuldade foi adaptar o código de leitura de imagens para a leitura de arquivos DICOM, já que o modelo de previsão exige formatos e tamanhos específicos para gerar os resultados. Por exemplo, alguns arquivos armazenavam imagens com um tamanho maior que o limite de pixels esperado pela função `xrv.utils.read_xray_dcm`, o que exigiu um ajuste nos parâmetros para ler a imagem corretamente. Uma outra solução foi utilizar a função em `read_xray_dcm.py`, que trata especificamente as imagens deste projeto. Particularidades como essa demandaram várias adaptações no código para que as previsões fossem realizadas corretamente.

Os resultados com as previsões foram gerados em `results_torchxrayvision.json`.

## 4. Criar um DICOM SR (Structured Report) para cada arquivo DICOM com os resultados do modelo, e enviá-los para o PACS local OrthanC.

Para criar um DICOM SR, utilizei a biblioteca `pydicom` para manipular os arquivos DICOM e adicionar os resultados do modelo TorchXRayVision.

A biblioteca `highdicom` foi usada para criar um _Structured Report_ (SR) a partir de cada DICOM do projeto, que implementa o template _TID1500 Measurement Report_, uma forma padronizada de armazenar medições e avaliações gerais de imagens médicas.

Assim, o script `send_SR.py` foi criado para ler os arquivos DICOM, adicionar os resultados do modelo como um SR, e enviar esses arquivos para o PACS Orthanc.

Esta é a parte do projeto na qual senti maior dificuldade. Foi preciso entender a estrutura dos arquivos DICOM SR e como adicionar informações corretamente, já que, nesses arquivos, os dados são organizadas de forma hierárquica e, por isso, deve-se tomar cuidado ao criar cada instância do relatório.

## Considerações finais

Durante este desafio, consegui expandir meu conhecimento sobre processamento de imagens médicas e ferramentas que auxiliam no desenvolvimento de software. Cada etapa do projeto foi uma oportunidade de aprendizado, desde a integração de diferentes bibliotecas até a adaptação de modelos de deep learning para aplicações médicas, solidificando meu entendimento sobre o impacto da inteligência artifical e da computação como um todo na área da saúde.