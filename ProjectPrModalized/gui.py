import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk
from io import BytesIO
import threading
import requests

class TiendaGUI:
    def __init__(self, root,productos,carrito,ventas):
        self.root = root
        style = ttk.Style()
        style.theme_use('clam')
        self.root.title("Tienda WAILMER 🌊")
        self.root.geometry("900x600")
        self.root.configure(bg="#e0f7fa")
        self.productos_obj = productos
        self.productos = productos.obtener()
        self.carrito = carrito
        self.ventas = ventas

        # Estilos personalizados    
        self.estilo_widgets()
            
        
        # Crear frames
        self.crear_frames()
        # Mostrar categorías disponibles
        self.cargar_categorias()
        # Por defecto, mostrar la pantalla de inicio
        self.mostrar_frame_inicio()

    
    def estilo_widgets(self):
        style = ttk.Style(self.root)
        style.theme_use('default')
        
        style.configure("TButton",
                        background="#00796B",
                        foreground="white",
                        font=("Arial", 11, "bold"),
                        padding=6)
        
        style.configure("CustomCombobox.TCombobox",
                    fieldbackground="#e0f7fa",
                    background="#41b3c2",
                    foreground="#060a0a",
                    font=("Arial", 14))
        
        style.map("TButton",
                background=[('active', '#009688')])
        
        style.configure("TFrame", background="#e0f7fa")
        style.configure("TLabel", background="#e0f7fa", font=("Arial", 12))
        style.configure("TNotebook", background="#b2ebf2", padding=10)
        style.configure("TNotebook.Tab", background="#4dd0e1", padding=10)

    def crear_frames(self):
            self.notebook = ttk.Notebook(self.root)
            self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            self.frame_inicio = ttk.Frame(self.notebook)
            self.frame_busqueda = ttk.Frame(self.notebook)
            self.frame_categorias = ttk.Frame(self.notebook)
            self.frame_carrito = ttk.Frame(self.notebook)
            self.frame_ventas = ttk.Frame(self.notebook)
            
            self.notebook.add(self.frame_inicio, text="Inicio")
            self.notebook.add(self.frame_busqueda, text="Buscar Productos")
            self.notebook.add(self.frame_categorias, text="Categorías")
            self.notebook.add(self.frame_carrito, text="Carrito")
            self.notebook.add(self.frame_ventas, text="Ventas")
            
            self.configurar_frame_inicio()
            self.configurar_frame_busqueda()
            self.configurar_frame_categorias()
            self.configurar_frame_carrito()
            self.configurar_frame_ventas()
        
    def configurar_frame_inicio(self):
        label_titulo = tk.Label(self.frame_inicio, text="🏪 Tienda WAILMER 🏪", font=("Arial", 24, "bold"), bg="#e0f7fa", fg="#00695c")
        label_titulo.pack(pady=20)
        
        subtitulo = tk.Label(self.frame_inicio, text="🌊 ¡Productos submarinos! 🌊", font=("Arial", 18), bg="#e0f7fa", fg="#00796b")
        subtitulo.pack(pady=10)
        
        frame_botones = ttk.Frame(self.frame_inicio)
        frame_botones.pack(pady=30)
        
        botones = [
            ("Buscar Productos", lambda: self.notebook.select(self.frame_busqueda)),
            ("Ver Categorías", lambda: self.notebook.select(self.frame_categorias)),
            ("Ver Carrito", lambda: self.notebook.select(self.frame_carrito)),
            ("Ventas Realizadas", lambda: self.notebook.select(self.frame_ventas)),
        ]
        
        for i, (texto, comando) in enumerate(botones):
            boton = ttk.Button(frame_botones, text=texto, command=comando)
            boton.grid(row=i//2, column=i%2, padx=20, pady=10)
            self.agregar_hover(boton)


    def agregar_hover(self, boton):
        """Agrega un efecto hover simple a un botón"""
        def on_enter(e):
            boton.configure(style="Hover.TButton")
        def on_leave(e):
            boton.configure(style="TButton")

        style = ttk.Style()
        style.configure("Hover.TButton", background="#00bfa5", foreground="white")
        boton.bind("<Enter>", on_enter)
        boton.bind("<Leave>", on_leave)
    

    def configurar_frame_busqueda(self):
        # Frame de búsqueda
        frame_buscar = ttk.Frame(self.frame_busqueda)
        frame_buscar.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(frame_buscar, text="Buscar producto por nombre:", bg="#e0f7fa", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.entry_busqueda = ttk.Entry(frame_buscar, width=40)
        self.entry_busqueda.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame_buscar, text="Buscar", command=self.buscar_producto).grid(row=0, column=2, padx=5, pady=5)
        
        # Frame para mostrar resultados
        self.frame_resultados_busqueda = ttk.Frame(self.frame_busqueda)
        self.frame_resultados_busqueda.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollable canvas para productos
        self.canvas_resultados = tk.Canvas(self.frame_resultados_busqueda)
        scrollbar = ttk.Scrollbar(self.frame_resultados_busqueda, orient="vertical", command=self.canvas_resultados.yview)
        self.scrollable_frame_resultados = ttk.Frame(self.canvas_resultados)
        
        self.scrollable_frame_resultados.bind(
            "<Configure>",
            lambda e: self.canvas_resultados.configure(
                scrollregion=self.canvas_resultados.bbox("all")
            )
        )
        
        self.canvas_resultados.create_window((0, 0), window=self.scrollable_frame_resultados, anchor="nw")
        self.canvas_resultados.configure(yscrollcommand=scrollbar.set)
        
        self.canvas_resultados.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def configurar_frame_categorias(self):
      # Marco para lista de categorías
      frame_lista_cat = ttk.Frame(self.frame_categorias)
      frame_lista_cat.pack(fill=tk.X, padx=10, pady=10)
      
      tk.Label(frame_lista_cat, text="Selecciona una categoría:", bg="#e0f7fa", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)

      self.combo_categorias = ttk.Combobox(frame_lista_cat, state="readonly", width=30, style="CustomCombobox.TCombobox")
      self.combo_categorias.pack(side=tk.LEFT, padx=5)
      
      ttk.Button(frame_lista_cat, text="Ver Productos", command=self.mostrar_productos_categoria).pack(side=tk.LEFT, padx=5)

      # Marco para mostrar productos por categoría
      self.frame_productos_categoria = ttk.Frame(self.frame_categorias)
      self.frame_productos_categoria.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

      # Canvas con scroll
      self.canvas_categorias = tk.Canvas(self.frame_productos_categoria, bg="#e0f7fa", highlightthickness=0)
      scrollbar = ttk.Scrollbar(self.frame_productos_categoria, orient="vertical", command=self.canvas_categorias.yview)
      
      self.scrollable_frame_categorias = ttk.Frame(self.canvas_categorias)
      
      self.scrollable_frame_categorias.bind(
          "<Configure>",
          lambda e: self.canvas_categorias.configure(
              scrollregion=self.canvas_categorias.bbox("all")
          )
      )

      # Nuevo contenedor centrado dentro del frame desplazable
      self.center_frame = ttk.Frame(self.scrollable_frame_categorias)
      self.center_frame.pack(anchor="center")  # Esta línea centra los productos dentro del scrollable frame

      self.canvas_categorias.create_window((0, 0), window=self.scrollable_frame_categorias, anchor="nw")
      self.canvas_categorias.configure(yscrollcommand=scrollbar.set)

      self.canvas_categorias.pack(side="left", fill="both", expand=True)
      scrollbar.pack(side="right", fill="y")

    
    def configurar_frame_carrito(self):
        # Título
        tk.Label(self.frame_carrito, text="🛒 Carrito de Compras", bg="#e0f7fa" , font=("Arial", 16, "bold")).pack(pady=10)
        
        # Frame para los productos en el carrito
        self.frame_productos_carrito = ttk.Frame(self.frame_carrito)
        self.frame_productos_carrito.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollable canvas para productos del carrito
        self.canvas_carrito = tk.Canvas(self.frame_productos_carrito)
        scrollbar = ttk.Scrollbar(self.frame_productos_carrito, orient="vertical", command=self.canvas_carrito.yview)
        self.scrollable_frame_carrito = ttk.Frame(self.canvas_carrito)
        
        self.scrollable_frame_carrito.bind(
            "<Configure>",
            lambda e: self.canvas_carrito.configure(
                scrollregion=self.canvas_carrito.bbox("all")
            )
        )
        
        self.canvas_carrito.create_window((0, 0), window=self.scrollable_frame_carrito, anchor="nw")
        self.canvas_carrito.configure(yscrollcommand=scrollbar.set)
        
        self.canvas_carrito.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame para totales y finalizar compra
        frame_total = ttk.Frame(self.frame_carrito)
        frame_total.pack(fill=tk.X, padx=10, pady=10)
        
        self.label_total = tk.Label(frame_total, text="Total: $0.00", bg="#e0f7fa" ,font=("Arial", 14, "bold"))
        self.label_total.pack(side=tk.LEFT, padx=10)
        
        self.actualizar_carrito()
        
        ttk.Button(frame_total, text="Finalizar Compra", command=self.finalizar_compra).pack(side=tk.RIGHT, padx=10)

    
    def configurar_frame_ventas(self):
        # Título
        tk.Label(self.frame_ventas, text="📊 Ventas Realizadas", font=("Arial", 16, "bold"), bg="#e0f7fa").pack(pady=10)
        
        # Área de texto para mostrar ventas
        self.texto_ventas = scrolledtext.ScrolledText(self.frame_ventas, wrap=tk.WORD, width=80, height=20)
        self.texto_ventas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Botón para actualizar ventas
        ttk.Button(self.frame_ventas, text="Actualizar Ventas", command=self.mostrar_ventas).pack(pady=10)
        
        # Mostrar ventas inicialmente
        self.mostrar_ventas()
    
    def cargar_categorias(self):
        """Carga las categorías disponibles en el combobox"""
        categorias_unicas = set(producto["Categoria"] for producto in self.productos if "Categoria" in producto)
        self.combo_categorias['values'] = sorted(list(categorias_unicas))
        if self.combo_categorias['values']:
            self.combo_categorias.current(0)
    
    def mostrar_frame_inicio(self):
        """Muestra el frame de inicio"""
        self.notebook.select(self.frame_inicio)
    
    def buscar_producto(self):
        """Busca un producto por nombre"""
        nombre_busqueda = self.entry_busqueda.get().strip().lower()
        if not nombre_busqueda:
            messagebox.showwarning("Búsqueda Vacía", "Por favor, ingresa un término de búsqueda.")
            return
            
        # Limpiar resultados anteriores
        for widget in self.scrollable_frame_resultados.winfo_children():
            widget.destroy()
            
        # Buscar productos que coincidan
        encontrados = [producto for producto in self.productos if nombre_busqueda in producto["Nombre"].lower()]
        
        if not encontrados:
            tk.Label(self.scrollable_frame_resultados, text="❌ No se encontraron productos.",bg="#e0f7fa").grid(row=0, column=0, padx=10, pady=10)
            return
            
        # Mostrar productos encontrados
        self.mostrar_productos(encontrados, self.scrollable_frame_resultados)
    
    def mostrar_productos_categoria(self):
        """Muestra los productos de una categoría seleccionada"""
        categoria_seleccionada = self.combo_categorias.get()
        if not categoria_seleccionada:
            messagebox.showwarning("Categoría no seleccionada", "Por favor, selecciona una categoría.")
            return

        # Limpiar productos anteriores del frame centrado
        for widget in self.center_frame.winfo_children():
            widget.destroy()

        productos_categoria = [
            producto for producto in self.productos 
            if producto["Categoria"].lower() == categoria_seleccionada.lower()
        ]

        if not productos_categoria:
            tk.Label(self.center_frame, text="❌ No hay productos en esta categoría.").grid(row=0, column=0, padx=10, pady=10)
            return

        # Mostrar productos centrados
        self.mostrar_productos(productos_categoria, self.center_frame)

    def mostrar_productos(self, productos, frame_destino):
        """Muestra una lista de productos en el frame especificado"""
        # Usamos grid para organizar los productos en filas y columnasx
        row, col = 0, 0
        max_col = 2  # Número máximo de columnas
        
        for producto in productos:
            # Frame para cada producto
            frame_producto = ttk.Frame(frame_destino, borderwidth=2, relief="groove")
            frame_producto.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            # Imagen del producto
            self.cargar_imagen_producto(producto, frame_producto)
            
            # Información del producto
            tk.Label(frame_producto, text=producto["Nombre"],bg="#e0f7fa", font=("Arial", 12, "bold"), wraplength=200).grid(row=1, column=0, padx=5, pady=2)
            tk.Label(frame_producto, text=f"Precio: ${producto['Precio']}", font=("Arial", 10),bg="#e0f7fa").grid(row=2, column=0, padx=5, pady=2)
            tk.Label(frame_producto, text=f"Stock: {producto['Stock']} unidades", font=("Arial", 10),bg="#e0f7fa").grid(row=3, column=0, padx=5, pady=2)
            
            # Frame para cantidad y botón
            frame_acciones = ttk.Frame(frame_producto)
            frame_acciones.grid(row=4, column=0, padx=5, pady=5)
            
            tk.Label(frame_acciones, text="Cantidad:",bg="#e0f7fa").pack(side=tk.LEFT, padx=2)
            
            # Spinbox para la cantidad
            cantidad_var = tk.StringVar(value="1")
            spinbox = ttk.Spinbox(frame_acciones, from_=1, to=producto["Stock"], textvariable=cantidad_var, width=5)
            spinbox.pack(side=tk.LEFT, padx=2)
            
            # Botón para agregar al carrito
            ttk.Button(frame_acciones, text="Agregar al Carrito", 
                    command=lambda p=producto, cv=cantidad_var: self._agregar_al_carrito(p, cv)).pack(side=tk.LEFT, padx=2)
            
            # Actualizar posición para el siguiente producto
            col += 1
            if col >= max_col:
                col = 0
                row += 1
    
    def cargar_imagen_producto(self, producto, frame_destino):
        """Carga y muestra la imagen del producto"""
        frame_imagen = ttk.Frame(frame_destino, width=200, height=150)
        frame_imagen.grid(row=0, column=0, padx=5, pady=5)
        
        # Label para la imagen
        label_imagen = tk.Label(frame_imagen, text="Cargando imagen...", bg="#e0f7fa", width=120, height=130)
        label_imagen.pack(fill=tk.BOTH, expand=True)
        # Cargar imagen en un hilo separado para no bloquear la interfaz
        if "Imagen_URL" in producto and producto["Imagen_URL"]:
            threading.Thread(target=self.cargar_imagen_thread, 
                            args=(producto["Imagen_URL"], label_imagen), 
                            daemon=True).start()
        else:
            label_imagen.config(text="Sin imagen disponible")

    def cargar_imagen_thread(self, url, label):
        """Carga la imagen en un hilo separado"""
        try:
            # Descargar la imagen
            response = requests.get(url, timeout=10)  # Añadido timeout
            if response.status_code == 200:
                # Convertir a imagen
                image_data = BytesIO(response.content)
                image = Image.open(image_data)
                # Redimensionar manteniendo proporciones
                image.thumbnail((200, 150))
                
                # IMPORTANTE: Todas las actualizaciones a la GUI deben ir en el hilo principal
                def actualizar_label():
                    try:
                        photo = ImageTk.PhotoImage(image)
                        label.config(image=photo, text="")  # Limpiar el texto
                        # Guardamos la referencia como atributo del label
                        label.image_ref = photo  # Nombre diferente para evitar confusiones
                    except Exception as e:
                        print(f"Error al mostrar la imagen: {str(e)}")  # Debug
                        label.config(text=f"Error al mostrar: {str(e)[:20]}...")
                
                # Programar la actualización en el hilo principal
                self.root.after(0, actualizar_label)
            else:
                print(f"Error al descargar: Status code {response.status_code}")  # Debug
                self.root.after(0, lambda: label.config(text=f"Error: Status {response.status_code}"))
        except requests.RequestException as e:
            print(f"Error de solicitud: {str(e)}")  # Debug
            self.root.after(0, lambda: label.config(text=f"Error de red: {str(e)[:20]}..."))
        except Exception as e:
            print(f"Error inesperado: {str(e)}")  # Debug
            self.root.after(0, lambda: label.config(text=f"Error: {str(e)[:20]}..."))
    
    def actualizar_carrito(self):
        for widget in self.scrollable_frame_carrito.winfo_children():
             widget.destroy()

        carrito = self.carrito.obtener_productos()  

        if not carrito:
            tk.Label(self.scrollable_frame_carrito, text="🛒 Tu carrito está vacío.",
                    font=("Arial", 12), bg="#e0f7fa").grid(row=0, column=0, padx=10, pady=10)
            self.label_total.config(text="Total: $0.00")
            return

        for idx, item in enumerate(carrito):
            frame_item = ttk.Frame(self.scrollable_frame_carrito, borderwidth=1, relief="groove")
            frame_item.grid(row=idx, column=0, sticky="ew", padx=10, pady=5)

            subtotal = item["Precio"] * item["Cantidad"]

            tk.Label(frame_item, text=item["Nombre"], font=("Arial", 12), bg="#e0f7fa").grid(row=0, column=0, sticky="w", padx=5, pady=2)
            tk.Label(frame_item, text=f"Precio: ${item['Precio']}", font=("Arial", 10), bg="#e0f7fa").grid(row=1, column=0, sticky="w", padx=5, pady=2)
            tk.Label(frame_item, text=f"Cantidad: {item['Cantidad']}", font=("Arial", 10), bg="#e0f7fa").grid(row=2, column=0, sticky="w", padx=5, pady=2)
            tk.Label(frame_item, text=f"Subtotal: ${subtotal:.2f}", font=("Arial", 10), bg="#e0f7fa").grid(row=3, column=0, sticky="w", padx=5, pady=2)

            if "Categoria" in item:
                tk.Label(frame_item, text=f"Categoría: {item['Categoria']}", font=("Arial", 10), bg="#e0f7fa").grid(row=4, column=0, sticky="w", padx=5, pady=2)

            ttk.Button(frame_item, text="Eliminar",
                    command=lambda id=item["ID"]: self.eliminar_del_carrito(id)).grid(row=2, column=1, rowspan=2, padx=5, pady=5)

        self.label_total.config(text=f"Total: ${self.carrito.obtener_total():.2f}")  # usa el objeto
    

    def _agregar_al_carrito(self, producto, cantidad_var):
        exito = self.carrito.agregar_al_carrito(producto, cantidad_var)
        if exito:
            messagebox.showinfo("Producto agregado", f"{producto['Nombre']} agregado al carrito.")
            self.actualizar_carrito()

    def eliminar_del_carrito(self, producto_id):
        nombre = self.carrito.eliminar(producto_id)  
        self.actualizar_carrito()
        if nombre:
            messagebox.showinfo("Producto eliminado", f"{nombre} ha sido eliminado del carrito.")
    

    def confirmar_compra(self, nombre, email, ventana):
        exito, resultado = self.ventas.procesar_compra(
            nombre, email, self.carrito.obtener_productos()
        )
        if not exito:
            messagebox.showerror("Datos incompletos", resultado)
            return
        self.carrito.limpiar()
        ventana.destroy()
        messagebox.showinfo("Compra exitosa", f"¡Gracias! Total: ${resultado:.2f}")
        self.actualizar_carrito()
        self.mostrar_ventas()

    def finalizar_compra(self):
        """Finaliza la compra actual"""
        productos = self.carrito.obtener_productos()

        if not productos:
            messagebox.showinfo("Carrito vacío", "No hay productos en el carrito.")
            return

        # Ventana de datos
        ventana_compra = tk.Toplevel(self.root)
        ventana_compra.title("Finalizar Compra")
        ventana_compra.geometry("400x300")
        ventana_compra.transient(self.root)
        ventana_compra.grab_set()

        # Formulario
        tk.Label(ventana_compra, text="Completa tus datos", font=("Arial", 14, "bold")).pack(pady=10)

        frame_form = ttk.Frame(ventana_compra)
        frame_form.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        tk.Label(frame_form, text="Nombre completo:",bg="#e0f7fa").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        entry_nombre = ttk.Entry(frame_form, width=30)
        entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Correo electrónico:",bg="#e0f7fa").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        entry_email = ttk.Entry(frame_form, width=30)
        entry_email.grid(row=1, column=1, padx=5, pady=5)

        # Total
        total = self.carrito.obtener_total()
        tk.Label(frame_form, text=f"Total a pagar: ${total:.2f}", font=("Arial", 12, "bold"),bg="#e0f7fa").grid(row=2, column=0, columnspan=2, pady=10)

        frame_botones = ttk.Frame(ventana_compra)
        frame_botones.pack(pady=10)


        ttk.Button(frame_botones, text="Cancelar", command=ventana_compra.destroy).pack(side=tk.LEFT, padx=10)
        #Confirmar compra
        ttk.Button(frame_botones, text="Confirmar Compra", 
                command=lambda: self.confirmar_compra(entry_nombre.get(), entry_email.get(),ventana_compra)).pack(side=tk.RIGHT, padx=10)

    

    def mostrar_ventas(self):
        self.texto_ventas.delete(1.0, tk.END)

        ventas = self.ventas.cargar_ventas()  

        if not ventas:
            self.texto_ventas.insert(tk.END, "No hay ventas registradas.")
            return

        for i, venta in enumerate(ventas, start=1):
            self.texto_ventas.insert(tk.END, f"📌 Venta #{i}\n")
            self.texto_ventas.insert(tk.END, f"📅 Fecha: {venta.get('Fecha', 'Sin fecha')}\n")
            self.texto_ventas.insert(tk.END, f"👤 Cliente: {venta['Nombre']}\n")
            self.texto_ventas.insert(tk.END, f"📧 Email: {venta['Email']}\n")  # clave corregida

            self.texto_ventas.insert(tk.END, "\n🛒 Productos:\n")
            for producto in venta["Productos Comprados"]:
                nombre = producto.get('Nombre', 'Desconocido')
                cantidad = producto.get('Cantidad', 0)
                self.texto_ventas.insert(tk.END, f"  - {nombre} x {cantidad}\n")

            total = venta.get('Total', 0.0)
            self.texto_ventas.insert(tk.END, f"\n💰 Total: ${total:.2f}\n")
            self.texto_ventas.insert(tk.END, "══════════════════════════════════════════════════\n\n")
