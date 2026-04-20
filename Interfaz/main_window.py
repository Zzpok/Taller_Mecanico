import customtkinter as ctk
from Interfaz.permisos import get_secciones
from Interfaz.Frames.clientes_frame import ClientesFrame
from Interfaz.Frames.vehiculos_frame import VehiculosFrame
from Interfaz.Frames.mecanicos_frame import MecanicosFrame
from Interfaz.Frames.ordenes_frame import OrdenesFrame
from Interfaz.Frames.servicio_frame import ServiciosFrame
from Interfaz.Frames.repuestos_frame import RepuestosFrame
from Interfaz.Frames.factura_frame import FacturasFrame
from Interfaz.Frames.usuarios_frame import UsuariosFrame


SIDEBAR_COLOR  = "#1a1a2e"
SIDEBAR_HOVER  = "#16213e"
ACCENT_COLOR   = "#e94560"
ACCENT_HOVER   = "#c73652"
TEXT_PRIMARY   = "#eaeaea"
TEXT_SECONDARY = "#8888aa"
BG_MAIN        = "#0f0f23"

# Todos los items del menu con su seccion
ALL_MENU_ITEMS = [
    ("Clientes",  "👤", "clientes"),
    ("Vehículos", "🚗", "vehiculos"),
    ("Mecánicos", "🔧", "mecanicos"),
    ("Órdenes",   "📋", "ordenes"),
    ("Servicios", "⚙️",  "servicios"),
    ("Repuestos", "🔩", "repuestos"),
    ("Facturas",  "🧾", "facturas"),
    ("Usuarios", "👥", "usuarios"),
]

FRAME_MAP = {
    "clientes":  ClientesFrame,
    "vehiculos": VehiculosFrame,
    "mecanicos": MecanicosFrame,
    "ordenes":   OrdenesFrame,
    "servicios": ServiciosFrame,
    "repuestos": RepuestosFrame,
    "facturas":  FacturasFrame,
    "usuarios": UsuariosFrame,
}


class MainWindow(ctk.CTk):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario

        # Filtrar menu segun el rol
        secciones = get_secciones(usuario.rol)
        self.menu_items = [
            item for item in ALL_MENU_ITEMS
            if item[2] in secciones
        ]

        self.title("Taller Mecánico")
        self.geometry("1280x780")
        self.minsize(1024, 680)
        self.configure(fg_color=BG_MAIN)

        self.current_frame  = None
        self.nav_buttons    = {}
        self.active_section = self.menu_items[0][2] if self.menu_items else None

        self._build_layout()
        if self.active_section:
            self._show_frame(self.active_section)

    def _build_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._build_sidebar()
        self.content_area = ctk.CTkFrame(self, fg_color=BG_MAIN, corner_radius=0)
        self.content_area.grid(row=0, column=1, sticky="nsew")
        self.content_area.grid_columnconfigure(0, weight=1)
        self.content_area.grid_rowconfigure(0, weight=1)

    def _build_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=SIDEBAR_COLOR)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        sidebar.grid_rowconfigure(len(self.menu_items) + 3, weight=1)

        # Logo
        logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        logo_frame.grid(row=0, column=0, padx=20, pady=(28, 20), sticky="ew")
        ctk.CTkLabel(logo_frame, text="🔧", font=ctk.CTkFont(size=28)).pack(anchor="w")
        ctk.CTkLabel(logo_frame, text="Taller Mecánico", font=ctk.CTkFont(size=15, weight="bold"), text_color=TEXT_PRIMARY).pack(anchor="w", pady=(4, 0))
        ctk.CTkLabel(logo_frame, text="Sistema de Gestión", font=ctk.CTkFont(size=11), text_color=TEXT_SECONDARY).pack(anchor="w")

        ctk.CTkFrame(sidebar, height=1, fg_color="#2a2a4a").grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 12))

        # Botones de navegación filtrados por rol
        for i, (label, icon, key) in enumerate(self.menu_items):
            btn = ctk.CTkButton(
                sidebar, text=f"  {icon}  {label}", anchor="w", height=42,
                corner_radius=8, border_width=0, fg_color="transparent",
                hover_color=SIDEBAR_HOVER, text_color=TEXT_SECONDARY,
                font=ctk.CTkFont(size=13),
                command=lambda k=key: self._show_frame(k),
            )
            btn.grid(row=i + 2, column=0, padx=12, pady=3, sticky="ew")
            self.nav_buttons[key] = btn

        # Info del usuario + cerrar sesión al fondo
        footer = ctk.CTkFrame(sidebar, fg_color="transparent")
        footer.grid(row=len(self.menu_items) + 3, column=0, padx=12, pady=16, sticky="sew")

        ctk.CTkFrame(footer, height=1, fg_color="#2a2a4a").pack(fill="x", pady=(0, 10))

        # Avatar y nombre
        user_frame = ctk.CTkFrame(footer, fg_color="#16213e", corner_radius=8)
        user_frame.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(
            user_frame,
            text=self.usuario.username[0].upper(),
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=ACCENT_COLOR,
            width=36, height=36,
            fg_color="#2a1a1a",
            corner_radius=18,
        ).pack(side="left", padx=10, pady=8)

        info = ctk.CTkFrame(user_frame, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(info, text=self.usuario.username, font=ctk.CTkFont(size=12, weight="bold"), text_color=TEXT_PRIMARY, anchor="w").pack(anchor="w")
        ctk.CTkLabel(info, text=self.usuario.rol.capitalize(), font=ctk.CTkFont(size=11), text_color=TEXT_SECONDARY, anchor="w").pack(anchor="w")

        ctk.CTkButton(
            footer, text="Cerrar sesión",
            height=34, corner_radius=8,
            fg_color="#2a2a4a", hover_color=ACCENT_COLOR,
            text_color=TEXT_SECONDARY,
            font=ctk.CTkFont(size=12),
            command=self._cerrar_sesion,
        ).pack(fill="x")

    def _show_frame(self, section: str):
        if self.current_frame:
            self.current_frame.destroy()

        if self.active_section in self.nav_buttons:
            self.nav_buttons[self.active_section].configure(fg_color="transparent", text_color=TEXT_SECONDARY)

        self.active_section = section
        self.nav_buttons[section].configure(fg_color=ACCENT_COLOR, text_color="#ffffff")

        FrameClass = FRAME_MAP[section]
        self.current_frame = FrameClass(self.content_area)
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    def _cerrar_sesion(self):
        self.destroy()
        # Relanzar el login
        from Autenticacion.login_window import LoginWindow
        import Interfaz.main_window as mw
        login = LoginWindow()
        login.mainloop()
        if login.usuario:
            app = mw.MainWindow(login.usuario)
            app.mainloop()