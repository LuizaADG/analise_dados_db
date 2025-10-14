import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

#print("DB_USER:", os.getenv("DB_USER"))
#print("DB_PASS:", os.getenv("DB_PASS"))
#print("DB_HOST:", os.getenv("DB_HOST"))
#print("DB_PORT:", os.getenv("DB_PORT"))
#print("DB_NAME:", os.getenv("DB_NAME"))

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Criar engine de conexão
engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Testar conexão
with engine.connect() as conn:
    print("✅ Conexão com PostgreSQL estabelecida com sucesso!")
    # Criar tabela e inserir dados de exemplo
    data = {
        'produto': ['Notebook', 'Mouse', 'Teclado', 'Monitor'],
        'quantidade': [10, 25, 15, 8],
        'preco': [3500, 80, 120, 900]
    }
    df = pd.DataFrame(data)
    df.to_sql('vendas', conn, if_exists='replace', index=False)
    print("📦 Tabela 'vendas' criada e populada com sucesso!")