#from DataBase.conexion import Conexion

#conexion = Conexion().conectar()

#if conexion:
#    print("✅ Conexión exitosa")

#else:
    #print("❌ Error de conexión")

import tkinter as tk

root = tk.Tk()
root.title("Prueba")
root.geometry("300x200")

tk.Label(root, text="Funciona").pack()

root.mainloop()