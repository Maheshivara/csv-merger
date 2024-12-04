# CSV Merger

## O que é

> [!NOTE]
> Isso é um utilitário para unir dois arquivos do tipo csv que possuam uma coluna em comum por meio de uma interface gráfica simples, caso você possua interesse em algo mais sofisticado e performático (embora sem interface gráfica) verifique a ferramenta [miller](https://miller.readthedocs.io/en/latest/).

Um utilitário que usa a biblioteca Tkinter para prover uma interface gráfica (muito) básica para a junção de dois arquivos csv por meio de uma coluna em comum, para a junção a ferramenta se utiliza da biblioteca [pandas](https://pandas.pydata.org).

## Como Rodar

### Ferramentas

- [python](https://www.python.org) >= 3.12
- [uv](https://github.com/astral-sh/uv)

### Instruções

1. Basta clonar esse repositório no local desejado e usar o comando:
   ```bash
   uv sync
   ```
   Esse comando irá criar e configurar o ambiente virtual do projeto com as bibliotecas necessárias.

#### Pelo Código Fonte

1. Inicie o utilitário com:
   ```bash
   uv run main.py
   ```

#### Para Buildar

> [!WARNING]
> No Linux é necessário instalar os pacotes [patchelf](https://github.com/NixOS/patchelf) e `python3-dev` usados pela nuitka, além do `python3-tk` necessário para a aplicação.

1. O build é feito por meio da ferramenta [nuitka](https://nuitka.net), para realizar o build basta rodar o comando:
   ```bash
   uv run -m nuitka --onefile --enable-plugin=tk-inter --windows-console-mode=disable --output-dir=./dist main.py
   ```
   Esse comando irá buildar o projeto com apenas um arquivo final (`--onefile`), adicionando o que for necessário do Tkinter (`--enable-plugin=tk-inter`) e sem uma janela de console (`--windows-console-mode=disable`) na pasta dist/diretório (`--output-dir=./dist`).
2. Inicie o arquivo executável na pasta `dist`.

## Como Usar

1. Selecione os dois arquivos que deseja unir através dos botões de seleção.
2. Na caixa de escolha ao lado direito de cada botão de seleção escolha o nome da coluna pela qual você deseja que o documento seja unido.
3. Escolha a pasta de destino do documento.
4. Selecione as colunas que devem ser mantidas de cada documento (ao menos uma em cada).
5. Pressione o botão de `confirmar` na parte inferior da tela.

Com tudo ocorrendo bem o novo documento deve ser criado na pasta escolhida no passo 3, o nome será algo como `merged_20241203184532.csv` com a parte numérica sendo retirada da data atual.
