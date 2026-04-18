import customtkinter as ctk
from Servicios.Vehiculos_serv import listar_vehiculos, crear_vehiculo, editar_vehiculo
from Servicios.Clientes_serv import listar_clientes
from Componentes.Vehiculos import Vehiculo
from Interfaz.Frames.base_frame import BaseFrame

BG_MAIN        = "#0f0f23"
CARD_COLOR     = "#1a1a2e"
ACCENT_COLOR   = "#e94560"
ACCENT_HOVER   = "#c73652"
TEXT_PRIMARY   = "#eaeaea"
TEXT_SECONDARY = "#8888aa"


class VehiculosFrame(BaseFrame):
    title_text      = "Vehículos"
    subtitle_text   = "Registro de vehículos en el taller"
    add_button_text = "+ Nuevo Vehículo"
    columns = [
        ("ID",       55),
        ("Placa",   100),
        ("Marca",   120),
        ("Modelo",  120),
        ("Año",      70),
        ("Color",   100),
        ("Cliente", 160),
    ]

    def _load_data(self):
        try:
            resultados = listar_vehiculos()
            # tupla esperada: (id_vehiculo, placa, marca, modelo, año, color, id_cliente)
            self.rows_data = [
                Vehiculo(
                    id_vehiculo = r[0],
                    placa       = r[1],
                    marca       = r[2],
                    modelo      = r[3],
                    año         = r[4],
                    color       = r[5],
                    id_cliente  = r[6],
                )
                for r in resultados
            ]
            clientes = listar_clientes()
            self.clientes_map = {c[0]: f"{c[1]} {c[2]}" for c in clientes}
        except Exception as e:
            print(f"Error cargando vehículos: {e}")
            self.rows_data    = []
            self.clientes_map = {}
        self._render_rows(self.rows_data)

    def row_values(self, row) -> list:
        nombre_cliente = getattr(self, "clientes_map", {}).get(row.id_cliente, str(row.id_cliente))
        return [
            row.id_vehiculo,
            row.placa,
            row.marca,
            row.modelo,
            row.año,
            row.color,
            nombre_cliente,
        ]

    def on_add(self):
        VehiculoFormModal(self, row=None, clientes_map=getattr(self, "clientes_map", {}), callback=self._load_data)

    def on_edit(self, row):
        VehiculoFormModal(self, row=row, clientes_map=getattr(self, "clientes_map", {}), callback=self._load_data)

    def on_delete(self, row):
        ConfirmarEliminarDialog(
            parent=self,
            nombre=f"{row.placa} - {row.marca} {row.modelo}",
            on_confirm=lambda: self._do_delete(row.id_vehiculo),
        )

    def _do_delete(self, id_vehiculo):
        try:
            from DataBase.conexion import Conexion
            conexion = Conexion().conectar()
            cursor   = conexion.cursor()
            cursor.execute("DELETE FROM vehiculos WHERE id_vehiculo = %s", (id_vehiculo,))
            conexion.commit()
            conexion.close()
        except Exception as e:
            print(f"Error eliminando vehículo: {e}")
        self._load_data()


