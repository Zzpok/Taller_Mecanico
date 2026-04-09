import tkinter as tk
from tkinter import messagebox
from Autenticacion.Autenticacion_serv import login


def iniciar_sesion():
    username = entry_user.get()
    password = entry_pass.get()

    if not username or not password:
        messagebox.showwarning("Error", "Campos vacíos")
        return

    usuario = login(username, password)

    if usuario:
        ventana.destroy()
        abrir_app(usuario)
    else:
        messagebox.showerror("Error", "Datos incorrectos")


def abrir_app(usuario):
    import Interfaz.app as app
    app.iniciar(usuario)


ventana = tk.Tk()
ventana.title("Login - Taller")
ventana.geometry("300x220")

tk.Label(ventana, text="Usuario").pack(pady=5)
entry_user = tk.Entry(ventana)
entry_user.pack()

tk.Label(ventana, text="Contraseña").pack(pady=5)
entry_pass = tk.Entry(ventana, show="*")
entry_pass.pack()

tk.Button(ventana, text="Ingresar", command=iniciar_sesion).pack(pady=15)

ventana.mainloop()