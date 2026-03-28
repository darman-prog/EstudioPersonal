def ingresoNotas():
    listaNotas = []
    nombre = input("Ingresa el nombre del estudiante: ")
    for i in range(1,4):
        nota = float(input(f"ingreso la nota del estudiante numero {i} = "))
        listaNotas.append(nota)
    promedioNotas = sum(listaNotas) / len(listaNotas)
    if promedioNotas < 3:
        resultado = "Desaprueba"
        print(f"""Nombre: {nombre}\nPromedio: {promedioNotas}\nResultado: {resultado}""")
    else:
        resultado = "Aprueba"
        print(f"""Nombre: {nombre}\nPromedio: {promedioNotas}\nResultado: {resultado}""")



# ingresoNotas()


def FiltadoNumeros():
    listaNumeros = []
    listaNumerosPares = []
    for i in range(1,11):
        try:
            num = int(input(f"({i}/10) Ingresa un numero = "))
        except ValueError:
            print("solo valores en formato entero")
            return
        if num % 2 == 0:
            listaNumeros.append(num)
            listaNumerosPares.append(num)
        else:
            listaNumeros.append(num)
    print(f"Original: {listaNumeros}\nPares: {listaNumerosPares}\nCantidad de pares: {len(listaNumerosPares)}")

FiltadoNumeros()


def menuInteractivo():
    inventario = []
    Ciclo = True
    while Ciclo != False:
        print("1.Agregar producto\n2.Ver inventario\n3.Valor total\n4.eliminar producto\n5.salida")
        
        try:
            respuesta = int(input("Ingresa una opcion = "))
        except ValueError:
            print("Ingresa una entrada de teclado en formato de numero entero")
            continue
        if respuesta == 1:
            productosLlamado = AgregarProducto(inventario)
            inventario.append(productosLlamado)
            
        elif respuesta == 2:
            VerInventario(inventario )
        elif respuesta == 3:
            ValorTotal(inventario)
        elif respuesta == 4:
            inventario = eliminarProducto(inventario)
        else:
            print("saliendo del programa....")
            Ciclo = False



def AgregarProducto(inventario):
    print("Entraste a AgregarProducto")
    nombre = input("Ingresa el nombre del producto = ")
    precio = float(input("Ingresa el precio del producto = "))
    inventario = {"nombre":nombre,
                  "precio":precio}
    print(f"Producto Agregado = {inventario}")
    return inventario

def VerInventario(inventario):
    print("Entraste a VerInventario")
    for i in inventario:
        print(i)
            

def ValorTotal(inventario):
    print("Entraste a ValorTotal")
    total = 0
    for i  in inventario:
        total += i["precio"]
    print(total )

def eliminarProducto(inventario):
    print("Entraste a eliminar producto")
    nombreEliminar = input("ingresa el nombre del producto que deseas eliminar = ")

    bandera = False
    for producto in inventario:
        if  producto["nombre"]==nombreEliminar :
            inventario.remove(producto)
            print(f"producto {nombreEliminar} eliminado con exito")
            bandera = True
            break

    if not bandera:
        print("producto no encontrado")

    return inventario

# menuInteractivo()