from abc import ABC, abstractmethod

# Esta clase representa a una persona y cumple el principio de responsabilidad única.
class Persona:
    def __init__(self, tipo_documento, identificacion, nombres, apellidos, sexo, genero,
                 nacionalidad, fecha_nacimiento, autoidentificacion, correo, celular):
        self.tipo_documento = tipo_documento
        self.__identificacion = identificacion
        self.nombres = nombres
        self.apellidos = apellidos
        self.sexo = sexo
        self.genero = genero
        self.nacionalidad = nacionalidad
        self.fecha_nacimiento = fecha_nacimiento
        self.autoidentificacion = autoidentificacion
        self.correo = correo
        self.celular = celular

    # Se aplica encapsulamiento para proteger el atributo identificación.
    @property
    def identificacion(self):
        return self.__identificacion

    # Este método devuelve información básica sin modificar el estado del objeto.
    def informacion_basica(self):
        return f"{self.nombres} {self.apellidos} ({self.identificacion})"


# Esta clase hereda a Persona sin cambiar su comportamiento, cumpliendo el principio de Liskov.
class Aspirante(Persona):
    def __init__(self, idAspirante, tipo_documento, identificacion, nombres, apellidos, sexo, genero,
                 nacionalidad, fecha_nacimiento, autoidentificacion, correo, celular, calificacion,
                 vulnerabilidad_socioeconomica,
                 merito_academico,
                 bachiller_pueblos_nacionalidad,
                 bachiller_periodo_academico,
                 discapacidad):

        super().__init__(
            tipo_documento, identificacion, nombres, apellidos, sexo, genero,
            nacionalidad, fecha_nacimiento, autoidentificacion, correo, celular
        )

        self.idAspirante = idAspirante
        self.calificacion = calificacion
        self.vulnerabilidad_socioeconomica = vulnerabilidad_socioeconomica
        self.merito_academico = merito_academico
        self.bachiller_pueblos_nacionalidad = bachiller_pueblos_nacionalidad
        self.bachiller_periodo_academico = bachiller_periodo_academico
        self.discapacidad = discapacidad


# Esta clase gestiona los cupos de una carrera respetando el principio SRP.
class Carrera:
    def __init__(self, nombre, modalidad, jornada, cupos):
        self.nombre = nombre
        self.modalidad = modalidad
        self.jornada = jornada
        self.cupos = cupos

    # Este método verifica disponibilidad 
    def tiene_cupos(self):
        return self.cupos > 0

    # Este método modifica los cupos de forma controlada.
    def asignar_cupo(self):
        if self.tiene_cupos():
            self.cupos -= 1
            return True
        return False


# Esta interfaz define el comportamiento común de las reglas aplicando ISP.
class ReglaGrupo(ABC):
    @abstractmethod
    def pertenece(self, aspirante):
        pass

    @property
    @abstractmethod
    def nombre(self):
        pass


class ReglaDiscapacidad(ReglaGrupo):
    def pertenece(self, aspirante):
        return aspirante.discapacidad

    @property
    def nombre(self):
        return "DISCAPACIDAD"


# Esta clase implementa una estrategia concreta usando el patrón Strategy.
class ReglaMerito(ReglaGrupo):
    def pertenece(self, aspirante):
        return aspirante.merito_academico

    @property
    def nombre(self):
        return "MÉRITO ACADÉMICO"



class ReglaVulnerabilidad(ReglaGrupo):
    def pertenece(self, aspirante):
        return aspirante.vulnerabilidad_socioeconomica

    @property
    def nombre(self):
        return "VULNERABILIDAD SOCIOECONÓMICA"


class ReglaPueblos(ReglaGrupo):
    def pertenece(self, aspirante):
        return aspirante.bachiller_pueblos_nacionalidad

    @property
    def nombre(self):
        return "BACHILLER PUEBLOS Y NACIONALIDADES"


class ReglaBachillerUltimo(ReglaGrupo):
    def pertenece(self, aspirante):
        return aspirante.bachiller_periodo_academico

    @property
    def nombre(self):
        return "BACHILLER ÚLTIMO AÑO"

# Esta clase gestiona la asignación de cupos aplicando DIP.
class SistemaAsignacion:

    def __init__(self, reglas):
        self.reglas = reglas

    def asignar(self, aspirante, carrera):
        for regla in self.reglas:
            if regla.pertenece(aspirante) and carrera.tiene_cupos():
                carrera.asignar_cupo()
                return regla.nombre
        return "SIN CUPO"



# Ejemplo de uso

carrera_admin = Carrera(
    nombre="Administración de Empresas",
    modalidad="Presencial",
    jornada="Nocturna",
    cupos=35
)

# Se instancia el sistema con las reglas en el orden de prioridad definido
sistema = SistemaAsignacion([
    ReglaDiscapacidad(),
    ReglaMerito(),
    ReglaVulnerabilidad(),
    ReglaPueblos(),
    ReglaBachillerUltimo()
])


aspirante1 = Aspirante(
    idAspirante=1,
    tipo_documento="CÉDULA",
    identificacion="1350432058",
    nombres="Jhon",
    apellidos="Zambrano",
    sexo="HOMBRE",
    genero="MASCULINO",
    nacionalidad="ECUATORIANA",
    fecha_nacimiento="2005-03-12",
    autoidentificacion="Montubio",
    correo="jhon@example.com",
    celular="0999999999",
    calificacion=795,
    vulnerabilidad_socioeconomica=False,
    merito_academico=True,
    bachiller_pueblos_nacionalidad=False,
    bachiller_periodo_academico=False,
    discapacidad=False
)

aspirante2 = Aspirante(
    idAspirante=2,
    tipo_documento="CÉDULA",
    identificacion="1351658859",
    nombres="Liliana",
    apellidos="Loor",
    sexo="MUJER",
    genero="FEMENINO",
    nacionalidad="ECUATORIANA",
    fecha_nacimiento="2006-07-18",
    autoidentificacion="Mestiza",
    correo="liliana@example.com",
    celular="0988888888",
    calificacion=749,
    vulnerabilidad_socioeconomica=True,
    merito_academico=False,
    bachiller_pueblos_nacionalidad=False,
    bachiller_periodo_academico=False,
    discapacidad=True
)

aspirante3 = Aspirante(
    idAspirante=3,
    tipo_documento="CÉDULA",
    identificacion="1315374700",
    nombres="Luis",
    apellidos="Vera",
    sexo="HOMBRE",
    genero="MASCULINO",
    nacionalidad="ECUATORIANA",
    fecha_nacimiento="2005-11-09",
    autoidentificacion="Montubio",
    correo="luis@example.com",
    celular="0977777777",
    calificacion=742,
    vulnerabilidad_socioeconomica=False,
    merito_academico=False,
    bachiller_pueblos_nacionalidad=False,
    bachiller_periodo_academico=False,
    discapacidad=False
)

# Se ejecuta el proceso de asignación usando el sistema
print("Aspirante 1:", sistema.asignar(aspirante1, carrera_admin))
print("Aspirante 2:", sistema.asignar(aspirante2, carrera_admin))
print("Aspirante 3:", sistema.asignar(aspirante3, carrera_admin))

# Se muestra el estado final de los cupos
print("Cupos restantes:", carrera_admin.cupos)

