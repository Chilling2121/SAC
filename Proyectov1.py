#Proyecto de Sistema de Asignacion de Cupos
#SAC

#Clase Grupo-Prioritario   
class GrupoPrioritario:
    def __init__(self, id_grupo, nombres_grupo, descripcion, porcentaje_cupos):
        self.id_grupo = id_grupo
        self.nombres_grupo = nombres_grupo
        self.descripcion = descripcion
        self.porcentaje_cupos = porcentaje_cupos

    def calcular_cupos_reservados(self, total_cupos):
        return int((self.porcentaje_cupos / 100) * total_cupos)

    def __str__(self):
        return f"{self.nombres_grupo} ({self.porcentaje_cupos}%)"


#Clase Cupo
class Cupo:
    def __init__(self, id_cupo, carrera):
        self.id_cupo = id_cupo
        self.carrera = carrera
        self.aspirante = None
        self.estado = "Disponible"

    def asignar(self, aspirante):
        if self.estado != "Disponible":
            return False
        if self.carrera.asignar_cupo():
            self.aspirante = aspirante
            self.estado = "Asignado"
            return True
        return False

    def liberar(self):
        if self.estado == "Asignado":
            self.aspirante = None
            self.estado = "Disponible"
            self.carrera.cupos_ocupados -= 1

    def info(self):
        asignado = self.aspirante.nombres if self.aspirante else "Nadie"
        return f"Cupo {self.id_cupo} - {self.carrera.nombres}: {asignado}"


#Clase Aspirante
class Aspirante:
    def __init__(self, idAspirante, nombres, apellidos, identificacion, calificacion, merito_academico=False, vulnerabilidad=False):
        self.idAspirante = idAspirante
        self.nombres = nombres
        self.apellidos = apellidos
        self.__identificacion = identificacion   # privado
        self.calificacion = calificacion
        self.merito_academico = merito_academico
        self.vulnerabilidad = vulnerabilidad
        self.grupo_prioritario = None
        self.estado = "Registrado"

    # Encapsulamiento
    @property
    def identificacion(self):
        return self.__identificacion

    def asignar_grupo(self):
        if self.merito_academico:
            self.grupo_prioritario = "Mérito Académico"
        elif self.vulnerabilidad:
            self.grupo_prioritario = "Vulnerabilidad Socioeconómica"
        else:
            self.grupo_prioritario = "Población General"
        return self.grupo_prioritario

    def informacion(self):
        return f"{self.nombres} {self.apellidos} ({self.identificacion}) - Grupo: {self.grupo_prioritario or 'Sin asignar'}"


#No implementados por el momento
    #Método para Postular a una carrera
    #def Postular(self):
        #print("El aspirante se postula a una carrera")
        
    #def aceptar_cupo(self):
        #pass
    
    #def rechazar_cupo(self):
        #pass


#Clase Carrera
class Carrera:
    def __init__(self, id_carrera, nombres, facultad, total_cupos):
        self.id_carrera = id_carrera
        self.nombres = nombres
        self.facultad = facultad
        self.total_cupos = total_cupos
        self.cupos_ocupados = 0
        self.cupos_por_grupo = {}

    def asignar_cupo(self):
        if self.cupos_ocupados < self.total_cupos:
            self.cupos_ocupados += 1
            return True
        else:
            print(f"[X] No hay cupos disponibles en {self.nombres}.")
            return False

    def cupos_disponibles(self):
        return self.total_cupos - self.cupos_ocupados

    def distribuir_cupos_por_grupo(self, grupos):
        for grupo in grupos:
            self.cupos_por_grupo[grupo.nombres_grupo] = grupo.calcular_cupos_reservados(self.total_cupos)
        return self.cupos_por_grupo

    def mostrar_info(self):
        return f"{self.nombres} ({self.facultad}) - Cupos totales: {self.total_cupos} | Disponibles: {self.cupos_disponibles()}"



#Clase Puntaje
class Puntaje:
    minimo_requerido = 800

    def __init__(self, aspirante, nota_examen, nota_bachillerato):
        if not (0 <= nota_examen <= 1000):
            raise ValueError("La nota de examen debe estar entre 0 y 1000.")
        if not (0 <= nota_bachillerato <= 10):
            raise ValueError("La nota de bachillerato debe estar entre 0 y 10.")
        self.aspirante = aspirante
        self.nota_examen = nota_examen
        self.nota_bachillerato = nota_bachillerato
        self.puntaje_final = 0

    def calcular_ponderado(self):
        self.puntaje_final = (self.nota_examen * 0.5) + ((self.nota_bachillerato * 100) * 0.5)
        return self.puntaje_final

    def cumple_requisito(self, minimo=None):
        umbral = minimo or Puntaje.minimo_requerido
        return self.puntaje_final >= umbral

    def resumen(self):
        return f"{self.aspirante.nombres} - Puntaje final: {self.puntaje_final} ({'Cumple' if self.cumple_requisito() else 'No cumple'})"



