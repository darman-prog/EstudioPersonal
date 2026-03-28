def clasificar_estudiantes(nombre,nota_final,asistencia):
    estados = ["Aprobado","Habilita","Reprobado"]
    if nota_final >= 3 and asistencia > 80:
        return f"{nombre}: {estados[0]}"
    elif nota_final >= 2.5 and nota_final <= 2.9 and asistencia > 80:
        return f"{nombre}: {estados[1]}"
    else:
        return f"{nombre}: {estados[2]}"

# clasificadorEpico = clasificar_estudiantes("Diego",5,90)
# print(clasificadorEpico)

def primos_en_rango(num1,num2):
    lista_primos = []
    for i in range(num1,num2+1):
        if i < 2: continue
        es_primo = True
        for j in range(2,int(i**0.5) + 1):
            if i % j == 0:
                es_primo = False
                break
        if es_primo:
            lista_primos.append(i)
    print(lista_primos,f" encontre en total {len(lista_primos)} primos ")

# primos_en_rango(10,20)


def es_palindromo(nombre):
    nombreVerificacion = nombre[::-1]
    if nombre == nombreVerificacion:
        print(True)
    else:
        print(False)
es_palindromo("radio")