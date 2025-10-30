#Proyecto de Sistema de Asignacion de Cupos
#SAC

# Clase Base - Persona
class Persona:
    #Recibe los datos basicos de una persona
    def __init__(self, tipo_documento, identificacion, nombres, apellidos, sexo, genero,
                nacionalidad, fecha_nacimiento, autoidentificacion, correo, celular):
        # Datos de identidad y contacto
        self.tipo_documento = tipo_documento
        self.__identificacion = identificacion # Atributo privado o encapsulado
        self.nombres = nombres
        self.apellidos = apellidos
        self.sexo = sexo
        self.genero = genero
        self.nacionalidad = nacionalidad
        self.fecha_nacimiento = fecha_nacimiento
        self.autoidentificacion = autoidentificacion
        self.correo = correo
        self.celular = celular

    @property #propiedad de solo lectura
    def identificacion(self): #no recibe parametros
        return self.__identificacion #retorna el valor del atributo privado

    def informacion_basica(self): #no recibe parametros
        #retorna una cadena con el nombre completo y la identificacion
        return f"{self.nombres} {self.apellidos} ({self.identificacion})"


# Clase Aspirante que hereda de la clase  Persona
class Aspirante(Persona):
    #Recibe los datos especificos de un aspirante
    def __init__(self, idAspirante, tipo_documento, identificacion, nombres, apellidos, sexo, genero,
                nacionalidad, fecha_nacimiento, autoidentificacion, correo, celular,
                calificacion, merito_academico=False, vulnerabilidad=False):
        # Llama al constructor de la clase base Persona
        super().__init__(tipo_documento, identificacion, nombres, apellidos, sexo, genero,
                        nacionalidad, fecha_nacimiento, autoidentificacion, correo, celular)
        # Datos especificos del aspirante
        self.idAspirante = idAspirante
        self.calificacion = calificacion # nota de bachillerato
        self.merito_academico = merito_academico
        self.vulnerabilidad = vulnerabilidad
        self.grupo_prioritario = None # Inicialmente sin grupo asignado
        self.estado = "Registrado" # Estado inicial del aspirante

    def asignar_grupo(self): #no recibe parametros
        # Asigna el grupo prioritario basado en las condiciones
        if self.merito_academico:
            self.grupo_prioritario = "Mérito Académico"
        elif self.vulnerabilidad:
            self.grupo_prioritario = "Vulnerabilidad Socioeconómica"
        else:
            self.grupo_prioritario = "Población General"
        return self.grupo_prioritario
    # Retorna la informacion completa del aspirante
    def informacion(self):
        return f"{self.informacion_basica()} - Grupo: {self.grupo_prioritario or 'Sin asignar'}"


# Clase GrupoPrioritario
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

# Clase Carrera
class Carrera:
    #Recibe los datos de una carrera
    def __init__(self, id_carrera, nombres, facultad, total_cupos):
        # Datos de la carrera
        self.id_carrera = id_carrera
        self.nombres = nombres
        self.facultad = facultad
        self.total_cupos = total_cupos
        self.cupos_ocupados = 0
        self.cupos_por_grupo = {}
    # Asigna un cupo si hay disponibilidad
    def asignar_cupo(self):
        # Verifica si hay cupos disponibles
        if self.cupos_ocupados < self.total_cupos:
            # si hay cupos disponibles, asigna uno incrementando el contador
            self.cupos_ocupados += 1
            # Retorna True indicando que se asigno un cupo
            return True
        # Si no hay cupos disponibles, retorna False e imprime un mensaje
        print(f"[X] No hay cupos disponibles en {self.nombres}.")
        return False
    # Retorna la cantidad de cupos disponibles
    def cupos_disponibles(self):
        # Calcula y retorna los cupos disponibles de la carrera
        return self.total_cupos - self.cupos_ocupados
    # Distribuye los cupos por grupo prioritario
    def distribuir_cupos_por_grupo(self, grupos):
        # Calcula y almacena los cupos reservados por cada grupo prioritario
        self.cupos_por_grupo = {g.nombres_grupo: g.calcular_cupos_reservados(self.total_cupos) for g in grupos}
        # Retorna el diccionario con los cupos por grupo
        return self.cupos_por_grupo
    # Muestra la informacion de la carrera
    def mostrar_info(self):
        return f"{self.nombres} ({self.facultad}) - Cupos totales: {self.total_cupos} | Disponibles: {self.cupos_disponibles()}"