#Ejemplo de uso de las clases
if __name__ == "__main__": #Para pruebas dentro del mismo archivo en la terminal
    # Crear grupos prioritarios
    grupo1 = GrupoPrioritario(1, "Discapacitados", "Aspirantes con discapacidades", 5) #Numero final es el porcentaje de cupos a este grupo
    grupo2 = GrupoPrioritario(2, "Indígenas", "Aspirantes de comunidades indígenas", 3)

    # Crear carreras
    carrera1 = Carrera(1, "Ingeniería en Sistemas", "Facultad de Ciencias de la vida y tecnología", 50) #Total de cupos (50)
    carrera2 = Carrera(2, "Medicina", "Facultad de Ciencias de la Salud", 30)

# Crear los aspirantes
# Crear el primer aspirante
aspirante1 = Aspirante(
idAspirante=1,
tipo_documento="Cédula",
identificacion="1101234567",
nombres="Ana",
apellidos="Pérez",
sexo="F",
genero="Femenino",
nacionalidad="Ecuatoriana",
fecha_nacimiento="2005-03-10",
autoidentificacion="Mestiza/o",
correo="ana@email.com",
celular="0999999999",
titulo_homologado=True,
tipo_unidad_educativa="Fiscal",
calificacion=9.5,
cuadro_honor=True,
vulnerabilidad_socioeconomica=False,
merito_academico=True,
bachiller_pueblos_nacionalidad=False,
bachiller_periodo_academico=True,
poblacion_general=False
)

# Crear el segundo aspirante
aspirante2 = Aspirante(
idAspirante=2,
tipo_documento="Cédula",
identificacion="1109876543",
nombres="Luis",
apellidos="García",
sexo="M",
genero="Masculino",
nacionalidad="Ecuatoriana",
fecha_nacimiento="2005-07-22",
autoidentificacion="Afroecuatoriana/o",
correo="luis@email.com",
celular="0988888888",
titulo_homologado=True,
tipo_unidad_educativa="Particular",
calificacion=8.7,
cuadro_honor=False,
vulnerabilidad_socioeconomica=True,
merito_academico=False,
bachiller_pueblos_nacionalidad=False,
bachiller_periodo_academico=True,
poblacion_general=False
)

print("___________________________________________________________________________")
# Crear puntajes
puntaje1 = Puntaje(1, aspirante1, 850, 9.5)
puntaje2 = Puntaje(2, aspirante2, 780, 8.0)

print("___________________________________________________________________________")
# Calcular puntajes ponderados
puntaje1.calcular_ponderado()
puntaje2.calcular_ponderado()


print("___________________________________________________________________________")
# Mostrar información
aspirante1.informacion_Aspirante()
puntaje1.mostrar_puntaje()
carrera1.mostrar_info()

print("___________________________________________________________________________")
aspirante2.informacion_Aspirante()
puntaje2.mostrar_puntaje()
carrera2.mostrar_info()

print("___________________________________________________________________________")
# Asignar grupo prioritario según la normativa
aspirante1.asignar_grupo()
aspirante2.asignar_grupo()

print("___________________________________________________________________________")
# Verificar si los aspirantes cumplen el requisito mínimo actual
print("Mínimo requerido (Atributo de clase):", Puntaje.minimo_requerido)
print(f"{aspirante1.nombres} cumple requisito: {puntaje1.cumple_requisito()}")  # 800 por defecto
print(f"{aspirante2.nombres} cumple requisito: {puntaje2.cumple_requisito()}")

print("___________________________________________________________________________")
# Cambiar el puntaje mínimo global (afecta a todos los objetos de la clase)
Puntaje.minimo_requerido = 750
print("Nuevo mínimo requerido (Atributo de clase):", Puntaje.minimo_requerido)


print("___________________________________________________________________________")
# Re-evaluar SIN recrear los objetos: el método usa el nuevo valor de la clase.
print(f"{aspirante1.nombres} cumple con el nuevo mínimo: {puntaje1.cumple_requisito()}")
print(f"{aspirante2.nombres} cumple con el nuevo mínimo: {puntaje2.cumple_requisito()}")


print("___________________________________________________________________________")
# Crear cupos y asignar aspirantes
cupo1 = Cupo(1, carrera1)
cupo2 = Cupo(2, carrera2)

cupo1.asignar_aspirante(aspirante1)
cupo2.asignar_aspirante(aspirante2)

cupo1.mostrar_info()
cupo2.mostrar_info()