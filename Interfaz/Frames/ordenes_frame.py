import customtkinter as ctk
from Servicios.OrdenTrabajo_serv import listar_ordenes, crear_orden_trabajo, cambiar_estado, registrar_diagnostico, asignar_mecanico, eliminar_orden
from Servicios.Clientes_serv import listar_clientes
from Servicios.Vehiculos_serv import listar_vehiculos
from Servicios.Mecanico_serv import listar_mecanicos
from Componentes.OrdenTrabajo import OrdenTrabajo
from Interfaz.Frames.base_frame import BaseFrame

BG_MAIN        = "#0f0f23"
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
            # tupla: (id_orden, fecha_inicio, fecha_fin, estado, diagnostico, id_mecanico, id_vehiculo, id_cliente)
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
        self.row           = row
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
                id_orden     = None,
                fecha_inicio = None,
                fecha_fin    = fecha_fin or None,
                estado       = "pendiente",
                diagnostico  = diagnostico,
                id_mecanico  = id_mecanico,
                id_vehiculo  = id_vehiculo,
                id_cliente   = id_cliente,
            )
            crear_orden_trabajo(orden)
        except Exception as e:
            self.error_label.configure(text=f"Error: {e}")
            return

        if self.callback:
            self.callback()
        self.destroy()


class OrdenDetalleModal(ctk.CTkToplevel):
    """Modal para VER y EDITAR una orden — cambiar estado, mecánico y diagnóstico."""
    def __init__(self, parent, row, clientes_map, vehiculos_map, mecanicos_map, callback):
        super().__init__(parent)
        self.row           = row
        self.clientes_map  = clientes_map
        self.vehiculos_map = vehiculos_map
        self.mecanicos_map = mecanicos_map
        self.callback      = callback
        self.title(f"Orden #{row.id_orden}")
        self.geometry("460x580")
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
            wrap, text=f"Orden #{self.row.id_orden}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(anchor="w")

        # Info de solo lectura
        info_frame = ctk.CTkFrame(wrap, fg_color="#16213e", corner_radius=8)
        info_frame.pack(fill="x", pady=(12, 16))
        for label, valor in [
            ("Cliente",      self.clientes_map.get(self.row.id_cliente, "-")),
            ("Vehículo",     self.vehiculos_map.get(self.row.id_vehiculo, "-")),
            ("Fecha inicio", str(self.row.fecha_inicio)[:10] if self.row.fecha_inicio else "-"),
            ("Fecha fin",    str(self.row.fecha_fin)[:10]    if self.row.fecha_fin    else "-"),
        ]:
            row_f = ctk.CTkFrame(info_frame, fg_color="transparent")
            row_f.pack(fill="x", padx=14, pady=3)
            ctk.CTkLabel(row_f, text=label, font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY, width=100, anchor="w").pack(side="left")
            ctk.CTkLabel(row_f, text=valor,  font=ctk.CTkFont(size=12), text_color=TEXT_PRIMARY,   anchor="w").pack(side="left")

        # Cambiar estado
        ctk.CTkLabel(wrap, text="Estado", font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(anchor="w")
        self.estado_var = ctk.StringVar(value=self.row.estado or "pendiente")
        ctk.CTkOptionMenu(
            wrap, values=ESTADOS, variable=self.estado_var,
            height=36, corner_radius=8, fg_color="#0f0f23",
            button_color="#2a2a4a", button_hover_color="#3a3a5a", text_color=TEXT_PRIMARY,
        ).pack(fill="x", pady=(3, 10))

        # Cambiar mecánico
        self.mec_ids  = list(self.mecanicos_map.keys())
        self.mec_noms = list(self.mecanicos_map.values())
        ctk.CTkLabel(wrap, text="Mecánico asignado", font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(anchor="w")
        selected_mec = self.mecanicos_map.get(self.row.id_mecanico, self.mec_noms[0] if self.mec_noms else "")
        self.mecanico_var = ctk.StringVar(value=selected_mec)
        ctk.CTkOptionMenu(
            wrap, values=self.mec_noms if self.mec_noms else ["Sin mecánicos"],
            variable=self.mecanico_var, height=36, corner_radius=8,
            fg_color="#0f0f23", button_color="#2a2a4a",
            button_hover_color="#3a3a5a", text_color=TEXT_PRIMARY,
        ).pack(fill="x", pady=(3, 10))

        # Diagnóstico
        ctk.CTkLabel(wrap, text="Diagnóstico", font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(anchor="w")
        self.diagnostico_entry = ctk.CTkTextbox(
            wrap, height=80, corner_radius=8,
            fg_color="#0f0f23", border_color="#2a2a4a", border_width=1,
            text_color=TEXT_PRIMARY,
        )
        if self.row.diagnostico:
            self.diagnostico_entry.insert("1.0", self.row.diagnostico)
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
            btn_frame, text="Guardar Cambios", height=38, corner_radius=8,
            fg_color=ACCENT_COLOR, hover_color=ACCENT_HOVER,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._save,
        ).grid(row=0, column=1, padx=(6, 0), sticky="ew")

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