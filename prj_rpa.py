# -*- coding: utf-8 -*-
"""
Projeto Prático de RPA
Aluno: <Seu Nome>
Descrição: Automação que coleta conselhos aleatórios da Advice Slip API,
armazena dados em SQLite, processa textos verificando padrões com regex
e envia um relatório por e-mail incluindo as frases coletadas, sem armazenar senha no código.
"""

import os
import requests
import sqlite3
import re
import smtplib
import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


API_URL          = "https://api.adviceslip.com/advice" 
DB_NAME          = "projeto_rpa.db"

EMAIL_HOST       = "smtp.gmail.com"
EMAIL_PORT       = 587
EMAIL_HOST_USER  = os.getenv("SMTP_USER") or input("Digite seu e-mail (SMTP_USER): ")
EMAIL_FROM       = EMAIL_HOST_USER
EMAIL_TO         = os.getenv("EMAIL_TO") or input("Digite o e-mail destinatário (EMAIL_TO): ")


def fetch_data():
    """
    Faz requisição à API e retorna lista de registros com campos relevantes.
    """
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json().get("slip", {})
    return [{
        "id": data.get("id"),
        "advice": data.get("advice")
    }]

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS raw_data (
            id INTEGER PRIMARY KEY,
            advice TEXT
        )
        '''
    )
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS dados_processados (
            id INTEGER PRIMARY KEY,
            advice TEXT,
            has_pattern INTEGER
        )
        '''
    )
    conn.commit()
    conn.close()


def store_raw_data(records):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    for rec in records:
        cursor.execute(
            'INSERT OR IGNORE INTO raw_data (id, advice) VALUES (?, ?)',
            (rec["id"], rec["advice"])
        )
    conn.commit()
    conn.close()

def process_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, advice FROM raw_data')
    rows = cursor.fetchall()

    processed = []
    pattern = re.compile(r"\b\w{7,}\b")  
    for id_, advice in rows:
        has_long_word = bool(pattern.search(advice))
        processed.append((id_, advice, int(has_long_word)))

    cursor.executemany(
        '''
        INSERT OR REPLACE INTO dados_processados (id, advice, has_pattern)
        VALUES (?, ?, ?)
        ''', processed
    )
    conn.commit()
    conn.close()
    return processed

def generate_report(processed):
    total = len(processed)
    matches = sum(item[2] for item in processed)
    report_lines = [
        "Relatório de Dados - Projeto RPA",
        f"Total de registros coletados: {total}",
        f"Registros com palavra de 7+ caracteres: {matches}",
        "", 
        "Frases coletadas:"
    ]
    for _, advice, _ in processed:
        report_lines.append(f"- {advice}")

    return "\n".join(report_lines)

def send_email(report):
    password = getpass.getpass("Digite sua App Password do Gmail: ") # SENHA:gnza kqyc anfr wwrx
                                                                     # EMAIL: rpaprojeto91@gmail.com
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg['Subject'] = "[Projeto RPA] Relatório de Execução"
    msg.attach(MIMEText(report, 'plain'))

    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.starttls()
        server.login(EMAIL_HOST_USER, password)
        server.send_message(msg)

    print("E-mail enviado com sucesso.")

def main():
    init_db()
    records = fetch_data()
    store_raw_data(records)
    processed = process_data()
    report = generate_report(processed)
    send_email(report)

if __name__ == '__main__':
    main()
