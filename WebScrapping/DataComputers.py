from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
import os


# =========================
# 🔹 UTILIDADES
# =========================

def limpiar_precio(precio):
    precio = precio.replace("$", "").replace(".", "").replace(",", "").strip()
    try:
        return int(precio)
    except:
        return None


def extraer_ram(texto):
    texto = texto.upper().replace(" ", "")
    
    for i in range(len(texto)):
        if texto[i:i+2] == "GB":
            numero = ""
            j = i - 1
            while j >= 0 and texto[j].isdigit():
                numero = texto[j] + numero
                j -= 1
            
            if numero:
                return int(numero)
    
    return None


def detectar_grafica(texto):
    texto = texto.lower()
    if "rtx" in texto or "gtx" in texto or "radeon" in texto:
        return "dedicada"
    return "integrada"


# =========================
# 🔹 PARSER INTELIGENTE
# =========================

def parsear_dinamico(nombre, specs):
    # 🟢 Caso Alkosto (con "-")
    if " - " in nombre:
        partes = nombre.split(" - ")
        
        data = {
            "procesador": None,
            "ram_gb": None,
            "almacenamiento": None,
            "tipo_almacenamiento": None
        }

        for parte in partes:
            p = parte.lower()

            if "intel" in p or "ryzen" in p:
                data["procesador"] = parte.strip()

            if "ram" in p and "gb" in p:
                numero = "".join([c for c in parte if c.isdigit()])
                if numero:
                    data["ram_gb"] = int(numero)

            if "ssd" in p or "hdd" in p:
                numero = "".join([c for c in parte if c.isdigit()])
                if numero:
                    data["almacenamiento"] = int(numero)

                if "ssd" in p:
                    data["tipo_almacenamiento"] = "SSD"
                elif "hdd" in p:
                    data["tipo_almacenamiento"] = "HDD"

        return data

    # 🔵 Caso Ktronix / otros
    else:
        texto = nombre + " " + " ".join(specs)

        return {
            "procesador": texto,
            "ram_gb": extraer_ram(texto),
            "almacenamiento": None,
            "tipo_almacenamiento": "SSD" if "ssd" in texto.lower() else None
        }


# =========================
# 🔹 SCRAPER
# =========================

def scrapear_tienda(url, xpath_items, xpath_nombre, xpath_precio, xpath_ul=None):
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0")
    
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(5)

    productos = []

    items = driver.find_elements(By.XPATH, xpath_items)

    for item in items:
        try:
            nombre = item.find_element(By.XPATH, xpath_nombre).text

            # 🔹 Precio
            try:
                precio_elemento = item.find_element(By.XPATH, xpath_precio)
                precio = precio_elemento.text.strip()

                if not precio:
                    precio = precio_elemento.get_attribute("textContent").strip()

                precio = limpiar_precio(precio)

            except:
                precio = None

            # 🔹 Specs
            specs = []
            if xpath_ul:
                try:
                    ul = item.find_element(By.XPATH, xpath_ul)
                    lis = ul.find_elements(By.TAG_NAME, "li")
                    specs = [li.text for li in lis]
                except:
                    pass

            # 🔥 Parseo
            data = parsear_dinamico(nombre, specs)
            grafica = detectar_grafica(nombre)

            productos.append({
                "nombre": nombre,
                "precio": precio,
                "ram_gb": data["ram_gb"],
                "procesador": data["procesador"],
                "almacenamiento": data["almacenamiento"],
                "tipo_almacenamiento": data["tipo_almacenamiento"],
                "tipo_grafica": grafica,
                "especificaciones": specs
            })

        except:
            continue

    driver.quit()
    return productos


# =========================
# 🔹 JSON SIN DUPLICADOS
# =========================

def guardar_json_sin_duplicados(nuevos_datos, archivo="computadores.json"):
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)
    else:
        datos = []

    existentes = set(pc["nombre"] for pc in datos)

    for pc in nuevos_datos:
        if pc["nombre"] not in existentes:
            datos.append(pc)

    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


