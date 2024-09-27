# Cluster Masters

* Andressa Almeida dos Santos
* João Felipe Peres Lima
* Mateus Eduardo Silva Ribeiro
* Mauricio Gomes Rocha
* Philippe Augusto Monteiro Silva 

## Projeto de Sistemas Distribuídos - Cálculo de Aposentadoria

### Descrição do Projeto

Este projeto está sendo desenvolvido como parte da disciplina **Sistemas Distribuídos** na **Universidade Federal de Goiás (UFG)**. O objetivo é transformar um problema simples, o cálculo de aposentadoria, em um sistema robusto utilizando conceitos de sistemas distribuídos, incluindo **Peer-to-Peer (P2P)** e **Cloud Computing**.

Construiremos esse projeto com o fim de aplicar conceitos teóricos aprendidos em sala de aula em uma aplicação prática e escalável.

### Funcionalidades

- **Cálculo de aposentadoria**: O sistema realiza cálculos de aposentadoria de acordo com as regras fornecidas.
- **Solução distribuída**: O cálculo e armazenamento dos dados são distribuídos entre os nós da rede usando P2P.
- **Armazenamento em Cloud**: Os dados críticos são armazenados na nuvem para garantir persistência e acessibilidade.
- **Alta disponibilidade**: O sistema foi projetado para garantir alta disponibilidade e tolerância a falhas.
- **Escalabilidade**: Capacidade de escalar tanto horizontal quanto verticalmente para suportar grandes volumes de dados.

## Arquitetura

O sistema será desenvolvido utilizando uma arquitetura distribuída baseada em:

- **Peer-to-Peer (P2P)**: Utilizando uma rede P2P para compartilhar o processamento dos cálculos entre os usuários do sistema.
- **Cloud Computing**: A camada de armazenamento é suportada por uma solução de nuvem que garante a persistência dos dados de cálculo e registros de usuários.

## Tecnologias a serem Utilizadas

- **Linguagem**: [Python]
- **Framework de Comunicação**: [gRPC/RabbitMQ/ZeroMQ]
- **Banco de Dados na Nuvem**: [Firebase/AWS S3/Azure Blob Storage]
- **Plataforma de Nuvem**: [AWS/Azure/Google Cloud]
- **Ferramenta de Coordenação P2P**: [Chord/Kademlia]
- **Ferramenta de Controle de Versão**: GitHub
