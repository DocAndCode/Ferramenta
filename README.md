# Ferramenta
Ferramenta DocAndCode

### Dependências

Instale as dependências
* Python 3.6
````bash
sudo apt-get install python3.6
````
* Pip
````bash
sudo apt-get install python-pip
````
* requests
````bash
pip install requests
````

### Configuração

Clone o repositório com o código fonte

````bash
git clone https://github.com/DocAndCode/Ferramenta.git
````

Dentro do arquivo ````DocAndCode.py```` configure as variáveis necessárias

````python
#######################################################
################     CONFIGURATION     ################
####    Set below variables before running this    ####
#######################################################
# @OAUTHTOKEN: Your GitHub Personal Access Token
# @repoOwner: Repository Owner
#   e.g. torvalds
# @repoName: Repository Name
#   e.g. linux
#######################################################
OAUTHTOKEN = ''
repoOwner = ''
repoName = ''
#######################################################
````

* **OAUTHTOKEN**: Token de acesso pessoal. Veja como obter o seu [aqui](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/).
* **repoOwner**: Nome do dono do repositório ou organização a qual ele pertence.
* **repoName**: Nome do repositório

### Executar

#### [Atenção] Leia antes de executar o script
> Ao executar o script são gerados o arquivo ````DocAndCode.md```` e o diretório ````Report/````
>
> * ````DocAndCode.md````: Arquivo que contém o link para o relatório individual de cada _issue_ do repositório
> * ````Report/````: Diretório que contém os arquivos com o relatório de cada _issue_

Com a informação acima, recomenda-se executar o script com umas das opções abaixo:

**[Recomendado] Opção 1**
* Configure o caminho onde o relatório será gerado (raiz do diretório da wiki do seu projeto) alterando a variável ````dirPath````
````python
dirPath = 'caminho_diretorio.wiki/'
````

**Opção 2**
* Copie o arquivo DocAndCode.py para a raiz do diretório da wiki do seu projeto
* Execute o script:
````$ python3 DocAndCode.py````

**Opção 3**
* Execute o script:
````$ python3 DocAndCode.py````
* Copie os arquivos gerados para o diretório raiz da wiki do seu projeto.

## 3. Resultado

Após a execução do script é gerada a seguinte estrutura de arquivos:

````
.
├── DocAndCode.md
└── Report
    └── issue_1.md
    └── issue_2.md
    └── issue_3.md
    └── issue_4.md
    └── ...
````

Onde o arquivo ````DocAndCode.md```` contém a referência para todos os relatórios individuais.
Já o diretório ````Report/```` contém o relatório de cada uma das issues sendo um arquivo para cada issue, o nome do arquivo é composto pelo prefixo ````issue_```` + o id da issue.
