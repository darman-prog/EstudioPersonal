import requests
import json
import os

class Productos:
    def __init__(self, archivo_json="Productos.json"):
        self.archivo_json = archivo_json
        self.categorias = [
            "groceries", "mens-shirts", "mens-shoes", "mens-watches",
            "womens-bags", "womens-dresses", "womens-jewellery",
            "womens-shoes", "womens-watches", "tablets", "smartphones", "laptops"
        ]
        self.stock = 20
        self.lista = self._cargar()

    def _cargar(self):
        """Carga desde JSON local, si no existe llama al API"""
        if os.path.exists(self.archivo_json):
            try:
                with open(self.archivo_json, "r") as archivo:
                    return json.load(archivo)
            except Exception:
                pass
        return self._cargar_desde_api()

    def _cargar_desde_api(self):
        """Llama al API, transforma y guarda el JSON"""
        raw = []
        for categoria in self.categorias:
            try:
                url = f"https://dummyjson.com/products/category/{categoria}"
                respuesta = requests.get(url, timeout=10)
                datos = respuesta.json()
                if "products" in datos:
                    raw.extend(datos["products"])
            except Exception as e:
                print(f"Error al cargar categoría {categoria}: {str(e)}")
                continue 

        raw = sorted(raw, key=lambda x: x["price"])
        lista = []
        for p in raw:
            imagen_url = ""
            if "images" in p and p["images"]:
                imagen_url = p["images"][0]
            elif "thumbnail" in p:
                imagen_url = p["thumbnail"]

            lista.append({
                "ID":        p["id"],
                "Nombre":    p["title"],
                "Precio":    p["price"],
                "Stock":     self.stock,
                "Categoria": p["category"],
                "Imagen_URL": imagen_url
            })

        with open(self.archivo_json, "w") as archivo:
            json.dump(lista, archivo, indent=4)

        return lista

    def obtener(self):
        return self.lista