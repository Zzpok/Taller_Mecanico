import customtkinter as ctk
from Servicios.Factura_serv import listar_facturas, crear_factura, eliminar_factura
from Servicios.OrdenTrabajo_serv import listar_ordenes
from Componentes.Facturas import Factura
from Interfaz.Frames.base_frame import BaseFrame

BG_MAIN        = "#0f0f23"
ACCENT_COLOR   = "#e94560"
ACCENT_HOVER   = "#c73652"
TEXT_PRIMARY   = "#eaeaea"
TEXT_SECONDARY = "#8888aa"

METODOS_PAGO = ["efectivo", "tarjeta_credito", "tarjeta_debito", "transferencia"]


class FacturasFrame(BaseFrame):
    title_text      = "Facturas"
    subtitle_text   = "Historial de facturación"
    add_button_text = "+ Nueva Factura"
    columns = [
        ("ID",          55),
        ("Fecha",      120),
        ("Orden",       80),
        ("Subtotal",   110),
        ("Impuestos",  110),
        ("Total",      110),
        ("Método pago",130),
    ]

    def _load_data(self):
        try:
            resultados = listar_facturas()
            # tupla: (id_factura, fecha, subtotal, impuestos, total, metodo_pago, id_orden)
            self.rows_data = [
                Factura(
                    id_factura  = r[0],
                    fecha       = r[1],
                    subtotal    = r[2],
                    impuestos   = r[3],
                    total       = r[4],
                    metodo_pago = r[5],
                    id_orden    = r[6],
                )
                for r in resultados
            ]
            ordenes = listar_ordenes()
            self.ordenes_map = {o[0]: f"Orden #{o[0]}" for o in ordenes}

        except Exception as e:
            print(f"Error cargando facturas: {e}")
            self.rows_data   = []
            self.ordenes_map = {}
        self._render_rows(self.rows_data)

    def row_values(self, row) -> list:
        return [
            row.id_factura,
            str(row.fecha)[:10] if row.fecha else "-",
            self.ordenes_map.get(row.id_orden, f"#{row.id_orden}"),
            f"${float(row.subtotal):,.0f}"  if row.subtotal  else "$0",
            f"${float(row.impuestos):,.0f}" if row.impuestos else "$0",
            f"${float(row.total):,.0f}"     if row.total     else "$0",
            row.metodo_pago or "-",
        ]

    def on_add(self):
        FacturaFormModal(
            self,
            ordenes_map = getattr(self, "ordenes_map", {}),
            callback    = self._load_data,
        )

    def on_edit(self, row):
        # Las facturas no se editan, solo se ven en detalle
        FacturaDetalleModal(self, row=row)

    def on_delete(self, row):
        ConfirmarEliminarDialog(
            parent=self,
            nombre=f"Factura #{row.id_factura}",
            on_confirm=lambda: self._do_delete(row.id_factura),
        )

    def _do_delete(self, id_factura):
        try:
            eliminar_factura(id_factura)
        except Exception as e:
            print(f"Error eliminando factura: {e}")
        self._load_data()


