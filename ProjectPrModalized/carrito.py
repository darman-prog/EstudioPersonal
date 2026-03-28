from tkinter import messagebox
import os
import json

class Carrito:
    def __init__(self, archivo_json="carrito.json"):
        self.archivo_json = archivo_json
        self.items = self._cargar()       

    def _cargar(self):
        if os.path.exists(self.archivo_json):
            try:
                with open(self.archivo_json, "r") as archivo:
                    return json.load(archivo)
            except Exception:
                return []
        return []

    def _guardar(self):
        with open(self.archivo_json, "w", encoding="utf-8") as archivo:
            json.dump(self.items, archivo, indent=4)

    def obtener_productos(self):
        return self.items

    def obtener_total(self):
        total = 0
        for item in self.items:
            try:
                total += float(item.get("Precio", 0)) * int(item.get("Cantidad", 0))
            except (ValueError, TypeError):
                continue
        return total

    def agregar_al_carrito(self, producto, cantidad_var):
        try:
            cantidad = int(cantidad_var.get())
        except ValueError:
            messagebox.showwarning("Entrada inválida", "Por favor ingrese una cantidad válida.")
            return False

        if cantidad <= 0:
            messagebox.showwarning("Cantidad inválida", "Por favor seleccione una cantidad mayor a 0.")
            return False

        if cantidad > producto["Stock"]:
            messagebox.showwarning("Stock insuficiente", f"Solo hay {producto['Stock']} unidades disponibles.")
            return False

        for item in self.items:               # usa self.items, no el JSON
            if item["ID"] == producto["ID"]:
                item["Cantidad"] += cantidad
                item["Total"] = item["Precio"] * item["Cantidad"]
                self._guardar()
                return True

        self.items.append({
            "ID":       producto["ID"],
            "Nombre":   producto["Nombre"],
            "Precio":   producto["Precio"],
            "Cantidad": cantidad,
            "Total":    producto["Precio"] * cantidad
        })
        self._guardar()
        return True                           # gui.py usa este True para mostrar el mensaje

    def eliminar(self, producto_id):
        for item in self.items:
            if item["ID"] == producto_id:
                nombre = item["Nombre"]
                self.items.remove(item)
                self._guardar()
                return nombre             
        return None

    def limpiar(self):
        self.items.clear()
        self._guardar()