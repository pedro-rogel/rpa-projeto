# Projeto Prático de RPA

Este repositório contém o código-fonte do **Projeto Prático de RPA**, que coleta conselhos da Advice Slip API, armazena os dados em um banco SQLite, processa padrões de texto com regex e envia um relatório por e‑mail.

---

## Conteúdo

* [Descrição](#descrição)
* [Pré-requisitos](#pré-requisitos)
* [Instalação](#instalação)
* [Configuração](#configuração)
* [Uso](#uso)
* [Estrutura do Banco de Dados](#estrutura-do-banco-de-dados)
* [Personalização](#personalização)
* [Contribuição](#contribuição)
* [Licença](#licença)

---

## Descrição

O script `projeto_rpa.py` executa as seguintes etapas de forma automatizada:

1. **Coleta**: faz requisição à Advice Slip API e extrai conselhos aleatórios.
2. **Armazenamento**: cria/atualiza um banco SQLite (`projeto_rpa.db`) com tabelas para dados brutos e processados.
3. **Processamento**: aplica regex para identificar palavras com 7 ou mais caracteres e sinaliza cada registro.
4. **Relatório**: gera um texto contendo totais e lista de todas as frases coletadas.
5. **Envio de e‑mail**: conecta ao SMTP do Gmail via TLS e envia o relatório por e‑mail, solicitando App Password em tempo de execução.

---

## Pré-requisitos

* Python 3.8 ou superior
* Acesso à internet para chamadas à API e ao servidor SMTP
* Se quiser utilizar um email pronto:
<br/>
email: rpaprojeto91@gmail.com <br/>
senha: gnza kqyc anfr wwrx

### Bibliotecas Python

```bash
pip install requests
```

*As bibliotecas `sqlite3`, `re`, `smtplib`, `email` e `getpass` fazem parte da biblioteca padrão do Python.*

---

## Instalação

1. Clone este repositório:

   ```bash
   ```

git clone \<URL\_DO\_REPOSITORIO>
cd \<NOME\_DO\_REPOSITORIO>

````
2. (Opcional) Crie e ative um ambiente virtual:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
````

3. Instale a dependência:

   ```bash
   ```

pip install requests

````

---

## Configuração

Antes de executar, é necessário definir variáveis de ambiente ou informar valores no prompt:

- **SMTP_USER**: seu endereço de e-mail Gmail (`PEDROROGEL3@gmail.com`)
- **EMAIL_TO**: e-mail do destinatário que receberá o relatório

Exemplo (Linux/macOS):
```bash
export SMTP_USER="seu.email@gmail.com"
export EMAIL_TO="destino@example.com"
````

> **Observação:** certifique-se de ter ativado a Verificação em Duas Etapas no Gmail e gerado uma App Password em [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).

---

## Uso

Execute o script com:

```bash
python projeto_rpa.py
```

Durante a execução, siga os prompts:

1. **(se não definiu SMTP\_USER)** Digite seu e-mail Gmail.
2. Digite sua **App Password** do Gmail (senha de 16 caracteres).

Ao final, você verá:

```
E-mail enviado com sucesso.
```

E o relatório chegará no e-mail configurado.

---

## Estrutura do Banco de Dados

O arquivo `projeto_rpa.db` contém duas tabelas:

* `raw_data`

  * `id` INTEGER PRIMARY KEY
  * `advice` TEXT
* `dados_processados`

  * `id` INTEGER PRIMARY KEY
  * `advice` TEXT
  * `has_pattern` INTEGER (1 se há palavra ≥7 caracteres, 0 caso contrário)

---

## Personalização

* **Regex**: para alterar o critério de processamento, edite a expressão em `pattern = re.compile(r"\b\w{7,}\b")`.
* **Formato do relatório**: modifique a função `generate_report` para gerar HTML ou outro layout.
* **Servidor SMTP**: ajuste `EMAIL_HOST` e `EMAIL_PORT` para outros provedores (Outlook, Yahoo, etc.).

---

## Contribuição

Pull requests são bem-vindos. Para sugestões ou correções, crie uma issue descrevendo a proposta.

---

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
