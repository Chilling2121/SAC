// Proyecto: Sistema de Asignación de Cupos (SAC) en TypeScript

// Clase base que representa a una persona dentro del sistema
// Aplica encapsulamiento usando un atributo privado
class Persona {
  private identificacionPrivada: string;

  constructor(
    public tipoDocumento: string,
    identificacion: string,
    public nombres: string,
    public apellidos: string,
    public sexo: string,
    public genero: string,
    public nacionalidad: string,
    public fechaNacimiento: string,
    public autoidentificacion: string,
    public correo: string,
    public celular: string
  ) {
    this.identificacionPrivada = identificacion;
  }

  // Getter para acceder a la identificación sin exponer el atributo privado
  get identificacion(): string {
    return this.identificacionPrivada;
  }
}

// Aspirante hereda de Persona y añade atributos necesarios para la asignación de cupos
class Aspirante extends Persona {
  constructor(
    public idAspirante: number,
    tipoDocumento: string,
    identificacion: string,
    nombres: string,
    apellidos: string,
    sexo: string,
    genero: string,
    nacionalidad: string,
    fechaNacimiento: string,
    autoidentificacion: string,
    correo: string,
    celular: string,

    // Datos utilizados para la lógica de asignación
    public puntaje: number,
    public vulnerabilidad: boolean,
    public merito: boolean,
    public pueblosNacionalidades: boolean,
    public bachillerUltimoAnio: boolean
  ) {
    super(
      tipoDocumento,
      identificacion,
      nombres,
      apellidos,
      sexo,
      genero,
      nacionalidad,
      fechaNacimiento,
      autoidentificacion,
      correo,
      celular
    );
  }
}

// Representa una carrera con un número limitado de cupos
class Carrera {
  constructor(
    public nombre: string,
    public cuposTotales: number
  ) {}

  // Reduce un cupo disponible si existen cupos
  asignarCupo(): boolean {
    if (this.cuposTotales > 0) {
      this.cuposTotales--;
      return true;
    }
    return false;
  }
}

// Interfaz que define el contrato que deben cumplir todas las reglas de asignación
// Permite aplicar polimorfismo y el principio abierto/cerrado
interface ReglaGrupo {
  nombre: string;
  porcentaje: number;
  cuposDisponibles: number;
  pertenece(aspirante: Aspirante): boolean;
}

// Regla para aspirantes con mérito académico
class ReglaMerito implements ReglaGrupo {
  nombre = "MÉRITO ACADÉMICO";
  porcentaje = 0.30;
  cuposDisponibles = 0;

  pertenece(a: Aspirante): boolean {
    return a.merito;
  }
}

// Regla para aspirantes con vulnerabilidad socioeconómica
class ReglaVulnerabilidad implements ReglaGrupo {
  nombre = "VULNERABILIDAD SOCIOECONÓMICA";
  porcentaje = 0.25;
  cuposDisponibles = 0;

  pertenece(a: Aspirante): boolean {
    return a.vulnerabilidad;
  }
}

// Regla para pueblos y nacionalidades
class ReglaPueblos implements ReglaGrupo {
  nombre = "PUEBLOS Y NACIONALIDADES";
  porcentaje = 0.15;
  cuposDisponibles = 0;

  pertenece(a: Aspirante): boolean {
    return a.pueblosNacionalidades;
  }
}

// Regla para bachilleres del último año
class ReglaBachiller implements ReglaGrupo {
  nombre = "BACHILLER ÚLTIMO AÑO";
  porcentaje = 0.10;
  cuposDisponibles = 0;

  pertenece(a: Aspirante): boolean {
    return a.bachillerUltimoAnio;
  }
}

// Clase central que coordina todo el proceso de asignación
class SistemaAsignacion {
  constructor(private reglas: ReglaGrupo[]) {}

  // Calcula cuántos cupos corresponden a cada grupo según porcentajes
  calcularCupos(carrera: Carrera): void {
    for (const regla of this.reglas) {
      regla.cuposDisponibles = Math.floor(
        carrera.cuposTotales * regla.porcentaje
      );
    }
  }

  // Asigna cupos respetando prioridad de grupos y puntaje
  asignar(carrera: Carrera, aspirantes: Aspirante[]) {
    this.calcularCupos(carrera);

    // Se ordenan los aspirantes por puntaje (mayor a menor)
    aspirantes.sort((a, b) => b.puntaje - a.puntaje);

    const resultados: any[] = [];

    for (const aspirante of aspirantes) {
      let asignado = false;

      // Se evalúan las reglas en el orden definido (prioridad normativa)
      for (const regla of this.reglas) {
        if (
          regla.pertenece(aspirante) &&
          regla.cuposDisponibles > 0 &&
          carrera.cuposTotales > 0
        ) {
          regla.cuposDisponibles--;
          carrera.asignarCupo();
          resultados.push({
            aspirante: aspirante.nombres,
            resultado: "ASIGNADO",
            grupo: regla.nombre
          });
          asignado = true;
          break;
        }
      }

      // Si no pertenece a ningún grupo prioritario, se asigna como población general
      if (!asignado && carrera.cuposTotales > 0) {
        carrera.asignarCupo();
        resultados.push({
          aspirante: aspirante.nombres,
          resultado: "ASIGNADO",
          grupo: "POBLACIÓN GENERAL"
        });
      }

      // Si ya no hay cupos disponibles
      if (!asignado && carrera.cuposTotales === 0) {
        resultados.push({
          aspirante: aspirante.nombres,
          resultado: "SIN CUPO",
          grupo: null
        });
      }
    }

    return resultados;
  }
}

// Ejecución de ejemplo del sistema
const sistema = new SistemaAsignacion([
  new ReglaMerito(),
  new ReglaVulnerabilidad(),
  new ReglaPueblos(),
  new ReglaBachiller()
]);

const carrera = new Carrera("Administración de Empresas", 10);

const aspirantes: Aspirante[] = [
  new Aspirante(1,"CÉDULA","1","Ana","Loor","MUJER","FEMENINO","EC","2005","Mestiza","a@mail","099",850,true,true,false,false),
  new Aspirante(2,"CÉDULA","2","Luis","Vera","HOMBRE","MASCULINO","EC","2004","Montubio","b@mail","098",820,false,false,true,false),
  new Aspirante(3,"CÉDULA","3","Carlos","Paz","HOMBRE","MASCULINO","EC","2005","Mestizo","c@mail","097",780,false,false,false,false)
];

console.log(sistema.asignar(carrera, aspirantes));
console.log("Cupos restantes:", carrera.cuposTotales);
