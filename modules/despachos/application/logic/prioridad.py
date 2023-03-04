def prioridad(valor):
    if valor > 5000000:
        return "prioridad_alta"
    elif valor > 1000000:
        return "prioridad_media"
    else:
        return "prioridad_baja" 