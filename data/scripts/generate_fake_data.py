from faker import Faker
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# Cria conexão
engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# Instancia o Faker
fake = Faker("pt_BR")

# Gera dados
data = []
for _ in range(100):  # número de registros
    data.append({
        "id_cliente": _ + 1,
        "nome": fake.name(),
        "email": fake.email(),
        "cidade": fake.city(),
        "data_cadastro": fake.date_between(start_date="-2y", end_date="today"),
        "valor_gasto": round(fake.random_number(digits=4) * 1.2, 2)
    })

# Cria DataFrame
df = pd.DataFrame(data)

# Salva em CSV (opcional)
df.to_csv("data/clientes.csv", index=False)

# Envia pro banco
with engine.connect() as conn:
    df.to_sql("clientes", conn, if_exists="replace", index=False)
    print("✅ Dados fake inseridos com sucesso!")
