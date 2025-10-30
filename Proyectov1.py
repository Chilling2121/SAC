#Estrucutra del Proyecto de Sistema de Asignacion de Cupos
#SAC

#Clase Grupo-Prioritario   
class GrupoPrioritario:
    def __init__(self, id_grupo, nombres_grupo, descripcion, porcentaje_cupos):
        self.id_grupo = id_grupo
        self.nombres_grupo = nombres_grupo
        self.descripcion = descripcion
        self.porcentaje_cupos = porcentaje_cupos
#Metodos de la clase GrupoPrioritario
    def calcular_cupos_reservados(self, total_cupos):
        #Calcula los cupos aginados al grupo
        return int((self.porcentaje_cupos / 100) * total_cupos)
    def calcular_cupos_restantes(self, total_cupos, usados):
    #Devuelve los cupos que aún quedan disponibles dentro del porcentaje.
        cupos_reservados = int((self.porcentaje_cupos / 100) * total_cupos)
        return max(0, cupos_reservados - usados)
    def mostrar_info(self):
        print(f"Grupo: {self.nombres_grupo}")
        print(f"Porcentaje reservado: {self.porcentaje_cupos}%")



#Clase Cupo
class Cupo:
    def __init__(self, id_cupo, carrera, aspirante=None):
        self.id_cupo = id_cupo
        self.carrera = carrera
        self.aspirante = aspirante
        self.estado = "Disponible"
#Metodos de la clase Cupo
    def asignar_aspirante(self, aspirante):
        # Verifica que el cupo esté libre
        if self.estado != "Disponible":
            print("Este cupo ya está asignado a otro aspirante.")
            return False

        # Pide a la carrera ocupar un cupo (usa el método de la clase Carrera)
        if self.carrera.asignar_cupo():
            self.aspirante = aspirante
            self.estado = "Asignado"
            return True
        else:
            # La carrera no tenía disponibilidad
            return False
            #Verifica si la carrera aún tiene cupos disponibles.
            disponibles = self.carrera.cupos_disponibles()
            if disponibles > 0:
                print(f"Hay {disponibles} cupos disponibles en {self.carrera.nombres}.")
            else:
                print(f"Límite de cupos alcanzado en {self.carrera.nombres}.")
    def mostrar_info(self):
            if self.aspirante:
                print(f"Cupo {self.id_cupo} - {self.carrera.nombres}: Asignado a {self.aspirante.nombres}")
            else:
                print(f"Cupo {self.id_cupo} - {self.carrera.nombres}: Disponible")


#Clase Aspirante - Representa a la persona que solicita un cupo