class FacturaFormModal(ctk.CTkToplevel):
    def __init__(self, parent, ordenes_map=None, callback=None):
        super().__init__(parent)
        self.ordenes_map = ordenes_map or {}
        self.callback    = callback
        self.title("Nueva Factura")
        self.geometry("440x620")
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
            wrap, text="Nueva Factura",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(anchor="w", pady=(0, 18))

        self.ord_ids  = list(self.ordenes_map.keys())
        self.ord_noms = list(self.ordenes_map.values())

        ctk.CTkLabel(wrap, text="Orden de Trabajo", font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(anchor="w")
        self.orden_var = ctk.StringVar(value=self.ord_noms[0] if self.ord_noms else "Sin órdenes")
        ctk.CTkOptionMenu(
            wrap, values=self.ord_noms if self.ord_noms else ["Sin órdenes"],
            variable=self.orden_var, height=36, corner_radius=8,
            fg_color="#0f0f23", button_color="#2a2a4a",
            button_hover_color="#3a3a5a", text_color=TEXT_PRIMARY,
        ).pack(fill="x", pady=(3, 10))

        ctk.CTkLabel(wrap, text="Fecha (YYYY-MM-DD)", font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(anchor="w")
        self.fecha_entry = ctk.CTkEntry(
            wrap, placeholder_text="Ej: 2025-06-15",
            height=36, corner_radius=8,
            fg_color="#0f0f23", border_color="#2a2a4a",
            text_color=TEXT_PRIMARY, placeholder_text_color="#555577",
        )
        self.fecha_entry.pack(fill="x", pady=(3, 10))

        fields = [
            ("Subtotal",  "subtotal",  "Ej: 80000"),
            ("Impuestos", "impuestos", "Ej: 15200"),
            ("Total",     "total",     "Ej: 95200"),
        ]
        self.entries = {}
        for label, key, placeholder in fields:
            ctk.CTkLabel(wrap, text=label, font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(anchor="w")
            entry = ctk.CTkEntry(
                wrap, placeholder_text=placeholder, height=36, corner_radius=8,
                fg_color="#0f0f23", border_color="#2a2a4a",
                text_color=TEXT_PRIMARY, placeholder_text_color="#555577",
            )
            entry.pack(fill="x", pady=(3, 10))
            self.entries[key] = entry

        ctk.CTkLabel(wrap, text="Método de pago", font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(anchor="w")
        self.metodo_var = ctk.StringVar(value=METODOS_PAGO[0])
        ctk.CTkOptionMenu(
            wrap, values=METODOS_PAGO, variable=self.metodo_var,
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
        fecha  = self.fecha_entry.get().strip()
        datos  = {k: e.get().strip() for k, e in self.entries.items()}
        metodo = self.metodo_var.get()
        ord_val = self.orden_var.get()

        if not fecha or not datos["subtotal"] or not datos["total"]:
            self.error_label.configure(text="Fecha, subtotal y total son obligatorios.")
            return

        id_orden = self.ord_ids[self.ord_noms.index(ord_val)] if ord_val in self.ord_noms else None
        if not id_orden:
            self.error_label.configure(text="Selecciona una orden válida.")
            return

        try:
            subtotal  = float(datos["subtotal"])
            impuestos = float(datos["impuestos"]) if datos["impuestos"] else 0
            total     = float(datos["total"])
        except ValueError:
            self.error_label.configure(text="Subtotal, impuestos y total deben ser números.")
            return

        try:
            factura = Factura(
                id_factura  = None,
                fecha       = fecha,
                subtotal    = subtotal,
                impuestos   = impuestos,
                total       = total,
                metodo_pago = metodo,
                id_orden    = id_orden,
            )
            crear_factura(factura)
        except Exception as e:
            self.error_label.configure(text=f"Error: {e}")
            return

        if self.callback:
            self.callback()
        self.destroy()


class FacturaDetalleModal(ctk.CTkToplevel):
    """Modal de solo lectura para ver el detalle de una factura."""
    def __init__(self, parent, row):
        super().__init__(parent)
        self.row = row
        self.title(f"Factura #{row.id_factura}")
        self.geometry("380x360")
        self.resizable(False, False)
        self.configure(fg_color="#1a1a2e")
        self.attributes("-topmost", True)
        self.grab_set()
        self.focus_force()
        self._build()

    def _build(self):
        wrap = ctk.CTkFrame(self, fg_color="transparent")
        wrap.pack(padx=28, pady=28, fill="both", expand=True)

        ctk.CTkLabel(
            wrap, text=f"Factura #{self.row.id_factura}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(anchor="w", pady=(0, 16))

        card = ctk.CTkFrame(wrap, fg_color="#16213e", corner_radius=8)
        card.pack(fill="x")

        for label, valor in [
            ("Fecha",       str(self.row.fecha)[:10] if self.row.fecha else "-"),
            ("Orden",       f"#{self.row.id_orden}"),
            ("Subtotal",    f"${float(self.row.subtotal):,.0f}"  if self.row.subtotal  else "$0"),
            ("Impuestos",   f"${float(self.row.impuestos):,.0f}" if self.row.impuestos else "$0"),
            ("Total",       f"${float(self.row.total):,.0f}"     if self.row.total     else "$0"),
            ("Método pago", self.row.metodo_pago or "-"),
        ]:
            row_f = ctk.CTkFrame(card, fg_color="transparent")
            row_f.pack(fill="x", padx=16, pady=5)
            ctk.CTkLabel(row_f, text=label, font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY, width=110, anchor="w").pack(side="left")
            ctk.CTkLabel(row_f, text=valor,  font=ctk.CTkFont(size=13, weight="bold"), text_color=TEXT_PRIMARY, anchor="w").pack(side="left")

        ctk.CTkButton(
            wrap, text="Cerrar", height=38, corner_radius=8,
            fg_color="#2a2a4a", hover_color="#3a3a5a", text_color=TEXT_SECONDARY,
            command=self.destroy,
        ).pack(fill="x", pady=(20, 0))


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
            wrap, text="¿Eliminar factura?",
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