import pandas as pd
import random
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from sqlalchemy import text

load_dotenv()
engine = create_engine(f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")

# pega ids válidos
clientes_df = pd.read_sql("SELECT id_cliente FROM clientes;", engine)
ids = clientes_df["id_cliente"].tolist()

# pega vendas NULL
vendas_null = pd.read_sql("SELECT * FROM vendas WHERE id_cliente IS NULL;", engine)

with engine.begin() as conn:
        for idx, row in vendas_null.iterrows():
            conn.execute(
                text(
                    "UPDATE vendas SET id_cliente = :id_cliente WHERE id_venda = :id_venda"
                ),
                {"id_cliente": random.choice(ids), "id_venda": row["id_venda"]}
            )