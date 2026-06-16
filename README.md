# Criptografia

## Objetivo

### Este repostiório tem o objetivo de expor o passo a passo de meus estudos em criptografia

## Tipos de Criptografia

### Simétrica

A chave que cifra é a mesma chave que decifra.

Antes de executar o teste leia um pouco da teoria por trás da criptografia simétrica [aqui](simetrica/teoria_simétrica.md)

Como executar o teste

Faça o clone 📑 do repositório em seu computador.

Entre no repositório com o comando:

```cmd
cd ciberseguranca
```

agora basta entrar no diretório simetrica

```cmd
cd simetrica
```

E executar o compando python:

```python
python_simulacao.py
```

Verá o passo a passo no prompt da criação dos códigos públicos, chave pública, chave secreta, cifragem de mensagem e decifragem da mesma, de uma ponta a outra.

## Teconologias utilizadas

🐍 python
Módulos:

```python
 hashlib
 secrets # é muito mais seguro que random por conta das repetições da random
 cryptography
```

## Teoria por trás

Para entender um pouco a respeito do assunto e métodos utilizados na construção da classe no arquivo `script_simetrica.py` leia o arquivo [teoria.md](teoria.md)

### Assimétrica

Importante que inicialmente leia as teorias nos arquivos [Teoria Criptografia Assimétrica](assimetrica/teoria_assimetrica.md), caso naõ tenha interesse na teoria geral, pode ler os documentos específicos aos algoritmos:

- [RSA](assimetrica/rsa.md)
- [ECC](assimetrica/ecc.md)

Somente depois tentar proceder com os testes do código.
