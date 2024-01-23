import csv
import random
from datetime import datetime, timedelta

def gerar_dados_csv(numero_registros):
    categorias = ['alimentação', 'transporte', 'lazer', 'saúde', 'serviços', 'outros']
    pagamentos = ['crédito', 'débito']

    with open('expenses.csv', 'w', newline='') as arquivo_csv:
        campo_nomes = ['DATA', 'VALOR', 'CATEGORIA', 'DESCRIÇÃO', 'PAGAMENTO']
        escritor_csv = csv.DictWriter(arquivo_csv, fieldnames=campo_nomes)
        escritor_csv.writeheader()

        for _ in range(numero_registros):
            data = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%d/%m/%Y')
            valor = f'R$ {random.uniform(1, 100):.2f}'
            categoria = random.choice(categorias)
            descricao = ' '.join([categoria] + [f'palavra{i}' for i in range(random.randint(1, 5))])
            pagamento = random.choice(pagamentos)

            escritor_csv.writerow({
                'DATA': data,
                'VALOR': valor,
                'CATEGORIA': categoria,
                'DESCRIÇÃO': descricao,
                'PAGAMENTO': pagamento
            })

if __name__ == "__main__":
    numero_registros = 100  # Defina o número desejado de registros
    gerar_dados_csv(numero_registros)
    print(f'{numero_registros} registros gerados com sucesso no arquivo "expenses.csv".')
