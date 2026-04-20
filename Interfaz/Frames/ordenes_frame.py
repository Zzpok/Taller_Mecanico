import customtkinter as ctk
from Servicios.OrdenTrabajo_serv import listar_ordenes, crear_orden_trabajo, cambiar_estado, registrar_diagnostico, asignar_mecanico, eliminar_orden
from Servicios.detalleord_serv import listar_detalle_orden, crear_detalle_orden, eliminar_detalle_orden
from Servicios.Clientes_serv import listar_clientes
from Servicios.Vehiculos_serv import listar_vehiculos
from Servicios.Mecanico_serv import listar_mecanicos
from Servicios.Servicio_serv import listar_servicios
from Servicios.Repuestos_serv import listar_repuestos
from Componentes.OrdenTrabajo import OrdenTrabajo
from Componentes.DetalleOrd import DetalleOrd
from Interfaz.Frames.base_frame import BaseFrame

BG_MAIN        = "#0f0f23"
CARD_COLOR     = "#1a1a2e"
ACCENT_COLOR   = "#e94560"
ACCENT_HOVER   = "#c73652"
TEXT_PRIMARY   = "#eaeaea"
TEXT_SECONDARY = "#8888aa"

ESTADOS = ["pendiente", "en_proceso", "terminado", "entregado"]


class OrdenesFrame(BaseFrame):
    title_text      = "Órdenes de Trabajo"
    subtitle_text   = "Control de órdenes activas y completadas"
    add_button_text = "+ Nueva Orden"
    columns = [
        ("ID",          50),
        ("Fecha ini.", 110),
        ("Fecha fin",  110),
        ("Estado",     100),
        ("Cliente",    140),
        ("Vehículo",   130),
        ("Mecánico",   140),
    ]

    def _load_data(self):
        try:
            resultados = listar_ordenes()
            self.rows_data = [
                OrdenTrabajo(
                    id_orden     = r[0],
                    fecha_inicio = r[1],
                    fecha_fin    = r[2],
                    estado       = r[3],
                    diagnostico  = r[4],
                    id_mecanico  = r[5],
                    id_vehiculo  = r[6],
                    id_cliente   = r[7],
                )
                for r in resultados
            ]
            clientes  = listar_clientes()
            vehiculos = listar_vehiculos()
            mecanicos = listar_mecanicos()

            self.clientes_map  = {c[0]: f"{c[1]} {c[2]}" for c in clientes}
            self.vehiculos_map = {v[0]: f"{v[1]} {v[2]}" for v in vehiculos}
            self.mecanicos_map = {m[0]: f"{m[1]} {m[2]}" for m in mecanicos}

        except Exception as e:
            print(f"Error cargando órdenes: {e}")
            self.rows_data     = []
            self.clientes_map  = {}
            self.vehiculos_map = {}
            self.mecanicos_map = {}
        self._render_rows(self.rows_data)

    def row_values(self, row) -> list:
        return [
            row.id_orden,
            str(row.fecha_inicio)[:10] if row.fecha_inicio else "-",
            str(row.fecha_fin)[:10]    if row.fecha_fin    else "-",
            row.estado or "pendiente",
            self.clientes_map.get(row.id_cliente,   str(row.id_cliente)),
            self.vehiculos_map.get(row.id_vehiculo, str(row.id_vehiculo)),
            self.mecanicos_map.get(row.id_mecanico, str(row.id_mecanico)),
        ]

    def on_add(self):
        OrdenFormModal(
            self, row=None,
            clientes_map  = getattr(self, "clientes_map",  {}),
            vehiculos_map = getattr(self, "vehiculos_map", {}),
            mecanicos_map = getattr(self, "mecanicos_map", {}),
            callback=self._load_data,
        )

    def on_edit(self, row):
        OrdenDetalleModal(
            self, row=row,
            clientes_map  = getattr(self, "clientes_map",  {}),
            vehiculos_map = getattr(self, "vehiculos_map", {}),
            mecanicos_map = getattr(self, "mecanicos_map", {}),
            callback=self._load_data,
        )

    def on_delete(self, row):
        ConfirmarEliminarDialog(
            parent=self,
            nombre=f"Orden #{row.id_orden}",
            on_confirm=lambda: self._do_delete(row.id_orden),
        )

    def _do_delete(self, id_orden):
        try:
            eliminar_orden(id_orden)
        except Exception as e:
            print(f"Error eliminando orden: {e}")
        self._load_data()


