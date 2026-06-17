# Criptografia

## Objetivo

### Este repostiório tem o objetivo de expor o passo a passo de meus estudos em criptografia

## Tipos de Criptografia

### Simétrica

A chave que cifra é a mesma chave que decifra.

Antes de executar o teste leia um pouco da teoria por trás da criptografia simétrica [aqui](simetrica/teoria_simétrica.md)

Como executar o teste

1. Faça o clone 📑 do repositório em seu computador.

   ```cmd
      git clone git@github.com:guedesindev/ciberseguranca.git
   ```

2. Acesse o repositório com o comando:

   ```cmd
      cd ciberseguranca
   ```

3. Execute o ambiente virtual

   ```cmd
      #windows
      venv\Scripts\activate

      #linux ou mac
      source venv/bin/activate
    ```

4. Acesse o diretório simetrica

   ```cmd
      cd simetrica
   ```

5. Execute o projeto

   ```python
      python simulacao.py
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

## Teoria por trás da criptografia

Para entender um pouco a respeito do assunto e métodos utilizados na construção da classe no arquivo `script_simetrica.py` leia o arquivo [teoria.md](teoria.md)

### Assimétrica

Importante que inicialmente leia as teorias nos arquivos [Teoria Criptografia Assimétrica](assimetrica/teoria_assimetrica.md), caso naõ tenha interesse na teoria geral, pode ler os documentos específicos aos algoritmos:

- [RSA](assimetrica/rsa.md)
- [ECC](assimetrica/ecc.md)

Somente depois tentar proceder com os testes do código.

### Para testar o código

1. Faça o clone do repositório:

    ```cmd
        git clone git@github.com:guedesindev/ciberseguranca.git
    ```

2. Acesse o repositório com o comando:

    ```cmd
        # acesse o  diretório cibersegurança
        cd ciberseguranca
    ```

3. Execute o ambiente virtual

   ```python
     # windows
     venv\Scripts\activate

     # linux ou mac
     source venv/bin/activate
   ```

4. Acesse o diretório assimetrica

    ```cmd
        cd assimetrica
    ```

5. Execute o projeto

    ```cmd
        python simulacao_rsa.py
    ```
