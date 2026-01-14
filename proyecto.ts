// Proyecto: Sistema de Asignación de Cupos (SAC) en TypeScript

class Persona {
  private identificacionPrivada: string;

  constructor(
    public tipo_documento: string,
    identificacion: string,
    public nombres: string,
    public apellidos: string,
    public sexo: string,
    public genero: string,
    public nacionalidad: string,
    public fecha_nacimiento: string,
    public autoidentificacion: string,
    public correo: string,
    public celular: string
  ) {
    this.identificacionPrivada = identificacion;
  }

  get identificacion(): string {
    return this.identificacionPrivada;
  }

  informacion_basica(): string {
    return `${this.nombres} ${this.apellidos} (${this.identificacion})`;
  }
}

class Aspirante extends Persona {
  constructor(
    public idAspirante: number,
    tipo_documento: string,
    identificacion: string,
    nombres: string,
    apellidos: string,
    sexo: string,
    genero: string,
    nacionalidad: string,
    fecha_nacimiento: string,
    autoidentificacion: string,
    correo: string,
    celular: string,
    public calificacion: number,
    public vulnerabilidad_socioeconomica: boolean,
    public merito_academico: boolean,
    public bachiller_pueblos_nacionalidad: boolean,
    public bachiller_periodo_academico: boolean
  ) {
    super(
      tipo_documento,
      identificacion,
      nombres,
      apellidos,
      sexo,
      genero,
      nacionalidad,
      fecha_nacimiento,
      autoidentificacion,
      correo,
      celular
    );
  }
}

class Carrera {
  constructor(
    public nombre: string,
    public modalidad: string,
    public jornada: string,
    public cupos: number
  ) {}

  tiene_cupos(): boolean {
    return this.cupos > 0;
  }

  asignar_cupo(): boolean {
    if (this.tiene_cupos()) {
      this.cupos -= 1;
      return true;
    }
    return false;
  }
}

// Interfaz equivalente a la clase abstracta de Python
interface ReglaGrupo {
  pertenece(aspirante: Aspirante): boolean;
  readonly nombre: string;
}

class ReglaMerito implements ReglaGrupo {
  pertenece(aspirante: Aspirante): boolean {
    return aspirante.merito_academico;
  }
  get nombre(): string {
    return "MÉRITO ACADÉMICO";
  }
}

class ReglaVulnerabilidad implements ReglaGrupo {
  pertenece(aspirante: Aspirante): boolean {
    return aspirante.vulnerabilidad_socioeconomica;
  }
  get nombre(): string {
    return "VULNERABILIDAD SOCIOECONÓMICA";
  }
}

class ReglaPueblos implements ReglaGrupo {
  pertenece(aspirante: Aspirante): boolean {
    return aspirante.bachiller_pueblos_nacionalidad;
  }
  get nombre(): string {
    return "BACHILLER PUEBLOS Y NACIONALIDADES";
  }
}

class ReglaBachillerUltimo implements ReglaGrupo {
  pertenece(aspirante: Aspirante): boolean {
    return aspirante.bachiller_periodo_academico;
  }
  get nombre(): string {
    return "BACHILLER ÚLTIMO AÑO";
  }
}

type ResultadoAsignacion = {
  resultado: "ASIGNADO" | "SIN CUPO";
  grupo: string | null;
  carrera: string;
};

class SistemaAsignacion {
  constructor(private reglas: ReglaGrupo[]) {}

  asignar(carrera: Carrera, aspirante: Aspirante): ResultadoAsignacion {
    if (!carrera.tiene_cupos()) {
      return { resultado: "SIN CUPO", grupo: null, carrera: carrera.nombre };
    }

    for (const regla of this.reglas) {
      if (regla.pertenece(aspirante)) {
        carrera.asignar_cupo();
        return { resultado: "ASIGNADO", grupo: regla.nombre, carrera: carrera.nombre };
      }
    }

    carrera.asignar_cupo();
    return { resultado: "ASIGNADO", grupo: "POBLACIÓN GENERAL", carrera: carrera.nombre };
  }
}

// Ejemplo de uso

const sistema = new SistemaAsignacion([
  new ReglaMerito(),
  new ReglaVulnerabilidad(),
  new ReglaPueblos(),
  new ReglaBachillerUltimo(),
]);

const carrera_admin = new Carrera("Administración de Empresas", "Presencial", "Nocturna", 35);

const aspirante1 = new Aspirante(
  1,
  "CÉDULA",
  "1350432058",
  "Jhon",
  "Zambrano",
  "HOMBRE",
  "MASCULINO",
  "ECUATORIANA",
  "2005-03-12",
  "Montubio",
  "jhon@example.com",
  "0999999999",
  795,
  false,
  true,
  false,
  false
);

const aspirante2 = new Aspirante(
  2,
  "CÉDULA",
  "1351658859",
  "Liliana",
  "Loor",
  "MUJER",
  "FEMENINO",
  "ECUATORIANA",
  "2006-07-18",
  "Mestiza",
  "liliana@example.com",
  "0988888888",
  749,
  true,
  false,
  false,
  false
);

const aspirante3 = new Aspirante(
  3,
  "CÉDULA",
  "1315374700",
  "Luis",
  "Vera",
  "HOMBRE",
  "MASCULINO",
  "ECUATORIANA",
  "2005-11-09",
  "Montubio",
  "luis@example.com",
  "0977777777",
  742,
  false,
  false,
  false,
  false
);

console.log("Aspirante 1");
console.log(sistema.asignar(carrera_admin, aspirante1));

console.log("Aspirante 2");
console.log(sistema.asignar(carrera_admin, aspirante2));

console.log("Aspirante 3");
console.log(sistema.asignar(carrera_admin, aspirante3));

console.log("Cupos restantes:", carrera_admin.cupos);