class OrdenFormModal(ctk.CTkToplevel):
    """Modal para CREAR una nueva orden."""
    def __init__(self, parent, row=None, clientes_map=None, vehiculos_map=None, mecanicos_map=None, callback=None):
        super().__init__(parent)
        self.clientes_map  = clientes_map  or {}
        self.vehiculos_map = vehiculos_map or {}
        self.mecanicos_map = mecanicos_map or {}
        self.callback      = callback
        self.title("Nueva Orden de Trabajo")
        self.geometry("460x560")
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
            wrap, text="Nueva Orden de Trabajo",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(anchor="w", pady=(0, 18))

        self.cli_ids  = list(self.clientes_map.keys())
        self.cli_noms = list(self.clientes_map.values())
        self.veh_ids  = list(self.vehiculos_map.keys())
        self.veh_noms = list(self.vehiculos_map.values())
        self.mec_ids  = list(self.mecanicos_map.keys())
        self.mec_noms = list(self.mecanicos_map.values())

        def make_dropdown(label, nombres):
            ctk.CTkLabel(wrap, text=label, font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(anchor="w")
            var = ctk.StringVar(value=nombres[0] if nombres else "Sin registros")
            ctk.CTkOptionMenu(
                wrap, values=nombres if nombres else ["Sin registros"],
                variable=var, height=36, corner_radius=8,
                fg_color="#0f0f23", button_color="#2a2a4a",
                button_hover_color="#3a3a5a", text_color=TEXT_PRIMARY,
            ).pack(fill="x", pady=(3, 10))
            return var

        self.cliente_var  = make_dropdown("Cliente",  self.cli_noms)
        self.vehiculo_var = make_dropdown("Vehículo", self.veh_noms)
        self.mecanico_var = make_dropdown("Mecánico", self.mec_noms)

        ctk.CTkLabel(wrap, text="Fecha fin estimada (YYYY-MM-DD)", font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(anchor="w")
        self.fecha_fin_entry = ctk.CTkEntry(
            wrap, placeholder_text="Ej: 2025-12-31",
            height=36, corner_radius=8,
            fg_color="#0f0f23", border_color="#2a2a4a",
            text_color=TEXT_PRIMARY, placeholder_text_color="#555577",
        )
        self.fecha_fin_entry.pack(fill="x", pady=(3, 10))

        ctk.CTkLabel(wrap, text="Diagnóstico", font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(anchor="w")
        self.diagnostico_entry = ctk.CTkTextbox(
            wrap, height=70, corner_radius=8,
            fg_color="#0f0f23", border_color="#2a2a4a", border_width=1,
            text_color=TEXT_PRIMARY,
        )
        self.diagnostico_entry.pack(fill="x", pady=(3, 10))

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
            btn_frame, text="Crear Orden", height=38, corner_radius=8,
            fg_color=ACCENT_COLOR, hover_color=ACCENT_HOVER,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._save,
        ).grid(row=0, column=1, padx=(6, 0), sticky="ew")

    def _get_id(self, var, ids, nombres):
        val = var.get()
        return ids[nombres.index(val)] if val in nombres else None

    def _save(self):
        id_cliente  = self._get_id(self.cliente_var,  self.cli_ids, self.cli_noms)
        id_vehiculo = self._get_id(self.vehiculo_var, self.veh_ids, self.veh_noms)
        id_mecanico = self._get_id(self.mecanico_var, self.mec_ids, self.mec_noms)
        fecha_fin   = self.fecha_fin_entry.get().strip()
        diagnostico = self.diagnostico_entry.get("1.0", "end").strip()

        if not id_cliente or not id_vehiculo or not id_mecanico:
            self.error_label.configure(text="Selecciona cliente, vehículo y mecánico.")
            return

        try:
            orden = OrdenTrabajo(
                id_orden=None, fecha_inicio=None,
                fecha_fin=fecha_fin or None, estado="pendiente",
                diagnostico=diagnostico, id_mecanico=id_mecanico,
                id_vehiculo=id_vehiculo, id_cliente=id_cliente,
            )
            crear_orden_trabajo(orden)
        except Exception as e:
            self.error_label.configure(text=f"Error: {e}")
            return

        if self.callback:
            self.callback()
        self.destroy()


class OrdenDetalleModal(ctk.CTkToplevel):
    """Modal para VER y EDITAR una orden con sus detalles (servicios y repuestos)."""
    def __init__(self, parent, row, clientes_map, vehiculos_map, mecanicos_map, callback):
        super().__init__(parent)
        self.row           = row
        self.clientes_map  = clientes_map
        self.vehiculos_map = vehiculos_map
        self.mecanicos_map = mecanicos_map
        self.callback      = callback
        self.title(f"Orden #{row.id_orden}")
        self.geometry("580x780")
        self.resizable(False, True)
        self.configure(fg_color="#1a1a2e")
        self.attributes("-topmost", True)
        self.grab_set()
        self.focus_force()

        # Cargar servicios y repuestos para los dropdowns de detalles
        try:
            servicios = listar_servicios()
            repuestos = listar_repuestos()
            self.servicios_map = {s[0]: f"{s[1]} (${float(s[3]):,.0f})" for s in servicios}
            self.repuestos_map = {r[0]: f"{r[1]} (${float(r[4]):,.0f})" for r in repuestos}
        except Exception as e:
            print(f"Error cargando servicios/repuestos: {e}")
            self.servicios_map = {}
            self.repuestos_map = {}

        self._build()
        self._load_detalles()

    def _build(self):
        # Scroll principal
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="#1a1a2e", corner_radius=0)
        self.scroll.pack(fill="both", expand=True, padx=0, pady=0)
        wrap = self.scroll

        # Encabezado
        ctk.CTkLabel(
            wrap, text=f"Orden #{self.row.id_orden}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(anchor="w", padx=28, pady=(24, 4))

        # Info de solo lectura
        info_frame = ctk.CTkFrame(wrap, fg_color="#16213e", corner_radius=8)
        info_frame.pack(fill="x", padx=28, pady=(8, 16))
        for label, valor in [
            ("Cliente",      self.clientes_map.get(self.row.id_cliente, "-")),
            ("Vehículo",     self.vehiculos_map.get(self.row.id_vehiculo, "-")),
            ("Fecha inicio", str(self.row.fecha_inicio)[:10] if self.row.fecha_inicio else "-"),
            ("Fecha fin",    str(self.row.fecha_fin)[:10]    if self.row.fecha_fin    else "-"),
        ]:
            row_f = ctk.CTkFrame(info_frame, fg_color="transparent")
            row_f.pack(fill="x", padx=14, pady=3)
            ctk.CTkLabel(row_f, text=label, font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY, width=100, anchor="w").pack(side="left")
            ctk.CTkLabel(row_f, text=valor,  font=ctk.CTkFont(size=12), text_color=TEXT_PRIMARY, anchor="w").pack(side="left")

        # Estado
        ctk.CTkLabel(wrap, text="Estado", font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(anchor="w", padx=28)
        self.estado_var = ctk.StringVar(value=self.row.estado or "pendiente")
        ctk.CTkOptionMenu(
            wrap, values=ESTADOS, variable=self.estado_var,
            height=36, corner_radius=8, fg_color="#0f0f23",
            button_color="#2a2a4a", button_hover_color="#3a3a5a", text_color=TEXT_PRIMARY,
        ).pack(fill="x", padx=28, pady=(3, 10))

        # Mecánico
        self.mec_ids  = list(self.mecanicos_map.keys())
        self.mec_noms = list(self.mecanicos_map.values())
        ctk.CTkLabel(wrap, text="Mecánico asignado", font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(anchor="w", padx=28)
        selected_mec = self.mecanicos_map.get(self.row.id_mecanico, self.mec_noms[0] if self.mec_noms else "")
        self.mecanico_var = ctk.StringVar(value=selected_mec)
        ctk.CTkOptionMenu(
            wrap, values=self.mec_noms if self.mec_noms else ["Sin mecánicos"],
            variable=self.mecanico_var, height=36, corner_radius=8,
            fg_color="#0f0f23", button_color="#2a2a4a",
            button_hover_color="#3a3a5a", text_color=TEXT_PRIMARY,
        ).pack(fill="x", padx=28, pady=(3, 10))

        # Diagnóstico
        ctk.CTkLabel(wrap, text="Diagnóstico", font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(anchor="w", padx=28)
        self.diagnostico_entry = ctk.CTkTextbox(
            wrap, height=70, corner_radius=8,
            fg_color="#0f0f23", border_color="#2a2a4a", border_width=1,
            text_color=TEXT_PRIMARY,
        )
        if self.row.diagnostico:
            self.diagnostico_entry.insert("1.0", self.row.diagnostico)
        self.diagnostico_entry.pack(fill="x", padx=28, pady=(3, 16))

        # ── SECCIÓN DETALLES ──────────────────────────────────────────
        sep = ctk.CTkFrame(wrap, height=1, fg_color="#2a2a4a")
        sep.pack(fill="x", padx=28, pady=(0, 12))

        header_det = ctk.CTkFrame(wrap, fg_color="transparent")
        header_det.pack(fill="x", padx=28, pady=(0, 8))
        header_det.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header_det, text="Servicios y Repuestos",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            header_det, text="+ Agregar",
            height=30, width=90, corner_radius=6,
            fg_color=ACCENT_COLOR, hover_color=ACCENT_HOVER,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._abrir_agregar_detalle,
        ).grid(row=0, column=1, sticky="e")

        # Contenedor donde se renderizan los detalles
        self.detalles_container = ctk.CTkFrame(wrap, fg_color="transparent")
        self.detalles_container.pack(fill="x", padx=28, pady=(0, 16))

        # ── BOTONES GUARDAR ───────────────────────────────────────────
        sep2 = ctk.CTkFrame(wrap, height=1, fg_color="#2a2a4a")
        sep2.pack(fill="x", padx=28, pady=(0, 12))

        self.error_label = ctk.CTkLabel(wrap, text="", font=ctk.CTkFont(size=12), text_color=ACCENT_COLOR)
        self.error_label.pack(anchor="w", padx=28)

        btn_frame = ctk.CTkFrame(wrap, fg_color="transparent")
        btn_frame.pack(fill="x", padx=28, pady=(6, 24))
        btn_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            btn_frame, text="Cancelar", height=38, corner_radius=8,
            fg_color="#2a2a4a", hover_color="#3a3a5a", text_color=TEXT_SECONDARY,
            command=self.destroy,
        ).grid(row=0, column=0, padx=(0, 6), sticky="ew")

        ctk.CTkButton(
            btn_frame, text="Guardar Cambios", height=38, corner_radius=8,
            fg_color=ACCENT_COLOR, hover_color=ACCENT_HOVER,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._save,
        ).grid(row=0, column=1, padx=(6, 0), sticky="ew")

    def _load_detalles(self):
        # Limpiar contenedor
        for w in self.detalles_container.winfo_children():
            w.destroy()

        try:
            todos = listar_detalle_orden()
            # tupla: (id_detalle, id_orden, id_repuesto, id_servicio, cantidad, precio)
            self.detalles = [
                DetalleOrd(
                    id_detalle  = d[0],
                    id_orden    = d[1],
                    id_repuesto = d[2],
                    id_servicio = d[3],
                    cantidad    = d[4],
                    precio      = d[5],
                )
                for d in todos if d[1] == self.row.id_orden
            ]
        except Exception as e:
            print(f"Error cargando detalles: {e}")
            self.detalles = []

        if not self.detalles:
            ctk.CTkLabel(
                self.detalles_container,
                text="Sin detalles. Usa '+ Agregar' para añadir servicios o repuestos.",
                font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY,
            ).pack(anchor="w", pady=8)
            return

        for det in self.detalles:
            nombre_serv = self.servicios_map.get(det.id_servicio, "-")
            nombre_rep  = self.repuestos_map.get(det.id_repuesto, "-")

            row_f = ctk.CTkFrame(self.detalles_container, fg_color="#16213e", corner_radius=8)
            row_f.pack(fill="x", pady=3)
            row_f.grid_columnconfigure(0, weight=1)

            info = ctk.CTkFrame(row_f, fg_color="transparent")
            info.grid(row=0, column=0, padx=12, pady=8, sticky="w")

            ctk.CTkLabel(info, text=f"Servicio: {nombre_serv}", font=ctk.CTkFont(size=12), text_color=TEXT_PRIMARY).pack(anchor="w")
            ctk.CTkLabel(info, text=f"Repuesto: {nombre_rep}  |  Cantidad: {det.cantidad}  |  Precio: ${float(det.precio):,.0f}", font=ctk.CTkFont(size=11), text_color=TEXT_SECONDARY).pack(anchor="w")

            ctk.CTkButton(
                row_f, text="🗑", width=32, height=28, corner_radius=6,
                fg_color="#2a1a1a", hover_color="#4a1a1a", text_color=ACCENT_COLOR,
                command=lambda d=det: self._eliminar_detalle(d.id_detalle),
            ).grid(row=0, column=1, padx=8, pady=8)

    def _abrir_agregar_detalle(self):
        AgregarDetalleModal(
            self,
            id_orden       = self.row.id_orden,
            servicios_map  = self.servicios_map,
            repuestos_map  = self.repuestos_map,
            callback       = self._load_detalles,
        )

    def _eliminar_detalle(self, id_detalle):
        try:
            eliminar_detalle_orden(id_detalle)
        except Exception as e:
            print(f"Error eliminando detalle: {e}")
        self._load_detalles()

    def _save(self):
        try:
            nuevo_estado      = self.estado_var.get()
            nuevo_mecanico    = self.mecanico_var.get()
            nuevo_diagnostico = self.diagnostico_entry.get("1.0", "end").strip()

            id_mecanico = self.row.id_mecanico
            if nuevo_mecanico in self.mec_noms:
                id_mecanico = self.mec_ids[self.mec_noms.index(nuevo_mecanico)]

            cambiar_estado(self.row.id_orden, nuevo_estado)
            asignar_mecanico(self.row.id_orden, id_mecanico)
            registrar_diagnostico(self.row.id_orden, nuevo_diagnostico)

        except Exception as e:
            self.error_label.configure(text=f"Error: {e}")
            return

        if self.callback:
            self.callback()
        self.destroy()


class AgregarDetalleModal(ctk.CTkToplevel):
    """Modal para agregar un servicio/repuesto a una orden."""
    def __init__(self, parent, id_orden, servicios_map, repuestos_map, callback):
        super().__init__(parent)
        self.id_orden      = id_orden
        self.servicios_map = servicios_map
        self.repuestos_map = repuestos_map
        self.callback      = callback
        self.title("Agregar Detalle")
        self.geometry("420x380")
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
            wrap, text="Agregar Servicio / Repuesto",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(anchor="w", pady=(0, 16))

        # Servicio
        self.serv_ids  = list(self.servicios_map.keys())
        self.serv_noms = list(self.servicios_map.values())
        ctk.CTkLabel(wrap, text="Servicio", font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(anchor="w")
        self.servicio_var = ctk.StringVar(value=self.serv_noms[0] if self.serv_noms else "Sin servicios")
        ctk.CTkOptionMenu(
            wrap, values=self.serv_noms if self.serv_noms else ["Sin servicios"],
            variable=self.servicio_var, height=36, corner_radius=8,
            fg_color="#0f0f23", button_color="#2a2a4a",
            button_hover_color="#3a3a5a", text_color=TEXT_PRIMARY,
        ).pack(fill="x", pady=(3, 10))

        # Repuesto
        self.rep_ids  = list(self.repuestos_map.keys())
        self.rep_noms = list(self.repuestos_map.values())
        ctk.CTkLabel(wrap, text="Repuesto (opcional)", font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(anchor="w")
        self.repuesto_var = ctk.StringVar(value=self.rep_noms[0] if self.rep_noms else "Ninguno")
        opts = ["Ninguno"] + self.rep_noms
        ctk.CTkOptionMenu(
            wrap, values=opts,
            variable=self.repuesto_var, height=36, corner_radius=8,
            fg_color="#0f0f23", button_color="#2a2a4a",
            button_hover_color="#3a3a5a", text_color=TEXT_PRIMARY,
        ).pack(fill="x", pady=(3, 10))

        # Cantidad y precio
        row_f = ctk.CTkFrame(wrap, fg_color="transparent")
        row_f.pack(fill="x")
        row_f.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(row_f, text="Cantidad", font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(row_f, text="Precio", font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).grid(row=0, column=1, sticky="w", padx=(8, 0))

        self.cantidad_entry = ctk.CTkEntry(
            row_f, placeholder_text="Ej: 2", height=36, corner_radius=8,
            fg_color="#0f0f23", border_color="#2a2a4a",
            text_color=TEXT_PRIMARY, placeholder_text_color="#555577",
        )
        self.cantidad_entry.grid(row=1, column=0, sticky="ew", pady=(3, 10))

        self.precio_entry = ctk.CTkEntry(
            row_f, placeholder_text="Ej: 50000", height=36, corner_radius=8,
            fg_color="#0f0f23", border_color="#2a2a4a",
            text_color=TEXT_PRIMARY, placeholder_text_color="#555577",
        )
        self.precio_entry.grid(row=1, column=1, sticky="ew", padx=(8, 0), pady=(3, 10))

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
            btn_frame, text="Agregar", height=38, corner_radius=8,
            fg_color=ACCENT_COLOR, hover_color=ACCENT_HOVER,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._save,
        ).grid(row=0, column=1, padx=(6, 0), sticky="ew")

    def _save(self):
        cantidad_str = self.cantidad_entry.get().strip()
        precio_str   = self.precio_entry.get().strip()

        if not cantidad_str or not precio_str:
            self.error_label.configure(text="Cantidad y precio son obligatorios.")
            return

        try:
            cantidad = int(cantidad_str)
            precio   = float(precio_str)
        except ValueError:
            self.error_label.configure(text="Cantidad debe ser entero y precio un número.")
            return

        serv_val = self.servicio_var.get()
        id_servicio = self.serv_ids[self.serv_noms.index(serv_val)] if serv_val in self.serv_noms else None

        rep_val = self.repuesto_var.get()
        id_repuesto = self.rep_ids[self.rep_noms.index(rep_val)] if rep_val in self.rep_noms else None

        try:
            detalle = DetalleOrd(
                id_detalle  = None,
                id_orden    = self.id_orden,
                id_repuesto = id_repuesto,
                id_servicio = id_servicio,
                cantidad    = cantidad,
                precio      = precio,
            )
            crear_detalle_orden(detalle)
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
            wrap, text="¿Eliminar orden?",
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