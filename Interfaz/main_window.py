import customtkinter as ctk
from Interfaz.Frames.clientes_frame import ClientesFrame
from Interfaz.Frames.vehiculos_frame import VehiculosFrame
from Interfaz.Frames.mecanicos_frame import MecanicosFrame
from Interfaz.Frames.servicio_frame import ServiciosFrame
from Interfaz.Frames.repuestos_frame import RepuestosFrame
from Interfaz.Frames.ordenes_frame import OrdenesFrame
from Interfaz.Frames.factura_frame import FacturasFrame

SIDEBAR_COLOR  = "#1a1a2e"
SIDEBAR_HOVER  = "#16213e"
ACCENT_COLOR   = "#e94560"
ACCENT_HOVER   = "#c73652"
TEXT_PRIMARY   = "#eaeaea"
TEXT_SECONDARY = "#8888aa"
BG_MAIN        = "#0f0f23"

MENU_ITEMS = [
    ("Clientes", "👤", "clientes"),
    ("Vehículos", "🚗", "vehiculos"),
    ("Mecánicos", "🔧", "mecanicos"),
    ("Servicios", "⚙️", "servicios"),
    ("Repuestos", "🔩", "repuestos"),
    ("Órdenes", "📋", "ordenes"),
    ("Facturas", "🧾", "facturas"),
]


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Taller Mecánico")
        self.geometry("1280x780")
        self.minsize(1024, 680)
        self.configure(fg_color=BG_MAIN)
        self.current_frame  = None
        self.nav_buttons    = {}
        self.active_section = "clientes"
        self._build_layout()
        self._show_frame("clientes")

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
        sidebar.grid_rowconfigure(len(MENU_ITEMS) + 2, weight=1)

        logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        logo_frame.grid(row=0, column=0, padx=20, pady=(28, 20), sticky="ew")
        ctk.CTkLabel(logo_frame, text="🔧", font=ctk.CTkFont(size=28)).pack(anchor="w")
        ctk.CTkLabel(logo_frame, text="Taller Mecánico", font=ctk.CTkFont(size=15, weight="bold"), text_color=TEXT_PRIMARY).pack(anchor="w", pady=(4, 0))
        ctk.CTkLabel(logo_frame, text="Sistema de Gestión", font=ctk.CTkFont(size=11), text_color=TEXT_SECONDARY).pack(anchor="w")

        ctk.CTkFrame(sidebar, height=1, fg_color="#2a2a4a").grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 12))

        for i, (label, icon, key) in enumerate(MENU_ITEMS):
            btn = ctk.CTkButton(
                sidebar, text=f"  {icon}  {label}", anchor="w", height=42,
                corner_radius=8, border_width=0, fg_color="transparent",
                hover_color=SIDEBAR_HOVER, text_color=TEXT_SECONDARY,
                font=ctk.CTkFont(size=13), command=lambda k=key: self._show_frame(k),
            )
            btn.grid(row=i + 2, column=0, padx=12, pady=3, sticky="ew")
            self.nav_buttons[key] = btn

        ctk.CTkLabel(sidebar, text="v1.0.0", font=ctk.CTkFont(size=11), text_color=TEXT_SECONDARY).grid(
            row=len(MENU_ITEMS) + 2, column=0, padx=20, pady=16, sticky="sw"
        )

    def _show_frame(self, section: str):
        if self.current_frame:
            self.current_frame.destroy()
        if self.active_section in self.nav_buttons:
            self.nav_buttons[self.active_section].configure(fg_color="transparent", text_color=TEXT_SECONDARY)
        self.active_section = section
        self.nav_buttons[section].configure(fg_color=ACCENT_COLOR, text_color="#ffffff")
        frame_map = {
            "clientes": ClientesFrame,
            "vehiculos": VehiculosFrame,
            "mecanicos": MecanicosFrame,
            "servicios": ServiciosFrame,
            "repuestos": RepuestosFrame,
            "ordenes": OrdenesFrame,
            "facturas": FacturasFrame,
        }
        FrameClass = frame_map[section]
        self.current_frame = FrameClass(self.content_area)
        self.current_frame.grid(row=0, column=0, sticky="nsew")