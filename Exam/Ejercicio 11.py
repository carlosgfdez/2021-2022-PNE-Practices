#Crea un programa principal que solicite la información de 5 estudiantes. Almacénalos en una lista e imprímela por pantalla

class Student:
    def __init__(self, nif, nexp, score):
        self.nif = nif
        self.nexp = nexp
        self.score = score

    def __str__(self):
        text = f"NIF: {self.nif}, Number of expedient: {self.nexp}, Maximum score: {self.score}"
        return text

for i in range(5):
    n = i + 1
    user_nif = input(f"Enter a NIF for student {n}: ")
    user_nexp = input(f"Enter a number of expedient for student {n}: ")
    user_score = input(f"Enter the maximum score for student {n}: ")
    s = Student(user_nif, user_nexp, user_score)
    print(f"Student {n}: {s}")