import customtkinter as ctk

BG_MAIN = "#0f0f23"
CARD_COLOR = "#1a1a2e"
ACCENT_COLOR = "#e94560"
ACCENT_HOVER = "#c73652"
TEXT_PRIMARY = "#eaeaea"
TEXT_SECONDARY = "#8888aa"
TABLE_HEADER_BG = "#16213e"
ROW_ALT = "#14142a"


class BaseFrame(ctk.CTkFrame):
    """
    Frame base reutilizable para todos los módulos del taller.
    Provee encabezado, botón de acción, tabla y formulario modal.
    """

    title_text = "Módulo"
    subtitle_text = ""
    columns = []          # lista de (nombre_col, ancho_px)
    add_button_text = "+ Agregar"

    def __init__(self, parent):
        super().__init__(parent, fg_color=BG_MAIN, corner_radius=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.rows_data = []
        self.row_widgets = []

        self._build_header()
        self._build_search_bar()
        self._build_table()
        self._load_data()

    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, padx=30, pady=(28, 4), sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text=self.title_text,
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).grid(row=0, column=0, sticky="w")

        if self.subtitle_text:
            ctk.CTkLabel(
                header,
                text=self.subtitle_text,
                font=ctk.CTkFont(size=13),
                text_color=TEXT_SECONDARY,
            ).grid(row=1, column=0, sticky="w")

        ctk.CTkButton(
            header,
            text=self.add_button_text,
            height=36,
            corner_radius=8,
            fg_color=ACCENT_COLOR,
            hover_color=ACCENT_HOVER,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.on_add,
        ).grid(row=0, column=1, rowspan=2, sticky="e")

    def _build_search_bar(self):
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.grid(row=1, column=0, padx=30, pady=(8, 12), sticky="ew")
        bar.grid_columnconfigure(0, weight=1)

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._filter_rows())

        ctk.CTkEntry(
            bar,
            placeholder_text="🔍  Buscar...",
            textvariable=self.search_var,
            height=36,
            corner_radius=8,
            fg_color=CARD_COLOR,
            border_color="#2a2a4a",
            text_color=TEXT_PRIMARY,
        ).grid(row=0, column=0, sticky="ew")

    def _build_table(self):
        container = ctk.CTkFrame(self, fg_color=CARD_COLOR, corner_radius=12)
        container.grid(row=2, column=0, padx=30, pady=(0, 24), sticky="nsew")
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(1, weight=1)

        thead = ctk.CTkFrame(container, fg_color=TABLE_HEADER_BG, corner_radius=0)
        thead.grid(row=0, column=0, sticky="ew", padx=0, pady=0)

        for col_i, (col_name, col_w) in enumerate(self.columns):
            ctk.CTkLabel(
                thead,
                text=col_name,
                width=col_w,
                anchor="w",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=TEXT_SECONDARY,
            ).grid(row=0, column=col_i, padx=(16 if col_i == 0 else 8, 8), pady=10, sticky="w")

        action_label = ctk.CTkLabel(
            thead,
            text="Acciones",
            width=100,
            anchor="center",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=TEXT_SECONDARY,
        )
        action_label.grid(row=0, column=len(self.columns), padx=8, pady=10)

        self.tbody_scroll = ctk.CTkScrollableFrame(
            container,
            fg_color="transparent",
            corner_radius=0,
        )
        self.tbody_scroll.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.tbody_scroll.grid_columnconfigure(0, weight=1)

        self.tbody = self.tbody_scroll

    def _render_rows(self, data):
        for w in self.row_widgets:
            w.destroy()
        self.row_widgets = []

        if not data:
            empty = ctk.CTkLabel(
                self.tbody,
                text="Sin registros para mostrar.",
                font=ctk.CTkFont(size=13),
                text_color=TEXT_SECONDARY,
            )
            empty.pack(pady=30)
            self.row_widgets.append(empty)
            return

        for r_i, row in enumerate(data):
            bg = ROW_ALT if r_i % 2 == 0 else "transparent"
            row_frame = ctk.CTkFrame(self.tbody, fg_color=bg, corner_radius=0, height=40)
            row_frame.pack(fill="x")
            self.row_widgets.append(row_frame)

            values = self.row_values(row)
            for col_i, (val, (_, col_w)) in enumerate(zip(values, self.columns)):
                ctk.CTkLabel(
                    row_frame,
                    text=str(val),
                    width=col_w,
                    anchor="w",
                    font=ctk.CTkFont(size=13),
                    text_color=TEXT_PRIMARY,
                ).grid(row=0, column=col_i, padx=(16 if col_i == 0 else 8, 8), pady=8, sticky="w")

            btn_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            btn_frame.grid(row=0, column=len(self.columns), padx=8, pady=4)

            ctk.CTkButton(
                btn_frame,
                text="✏",
                width=32,
                height=28,
                corner_radius=6,
                fg_color="#16213e",
                hover_color="#1f3060",
                text_color="#6ab0f5",
                command=lambda r=row: self.on_edit(r),
            ).pack(side="left", padx=2)

            ctk.CTkButton(
                btn_frame,
                text="🗑",
                width=32,
                height=28,
                corner_radius=6,
                fg_color="#2a1a1a",
                hover_color="#4a1a1a",
                text_color="#e94560",
                command=lambda r=row: self.on_delete(r),
            ).pack(side="left", padx=2)

    def _filter_rows(self):
        query = self.search_var.get().lower()
        if not query:
            self._render_rows(self.rows_data)
            return
        filtered = [
            r for r in self.rows_data
            if any(query in str(v).lower() for v in self.row_values(r))
        ]
        self._render_rows(filtered)

    def _load_data(self):
        """Sobrescribir para cargar datos desde el servicio."""
        self.rows_data = []
        self._render_rows(self.rows_data)

    def row_values(self, row) -> list:
        """Sobrescribir para extraer valores de cada fila."""
        return list(row)

    def on_add(self):
        """Sobrescribir para abrir formulario de creación."""
        pass

    def on_edit(self, row):
        """Sobrescribir para abrir formulario de edición."""
        pass

    def on_delete(self, row):
        """Sobrescribir para confirmar y eliminar un registro."""
        pass
