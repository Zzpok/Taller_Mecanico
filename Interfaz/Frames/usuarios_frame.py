import customtkinter as ctk
from Servicios.Usuarios_serv import listar_usuarios, crear_usuario, eliminar_usuario
from Componentes.Usuarios import Usuario
from Interfaz.Frames.base_frame import BaseFrame

BG_MAIN        = "#0f0f23"
ACCENT_COLOR   = "#e94560"
ACCENT_HOVER   = "#c73652"
TEXT_PRIMARY   = "#eaeaea"
TEXT_SECONDARY = "#8888aa"

ROLES = ["mecanico", "admin"]


class UsuariosFrame(BaseFrame):
    title_text      = "Usuarios"
    subtitle_text   = "Gestión de usuarios del sistema"
    add_button_text = "+ Nuevo Usuario"
    columns = [
        ("ID",        55),
        ("Username", 180),
        ("Rol",      120),
    ]

    def _load_data(self):
        try:
            resultados = listar_usuarios()
            # tupla: (id_usuario, username, password, rol)
            self.rows_data = [
                Usuario(
                    id_usuario = r[0],
                    username   = r[1],
                    password   = r[2],
                    rol        = r[3],
                )
                for r in resultados
            ]
        except Exception as e:
            print(f"Error cargando usuarios: {e}")
            self.rows_data = []
        self._render_rows(self.rows_data)

    def row_values(self, row) -> list:
        return [
            row.id_usuario,
            row.username,
            row.rol,
        ]

    def on_add(self):
        UsuarioFormModal(self, callback=self._load_data)

    def on_edit(self, row):
        # Los usuarios no se editan, solo se crean o eliminan
        pass

    def on_delete(self, row):
        ConfirmarEliminarDialog(
            parent=self,
            nombre=row.username,
            on_confirm=lambda: self._do_delete(row.id_usuario),
        )

    def _do_delete(self, id_usuario):
        try:
            eliminar_usuario(id_usuario)
        except Exception as e:
            print(f"Error eliminando usuario: {e}")
        self._load_data()


class UsuarioFormModal(ctk.CTkToplevel):
    def __init__(self, parent, callback=None):
        super().__init__(parent)
        self.callback = callback
        self.title("Nuevo Usuario")
        self.geometry("400x480")
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
            wrap, text="Nuevo Usuario",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(anchor="w", pady=(0, 18))

        # Username
        ctk.CTkLabel(wrap, text="Username", font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(anchor="w")
        self.username_entry = ctk.CTkEntry(
            wrap, placeholder_text="Ej: carlos_mec",
            height=36, corner_radius=8,
            fg_color="#0f0f23", border_color="#2a2a4a",
            text_color=TEXT_PRIMARY, placeholder_text_color="#555577",
        )
        self.username_entry.pack(fill="x", pady=(3, 10))

        # Password
        ctk.CTkLabel(wrap, text="Contraseña", font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(anchor="w")
        self.password_entry = ctk.CTkEntry(
            wrap, placeholder_text="Ingresa una contraseña",
            show="●", height=36, corner_radius=8,
            fg_color="#0f0f23", border_color="#2a2a4a",
            text_color=TEXT_PRIMARY, placeholder_text_color="#555577",
        )
        self.password_entry.pack(fill="x", pady=(3, 10))

        # Confirmar password
        ctk.CTkLabel(wrap, text="Confirmar contraseña", font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(anchor="w")
        self.password2_entry = ctk.CTkEntry(
            wrap, placeholder_text="Repite la contraseña",
            show="●", height=36, corner_radius=8,
            fg_color="#0f0f23", border_color="#2a2a4a",
            text_color=TEXT_PRIMARY, placeholder_text_color="#555577",
        )
        self.password2_entry.pack(fill="x", pady=(3, 10))

        # Rol
        ctk.CTkLabel(wrap, text="Rol", font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(anchor="w")
        self.rol_var = ctk.StringVar(value=ROLES[0])
        ctk.CTkOptionMenu(
            wrap, values=ROLES, variable=self.rol_var,
            height=36, corner_radius=8,
            fg_color="#0f0f23", button_color="#2a2a4a",
            button_hover_color="#3a3a5a", text_color=TEXT_PRIMARY,
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
            btn_frame, text="Crear Usuario", height=38, corner_radius=8,
            fg_color=ACCENT_COLOR, hover_color=ACCENT_HOVER,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._save,
        ).grid(row=0, column=1, padx=(6, 0), sticky="ew")

    def _save(self):
        username  = self.username_entry.get().strip()
        password  = self.password_entry.get().strip()
        password2 = self.password2_entry.get().strip()
        rol       = self.rol_var.get()

        if not username or not password:
            self.error_label.configure(text="Username y contraseña son obligatorios.")
            return

        if password != password2:
            self.error_label.configure(text="Las contraseñas no coinciden.")
            return

        if len(password) < 4:
            self.error_label.configure(text="La contraseña debe tener al menos 4 caracteres.")
            return

        try:
            usuario = Usuario(
                id_usuario = None,
                username   = username,
                password   = password,
                rol        = rol,
            )
            crear_usuario(usuario)
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
            wrap, text="¿Eliminar usuario?",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(anchor="w")

        ctk.CTkLabel(
            wrap, text=f'Se eliminará al usuario "{nombre}" permanentemente.',
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