class VehiculoFormModal(ctk.CTkToplevel):
    def __init__(self, parent, row=None, clientes_map=None, callback=None):
        super().__init__(parent)
        self.row           = row
        self.clientes_map  = clientes_map or {}
        self.callback      = callback
        self.title("Nuevo Vehículo" if row is None else "Editar Vehículo")
        self.geometry("440x640")
        self.resizable(False, False)
        self.configure(fg_color="#1a1a2e")
        self.attributes("-topmost", True)
        self.grab_set()
        self.focus_force()
        self._build()

    def _build(self):
        wrap = ctk.CTkFrame(self, fg_color="transparent")
        wrap.pack(padx=28, pady=24, fill="both", expand=True)

        ctk.CTkLabel(
            wrap,
            text="Nuevo Vehículo" if self.row is None else "Editar Vehículo",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(anchor="w", pady=(0, 18))

        fields = [
            ("Placa",  "placa",  "Ej: ABC123"),
            ("Marca",  "marca",  "Ej: Toyota"),
            ("Modelo", "modelo", "Ej: Corolla"),
            ("Año",    "año",    "Ej: 2020"),
            ("Color",  "color",  "Ej: Rojo"),
        ]

        self.entries = {}
        for label, key, placeholder in fields:
            ctk.CTkLabel(wrap, text=label, font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(anchor="w")
            entry = ctk.CTkEntry(
                wrap,
                placeholder_text=placeholder,
                height=36,
                corner_radius=8,
                fg_color="#0f0f23",
                border_color="#2a2a4a",
                text_color=TEXT_PRIMARY,
                placeholder_text_color="#555577",
            )
            if self.row is not None:
                valor = getattr(self.row, key, "")
                entry.insert(0, str(valor) if valor else "")
            entry.pack(fill="x", pady=(3, 10))
            self.entries[key] = entry

        # Dropdown de clientes
        ctk.CTkLabel(wrap, text="Cliente", font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(anchor="w")

        self.clientes_ids     = list(self.clientes_map.keys())
        self.clientes_nombres = list(self.clientes_map.values())

        selected = ""
        if self.row and self.row.id_cliente in self.clientes_map:
            selected = self.clientes_map[self.row.id_cliente]
        elif self.clientes_nombres:
            selected = self.clientes_nombres[0]

        self.cliente_var = ctk.StringVar(value=selected)
        ctk.CTkOptionMenu(
            wrap,
            values=self.clientes_nombres if self.clientes_nombres else ["Sin clientes"],
            variable=self.cliente_var,
            height=36,
            corner_radius=8,
            fg_color="#0f0f23",
            button_color="#2a2a4a",
            button_hover_color="#3a3a5a",
            text_color=TEXT_PRIMARY,
        ).pack(fill="x", pady=(3, 10))

        self.error_label = ctk.CTkLabel(wrap, text="", font=ctk.CTkFont(size=12), text_color=ACCENT_COLOR)
        self.error_label.pack(anchor="w")

        btn_frame = ctk.CTkFrame(wrap, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(6, 0))
        btn_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            btn_frame, text="Cancelar", height=38, corner_radius=8,
            fg_color="#2a2a4a", hover_color="#3a3a5a", text_color=TEXT_SECONDARY,
            command=self.destroy,
        ).grid(row=0, column=0, padx=(0, 6), sticky="ew")

        ctk.CTkButton(
            btn_frame, text="Guardar", height=38, corner_radius=8,
            fg_color=ACCENT_COLOR, hover_color=ACCENT_HOVER,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._save,
        ).grid(row=0, column=1, padx=(6, 0), sticky="ew")

    def _save(self):
        datos = {k: e.get().strip() for k, e in self.entries.items()}

        if not datos["placa"] or not datos["marca"]:
            self.error_label.configure(text="Placa y marca son obligatorios.")
            return

        nombre_seleccionado = self.cliente_var.get()
        if nombre_seleccionado not in self.clientes_nombres:
            self.error_label.configure(text="Selecciona un cliente válido.")
            return

        id_cliente = self.clientes_ids[self.clientes_nombres.index(nombre_seleccionado)]

        try:
            vehiculo = Vehiculo(
                id_vehiculo = self.row.id_vehiculo if self.row else None,
                placa       = datos["placa"].upper(),
                marca       = datos["marca"],
                modelo      = datos["modelo"],
                año         = datos["año"],
                color       = datos["color"],
                id_cliente  = id_cliente,
            )
            if self.row is None:
                crear_vehiculo(vehiculo)
            else:
                editar_vehiculo(vehiculo)
        except Exception as e:
            self.error_label.configure(text=f"Error: {e}")
            return

        if self.callback:
            self.callback()
        self.destroy()


class ConfirmarEliminarDialog(ctk.CTkToplevel):
    def __init__(self, parent, nombre: str, on_confirm):
        super().__init__(parent)
        self.on_confirm = on_confirm
        self.title("Confirmar eliminación")
        self.geometry("360x200")
        self.resizable(False, False)
        self.configure(fg_color="#1a1a2e")
        self.attributes("-topmost", True)
        self.grab_set()
        self.focus_force()
        self._build(nombre)

    def _build(self, nombre):
        wrap = ctk.CTkFrame(self, fg_color="transparent")
        wrap.pack(padx=28, pady=28, fill="both", expand=True)

        ctk.CTkLabel(
            wrap, text="¿Eliminar vehículo?",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(anchor="w")

        ctk.CTkLabel(
            wrap, text=f'Se eliminará "{nombre}" permanentemente.',
            font=ctk.CTkFont(size=13), text_color=TEXT_SECONDARY, wraplength=300,
        ).pack(anchor="w", pady=(8, 20))

        btn_frame = ctk.CTkFrame(wrap, fg_color="transparent")
        btn_frame.pack(fill="x")
        btn_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            btn_frame, text="Cancelar", height=36, corner_radius=8,
            fg_color="#2a2a4a", hover_color="#3a3a5a", text_color=TEXT_SECONDARY,
            command=self.destroy,
        ).grid(row=0, column=0, padx=(0, 6), sticky="ew")

        ctk.CTkButton(
            btn_frame, text="Sí, eliminar", height=36, corner_radius=8,
            fg_color=ACCENT_COLOR, hover_color=ACCENT_HOVER,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._confirm,
        ).grid(row=0, column=1, padx=(6, 0), sticky="ew")

    def _confirm(self):
        self.destroy()
        self.on_confirm()