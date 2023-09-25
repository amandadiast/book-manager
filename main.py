import tkinter as tk
import tkinter.ttk
from tkinter import messagebox
# estilizar botões mais tarde
from tkinter import PhotoImage
import sqlite3
import Databaser

# JANELA DE LOGIN -----------------------------------------------------
class Application(tk.Frame):
    """"Classe pai com janela principal"""""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.parent.geometry("500x400")
        self.configure(background="#592C22")
        self.parent.resizable(width=False, height=False)
        self.logo_image = tk.PhotoImage(file="bm.png")
        self.pack(expand=True, fill="both")
        self.widgets()

    def widgets(self):
        self.logo_label = tk.Label(self, image=self.logo_image, bg="white")
        self.logo_label.pack()

        self.title_label = tk.Label(self, fg="#D9B166", bg="#592C22", font=("Arial", 20, "bold"), text='BOOK MANAGER')
        self.title_label.pack(side="top", pady=10)

        self.username_label = tk.Label(self, bg="#592C22", font=("Charter BT", 14), text="Usuário:")
        self.username_label.pack()

        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=10)

        self.password_label = tk.Label(self, bg="#592C22", font=("Arial", 14), text="Senha:")
        self.password_label.pack()

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=10)  # Espaçamento entre senha e registro

        self.register_button = tk.Button(self, text="Registrar usuário", bg="#D9B166", width=20, command=self.register_window)
        self.register_button.pack()

        self.login_button = tk.Button(self, text="Login", bg="#D9B166", width=20, command=self.validate_credentials)
        self.login_button.pack()

        self.quit_button = tk.Button(self, text="SAIR", fg="red", bg="#D9B166", command=self.parent.destroy)
        self.quit_button.pack()


    def register_window(self):
        register_window = Register(self.parent)

    def validate_credentials(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Verificar se o usuário está registrado
        with Databaser.conn:  # Para usar o databaser
            cursor = Databaser.conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()
        if user:
            login_window = BookManager(self)
            self.hide_application()
        else:
            messagebox.showerror(title="Login Failed", message="Invalid credentials")

    def hide_application(self):
        self.parent.iconify()  # Minimiza a janela "Application"


# REGISTRO DE USUARIO -----------------------------------------------------
class Register(tk.Toplevel):
    """"Classe para registro de usuario"""""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("REGISTRO DE USUÁRIO")
        self.geometry("400x200")
        self.resizable(width=False, height=False)
        self.widgets()

    def widgets(self):
        self.name_label = tk.Label(self, text="Nome: ")
        self.name_label.pack()

        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        self.username_label = tk.Label(self, text="Usuário: ")
        self.username_label.pack()

        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        self.password_label = tk.Label(self, text="Senha: ")
        self.password_label.pack()

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        self.register_button = tk.Button(self, text="Registrar", command=self.register_db)
        self.register_button.pack()

    def register_db(self):
        # Função de registro do usuário
        Username = self.username_entry.get()
        Password = self.password_entry.get()
        Databaser.cursor.execute('''
        Insert into users(Username, Password) VALUES(?, ?)
        ''', (Username, Password))
        Databaser.conn.commit()
        # Databaser.conn.close()
        messagebox.showinfo(title="Register Info", message="Register Sucefull")

# JANELA PRINCIPAL -----------------------------------------------------
class BookManager(tk.Toplevel):
    """Classe utilizada para abrir janela 2 (gerenciador  de livros) herdada da janela 1 (login)"""""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("GERENCIADOR DE LIVROS")
        self.geometry("1020x500")
        self.resizable(width=False, height=False)
        self.widgets()
        self.preencher_tabela()

    def widgets(self):
        self.title_label = tk.Label(self, text="GERENCIADOR DE LIVROS")
        self.title_label.pack()

        self.bookregistration = tk.Button(self, text="Registre um Livro", width=20, command=self.windowregbook)
        self.bookregistration.pack()

        self.back_login = tk.Button(self, text="Volte para o Login", width=20, command=self.back_login)
        self.back_login.pack()

        #tabela aparecendo na janela principal
        self.tabela_livros = tkinter.ttk.Treeview(self, columns=("ID", "Autor", "Nome do Livro", "Nota"))
        self.tabela_livros.heading("#1", text="ID")
        self.tabela_livros.heading("#2", text="Autor")
        self.tabela_livros.heading("#3", text="Nome do Livro")
        self.tabela_livros.heading("#4", text="Nota")

        # Desativar a coluna em branco
        self.tabela_livros.config(show="headings")
        self.tabela_livros.pack(fill="both", expand=True)

        self.tabela_livros.pack()

#---
    # Edição tabela

    def edit_item(self):  # Edição de cada entry
        pass

#---
    def back_login(self):
        self.withdraw()

    def windowregbook(self):
        windowregbook = BookRegistration(self)

    def preencher_tabela(self):
        for v in self.tabela_livros.get_children():
            self.tabela_livros.delete(v)
        with Databaser.conn:
            cursor = Databaser.conn.cursor()
            cursor.execute("SELECT id, Autor, NomeLivro, NotaLivro FROM books")
            books = cursor.fetchall()
        for book in books:
            item = self.tabela_livros.insert("", "end", values=book)

# CADASTRAR LIVRO -----------------------------------------------------
class BookRegistration(tk.Toplevel):
    """"Classe usada para registro das informações (autor, titulo do livro e nota) conectadas ao banco de dados"""""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title("REGISTRO DE LIVRO")
        self.geometry("400x200")
        self.configure(background="#592C22")
        self.resizable(height=False, width=False)
        self.widgets()

    def widgets(self):

        self.autor_label = tk.Label(self, bg="#D9B166", width=12, text="Autor: ")
        self.autor_label.pack()

        self.autor_entry = tk.Entry(self)
        self.autor_entry.pack()

        self.nomelivro_label = tk.Label(self, bg="#D9B166", width=12, text="Nome do Livro: ")
        self.nomelivro_label.pack()

        self.nomelivro_entry = tk.Entry(self)
        self.nomelivro_entry.pack()

        self.notalivro_label = tk.Label(self, bg="#D9B166", width=12, text="Nota: ")
        self.notalivro_label.pack()

        self.notalivro_entry= tk.Entry(self)
        self.notalivro_entry.pack()

        self.regbook_button = tk.Button(self, bg="#D9B166", width=15, text="Registrar", command=self.regbook_db)
        self.regbook_button.pack()

        self.quit_button = tk.Button(self, text="SAIR", fg="red", bg="#D9B166", command=self.destroy)
        self.quit_button.pack()

    def regbook_db(self):
        try:
            Autor = self.autor_entry.get()
            NomeLivro = self.nomelivro_entry.get()
            NotaLivro = self.notalivro_entry.get()
            Databaser.cursor.execute('''
            Insert into books(Autor, NomeLivro, NotaLivro) VALUES(?, ?, ?)
            ''', (Autor, NomeLivro, NotaLivro))
            Databaser.conn.commit()
        except sqlite3.IntegrityError:
                messagebox.showinfo(title="Register Info", message="ERROR")
        finally:
                messagebox.showinfo(title="Register Info", message="Book Register Sucefull")
                #após registrar o livro no banco de dados, atualiza a tabela
                self.master.preencher_tabela()


root = tk.Tk()
window = Application(parent=root)  # passa a classe application para a janela principal
window.mainloop()
