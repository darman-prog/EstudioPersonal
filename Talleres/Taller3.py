def Reserva_hoteles(cliente,dias,tarifa,hbMar):
    dicReserva = {
        "Cliente":cliente,
        "Días de estancia":dias,
        "Tarifa diaria":tarifa,
        "Habitacion con vista al mar?": "Si" if hbMar else "No" 
    }
    print("**sistema de Reserva de Hoteles**")
    for titulo , dato in dicReserva.items():
        print(f"{titulo}: {dato}")


def pedidoDatos():

    while True:

        try:     
                cliente = input("Ingresa nombre del cliente: ")
                
                dias = int(input("Ingresa el numero de dias de instancia: "))
                
                tarifa = float(input("Ingresa la tarifa total a pagar: "))
                
                hbMar = int(input("Cuarto con vista al mar? = 1.Si 2.No"))

                if hbMar == 1:
                    hbMar = True
                else:
                    hbMar = False

                return cliente , dias , tarifa , hbMar
        except ValueError as e:
             return f"Datos Erroneos Volver a ingresar error en {e}"
        

def main():
     cliente,dias,tarifa,hb_mar = pedidoDatos()
     Reserva_hoteles(cliente,dias,tarifa,hb_mar)

# if __name__ == "__main__":
#      main()


def pedido_email():
    nombre = input("ingresa tu nombre para general el email: ")
    empresa = input("ingresa la empresa a la que pertenece el email: ")
    dominion = input("ingresa el dominio de la empresa: ")

    nombre = nombre.strip().replace(" ",".")
    dominion = dominion.strip().replace(" ",".")
    empresa = empresa.strip().replace(" ",".")

    return nombre,empresa,dominion    

def generador_email(nombre,empresa,dominio):
     emailCompleto = f"{nombre}@{empresa}.{dominio}"
     return emailCompleto

def main():
     nombre , empresa , dominio = pedido_email()
     email = generador_email(nombre,empresa,dominio)
     print(email)

# if __name__ == "__main__":
#      main()


lista = [1,2,3,4,5]

# elimina indices
lista.pop(2)
# elimina el valor en especifico
lista.remove(2)

print(lista)

