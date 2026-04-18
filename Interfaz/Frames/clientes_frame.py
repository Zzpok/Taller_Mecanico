import customtkinter as ctk
from Servicios.Clientes_serv import listar_clientes, crear_cliente, actualizar_cliente, eliminar_cliente
from Componentes.Clientes import Cliente
from Interfaz.Frames.base_frame import BaseFrame

BG_MAIN        = "#0f0f23"
CARD_COLOR     = "#1a1a2e"
ACCENT_COLOR   = "#e94560"
ACCENT_HOVER   = "#c73652"
TEXT_PRIMARY   = "#eaeaea"
TEXT_SECONDARY = "#8888aa"


class ClientesFrame(BaseFrame):
    title_text      = "Clientes"
    subtitle_text   = "Gestión de clientes registrados"
    add_button_text = "+ Nuevo Cliente"
    columns = [
        ("ID",         55),
        ("Nombre",    140),
        ("Apellido",  130),
        ("Teléfono",  120),
        ("Correo",    200),
        ("Dirección", 190),
    ]

    def _load_data(self):
        try:
            resultados = listar_clientes()
            # listar_clientes() retorna tuplas: (id, nombre, apellido, telefono, correo, direccion)
            self.rows_data = [
                Cliente(
                    id_cliente = r[0],
                    nombre     = r[1],
                    apellido   = r[2],
                    telefono   = r[3],
                    correo     = r[4],
                    direccion  = r[5],
                )
                for r in resultados
            ]
        except Exception as e:
            print(f"Error cargando clientes: {e}")
            self.rows_data = []
        self._render_rows(self.rows_data)

    def row_values(self, row) -> list:
        return [
            row.id_cliente,
            row.nombre,
            row.apellido,
            row.telefono,
            row.correo,
            row.direccion,
        ]

    def on_add(self):
        ClienteFormModal(self, row=None, callback=self._load_data)

    def on_edit(self, row):
        ClienteFormModal(self, row=row, callback=self._load_data)

    def on_delete(self, row):
        ConfirmarEliminarDialog(
            parent=self,
            nombre=f"{row.nombre} {row.apellido}",
            on_confirm=lambda: self._do_delete(row.id_cliente),
        )

    def _do_delete(self, id_cliente):
        try:
            eliminar_cliente(id_cliente)
        except Exception as e:
            print(f"Error eliminando cliente: {e}")
        self._load_data()


class ClienteFormModal(ctk.CTkToplevel):
    def __init__(self, parent, row=None, callback=None):
        super().__init__(parent)
        self.row      = row
        self.callback = callback
        self.title("Nuevo Cliente" if row is None else "Editar Cliente")
        self.geometry("440x560")
        self.resizable(False, False)
        self.configure(fg_color="#1a1a2e")
        self.grab_set()
        self.after(50, self.lift)
        self._build()

    def _build(self):
        wrap = ctk.CTkFrame(self, fg_color="transparent")
        wrap.pack(padx=28, pady=24, fill="both", expand=True)

        ctk.CTkLabel(
            wrap,
            text="Nuevo Cliente" if self.row is None else "Editar Cliente",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(anchor="w", pady=(0, 18))

        # (label, atributo_del_objeto, placeholder)
        fields = [
            ("Nombre",    "nombre",    "Ej: Juan"),
            ("Apellido",  "apellido",  "Ej: Pérez"),
            ("Teléfono",  "telefono",  "Ej: 3001234567"),
            ("Correo",    "correo",     "Ej: juan@correo.com"),
            ("Dirección", "direccion", "Ej: Calle 10 # 5-20"),
        ]

        self.entries = {}
        for label, key, placeholder in fields:
            ctk.CTkLabel(
                wrap,
                text=label,
                font=ctk.CTkFont(size=12),
                text_color=TEXT_SECONDARY,
            ).pack(anchor="w")

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

        self.error_label = ctk.CTkLabel(
            wrap,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=ACCENT_COLOR,
        )
        self.error_label.pack(anchor="w")

        btn_frame = ctk.CTkFrame(wrap, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(6, 0))
        btn_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            height=38,
            corner_radius=8,
            fg_color="#2a2a4a",
            hover_color="#3a3a5a",
            text_color=TEXT_SECONDARY,
            command=self.destroy,
        ).grid(row=0, column=0, padx=(0, 6), sticky="ew")

        ctk.CTkButton(
            btn_frame,
            text="Guardar",
            height=38,
            corner_radius=8,
            fg_color=ACCENT_COLOR,
            hover_color=ACCENT_HOVER,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._save,
        ).grid(row=0, column=1, padx=(6, 0), sticky="ew")

    def _save(self):
        datos = {k: e.get().strip() for k, e in self.entries.items()}

        if not datos["nombre"] or not datos["apellido"]:
            self.error_label.configure(text="Nombre y apellido son obligatorios.")
            return

        try:
            cliente = Cliente(
                id_cliente = self.row.id_cliente if self.row else None,
                nombre     = datos["nombre"],
                apellido   = datos["apellido"],
                telefono   = datos["telefono"],
                correo     = datos["correo"],
                direccion  = datos["direccion"],
            )

            if self.row is None:
                crear_cliente(cliente)
            else:
                actualizar_cliente(cliente)

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
        self.grab_set()
        self.after(50, self.lift)
        self._build(nombre)

    def _build(self, nombre):
        wrap = ctk.CTkFrame(self, fg_color="transparent")
        wrap.pack(padx=28, pady=28, fill="both", expand=True)

        ctk.CTkLabel(
            wrap,
            text="¿Eliminar cliente?",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(anchor="w")

        ctk.CTkLabel(
            wrap,
            text=f'Se eliminará a "{nombre}" permanentemente.',
            font=ctk.CTkFont(size=13),
            text_color=TEXT_SECONDARY,
            wraplength=300,
        ).pack(anchor="w", pady=(8, 20))

        btn_frame = ctk.CTkFrame(wrap, fg_color="transparent")
        btn_frame.pack(fill="x")
        btn_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            height=36,
            corner_radius=8,
            fg_color="#2a2a4a",
            hover_color="#3a3a5a",
            text_color=TEXT_SECONDARY,
            command=self.destroy,
        ).grid(row=0, column=0, padx=(0, 6), sticky="ew")

        ctk.CTkButton(
            btn_frame,
            text="Sí, eliminar",
            height=36,
            corner_radius=8,
            fg_color=ACCENT_COLOR,
            hover_color=ACCENT_HOVER,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._confirm,
        ).grid(row=0, column=1, padx=(6, 0), sticky="ew")

    def _confirm(self):
        self.destroy()
        self.on_confirm()
