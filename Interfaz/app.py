import tkinter as tk

def iniciar(usuario):
    root = tk.Tk()
    root.title("Sistema Taller Mecánico")
    root.geometry("500x400")

    tk.Label(root, text=f"Bienvenido {usuario.username}", font=("Arial", 14)).pack(pady=20)

    # 🔹 Botones principales
    tk.Button(root, text="Órdenes de Trabajo").pack(pady=5)
    tk.Button(root, text="Clientes").pack(pady=5)
    tk.Button(root, text="Vehículos").pack(pady=5)
    tk.Button(root, text="Facturación").pack(pady=5)

    root.mainloop()