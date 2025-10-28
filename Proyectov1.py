#Estrucutra del Proyecto de Sistema de Asignacion de Cupos
#SAC
#HOLA
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



#Clase Aspirante
class Aspirante:
    # El metodo __init__ es llamdo a crear un objeto (Constructor)
    def __init__(self, id_aspirante,nombres,apellidos,cedula,grupo_prioritario=None):
        #Atributos de instancia 
        self.id_aspirante=id_aspirante 
        self.nombres= nombres #self se refiere asi misma con su variable
        self.apellidos= apellidos
        self.cedula= cedula
        # Asigna el grupo prioritario recibido; si no se proporciona, crea uno por defecto "Población General"
        self.grupo_prioritario = grupo_prioritario or GrupoPrioritario(
            0, "Población General", "Aspirantes sin prioridad específica", 90
        )
        #Estado inicial del aspirante 
        self.estado = "Registrado"
#Metodos de la clase Aspirante
    def asignar_grupoo(self,grupo=None):
        if grupo:
            self.grupo_prioritario = grupo
        else:
            self.grupo_prioritario = GrupoPrioritario(
                0, "Población General", "Aspirantes sin prioridad específica", 90
            )
    def cambiar_estado(self, nuevo_estado):
        #Cambia el estado del aspirante (Registrado, Asignado, Admitido)
        self.estado = nuevo_estado
    def mostrar_informacion(self):
            grupo = self.grupo_prioritario.nombres_grupo if self.grupo_prioritario else "Ninguno"
            print(f"Aspirante: {self.nombres} {self.apellidos}")
            print(f"Grupo Prioritario: {grupo}")
            print(f"Estado: {self.estado}")


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

    # Crear aspirantes
    aspirante1 = Aspirante(1, "Carlos Enrique", "Espinoza Ponce", "1234567890", grupo1)
    aspirante2 = Aspirante(2, "Jonathan Estifen", "Delgado Santana", "0987654321", grupo2)

    # Crear puntajes
    puntaje1 = Puntaje(1, aspirante1, 850, 9.5)
    puntaje2 = Puntaje(2, aspirante2, 780, 8.0)

    # Calcular puntajes ponderados
    puntaje1.calcular_ponderado()
    puntaje2.calcular_ponderado()


    # Mostrar información
    aspirante1.mostrar_informacion()
    puntaje1.mostrar_puntaje()
    carrera1.mostrar_info()

    aspirante2.mostrar_informacion()
    puntaje2.mostrar_puntaje()
    carrera2.mostrar_info()

    # Verificar si los aspirantes cumplen el requisito mínimo actual
    print("Mínimo requerido (Atributo de clase):", Puntaje.minimo_requerido)
    print(f"{aspirante1.nombres} cumple requisito: {puntaje1.cumple_requisito()}")  # 800 por defecto
    print(f"{aspirante2.nombres} cumple requisito: {puntaje2.cumple_requisito()}")

    # Cambiar el puntaje mínimo global (afecta a todos los objetos de la clase)
    Puntaje.minimo_requerido = 750
    print("Nuevo mínimo requerido (Atributo de clase):", Puntaje.minimo_requerido)

    # Re-evaluar SIN recrear los objetos: el método usa el nuevo valor de la clase.
    print(f"{aspirante1.nombres} cumple con el nuevo mínimo: {puntaje1.cumple_requisito()}")
    print(f"{aspirante2.nombres} cumple con el nuevo mínimo: {puntaje2.cumple_requisito()}")


    # Crear cupos y asignar aspirantes
    cupo1 = Cupo(1, carrera1)
    cupo2 = Cupo(2, carrera2)

    cupo1.asignar_aspirante(aspirante1)
    cupo2.asignar_aspirante(aspirante2)

    cupo1.mostrar_info()
    cupo2.mostrar_info()