# Clase Cupo
class Cupo:
    #Recibe los datos de un cupo
    def __init__(self, id_cupo, carrera):
        self.id_cupo = id_cupo
        self.carrera = carrera
        self.aspirante = None # Inicialmente sin aspirante asignado
        self.estado = "Disponible" # Estado inicial del cupo

    def asignar(self, aspirante):
        # Asigna un aspirante al cupo si está disponible
        if self.estado != "Disponible": # Si el cupo no está disponible
            return False # Retorna False indicando que no se pudo asignar
        if self.carrera.asignar_cupo(): # Si se pudo asignar un cupo en la carrera
            self.aspirante = aspirante # Asigna el aspirante al cupo
            self.estado = "Asignado" # Cambia el estado del cupo a "Asignado"
            return True # Retorna True indicando que se asignó correctamente
        return False

    def info(self): #no recibe parametros
        asignado = self.aspirante.nombres if self.aspirante else "Nadie" #si no hay aspirante asignado
        return f"Cupo {self.id_cupo} - {self.carrera.nombres}: {asignado}" #retorna la informacion del cupo

# Clase Puntaje
class Puntaje:
    minimo_requerido = 800 # Atributo de clase para el puntaje minimo requerido
    #Recibe los datos para calcular el puntaje final
    def __init__(self, aspirante, nota_examen, nota_bachillerato):
        if not (0 <= nota_examen <= 1000): # calida la nota de examen
            raise ValueError("La nota de examen debe estar entre 0 y 1000.") #lanza un error si no es valida
        if not (0 <= nota_bachillerato <= 10): #valida la nota de bachillerato
            raise ValueError("La nota de bachillerato debe estar entre 0 y 10.") #lanza un error si no es valida
        # Datos del aspirante y sus notas
        self.aspirante = aspirante 
        self.nota_examen = nota_examen
        self.nota_bachillerato = nota_bachillerato
        self.puntaje_final = 0

    # Calcula el puntaje ponderado
    def calcular_ponderado(self):
        self.puntaje_final = (self.nota_examen * 0.5) + ((self.nota_bachillerato * 100) * 0.5)
        self.puntaje_final = round(self.puntaje_final, 2)
        return self.puntaje_final

    # Verifica si cumple el requisito minimo
    def cumple_requisito(self, minimo=None):
        umbral = minimo or Puntaje.minimo_requerido
        return self.puntaje_final >= umbral
    # Retorna un resumen del puntaje
    def resumen(self):
        return f"{self.aspirante.nombres} - Puntaje final: {self.puntaje_final} ({'Cumple' if self.cumple_requisito() else 'No cumple'})"


# Ejemplo de uso
if __name__ == "__main__": #sirve para ejecutar el codigo solo si se ejecuta este archivo directamente
    # Creacion de grupos prioritarios
    grupo1 = GrupoPrioritario(1, "Discapacitados", "Aspirantes con discapacidades", 5)
    grupo2 = GrupoPrioritario(2, "Indígenas", "Aspirantes de comunidades indígenas", 3)
    # Creacion de carreras
    carrera1 = Carrera(1, "Ingeniería en Sistemas", "Facultad de Ciencias de la Vida y Tecnología", 50)
    carrera2 = Carrera(2, "Medicina", "Facultad de Ciencias de la Salud", 30)
    # Creacion de aspirantes
    aspirante1 = Aspirante(1, "Cédula", "1101234567", "Ana", "Pérez", "F", "Femenino", "Ecuatoriana",
                        "2005-03-10", "Mestiza/o", "ana@email.com", "0999999999",
                        9.5, merito_academico=True)
    
    aspirante2 = Aspirante(2, "Cédula", "1109876543", "Luis", "García", "M", "Masculino", "Ecuatoriana",
                        "2005-07-22", "Afroecuatoriana/o", "luis@email.com", "0988888888",
                        8.7, vulnerabilidad=True)
    # Creacion de puntajes
    puntaje1 = Puntaje(aspirante1, 850, 9.5)
    puntaje2 = Puntaje(aspirante2, 780, 8.0)
    puntaje1.calcular_ponderado()
    puntaje2.calcular_ponderado()
    # Asignacion de grupos prioritarios
    aspirante1.asignar_grupo()
    aspirante2.asignar_grupo()
    # Mostrar informacion
    print("\n--- ASPIRANTES ---")
    print(aspirante1.informacion())
    print(aspirante2.informacion())
    # Mostrar puntajes
    print("\n--- PUNTAJES ---")
    print(puntaje1.resumen())
    print(puntaje2.resumen())
    # Mostrar informacion de carreras
    print("\n--- CUPOS POR CARRERA ---")
    print(carrera1.distribuir_cupos_por_grupo([grupo1, grupo2]))
    print(carrera2.distribuir_cupos_por_grupo([grupo1, grupo2]))
    # Asignacion de cupos
    cupo1 = Cupo(1, carrera1)
    cupo2 = Cupo(2, carrera2)
    cupo1.asignar(aspirante1)
    cupo2.asignar(aspirante2)
    # Mostrar informacion de cupos asignados
    print("\n--- CUPOS ASIGNADOS ---")
    print(cupo1.info())
    print(cupo2.info())
