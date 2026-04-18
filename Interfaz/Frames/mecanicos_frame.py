import customtkinter as ctk
from Servicios.Mecanico_serv import listar_mecanicos, crear_mecanico, actualizar_mecanico, eliminar_mecanico
from Componentes.Mecanico import Mecanico
from Interfaz.Frames.base_frame import BaseFrame

BG_MAIN        = "#0f0f23"
ACCENT_COLOR   = "#e94560"
ACCENT_HOVER   = "#c73652"
TEXT_PRIMARY   = "#eaeaea"
TEXT_SECONDARY = "#8888aa"

ESPECIALIDADES   = ["Mecánica general", "Electricidad", "Frenos", "Motor", "Suspensión", "Transmisión", "Aire acondicionado", "Otra"]
DISPONIBILIDADES = ["disponible", "no_disponible"]


class MecanicosFrame(BaseFrame):
    title_text      = "Mecánicos"
    subtitle_text   = "Gestión del personal técnico"
    add_button_text = "+ Nuevo Mecánico"
    columns = [
        ("ID",              55),
        ("Nombre",         130),
        ("Apellido",       130),
        ("Especialidad",   180),
        ("Disponibilidad", 130),
        ("Salario",        100),
    ]

    def _load_data(self):
        try:
            resultados = listar_mecanicos()
            self.rows_data = [
                Mecanico(
                    id_mecanico    = r[0],
                    nombre         = r[1],
                    apellido       = r[2],
                    especialidad   = r[3],
                    disponibilidad = r[4],
                    salario        = r[5],
                )
                for r in resultados
            ]
        except Exception as e:
            print(f"Error cargando mecánicos: {e}")
            self.rows_data = []
        self._render_rows(self.rows_data)

    def row_values(self, row) -> list:
        return [
            row.id_mecanico,
            row.nombre,
            row.apellido,
            row.especialidad,
            row.disponibilidad,
            f"${row.salario:,.0f}" if row.salario else "$0",
        ]

    def on_add(self):
        MecanicoFormModal(self, row=None, callback=self._load_data)

    def on_edit(self, row):
        MecanicoFormModal(self, row=row, callback=self._load_data)

    def on_delete(self, row):
        ConfirmarEliminarDialog(
            parent=self,
            nombre=f"{row.nombre} {row.apellido}",
            on_confirm=lambda: self._do_delete(row.id_mecanico),
        )

    def _do_delete(self, id_mecanico):
        try:
            eliminar_mecanico(id_mecanico)
        except Exception as e:
            print(f"Error eliminando mecánico: {e}")
        self._load_data()


class MecanicoFormModal(ctk.CTkToplevel):
    def __init__(self, parent, row=None, callback=None):
        super().__init__(parent)
        self.row      = row
        self.callback = callback
        self.title("Nuevo Mecánico" if row is None else "Editar Mecánico")
        self.geometry("440x560")
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
            text="Nuevo Mecánico" if self.row is None else "Editar Mecánico",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(anchor="w", pady=(0, 18))

        fields = [
            ("Nombre",   "nombre",   "Ej: Carlos"),
            ("Apellido", "apellido", "Ej: Gómez"),
            ("Salario",  "salario",  "Ej: 1500000"),
        ]

        self.entries = {}
        for label, key, placeholder in fields:
            ctk.CTkLabel(wrap, text=label, font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(anchor="w")
            entry = ctk.CTkEntry(
                wrap, placeholder_text=placeholder, height=36, corner_radius=8,
                fg_color="#0f0f23", border_color="#2a2a4a",
                text_color=TEXT_PRIMARY, placeholder_text_color="#555577",
            )
            if self.row is not None:
                valor = getattr(self.row, key, "")
                entry.insert(0, str(valor) if valor else "")
            entry.pack(fill="x", pady=(3, 10))
            self.entries[key] = entry

        ctk.CTkLabel(wrap, text="Especialidad", font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(anchor="w")
        self.especialidad_var = ctk.StringVar(value=self.row.especialidad if self.row else ESPECIALIDADES[0])
        ctk.CTkOptionMenu(
            wrap, values=ESPECIALIDADES, variable=self.especialidad_var,
            height=36, corner_radius=8, fg_color="#0f0f23",
            button_color="#2a2a4a", button_hover_color="#3a3a5a", text_color=TEXT_PRIMARY,
        ).pack(fill="x", pady=(3, 10))

        ctk.CTkLabel(wrap, text="Disponibilidad", font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(anchor="w")
        self.disponibilidad_var = ctk.StringVar(value=self.row.disponibilidad if self.row else DISPONIBILIDADES[0])
        ctk.CTkOptionMenu(
            wrap, values=DISPONIBILIDADES, variable=self.disponibilidad_var,
            height=36, corner_radius=8, fg_color="#0f0f23",
            button_color="#2a2a4a", button_hover_color="#3a3a5a", text_color=TEXT_PRIMARY,
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

        if not datos["nombre"] or not datos["apellido"]:
            self.error_label.configure(text="Nombre y apellido son obligatorios.")
            return

        try:
            salario = float(datos["salario"]) if datos["salario"] else 0
        except ValueError:
            self.error_label.configure(text="El salario debe ser un número.")
            return

        try:
            mecanico = Mecanico(
                id_mecanico    = self.row.id_mecanico if self.row else None,
                nombre         = datos["nombre"],
                apellido       = datos["apellido"],
                especialidad   = self.especialidad_var.get(),
                disponibilidad = self.disponibilidad_var.get(),
                salario        = salario,
            )
            if self.row is None:
                crear_mecanico(mecanico)
            else:
                actualizar_mecanico(mecanico)
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
            wrap, text="¿Eliminar mecánico?",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(anchor="w")

        ctk.CTkLabel(
            wrap, text=f'Se eliminará a "{nombre}" permanentemente.',
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