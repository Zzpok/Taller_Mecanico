# Permisos por rol
# Cada rol tiene una lista de secciones a las que puede acceder

PERMISOS = {
    "admin": [
        "clientes",
        "vehiculos",
        "mecanicos",
        "ordenes",
        "servicios",
        "repuestos",
        "facturas",
        "usuarios",
    ],
    "mecanico": [
        "ordenes",
        "vehiculos",
        "repuestos",
    ],
}


def get_secciones(rol: str) -> list:
    """Retorna las secciones permitidas para un rol."""
    return PERMISOS.get(rol, [])


def puede_acceder(rol: str, seccion: str) -> bool:
    """Verifica si un rol puede acceder a una sección."""
    return seccion in get_secciones(rol)