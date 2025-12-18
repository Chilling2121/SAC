#Integrantes del proyecto: JOSSELYN VANESSA DELGADO SALTOS, JONATHAN ESTIFEN DELGADO SANTANA,CARLOS ENRIQUE ESPINOZA PONCE, COLON DAVID MOREIRA ORDOÑEZ
#Proyecto de Sistema de Asignacion de Cupos
#SAC

# SOLID (SRP): 
# Clase que representa a una persona con sus datos básicos de identificación y contacto.
# Su única función es almacenar y proporcionar información personal.

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

    @property
    def identificacion(self):
        return self.__identificacion

    def informacion_basica(self):
        return f"{self.nombres} {self.apellidos} ({self.identificacion})"


class Aspirante(Persona):
    def __init__(self, idAspirante, tipo_documento, identificacion, nombres, apellidos, sexo, genero,
                 nacionalidad, fecha_nacimiento, autoidentificacion, correo, celular, calificacion,
                vulnerabilidad_socioeconomica, merito_academico, bachiller_pueblos_nacionalidad, bachiller_periodo_academico):
        
        #NUEVOS ATRIBUTOS PARA LA CLASE PERSONA
        super().__init__(tipo_documento, identificacion, nombres,apellidos, sexo,genero, nacionalidad, 
                         fecha_nacimiento, autoidentificacion, correo,celular)
        
        self.idAspirante = idAspirante
        self.calificacion = calificacion
        self.vulnerabilidad_socioeconomica = vulnerabilidad_socioeconomica
        self.merito_academico = merito_academico
        self.bachiller_pueblos_nacionalidad = bachiller_pueblos_nacionalidad
        self.bachiller_periodo_academico = bachiller_periodo_academico
        self.grupo_prioritario = None
        self.estado = "Registrado"


    # SOLID (SRP)
    # Asigna al aspirante un grupo prioritario según sus condiciones.
    # El aspirante no decide las reglas, solo recibe el grupo que le corresponde.

    def asignar_grupo(self, selector_grupo):
        self.grupo_prioritario = selector_grupo.seleccionar(self)
        return self.grupo_prioritario


# SOLID (SRP)
# Representa un grupo prioritario del sistema.
# Define el porcentaje de cupos que le corresponde dentro de una carrera.

class GrupoPrioritario:
    def __init__(self, id_grupo, nombre, descripcion, porcentaje_cupos):
        self.id_grupo = id_grupo
        self.nombre = nombre
        self.descripcion = descripcion
        self.porcentaje_cupos = porcentaje_cupos

    # Calcula los cupos reservados del grupo en base al total de cupos de la carrera.

    def calcular_cupos_reservados(self, total_cupos):
        return int((self.porcentaje_cupos / 100) * total_cupos)


# SOLID (SRP)
# Clase encargada de decidir a qué grupo prioritario pertenece un aspirante.
# Centraliza las reglas de clasificación para no mezclarlas con otras clases.

class SelectorGrupo:
    def __init__(self, grupo_merito, grupo_vulnerabilidad, grupo_general):
        self.grupo_merito = grupo_merito
        self.grupo_vulnerabilidad = grupo_vulnerabilidad
        self.grupo_general = grupo_general

    # Aplica las reglas y retorna el grupo prioritario correspondiente al aspirante.

    def seleccionar(self, aspirante):
        if aspirante.merito_academico:
            return self.grupo_merito
        if aspirante.vulnerabilidad:
            return self.grupo_vulnerabilidad
        return self.grupo_general


# SOLID (SRP): Puntaje solo calcula y valida puntaje, no asigna cupos.
class Puntaje:
    def __init__(self, aspirante, nota_examen, nota_bachillerato, regla_puntaje, minimo_requerido):
        self.aspirante = aspirante
        self.nota_examen = nota_examen
        self.nota_bachillerato = nota_bachillerato
        self.regla_puntaje = regla_puntaje
        self.minimo_requerido = minimo_requerido
        self.puntaje_final = 0

    def calcular(self):
        self.puntaje_final = self.regla_puntaje.calcular(self.nota_examen, self.nota_bachillerato)
        self.puntaje_final = round(self.puntaje_final, 2)
        return self.puntaje_final

    def cumple_minimo(self):
        return self.puntaje_final >= self.minimo_requerido


# SOLID (OCP): ReglaPuntaje permite cambiar la fórmula sin modificar Puntaje.
# Concepto: Open/Closed = abierto a extensión (nuevas reglas), cerrado a modificación (no tocar Puntaje).
class ReglaPuntaje:
    def __init__(self, peso_examen, peso_bachillerato, factor_bachillerato=100):
        self.peso_examen = peso_examen
        self.peso_bachillerato = peso_bachillerato
        self.factor_bachillerato = factor_bachillerato

    def calcular(self, nota_examen, nota_bachillerato):
        return (nota_examen * self.peso_examen) + ((nota_bachillerato * self.factor_bachillerato) * self.peso_bachillerato)


