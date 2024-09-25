from datetime import datetime
import sqlite3

print("Conectando...")
print("Criando a pasta")
db_path = "database/"
print("Conectando no banco")
conn = sqlite3.connect('database//db.sqlite3')
sql = 'DELETE FROM despesa'
conn.execute(sql)
conn.commit()
sql2 = 'DELETE FROM tipo_despesa'
conn.execute(sql2)
conn.commit()
sql3 = 'INSERT INTO tipo_despesa (descricao, data_insercao) VALUES (?,?)'
dados = [
      ('Conta de Luz', datetime.now().strftime("%Y-%m-%d %H:%M:%S")), 
      ('Alimentação', datetime.now().strftime("%Y-%m-%d %H:%M:%S")), 
      ('Aluguel', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
      ('Cartao de Credito', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
      ('Escola', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),  
      ('Gastos Extras', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),   
      ('Despesas no Exterior(Euro)', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),  
]
conn.executemany(sql3, dados)
conn.commit()
conn.close()