from faker import Faker
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import random

# Carrega variáveis do .env
load_dotenv()

# Cria conexão
engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# Instancia o Faker
fake = Faker("pt_BR")

# --- obter ids de clientes válidos (para FK) ---
try:
    clientes_df = pd.read_sql("SELECT id_cliente FROM clientes;", engine)
    clientes_ids = clientes_df["id_cliente"].tolist()
except Exception as e:
    print("Aviso: não foi possível ler clientes. Usando None para id_cliente.")
    clientes_ids = [None]

# --- gerar N vendas ---
N = 100
produtos_exemplo = ["Notebook", "Mouse", "Teclado", "Monitor", "Cabo", "Fone"]

vendas = []
for _ in range(N):
    id_cliente = random.choice(clientes_ids) if clientes_ids and random.random() > 0.1 else None
    vendas.append({
        "id_cliente": id_cliente,
        "data_venda": fake.date_between(start_date="-1y", end_date="today"),
        "produto": random.choice(produtos_exemplo),
        "quantidade": random.randint(1, 10),
        "preco": round(random.uniform(20.0, 4000.0), 2)
    })

df_vendas = pd.DataFrame(vendas)

# gravar CSV local (opcional)
df_vendas.to_csv("data/fake_vendas.csv", index=False)

# inserir no DB: append para não sobrescrever
with engine.begin() as conn:
    df_vendas.to_sql("vendas", conn, if_exists="append", index=False)

print(f"✅ Inseridas {len(df_vendas)} linhas na tabela 'vendas'.")
