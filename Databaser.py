import sqlite3

# REGISTRO DE USUARIO

conn = sqlite3.connect("bookmanager_database.db")
cursor = conn.cursor()
cursor.execute('''
          CREATE TABLE IF NOT EXISTS users (
              id INTEGER PRIMARY KEY,
              username TEXT NOT NULL,
              password TEXT NOT NULL
          )
      ''')

# REGISTRO DE LIVRO

cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            autor TEXT NOT NULL,
            nomelivro TEXT NOT NULL,
            notalivro TEXT NOT NULL 
            )
        ''')



print('DATABASE CONNECTED')