class Aspirante:
    # El metodo __init__ es llamdo a crear un objeto (Constructor)
    #Atributos de la instancia
    def __init__(
        self,
        idAspirante: int,
        tipo_documento: str,            #cédula, pasaporte
        identificacion: str,            #Número de cédula o pasaporte del aspirante 
        nombres: str,                   #Los nombres del Aspirante
        apellidos: str,                 #Apellidos del Aspirante
        sexo: str,                      #Registra el sexo del usuario - MUJER, HOMBRE
        genero: str,                    #Tipo de identidad de género autodefinida - Prefiero no contestar, Masculino, Femenino, otro.
        nacionalidad: str,              #Nacionalidad del ciudadano
        fecha_nacimiento: str,          #Fecha de nacimiento del usuario 
        autoidentificacion: str,        #Afroecuatoriana/o Afrodescendiente; Blanca/o; Indígena; Mestiza/o; Montubia/o; Mulata/o; Negra/o; Otro/a
        correo: str,                    #Correo electrónico del ciudadano
        celular: str,                   #Número de celular del ciudadano
        titulo_homologado: bool,        #Identifica si el ciudadano cuenta con título de bachiller homologado - SI, NO (True - False)
        tipo_unidad_educativa: str,     #Particular, Fiscal, Fiscomisional, Municipal
        calificacion: float,            #Nota de grado del ciudadano
        cuadro_honor: bool,             #Ciudadanos de tercer año de bachillerato que pertenecen al cuadro de honor - SI, NO (True - False)
        vulnerabilidad_socioeconomica: bool,    #Identifica se el ciudadano pasa por una vulnerabilidad socioeconómica - SI, NO (True - False)
        merito_academico: bool,                 #Identifica a los ciudadanos abanderados y escoltas de las instituciones educativas del último periodo académico en curso. - SI, NO (True - False)
        bachiller_pueblos_nacionalidad: bool,   #Identifica a los ciudadanos que estén cursando el último período del tercer año de bachillerato y que pertenecen a pueblos y nacionalidades. - SI, NO (True - False)
        bachiller_periodo_academico: bool,      #Identifica a los ciudadanos que estén cursando el último período del tercer año de bachillerato. - SI, NO (True - False)
        poblacion_general: bool                 #Identifica a los ciudadanos que no constan en los campos VULNERABILIDAD_SOCIOECONOMICA, MERITO_ACADEMICO, BACHILLER_PUEBLOS_NACIONALIDAD, BACHILLER_PER_ACADEMICO - SI, NO (True - False)
        ):  
        
        #Atributos o Datos personales
        self.idAspirante= idAspirante
        self.tipo_documento = tipo_documento
        self.identificacion = identificacion
        self.nombres = nombres
        self.apellidos = apellidos
        self.sexo = sexo
        self.genero = genero
        self.nacionalidad = nacionalidad
        self.fecha_nacimiento = fecha_nacimiento
        self.autoidentificacion = autoidentificacion
        
        #Atributos o Datos de Contacto
        self.correo = correo
        self.celular = celular
        
        #Atributos o datos académicos
        self.titulo_homologado = titulo_homologado
        self.tipo_unidad_educativa = tipo_unidad_educativa
        self.calificacion = calificacion
        self.cuadro_honor = cuadro_honor
        
        #Atributos de Condiciones especiales
        self.vulnerabilidad_socioeconomica = vulnerabilidad_socioeconomica
        self.merito_academico = merito_academico
        self.bachiller_pueblos_nacionalidad = bachiller_pueblos_nacionalidad
        self.bachiller_periodo_academico = bachiller_periodo_academico
        self.poblacion_general = poblacion_general
        
        #Estado inicial del aspirante 
        self.estado = "Registrado"
        
        
    #Métodos de la clase Aspirante
    
    #Metodo que muestra la información del estudiante    
    def informacion_Aspirante(self):    
        print(f"Nombre: {self.nombres} {self.apellidos}")
        print(f"ID: {self.identificacion}")
        print(f"Sexo: {self.sexo}")
        print(f"Nacionalidad: {self.nacionalidad}")
    
    
    #Método que decide a qué grupo prioritario pertenece el aspirante   
    def asignar_grupo(self):
        if self.merito_academico:
            self.grupo_prioritario = "Grupo de Mérito Académico"
        elif self.vulnerabilidad_socioeconomica:
            self.grupo_prioritario = "Grupo de Mayor Vulnerabilidad Socioeconómica"
        elif self.bachiller_pueblos_nacionalidad or self.bachiller_periodo_academico:
            self.grupo_prioritario = "Bachilleres del Último Periodo Académico"
        else:
            self.grupo_prioritario = "Población General"

        print(f"El aspirante {self.nombres} {self.apellidos} pertenece al grupo:{self.grupo_prioritario}")
        
     
    #Método para Postular a una carrera
    def Postular(self):
        print("El aspirante se postula a una carrera")
        
    def aceptar_cupo(self):
        pass
    
    def rechazar_cupo(self):
        pass


#Clase Carrera
class Carrera:
    def __init__(self, id_carrera, nombres, facultad, total_cupos):
        self.id_carrera = id_carrera
        self.nombres = nombres
        self.facultad = facultad
        self.total_cupos = total_cupos
        self.cupos_ocupados = 0

    def asignar_cupo(self):
        # Registra un cupo como ocupado si aún hay disponibilidad
        if self.cupos_ocupados < self.total_cupos:
            self.cupos_ocupados += 1
            return True
        else:
            print(f"Límite de cupos alcanzado en {self.nombres}.")
            return False

    def cupos_disponibles(self):
        return self.total_cupos - self.cupos_ocupados

    def mostrar_info(self):
        print(f"Carrera: {self.nombres} - Facultad: {self.facultad}")
        print(f"Cupos totales: {self.total_cupos} | Disponibles: {self.cupos_disponibles()}")


#Clase Puntaje
class Puntaje:
    #Atributo de clase
    minimo_requerido = 800  # Puntaje mínimo para acceder a cupo

    def __init__(self, id_puntaje, aspirante, nota_examen, nota_bachillerato):
        self.id_puntaje = id_puntaje
        self.aspirante = aspirante
        self.nota_examen = nota_examen          # sobre 1000
        self.nota_bachillerato = nota_bachillerato  # sobre 10
        self.puntaje_final = 0                  # ponderado total
#Metodos de la clase Puntaje
    def calcular_ponderado(self):
        examen_ponderado = (self.nota_examen * 0.5)
        bachillerato_ponderado = ((self.nota_bachillerato * 100) * 0.5)
        # nota_bachillerato * 100 convierte de escala 10 → 1000
        self.puntaje_final = examen_ponderado + bachillerato_ponderado
        return self.puntaje_final
    def cumple_requisito(self, minimo=None):
        #Verifica si el aspirante alcanza el puntaje mínimo para acceder a cupo.
        #Por ejemplo: mínimo 800/1000.
        objetivo = minimo if minimo is not None else Puntaje.minimo_requerido
        return self.puntaje_final >= objetivo
    def mostrar_puntaje(self):
        #Muestra los valores detallados del puntaje del aspirante.
        print(f"Aspirante: {self.aspirante.nombres} {self.aspirante.apellidos}")
        print(f"Examen de admisión: {self.nota_examen}/1000")
        print(f"Bachillerato: {self.nota_bachillerato}/10")
        print(f"Puntaje final ponderado: {self.puntaje_final}")

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