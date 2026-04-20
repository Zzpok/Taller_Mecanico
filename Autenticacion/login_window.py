import customtkinter as ctk
from Autenticacion.Autenticacion_serv import login

BG_MAIN        = "#0f0f23"
CARD_COLOR     = "#1a1a2e"
ACCENT_COLOR   = "#e94560"
ACCENT_HOVER   = "#c73652"
TEXT_PRIMARY   = "#eaeaea"
TEXT_SECONDARY = "#8888aa"


class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Taller Mecánico — Iniciar Sesión")
        self.geometry("420x500")
        self.resizable(False, False)
        self.configure(fg_color=BG_MAIN)
        self.usuario = None
        self._build()

    def _build(self):
        # Contenedor centrado
        wrap = ctk.CTkFrame(self, fg_color=CARD_COLOR, corner_radius=16)
        wrap.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85)

        # Logo / título
        ctk.CTkLabel(
            wrap, text="🔧",
            font=ctk.CTkFont(size=40),
        ).pack(pady=(36, 4))

        ctk.CTkLabel(
            wrap, text="Taller Mecánico",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack()

        ctk.CTkLabel(
            wrap, text="Inicia sesión para continuar",
            font=ctk.CTkFont(size=13),
            text_color=TEXT_SECONDARY,
        ).pack(pady=(4, 28))

        # Campos
        ctk.CTkLabel(wrap, text="Usuario", font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(anchor="w", padx=28)
        self.username_entry = ctk.CTkEntry(
            wrap, placeholder_text="Ingresa tu usuario",
            height=40, corner_radius=8,
            fg_color="#0f0f23", border_color="#2a2a4a",
            text_color=TEXT_PRIMARY, placeholder_text_color="#555577",
        )
        self.username_entry.pack(fill="x", padx=28, pady=(4, 14))

        ctk.CTkLabel(wrap, text="Contraseña", font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(anchor="w", padx=28)
        self.password_entry = ctk.CTkEntry(
            wrap, placeholder_text="Ingresa tu contraseña",
            show="●", height=40, corner_radius=8,
            fg_color="#0f0f23", border_color="#2a2a4a",
            text_color=TEXT_PRIMARY, placeholder_text_color="#555577",
        )
        self.password_entry.pack(fill="x", padx=28, pady=(4, 6))
        # Enter para hacer login
        self.password_entry.bind("<Return>", lambda e: self._do_login())

        self.error_label = ctk.CTkLabel(
            wrap, text="",
            font=ctk.CTkFont(size=12),
            text_color=ACCENT_COLOR,
        )
        self.error_label.pack(pady=(4, 0))

        ctk.CTkButton(
            wrap, text="Iniciar Sesión",
            height=42, corner_radius=8,
            fg_color=ACCENT_COLOR, hover_color=ACCENT_HOVER,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._do_login,
        ).pack(fill="x", padx=28, pady=(10, 36))

    def _do_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            self.error_label.configure(text="Completa todos los campos.")
            return

        usuario = login(username, password)

        if usuario is None:
            self.error_label.configure(text="Usuario o contraseña incorrectos.")
            self.password_entry.delete(0, "end")
            return

        # Login exitoso — guardar usuario y cerrar
        self.usuario = usuario
        self.destroy()