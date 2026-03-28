import json
import os
from datetime import datetime

class Ventas:
    def __init__(self, archivo_json="ventas.json"):
        self.archivo_json = archivo_json

    def procesar_compra(self, nombre, email, productos):
        """
        Recibe los datos del comprador y la lista de productos del carrito.
        Retorna (True, total) si fue exitoso, o (False, mensaje_error) si falló.
        """
        if not nombre or not email:
            return False, "Por favor, completa todos los campos obligatorios."

        productos_comprados = []
        total_a_pagar = 0.0

        for item in productos:
            subtotal = item["Precio"] * item["Cantidad"]
            total_a_pagar += subtotal
            productos_comprados.append({
                "Nombre":   item["Nombre"],
                "Precio":   item["Precio"],
                "Cantidad": item["Cantidad"],
                "Total":    subtotal
            })

        venta = {
            "Fecha":               datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Nombre":              nombre,
            "Email":               email,
            "Productos Comprados": productos_comprados,
            "Total":               total_a_pagar
        }

        self._guardar_venta(venta)
        return True, total_a_pagar

    def _guardar_venta(self, venta):
        """Carga el historial, agrega la venta nueva y guarda."""
        historial = self.cargar_ventas()
        historial.append(venta)
        with open(self.archivo_json, "w") as archivo:
            json.dump(historial, archivo, indent=4, ensure_ascii=False)

    def cargar_ventas(self):
        """Retorna la lista de ventas guardadas, o lista vacía si no existe."""
        if not os.path.exists(self.archivo_json):
            return []
        try:
            with open(self.archivo_json, "r") as archivo:
                return json.load(archivo)
        except Exception:
            return []