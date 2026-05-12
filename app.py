import customtkinter as ctk
from Autenticacion.login_window import LoginWindow
from Interfaz.main_window import MainWindow

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

if __name__ == "__main__":
    login = LoginWindow()
    login.mainloop()

    if login.usuario:
        app = MainWindow(login.usuario)
        app.mainloop()  