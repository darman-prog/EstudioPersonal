import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk
from io import BytesIO
import threading
import requests

class TiendaGUI:
    def __init__(self, root,productos,carrito,ventas):
        self.root = root
        self.style = ttk.Style(theme='cosmo')  # Se mantiene el mismo tema que en ProjectPr.py
        self.root.title("Tienda WAILMER 🌊")
        self.root.geometry("900x600")
        self.root.configure(bg="#e8f4f8")
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
        style = self.style
        
        # ── Botones principales ──────────────────────────────────────
        style.configure("TButton",
                        background="#0077b6",
                        foreground="white",
                        font=("Arial", 11, "bold"),
                        padding=8,
                        relief="flat",
                        borderwidth=0)
        style.map("TButton",
                background=[("active", "#023e8a"),
                            ("pressed", "#03045e")],
                foreground=[("active", "white")])

        # ── Botón de peligro (eliminar) ──────────────────────────────
        style.configure("Danger.TButton",
                        background="#e63946",
                        foreground="white",
                        font=("Arial", 10, "bold"),
                        padding=6,
                        relief="flat",
                        borderwidth=0)
        style.map("Danger.TButton",
                background=[("active", "#c1121f"),
                            ("pressed", "#9d0208")])

        # ── Botón secundario (cancelar, hover) ───────────────────────
        style.configure("Secondary.TButton",
                        background="#caf0f8",
                        foreground="#023e8a",
                        font=("Arial", 10, "bold"),
                        padding=6,
                        relief="flat",
                        borderwidth=0)
        style.map("Secondary.TButton",
                background=[("active", "#90e0ef"),
                            ("pressed", "#48cae4")])

        # ── Hover especial (pantalla inicio) ─────────────────────────
        style.configure("Hover.TButton",
                        background="#00b4d8",
                        foreground="white",
                        font=("Arial", 11, "bold"),
                        padding=8,
                        relief="flat")

        # ── Frames ───────────────────────────────────────────────────
        style.configure("TFrame",
                        background="#e8f4f8")

        style.configure("Card.TFrame",
                        background="white",
                        relief="flat",
                        borderwidth=1)

        # ── Labels ───────────────────────────────────────────────────
        style.configure("TLabel",
                        background="#e8f4f8",
                        font=("Arial", 11),
                        foreground="#023e8a")

        style.configure("Title.TLabel",
                        background="#e8f4f8",
                        font=("Arial", 22, "bold"),
                        foreground="#03045e")

        style.configure("Subtitle.TLabel",
                        background="#e8f4f8",
                        font=("Arial", 14),
                        foreground="#0077b6")

        style.configure("Price.TLabel",
                        background="white",
                        font=("Arial", 12, "bold"),
                        foreground="#0077b6")

        style.configure("Muted.TLabel",
                        background="white",
                        font=("Arial", 10),
                        foreground="#6c757d")

        style.configure("Total.TLabel",
                        background="#e8f4f8",
                        font=("Arial", 14, "bold"),
                        foreground="#03045e")

        # ── Notebook (pestañas) ──────────────────────────────────────
        style.configure("TNotebook",
                        background="#023e8a",
                        borderwidth=0,
                        tabmargins=[0, 0, 0, 0])

        style.configure("TNotebook.Tab",
                        background="#023e8a",
                        foreground="#90e0ef",
                        font=("Arial", 11),
                        padding=[16, 8])

        style.map("TNotebook.Tab",
                background=[("selected", "#0077b6"),
                            ("active",   "#034078")],
                foreground=[("selected", "white"),
                            ("active",   "white")])

        # ── Combobox ─────────────────────────────────────────────────
        style.configure("TCombobox",
                        fieldbackground="white",
                        background="#0077b6",
                        foreground="#023e8a",
                        font=("Arial", 11),
                        padding=6)

        style.configure("CustomCombobox.TCombobox",
                        fieldbackground="white",
                        background="#0077b6",
                        foreground="#023e8a",
                        font=("Arial", 12),
                        padding=6)

        # ── Entry (campos de texto) ───────────────────────────────────
        style.configure("TEntry",
                        fieldbackground="white",
                        foreground="#023e8a",
                        font=("Arial", 11),
                        padding=6)

        # ── Spinbox ──────────────────────────────────────────────────
        style.configure("TSpinbox",
                        fieldbackground="white",
                        foreground="#023e8a",
                        font=("Arial", 11),
                        padding=4)

        # ── Scrollbar ────────────────────────────────────────────────
        style.configure("TScrollbar",
                        background="#b8d8e8",
                        troughcolor="#e8f4f8",
                        borderwidth=0,
                        arrowsize=14)
        style.map("TScrollbar",
                background=[("active", "#0077b6")])

        # ── Ventana principal ─────────────────────────────────────────
        self.root.configure(bg="#e8f4f8")
        self.root.option_add("*Font", "Arial 11")

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
        
        # ── Header ───────────────────────────────────────────────────
        header = tk.Frame(self.frame_inicio, bg="#0077b6", height=120)
        header.pack(fill=tk.X)
        header.pack_propagate(False)  # mantiene el alto fijo

        tk.Label(header,
                text="🏪 Tienda WAILMER 🏪",
                font=("Arial", 26, "bold"),
                bg="#0077b6",
                fg="white").pack(pady=(22, 4))

        tk.Label(header,
                text="🌊 Productos submarinos al mejor precio 🌊",
                font=("Arial", 13),
                bg="#0077b6",
                fg="#caf0f8").pack()

        # ── Separador decorativo ─────────────────────────────────────
        tk.Frame(self.frame_inicio, bg="#00b4d8", height=3).pack(fill=tk.X)

        # ── Tarjetas de navegación ───────────────────────────────────
        frame_cards = tk.Frame(self.frame_inicio, bg="#e8f4f8")
        frame_cards.pack(expand=True, pady=30, padx=30)

        botones = [
            ("🔍", "Buscar Productos",  "Encuentra lo que necesitas",  lambda: self.notebook.select(self.frame_busqueda)),
            ("📦", "Ver Categorías",    "Explora por categoría",        lambda: self.notebook.select(self.frame_categorias)),
            ("🛒", "Ver Carrito",       "Revisa tu selección",          lambda: self.notebook.select(self.frame_carrito)),
            ("📊", "Ventas Realizadas", "Historial de compras",         lambda: self.notebook.select(self.frame_ventas)),
        ]

        for i, (icono, titulo, descripcion, comando) in enumerate(botones):
            row = i // 2
            col = i % 2

            # tarjeta blanca
            card = tk.Frame(frame_cards,
                            bg="white",
                            highlightbackground="#b8d8e8",
                            highlightthickness=1,
                            cursor="hand2")
            card.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")

            # contenido de la tarjeta
            tk.Label(card,
                    text=icono,
                    font=("Arial", 28),
                    bg="white").pack(pady=(18, 4))

            tk.Label(card,
                    text=titulo,
                    font=("Arial", 12, "bold"),
                    bg="white",
                    fg="#023e8a").pack()

            tk.Label(card,
                    text=descripcion,
                    font=("Arial", 10),
                    bg="white",
                    fg="#6c757d").pack(pady=(2, 18))

            # toda la tarjeta es clickeable
            for widget in [card] + card.winfo_children():
                widget.bind("<Button-1>", lambda e, cmd=comando: cmd())

            # efecto hover en la tarjeta completa
            self._hover_card(card, comando)

            # columnas con mismo ancho
            frame_cards.columnconfigure(col, weight=1, minsize=200)

        # ── Footer ───────────────────────────────────────────────────
        tk.Frame(self.frame_inicio, bg="#023e8a", height=3).pack(fill=tk.X, side=tk.BOTTOM)
        tk.Label(self.frame_inicio,
                text="Tienda WAILMER  •  Todos los derechos reservados",
                font=("Arial", 9),
                bg="#e8f4f8",
                fg="#6c757d").pack(side=tk.BOTTOM, pady=6)


    def agregar_hover(self, boton):
        """Agrega un efecto hover simple a un botón"""
        def on_enter(e):
            boton.configure(style="Hover.TButton")
        def on_leave(e):
            boton.configure(style="TButton")

        style = self.style
        # El estilo Hover.TButton ya está configurado en estilo_widgets,
        # pero recalculamos para garantizar consistencia si se modifica runtime.
        style.configure("Hover.TButton", background="#00bfa5", foreground="white")
        boton.bind("<Enter>", on_enter)
        boton.bind("<Leave>", on_leave)

    def _hover_card(self, card, comando):
        """Efecto hover para tarjetas de la pantalla de inicio"""
        def on_enter(e):
            card.configure(bg="#e8f4f8", highlightbackground="#0077b6")
            for w in card.winfo_children():
                try:
                    w.configure(bg="#e8f4f8")
                except Exception:
                    pass

        def on_leave(e):
            card.configure(bg="white", highlightbackground="#b8d8e8")
            for w in card.winfo_children():
                try:
                    w.configure(bg="white")
                except Exception:
                    pass

        def on_click(e):
            comando()

        for widget in [card] + card.winfo_children():
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", on_click)
    

    def _hover_card_producto(self, card, body):
        """Hover suave para tarjetas de producto"""
        def on_enter(e):
            card.configure(highlightbackground="#0077b6",
                        highlightthickness=2)

        def on_leave(e):
            card.configure(highlightbackground="#b8d8e8",
                        highlightthickness=1)

        for widget in [card, body] + body.winfo_children():
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

    def configurar_frame_busqueda(self):
        # Frame de búsqueda
        frame_buscar = ttk.Frame(self.frame_busqueda)
        frame_buscar.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(frame_buscar, text="Buscar producto por nombre:", bg="#e8f4f8", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
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
        # ── Header ───────────────────────────────────────────────────
        header = tk.Frame(self.frame_categorias, bg="#0077b6", height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(header,
                text="Explorar por Categoría",
                font=("Arial", 16, "bold"),
                bg="#0077b6",
                fg="white").pack(side=tk.LEFT, padx=20, pady=18)

        # ── Barra de selección ───────────────────────────────────────
        barra = tk.Frame(self.frame_categorias, bg="#e8f4f8", pady=12)
        barra.pack(fill=tk.X, padx=20)

        tk.Label(barra,
                text="Categoría:",
                font=("Arial", 11, "bold"),
                bg="#e8f4f8",
                fg="#023e8a").pack(side=tk.LEFT, padx=(0, 8))

        self.combo_categorias = ttk.Combobox(barra,
                                            state="readonly",
                                            width=28,
                                            font=("Arial", 11))
        self.combo_categorias.pack(side=tk.LEFT, padx=(0, 10))

        self.label_contador = tk.Label(barra,
                                        text="",
                                        font=("Arial", 10),
                                        bg="#e8f4f8",
                                        fg="#6c757d")
        self.label_contador.pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(barra,
                text="  Ver Productos  ",
                font=("Arial", 11, "bold"),
                bg="#0077b6",
                fg="white",
                activebackground="#023e8a",
                activeforeground="white",
                relief="flat",
                padx=10, pady=5,
                cursor="hand2",
                command=self.mostrar_productos_categoria).pack(side=tk.LEFT)

        # ── Separador ────────────────────────────────────────────────
        tk.Frame(self.frame_categorias, bg="#b8d8e8", height=1).pack(fill=tk.X, padx=20)

        # ── Área de productos con scroll ─────────────────────────────
        self.frame_productos_categoria = tk.Frame(self.frame_categorias, bg="#e8f4f8")
        self.frame_productos_categoria.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.canvas_categorias = tk.Canvas(self.frame_productos_categoria,
                                            bg="#e8f4f8",
                                            highlightthickness=0)

        scrollbar = ttk.Scrollbar(self.frame_productos_categoria,
                                orient="vertical",
                                command=self.canvas_categorias.yview)

        self.scrollable_frame_categorias = tk.Frame(self.canvas_categorias, bg="#e8f4f8")
        self.scrollable_frame_categorias.bind(
            "<Configure>",
            lambda e: self.canvas_categorias.configure(
                scrollregion=self.canvas_categorias.bbox("all")
            )
        )

        self.canvas_categorias.bind_all(
            "<MouseWheel>",
            lambda e: self.canvas_categorias.yview_scroll(int(-1*(e.delta/120)), "units")
        )

        self.center_frame = tk.Frame(self.scrollable_frame_categorias, bg="#e8f4f8")
        self.center_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # ── PRIMERO create_window, DESPUÉS el bind ───────────────────
        self.canvas_win = self.canvas_categorias.create_window(
            (0, 0),
            window=self.scrollable_frame_categorias,
            anchor="nw"
        )

        # ahora sí existe el item — el bind puede encontrarlo
        self.canvas_categorias.bind(
            "<Configure>",
            lambda e: self.canvas_categorias.itemconfig(
                self.canvas_win,      # usamos la referencia directa, no find_all()
                width=e.width
            )
        )

        self.canvas_categorias.configure(yscrollcommand=scrollbar.set)
        self.canvas_categorias.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    
    def configurar_frame_carrito(self):
        # Título
        tk.Label(self.frame_carrito, text=" Carrito de Compras", bg="#e8f4f8" , font=("Arial", 18, "bold")).pack(pady=10)
        
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
        
        self.label_total = tk.Label(frame_total, text="Total: $0.00", bg="#e8f4f8" ,font=("Arial", 14, "bold"))
        self.label_total.pack(side=tk.LEFT, padx=10)
        
        self.actualizar_carrito()
        
        ttk.Button(frame_total, text="Finalizar Compra", command=self.finalizar_compra).pack(side=tk.RIGHT, padx=10)

    
    def configurar_frame_ventas(self):
        # Título
        tk.Label(self.frame_ventas, text="📊 Ventas Realizadas", font=("Arial", 16, "bold"), bg="#e8f4f8").pack(pady=10)
        
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
            tk.Label(self.scrollable_frame_resultados, text="❌ No se encontraron productos.",bg="#e8f4f8").grid(row=0, column=0, padx=10, pady=10)
            return
            
        # Mostrar productos encontrados
        self.mostrar_productos(encontrados, self.scrollable_frame_resultados)
    



    def mostrar_productos_categoria(self):
            categoria_seleccionada = self.combo_categorias.get()
            if not categoria_seleccionada:
                messagebox.showwarning("Sin categoría", "Por favor selecciona una categoría.")
                return

            for widget in self.center_frame.winfo_children():
                widget.destroy()

            productos_categoria = [
                p for p in self.productos
                if p["Categoria"].lower() == categoria_seleccionada.lower()
            ]

            # actualiza el contador
            self.label_contador.config(
                text=f"{len(productos_categoria)} producto(s) encontrado(s)"
            )

            if not productos_categoria:
                tk.Label(self.center_frame,
                        text="No hay productos en esta categoría.",
                        font=("Arial", 12),
                        bg="#e8f4f8",
                        fg="#6c757d").grid(row=0, column=0, padx=10, pady=30)
                return

            self.mostrar_productos(productos_categoria, self.center_frame)

    def mostrar_productos(self, productos, frame_destino):
        """Muestra una lista de productos en el frame especificado"""
        row, col = 0, 0
        max_col = 2

        for producto in productos:

            # ── Tarjeta principal ────────────────────────────────────
            card = tk.Frame(frame_destino,
                            bg="white",
                            highlightbackground="#b8d8e8",
                            highlightthickness=1,
                            cursor="hand2")
            card.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")

            # ── Imagen ───────────────────────────────────────────────
            frame_imagen = tk.Frame(card, bg="#e8f4f8", height=160)
            frame_imagen.pack(fill=tk.X)
            frame_imagen.pack_propagate(False)

            label_imagen = tk.Label(frame_imagen,
                                    text="Cargando...",
                                    bg="#e8f4f8",
                                    fg="#90cce8",
                                    font=("Arial", 10))
            label_imagen.pack(expand=True)

            if "Imagen_URL" in producto and producto["Imagen_URL"]:
                threading.Thread(
                    target=self.cargar_imagen_thread,
                    args=(producto["Imagen_URL"], label_imagen),
                    daemon=True
                ).start()
            else:
                label_imagen.config(text="Sin imagen")

            # ── Separador azul decorativo ────────────────────────────
            tk.Frame(card, bg="#00b4d8", height=2).pack(fill=tk.X)

            # ── Cuerpo de la tarjeta ─────────────────────────────────
            body = tk.Frame(card, bg="white", padx=12, pady=10)
            body.pack(fill=tk.BOTH, expand=True)

            # Badge de categoría
            if "Categoria" in producto:
                badge = tk.Label(body,
                                text=producto["Categoria"].upper(),
                                font=("Arial", 8, "bold"),
                                bg="#e8f4f8",
                                fg="#0077b6",
                                padx=6, pady=2)
                badge.pack(anchor="w", pady=(0, 4))

            # Nombre
            tk.Label(body,
                    text=producto["Nombre"],
                    font=("Arial", 12, "bold"),
                    bg="white",
                    fg="#023e8a",
                    wraplength=200,
                    justify="left").pack(anchor="w")

            # Precio
            tk.Label(body,
                    text=f"${producto['Precio']:.2f}",
                    font=("Arial", 14, "bold"),
                    bg="white",
                    fg="#0077b6").pack(anchor="w", pady=(4, 0))

            # Stock con color según disponibilidad
            stock = producto["Stock"]
            stock_color = "#28a745" if stock > 10 else "#ffc107" if stock > 0 else "#dc3545"
            tk.Label(body,
                    text=f"Stock: {stock} unidades",
                    font=("Arial", 10),
                    bg="white",
                    fg=stock_color).pack(anchor="w", pady=(2, 8))

            # ── Separador ────────────────────────────────────────────
            tk.Frame(body, bg="#e8f4f8", height=1).pack(fill=tk.X, pady=(0, 8))

            # ── Fila cantidad + botón ────────────────────────────────
            frame_acciones = tk.Frame(body, bg="white")
            frame_acciones.pack(fill=tk.X)

            tk.Label(frame_acciones,
                    text="Cant:",
                    font=("Arial", 10),
                    bg="white",
                    fg="#6c757d").pack(side=tk.LEFT)

            cantidad_var = tk.StringVar(value="1")
            spinbox = ttk.Spinbox(frame_acciones,
                                from_=1,
                                to=producto["Stock"],
                                textvariable=cantidad_var,
                                width=4,
                                font=("Arial", 10))
            spinbox.pack(side=tk.LEFT, padx=(4, 8))

            btn = tk.Button(frame_acciones,
                            text="+ Agregar",
                            font=("Arial", 10, "bold"),
                            bg="#0077b6",
                            fg="white",
                            activebackground="#023e8a",
                            activeforeground="white",
                            relief="flat",
                            padx=10, pady=4,
                            cursor="hand2",
                            command=lambda p=producto, cv=cantidad_var: self._agregar_al_carrito(p, cv))
            btn.pack(side=tk.RIGHT)

            # ── Hover en la tarjeta ──────────────────────────────────
            self._hover_card_producto(card, body)

            # ── Posición siguiente ───────────────────────────────────
            col += 1
            if col >= max_col:
                col = 0
                row += 1

        # columnas con mismo peso
        for c in range(max_col):
            frame_destino.columnconfigure(c, weight=1)
    
    def cargar_imagen_producto(self, producto, frame_destino):
        """Carga y muestra la imagen del producto"""
        frame_imagen = ttk.Frame(frame_destino, width=200, height=150)
        frame_imagen.grid(row=0, column=0, padx=5, pady=5)
        
        # Label para la imagen
        label_imagen = tk.Label(frame_imagen, text="Cargando imagen...", bg="#e8f4f8", width=120, height=130)
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
                    font=("Arial", 16), bg="#6ec7e5").grid(row=0, column=0, padx=10, pady=10)
            self.label_total.config(text="Total: $0.00")
            return

        for idx, item in enumerate(carrito):
            frame_item = ttk.Frame(self.scrollable_frame_carrito, borderwidth=1, relief="groove")
            frame_item.grid(row=idx, column=0, sticky="ew", padx=10, pady=5)

            subtotal = item["Precio"] * item["Cantidad"]

            tk.Label(frame_item, text=item["Nombre"], font=("Arial", 12), bg="#e8f4f8").grid(row=0, column=0, sticky="w", padx=5, pady=2)
            tk.Label(frame_item, text=f"Precio: ${item['Precio']}", font=("Arial", 10), bg="#e8f4f8").grid(row=1, column=0, sticky="w", padx=5, pady=2)
            tk.Label(frame_item, text=f"Cantidad: {item['Cantidad']}", font=("Arial", 10), bg="#e8f4f8").grid(row=2, column=0, sticky="w", padx=5, pady=2)
            tk.Label(frame_item, text=f"Subtotal: ${subtotal:.2f}", font=("Arial", 10), bg="#e8f4f8").grid(row=3, column=0, sticky="w", padx=5, pady=2)

            if "Categoria" in item:
                tk.Label(frame_item, text=f"Categoría: {item['Categoria']}", font=("Arial", 10), bg="#e8f4f8").grid(row=4, column=0, sticky="w", padx=5, pady=2)

            ttk.Button(frame_item, text="Eliminar", style="Danger.TButton",
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

        tk.Label(frame_form, text="Nombre completo:",bg="#e8f4f8").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        entry_nombre = ttk.Entry(frame_form, width=30)
        entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Correo electrónico:",bg="#e8f4f8").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        entry_email = ttk.Entry(frame_form, width=30)
        entry_email.grid(row=1, column=1, padx=5, pady=5)

        # Total
        total = self.carrito.obtener_total()
        tk.Label(frame_form, text=f"Total a pagar: ${total:.2f}", font=("Arial", 12, "bold"),bg="#e8f4f8").grid(row=2, column=0, columnspan=2, pady=10)

        frame_botones = ttk.Frame(ventana_compra)
        frame_botones.pack(pady=10)


        ttk.Button(frame_botones, text="Cancelar",
           style="Secondary.TButton",
           command=ventana_compra.destroy)
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
