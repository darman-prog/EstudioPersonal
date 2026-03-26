def clasificar_estudiantes(nombre,nota_final,asistencia):
    estados = ["Aprobado","Habilita","Reprobado"]
    if nota_final >= 3 and asistencia > 80:
        return f"{nombre}: {estados[0]}"
    elif nota_final >= 2.5 and nota_final <= 2.9:
        return f"{nombre}: {estados[1]}"
    else:
        return f"{nombre}: {estados[2]}"

clasificadorEpico = clasificar_estudiantes("Diego",5,100)
print(clasificadorEpico)