# SOLID (SRP): Carrera solo administra cupos, reservas y ocupación.
class Carrera:
    def __init__(self, id_carrera, nombre, facultad, total_cupos):
        self.id_carrera = id_carrera
        self.nombre = nombre
        self.facultad = facultad
        self.total_cupos = total_cupos
        self.cupos_ocupados = 0
        self.cupos_reservados = {}
        self.cupos_ocupados_grupo = {}

    def configurar_reservas(self, grupos):
        for g in grupos:
            self.cupos_reservados[g.id_grupo] = g.calcular_cupos_reservados(self.total_cupos)
            self.cupos_ocupados_grupo[g.id_grupo] = 0

    def cupos_disponibles_totales(self):
        return self.total_cupos - self.cupos_ocupados

    def cupos_disponibles_grupo(self, grupo):
        return self.cupos_reservados.get(grupo.id_grupo, 0) - self.cupos_ocupados_grupo.get(grupo.id_grupo, 0)

    def asignar_por_grupo(self, grupo):
        if self.cupos_disponibles_totales() > 0 and self.cupos_disponibles_grupo(grupo) > 0:
            self.cupos_ocupados += 1
            self.cupos_ocupados_grupo[grupo.id_grupo] += 1
            return True
        return False

    def asignar_general(self):
        if self.cupos_disponibles_totales() > 0:
            self.cupos_ocupados += 1
            return True
        return False


# SOLID (ISP): Política de asignación con método simple (contrato pequeño).
# Concepto: Interface Segregation = “interfaces” pequeñas; aquí solo pedimos decidir asignación.
class PoliticaAsignacion:
    def __init__(self, permitir_general=True):
        self.permitir_general = permitir_general

    def intentar_asignar(self, carrera, aspirante):
        grupo = aspirante.grupo_prioritario

        if grupo and carrera.asignar_por_grupo(grupo):
            return True, "Cupo por grupo prioritario"

        if self.permitir_general and carrera.asignar_general():
            return True, "Cupo general"

        return False, "Sin cupo aplicable"


# SOLID (DIP): SAC depende de abstracciones/objetos inyectados (politica), no de detalles.
# Concepto: Dependency Inversion = el módulo alto nivel (SAC) NO crea la política; se la pasan (inyección).
class SAC:
    def __init__(self, politica_asignacion):
        self.politica_asignacion = politica_asignacion

    def asignar_cupo(self, carrera, puntaje):
        aspirante = puntaje.aspirante

        if not puntaje.cumple_minimo():
            return aspirante.idAspirante, carrera.nombre, "NO ASIGNADO", "No cumple puntaje mínimo"

        if carrera.cupos_disponibles_totales() <= 0:
            return aspirante.idAspirante, carrera.nombre, "NO ASIGNADO", "No hay cupos disponibles"

        ok, motivo = self.politica_asignacion.intentar_asignar(carrera, aspirante)
        if ok:
            aspirante.estado = "Asignado"
            return aspirante.idAspirante, carrera.nombre, "ASIGNADO", motivo

        return aspirante.idAspirante, carrera.nombre, "NO ASIGNADO", motivo


# SOLID (SRP): “Vista”/salida separada del SAC y de las entidades.
# Concepto: separar lógica de negocio de presentación.
class SalidaSAC:
    def mostrar(self, resultado):
        print(resultado)


if __name__ == "__main__":
    grupo_general = GrupoPrioritario(0, "General", "Población general", 0)
    grupo_merito = GrupoPrioritario(1, "Mérito", "Mérito académico", 5)
    grupo_vulnerabilidad = GrupoPrioritario(2, "Vulnerabilidad", "Vulnerabilidad socioeconómica", 3)

    selector = SelectorGrupo(grupo_merito, grupo_vulnerabilidad, grupo_general)

    carrera = Carrera(1, "Ingeniería en Sistemas", "Tecnología", 50)
    carrera.configurar_reservas([grupo_merito, grupo_vulnerabilidad])

    aspirante = Aspirante(
        1, "Cédula", "1101234567", "Ana", "Pérez", "F", "Femenino",
        "Ecuatoriana", "2005-03-10", "Mestiza/o", "ana@email.com", "0999999999",
        9.5, merito_academico=True
    )
    aspirante.asignar_grupo(selector)

    regla_puntaje = ReglaPuntaje(peso_examen=0.5, peso_bachillerato=0.5, factor_bachillerato=100)
    puntaje = Puntaje(
        aspirante,
        nota_examen=850,
        nota_bachillerato=9.5,
        regla_puntaje=regla_puntaje,
        minimo_requerido=800
    )
    puntaje.calcular()

    politica = PoliticaAsignacion(permitir_general=True)
    sac = SAC(politica_asignacion=politica)

    resultado = sac.asignar_cupo(carrera, puntaje)

    salida = SalidaSAC()
    salida.mostrar(resultado)



# ESTO ES LO NUEVO -------------------------------------------------------------------------

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

    @property
    def identificacion(self):
        return self.__identificacion

    def informacion_basica(self):
        return f"{self.nombres} {self.apellidos} ({self.identificacion})"
    

