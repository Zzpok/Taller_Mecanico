import customtkinter as ctk
from Servicios.Repuestos_serv import listar_repuestos, crear_repuesto, actualizar_repuesto, eliminar_repuesto
from Componentes.Repuestos import Repuestos
from Interfaz.Frames.base_frame import BaseFrame

BG_MAIN        = "#0f0f23"
ACCENT_COLOR   = "#e94560"
ACCENT_HOVER   = "#c73652"
TEXT_PRIMARY   = "#eaeaea"
TEXT_SECONDARY = "#8888aa"


class RepuestosFrame(BaseFrame):
    title_text      = "Repuestos"
    subtitle_text   = "Inventario de repuestos y piezas"
    add_button_text = "+ Nuevo Repuesto"
    columns = [
        ("ID",       55),
        ("Nombre",  200),
        ("Marca",   150),
        ("Stock",    80),
        ("Precio",  100),
    ]

    def _load_data(self):
        try:
            resultados = listar_repuestos()
            # tupla: (id_repuesto, nombre, marca, stock, precio)
            self.rows_data = [
                Repuestos(
                    id_repuesto = r[0],
                    nombre      = r[1],
                    marca       = r[2],
                    stock       = r[3],
                    precio      = r[4],
                )
                for r in resultados
            ]
        except Exception as e:
            print(f"Error cargando repuestos: {e}")
            self.rows_data = []
        self._render_rows(self.rows_data)

    def row_values(self, row) -> list:
        # Muestra advertencia si el stock es bajo
        stock_texto = f"⚠ {row.stock}" if isinstance(row.stock, int) and row.stock < 5 else str(row.stock)
        return [
            row.id_repuesto,
            row.nombre,
            row.marca,
            stock_texto,
            f"${float(row.precio):,.0f}" if row.precio else "$0",
        ]

    def on_add(self):
        RepuestoFormModal(self, row=None, callback=self._load_data)

    def on_edit(self, row):
        RepuestoFormModal(self, row=row, callback=self._load_data)

    def on_delete(self, row):
        ConfirmarEliminarDialog(
            parent=self,
            nombre=row.nombre,
            on_confirm=lambda: self._do_delete(row.id_repuesto),
        )

    def _do_delete(self, id_repuesto):
        try:
            eliminar_repuesto(id_repuesto)
        except Exception as e:
            print(f"Error eliminando repuesto: {e}")
        self._load_data()


class RepuestoFormModal(ctk.CTkToplevel):
    def __init__(self, parent, row=None, callback=None):
        super().__init__(parent)
        self.row      = row
        self.callback = callback
        self.title("Nuevo Repuesto" if row is None else "Editar Repuesto")
        self.geometry("440x480")
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
            text="Nuevo Repuesto" if self.row is None else "Editar Repuesto",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(anchor="w", pady=(0, 18))

        fields = [
            ("Nombre", "nombre", "Ej: Filtro de aceite"),
            ("Marca",  "marca",  "Ej: Bosch"),
            ("Stock",  "stock",  "Ej: 10"),
            ("Precio", "precio", "Ej: 25000"),
        ]

        self.entries = {}
        for label, key, placeholder in fields:
            ctk.CTkLabel(wrap, text=label, font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(anchor="w")
            entry = ctk.CTkEntry(
                wrap, placeholder_text=placeholder,
                height=36, corner_radius=8,
                fg_color="#0f0f23", border_color="#2a2a4a",
                text_color=TEXT_PRIMARY, placeholder_text_color="#555577",
            )
            if self.row is not None:
                valor = getattr(self.row, key, "")
                entry.insert(0, str(valor) if valor is not None else "")
            entry.pack(fill="x", pady=(3, 10))
            self.entries[key] = entry

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

        if not datos["nombre"]:
            self.error_label.configure(text="El nombre es obligatorio.")
            return

        try:
            stock  = int(datos["stock"])    if datos["stock"]  else 0
            precio = float(datos["precio"]) if datos["precio"] else 0
        except ValueError:
            self.error_label.configure(text="Stock debe ser entero y precio un número.")
            return

        try:
            repuesto = Repuestos(
                id_repuesto = self.row.id_repuesto if self.row else None,
                nombre      = datos["nombre"],
                marca       = datos["marca"],
                stock       = stock,
                precio      = precio,
            )
            if self.row is None:
                crear_repuesto(repuesto)
            else:
                actualizar_repuesto(repuesto)
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
            wrap, text="¿Eliminar repuesto?",
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