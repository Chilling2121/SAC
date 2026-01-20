// Proyecto: Sistema de Asignación de Cupos (SAC) en TypeScript


// 1) CLASE BASE: PERSONA
// Representa a una persona dentro del sistema.
// Se aplica encapsulamiento protegiendo la identificación (dato sensible).
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
    // Se guarda internamente para que no se manipule desde fuera.
    this.identificacionPrivada = identificacion;
  }

  // Getter: permite leer la identificación sin exponer el atributo privado.
  get identificacion(): string {
    return this.identificacionPrivada;
  }
}


// 2) CLASE DERIVADA: ASPIRANTE

// Aspirante hereda de Persona y añade datos necesarios para asignación de cupos.
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

    // Datos usados por la lógica de asignación
    public puntaje: number,
    public vulnerabilidad: boolean,
    public merito: boolean,
    public pueblosNacionalidades: boolean,
    public bachillerUltimoAnio: boolean
  ) {
    // Llama al constructor de Persona para inicializar los datos base.
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


// 3) CLASE: CARRERA
// Representa una carrera con un número limitado de cupos.
class Carrera {
  constructor(
    public nombre: string,
    public cuposTotales: number // Se reduce conforme se asignan cupos
  ) {}

  // Asigna un cupo si existe disponibilidad.
  asignarCupo(): boolean {
    if (this.cuposTotales > 0) {
      this.cuposTotales--;
      return true;
    }
    return false;
  }
}


// 4) INTERFAZ: REGLA DE GRUPO (CONTRATO)
// Define el contrato que deben cumplir todas las reglas de asignación.
// Permite polimorfismo y facilita extender el sistema (OCP).
interface ReglaGrupo {
  nombre: string;
  porcentaje: number;
  cuposDisponibles: number;
  pertenece(aspirante: Aspirante): boolean;
}


// Regla: Mérito Académico (30%)

class ReglaMerito implements ReglaGrupo {
  nombre = "MÉRITO ACADÉMICO";
  porcentaje = 0.30;
  cuposDisponibles = 0;

  pertenece(a: Aspirante): boolean {
    return a.merito;
  }
}


// Regla: Vulnerabilidad Socioeconómica (25%)

class ReglaVulnerabilidad implements ReglaGrupo {
  nombre = "VULNERABILIDAD SOCIOECONÓMICA";
  porcentaje = 0.25;
  cuposDisponibles = 0;

  pertenece(a: Aspirante): boolean {
    return a.vulnerabilidad;
  }
}


// Regla: Pueblos y Nacionalidades (15%)

class ReglaPueblos implements ReglaGrupo {
  nombre = "PUEBLOS Y NACIONALIDADES";
  porcentaje = 0.15;
  cuposDisponibles = 0;

  pertenece(a: Aspirante): boolean {
    return a.pueblosNacionalidades;
  }
}


// Regla: Bachiller Último Año (10%)

class ReglaBachiller implements ReglaGrupo {
  nombre = "BACHILLER ÚLTIMO AÑO";
  porcentaje = 0.10;
  cuposDisponibles = 0;

  pertenece(a: Aspirante): boolean {
    return a.bachillerUltimoAnio;
  }
}


// 5) CLASE CENTRAL: SISTEMAASIGNACION
// Coordina el proceso de asignación.
// Recibe reglas por constructor, evitando acoplamiento fuerte.
class SistemaAsignacion {
  constructor(private reglas: ReglaGrupo[]) {}

  // Calcula los cupos por grupo según el porcentaje definido.
  // Se usa Math.floor para evitar cupos decimales.
  calcularCupos(carrera: Carrera): void {
    for (const regla of this.reglas) {
      regla.cuposDisponibles = Math.floor(
        carrera.cuposTotales * regla.porcentaje
      );
    }
  }

  // Asigna cupos respetando prioridad de reglas y puntaje.
  asignar(carrera: Carrera, aspirantes: Aspirante[]) {
    this.calcularCupos(carrera);

    // Se prioriza a los aspirantes de mayor puntaje.
    aspirantes.sort((a, b) => b.puntaje - a.puntaje);

    const resultados: any[] = [];

    for (const aspirante of aspirantes) {
      let asignado = false;

      // Se evalúan las reglas en el orden definido (prioridad).
      for (const regla of this.reglas) {
        if (
          regla.pertenece(aspirante) &&
          regla.cuposDisponibles > 0 &&
          carrera.cuposTotales > 0
        ) {
          // Descuenta cupo del grupo y cupo total de la carrera.
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

      // Si no pertenece a grupos, entra a población general si hay cupos.
      if (!asignado && carrera.cuposTotales > 0) {
        carrera.asignarCupo();
        resultados.push({
          aspirante: aspirante.nombres,
          resultado: "ASIGNADO",
          grupo: "POBLACIÓN GENERAL"
        });
        asignado = true;
      }

      // Si ya no hay cupos, queda sin cupo.
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


// 6) EJECUCIÓN DE PRUEBA

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
  new Aspirante(3,"CÉDULA","3","Carlos","Paz","HOMBRE","MASCULINO","EC","2005","Mestizo","c@mail","097",780,false,true,false,false),
  new Aspirante(4,"CÉDULA","4","Ana2","Loor","MUJER","FEMENINO","EC","2005","Mestiza","a@mail","099",850,true,true,false,false),
  new Aspirante(5,"CÉDULA","5","Luis2","Vera","HOMBRE","MASCULINO","EC","2004","Montubio","b@mail","098",820,false,true,true,false),
  new Aspirante(6,"CÉDULA","6","Carlos2","Paz","HOMBRE","MASCULINO","EC","2005","Mestizo","c@mail","097",780,false,true,false,false),
  new Aspirante(7,"CÉDULA","7","Ana3","Loor","MUJER","FEMENINO","EC","2005","Mestiza","a@mail","099",850,true,true,false,false),
  new ReglaBachiller()
];

console.log(sistema.asignar(carrera, aspirantes));
console.log("Cupos restantes:", carrera.cuposTotales);