class Aspirante(Persona):
    def __init__(self, idAspirante, tipo_documento, identificacion, nombres, apellidos, sexo, genero,
                 nacionalidad, fecha_nacimiento, autoidentificacion, correo, celular, calificacion,
                vulnerabilidad_socioeconomica, merito_academico, bachiller_pueblos_nacionalidad, bachiller_periodo_academico):
        
        #NUEVOS ATRIBUTOS PARA LA CLASE PERSONA
        super().__init__(tipo_documento, identificacion, nombres,apellidos, sexo,genero, nacionalidad, 
                         fecha_nacimiento, autoidentificacion, correo,celular)
        
        self.idAspirante = idAspirante
        self.calificacion = calificacion
        self.vulnerabilidad_socioeconomica = vulnerabilidad_socioeconomica
        self.merito_academico = merito_academico
        self.bachiller_pueblos_nacionalidad = bachiller_pueblos_nacionalidad
        self.bachiller_periodo_academico = bachiller_periodo_academico
        self.grupo_prioritario = None
        self.estado = "Registrado"


#---------------------------------------------------------------------------------------

class Carrera:
    def __init__(self, nombre, modalidad, jornada, cupos):
        self.nombre = nombre
        self.modalidad = modalidad
        self.jornada = jornada
        self.cupos = cupos

    def tiene_cupos(self):
        return self.cupos > 0

    def asignar_cupo(self):
        if self.tiene_cupos():
            self.cupos -= 1
            return True
        return False

#--------------------------------------------------------------------------------

# Clase ReglaGrupo, toma una decisión
#Esta clase responde UNA pregunta: ¿Este aspirante pertenece a este grupo?


from abc import ABC, abstractmethod

class ReglaGrupo(ABC):
    @abstractmethod
    def pertenece(self, aspirante):
        pass

    @abstractmethod
    def nombre(self):
        pass



#Se refiere al grupo prioritario de Mérito Académico

class ReglaMerito(ReglaGrupo):
    def pertenece(self, aspirante):
        return aspirante.merito_academico == "SI"

    def nombre(self):
        return "MÉRITO ACADÉMICO"

# Grupo prioritario - Vulnerabilidad Socioeconómica

class ReglaVulnerabilidad(ReglaGrupo):
    def pertenece(self, aspirante):
        return aspirante.vulnerabilidad_socioeconomica == "SI"

    def nombre(self):
        return "VULNERABILIDAD SOCIOECONÓMICA"



#Grupo prioritario - Bachiller pueblos y nacionalidades

class ReglaPueblos(ReglaGrupo):
    def pertenece(self, aspirante):
        return aspirante.bachiller_pueblos_nacionalidad == "SI"

    def nombre(self):
        return "BACHILLER PUEBLOS Y NACIONALIDADES"
    

#Se refiere al grupo prioritario de Mérito Académico

class ReglaMerito(ReglaGrupo):
    def pertenece(self, aspirante):
        return aspirante.merito_academico == "SI"

    def nombre(self):
        return "MÉRITO ACADÉMICO"

# Grupo prioritario - Vulnerabilidad Socioeconómica

class ReglaVulnerabilidad(ReglaGrupo):
    def pertenece(self, aspirante):
        return aspirante.vulnerabilidad_socioeconomica == "SI"

    def nombre(self):
        return "VULNERABILIDAD SOCIOECONÓMICA"
    


#Grupo prioritario - Bachiller pueblos y nacionalidades

class ReglaPueblos(ReglaGrupo):
    def pertenece(self, aspirante):
        return aspirante.bachiller_pueblos_nacionalidad == "SI"

    def nombre(self):
        return "BACHILLER PUEBLOS Y NACIONALIDADES"
    

# Grupo prioritario Bachiller último año

class ReglaBachillerUltimo(ReglaGrupo):
    def pertenece(self, aspirante):
        return aspirante.bachiller_periodo_academico == "SI"

    def nombre(self):
        return "BACHILLER ÚLTIMO AÑO"
    


# Sistema de Asignación

class SistemaAsignacion:
    def __init__(self, reglas_en_orden):
        self.reglas = reglas_en_orden

    def asignar(self, carrera, aspirante):
        # 1. Validar cupos
        if not carrera.tiene_cupos():
            return "SIN CUPO"

        # 2. Determinar grupo según orden
        for regla in self.reglas:
            if regla.pertenece(aspirante):
                carrera.asignar_cupo()
                return f"ASIGNADO EN {regla.nombre()}"

        # 3. Población general
        carrera.asignar_cupo()
        return "ASIGNADO EN POBLACIÓN GENERAL"


#Sirve para definir el ORDEN y las REGLAS con las que se asignan los cupos.


sistema = SistemaAsignacion([
    ReglaMerito(),
    ReglaVulnerabilidad(),
    ReglaPueblos(),
    ReglaBachillerUltimo()
])
















