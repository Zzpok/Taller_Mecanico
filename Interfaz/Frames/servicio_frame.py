import customtkinter as ctk
from Servicios.Servicio_serv import listar_servicios, crear_servicio, actualizar_servicio, eliminar_servicio
from Componentes.Servicio import Servicio
from Interfaz.Frames.base_frame import BaseFrame

BG_MAIN        = "#0f0f23"
ACCENT_COLOR   = "#e94560"
ACCENT_HOVER   = "#c73652"
TEXT_PRIMARY   = "#eaeaea"
TEXT_SECONDARY = "#8888aa"


class ServiciosFrame(BaseFrame):
    title_text      = "Servicios"
    subtitle_text   = "Catálogo de servicios disponibles"
    add_button_text = "+ Nuevo Servicio"
    columns = [
        ("ID",           55),
        ("Nombre",      180),
        ("Descripción", 300),
        ("Costo",       100),
    ]

    def _load_data(self):
        try:
            resultados = listar_servicios()
            # tupla: (id_servicio, nombre, descripcion, costo)
            self.rows_data = [
                Servicio(
                    id_servicio = r[0],
                    nombre      = r[1],
                    descripcion = r[2],
                    costo       = r[3],
                )
                for r in resultados
            ]
        except Exception as e:
            print(f"Error cargando servicios: {e}")
            self.rows_data = []
        self._render_rows(self.rows_data)

    def row_values(self, row) -> list:
        return [
            row.id_servicio,
            row.nombre,
            row.descripcion,
            f"${float(row.costo):,.0f}" if row.costo else "$0",
        ]

    def on_add(self):
        ServicioFormModal(self, row=None, callback=self._load_data)

    def on_edit(self, row):
        ServicioFormModal(self, row=row, callback=self._load_data)

    def on_delete(self, row):
        ConfirmarEliminarDialog(
            parent=self,
            nombre=row.nombre,
            on_confirm=lambda: self._do_delete(row.id_servicio),
        )

    def _do_delete(self, id_servicio):
        try:
            eliminar_servicio(id_servicio)
        except Exception as e:
            print(f"Error eliminando servicio: {e}")
        self._load_data()


class ServicioFormModal(ctk.CTkToplevel):
    def __init__(self, parent, row=None, callback=None):
        super().__init__(parent)
        self.row      = row
        self.callback = callback
        self.title("Nuevo Servicio" if row is None else "Editar Servicio")
        self.geometry("440x470")
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
            text="Nuevo Servicio" if self.row is None else "Editar Servicio",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(anchor="w", pady=(0, 18))

        ctk.CTkLabel(wrap, text="Nombre", font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(anchor="w")
        self.nombre_entry = ctk.CTkEntry(
            wrap, placeholder_text="Ej: Cambio de aceite",
            height=36, corner_radius=8,
            fg_color="#0f0f23", border_color="#2a2a4a",
            text_color=TEXT_PRIMARY, placeholder_text_color="#555577",
        )
        if self.row:
            self.nombre_entry.insert(0, self.row.nombre or "")
        self.nombre_entry.pack(fill="x", pady=(3, 10))

        ctk.CTkLabel(wrap, text="Descripción", font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(anchor="w")
        self.descripcion_entry = ctk.CTkTextbox(
            wrap, height=80, corner_radius=8,
            fg_color="#0f0f23", border_color="#2a2a4a", border_width=1,
            text_color=TEXT_PRIMARY,
        )
        if self.row and self.row.descripcion:
            self.descripcion_entry.insert("1.0", self.row.descripcion)
        self.descripcion_entry.pack(fill="x", pady=(3, 10))

        ctk.CTkLabel(wrap, text="Costo", font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(anchor="w")
        self.costo_entry = ctk.CTkEntry(
            wrap, placeholder_text="Ej: 50000",
            height=36, corner_radius=8,
            fg_color="#0f0f23", border_color="#2a2a4a",
            text_color=TEXT_PRIMARY, placeholder_text_color="#555577",
        )
        if self.row:
            self.costo_entry.insert(0, str(self.row.costo) if self.row.costo else "")
        self.costo_entry.pack(fill="x", pady=(3, 10))

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
        nombre      = self.nombre_entry.get().strip()
        descripcion = self.descripcion_entry.get("1.0", "end").strip()
        costo_str   = self.costo_entry.get().strip()

        if not nombre:
            self.error_label.configure(text="El nombre es obligatorio.")
            return

        try:
            costo = float(costo_str) if costo_str else 0
        except ValueError:
            self.error_label.configure(text="El costo debe ser un número.")
            return

        try:
            servicio = Servicio(
                id_servicio = self.row.id_servicio if self.row else None,
                nombre      = nombre,
                descripcion = descripcion,
                costo       = costo,
            )
            if self.row is None:
                crear_servicio(servicio)
            else:
                actualizar_servicio(servicio)
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
        self.geometry("360x270")
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
            wrap, text="¿Eliminar servicio?",
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