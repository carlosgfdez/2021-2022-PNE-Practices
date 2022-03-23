#Escribe una clase llamada 'Student' que almacene el NIF, el número de expediente y la mejor nota de un estudiante
class Student:
    def __init__(self, nif, nexp, score):
        self.nif = nif
        self.nexp = nexp
        self.score = score

    def __str__(self):
        return f"NIF: {self.nif}, Number of expedient: {self.nexp}, Maximum score: {self.score}"

s1 = Student('1A', 1, 7.5)
print(s1)
s2 = Student('2B', 3, 5)
print(s2)