# =========================
# 🔹 FILTRO Y SCORING
# =========================

def filtrar_por_precio(lista, min_precio, max_precio):
    return [
        pc for pc in lista
        if pc["precio"] and min_precio <= pc["precio"] <= max_precio
    ]


def puntuacion(pc):
    score = 0

    if pc["ram_gb"]:
        if pc["ram_gb"] >= 16:
            score += 2
        elif pc["ram_gb"] >= 8:
            score += 1

    if pc["tipo_grafica"] == "dedicada":
        score += 3

    if "i7" in pc["nombre"].lower() or "ryzen 7" in pc["nombre"].lower():
        score += 2

    return score


# =========================
# 🔥 EJECUCIÓN
# =========================

# tiendas = [
#     {
#         "nombre": "Exito",
#         "url": "https://www.exito.com/s?q=computadores&sort=score_desc&page=0",
#         "items": "//div[.//h3[contains(@class,'styles_name__qQJiK')]]",
#         "nombre_xpath": ".//h3[contains(@class,'styles_name__qQJiK')]",
#         "precio_xpath": ".//span[contains(@class,'price_fs-price')]",
#         "ul": None
#     }
# ]

# todos_los_productos = []

# for tienda in tiendas:
#     print(f"Scrapeando {tienda['nombre']}...")

#     resultados = scrapear_tienda(
#         tienda["url"],
#         tienda["items"],
#         tienda["nombre_xpath"],
#         tienda["precio_xpath"],
#         tienda["ul"]
#     )

#     for r in resultados:
#         r["tienda"] = tienda["nombre"]

#     todos_los_productos.extend(resultados)

# # 💾 Guardar JSON
# guardar_json_sin_duplicados(todos_los_productos)

# # 🎯 Filtrar
# filtrados = filtrar_por_precio(todos_los_productos, 3000000, 4000000)

# # 🏆 Ranking
# ordenados = sorted(filtrados, key=lambda x: puntuacion(x), reverse=True)

# print("\n🏆 MEJORES OPCIONES:\n")
# for pc in ordenados[:5]:
#     print(puntuacion(pc), pc["nombre"], pc["precio"], pc["tienda"])


# =========================
# 🔥 NUEVA EJECUCIÓN (SOLO LECTURA DE JSON)
# =========================

archivo_json = "computadores.json"

if os.path.exists(archivo_json):
    # 1. Leer los datos del archivo que ya tienes
    with open(archivo_json, "r", encoding="utf-8") as f:
        todos_los_productos = json.load(f)
    
    print(f"✅ Se cargaron {len(todos_los_productos)} productos desde {archivo_json}")

    # 2. 🎯 Filtrar (usando tu función existente)
    # Ajusta los rangos de precio si lo deseas
    filtrados = filtrar_por_precio(todos_los_productos, 2500000, 4000000)

    # 3. 🏆 Ranking (usando tu función 'puntuacion')
    ordenados = sorted(filtrados, key=lambda x: puntuacion(x), reverse=True)

    # 4. Mostrar resultados
    print(f"\n✅ Se encontraron {len(filtrados)} productos en el rango de precio.")
    print("\n🏆 MEJORES OPCIONES SEGÚN RANKING:\n")
    
    if not ordenados:
        print("No se encontraron productos que coincidan con los filtros.")
    else:
        for pc in ordenados[:10]: # Mostramos los 10 mejores
            puntos = puntuacion(pc)
            print(f"⭐ {puntos} Pts | {pc['nombre']}")
            print(f"   💰 ${pc['precio']:,} | 📍 {pc.get('tienda', 'Tienda desconocida')}\n")

else:
    print(f"❌ Error: No se encontró el archivo '{archivo_json}'. Asegúrate de que el nombre sea correcto.")