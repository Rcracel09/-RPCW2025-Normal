# -RPCW2025-Normal
Teste de RPCW

## Nome: 

Daniel Henrique Cracel Rodrigues

## Numero: 

PG57871

## Requisitos

- Python 3.6 ou superior
- Biblioteca RDFLib (`pip install rdflib`)
- GraphDB (para execução das queries SPARQL)

## Estrutura de Arquivos

- `sapientia_base.ttl` - Ontologia base
- `sapientia_ind.ttl` - Ontologia povoada com indivíduos
- `populate_ontology.py` - Script para povoar a ontologia
- `sparql.txt` - Queries SPARQL para consultas e inferências
- Datasets JSON:
  - `conceitos.json`
  - `disciplinas.json`
  - `mestres.json`
  - `obras.json`
  - `pg57871.json`

## Passo a Passo

### 1. Preparação da Ontologia Base

A ontologia base já está definida no arquivo `sapientia_base.ttl`. 

### 2. Povoamento da Ontologia

Para povoar a ontologia com os indivíduos dos datasets JSON:

1. Coloque todos os arquivos (ontologia base + datasets JSON) no mesmo diretório
2. Execute o script de povoamento:

```bash
python populate_ontology.py
```

Este script irá gerar o arquivo `sapientia_ind.ttl`.

### 3. Execução das Queries

As queries estão organizadas no arquivo `sparql.txt`
