import ttkbootstrap as ttk
from productos import Productos
from carrito import Carrito
from ventas import Ventas
from gui import TiendaGUI

def main():

    root = ttk.Window(themename="cosmo")
    productos = Productos()
    carrito = Carrito()
    ventas = Ventas()
    app = TiendaGUI(root, productos, carrito , ventas)
    root.mainloop()


if __name__ == "__main__":
    main()