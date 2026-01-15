"use strict";
// Proyecto: Sistema de Asignación de Cupos (SAC) en TypeScript
Object.defineProperty(exports, "__esModule", { value: true });
class Persona {
    tipo_documento;
    nombres;
    apellidos;
    sexo;
    genero;
    nacionalidad;
    fecha_nacimiento;
    autoidentificacion;
    correo;
    celular;
    identificacionPrivada;
    constructor(tipo_documento, identificacion, nombres, apellidos, sexo, genero, nacionalidad, fecha_nacimiento, autoidentificacion, correo, celular) {
        this.tipo_documento = tipo_documento;
        this.nombres = nombres;
        this.apellidos = apellidos;
        this.sexo = sexo;
        this.genero = genero;
        this.nacionalidad = nacionalidad;
        this.fecha_nacimiento = fecha_nacimiento;
        this.autoidentificacion = autoidentificacion;
        this.correo = correo;
        this.celular = celular;
        this.identificacionPrivada = identificacion;
    }
    get identificacion() {
        return this.identificacionPrivada;
    }
    informacion_basica() {
        return `${this.nombres} ${this.apellidos} (${this.identificacion})`;
    }
}
class Aspirante extends Persona {
    idAspirante;
    calificacion;
    vulnerabilidad_socioeconomica;
    merito_academico;
    bachiller_pueblos_nacionalidad;
    bachiller_periodo_academico;
    constructor(idAspirante, tipo_documento, identificacion, nombres, apellidos, sexo, genero, nacionalidad, fecha_nacimiento, autoidentificacion, correo, celular, calificacion, vulnerabilidad_socioeconomica, merito_academico, bachiller_pueblos_nacionalidad, bachiller_periodo_academico) {
        super(tipo_documento, identificacion, nombres, apellidos, sexo, genero, nacionalidad, fecha_nacimiento, autoidentificacion, correo, celular);
        this.idAspirante = idAspirante;
        this.calificacion = calificacion;
        this.vulnerabilidad_socioeconomica = vulnerabilidad_socioeconomica;
        this.merito_academico = merito_academico;
        this.bachiller_pueblos_nacionalidad = bachiller_pueblos_nacionalidad;
        this.bachiller_periodo_academico = bachiller_periodo_academico;
    }
}
class Carrera {
    nombre;
    modalidad;
    jornada;
    cupos;
    constructor(nombre, modalidad, jornada, cupos) {
        this.nombre = nombre;
        this.modalidad = modalidad;
        this.jornada = jornada;
        this.cupos = cupos;
    }
    tiene_cupos() {
        return this.cupos > 0;
    }
    asignar_cupo() {
        if (this.tiene_cupos()) {
            this.cupos -= 1;
            return true;
        }
        return false;
    }
}
class ReglaMerito {
    pertenece(aspirante) {
        return aspirante.merito_academico;
    }
    get nombre() {
        return "MÉRITO ACADÉMICO";
    }
}
class ReglaVulnerabilidad {
    pertenece(aspirante) {
        return aspirante.vulnerabilidad_socioeconomica;
    }
    get nombre() {
        return "VULNERABILIDAD SOCIOECONÓMICA";
    }
}
class ReglaPueblos {
    pertenece(aspirante) {
        return aspirante.bachiller_pueblos_nacionalidad;
    }
    get nombre() {
        return "BACHILLER PUEBLOS Y NACIONALIDADES";
    }
}
class ReglaBachillerUltimo {
    pertenece(aspirante) {
        return aspirante.bachiller_periodo_academico;
    }
    get nombre() {
        return "BACHILLER ÚLTIMO AÑO";
    }
}
class SistemaAsignacion {
    reglas;
    constructor(reglas) {
        this.reglas = reglas;
    }
    asignar(carrera, aspirante) {
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
const aspirante1 = new Aspirante(1, "CÉDULA", "1350432058", "Jhon", "Zambrano", "HOMBRE", "MASCULINO", "ECUATORIANA", "2005-03-12", "Montubio", "jhon@example.com", "0999999999", 795, false, true, false, false);
const aspirante2 = new Aspirante(2, "CÉDULA", "1351658859", "Liliana", "Loor", "MUJER", "FEMENINO", "ECUATORIANA", "2006-07-18", "Mestiza", "liliana@example.com", "0988888888", 749, true, false, false, false);
const aspirante3 = new Aspirante(3, "CÉDULA", "1315374700", "Luis", "Vera", "HOMBRE", "MASCULINO", "ECUATORIANA", "2005-11-09", "Montubio", "luis@example.com", "0977777777", 742, false, false, false, false);
console.log("Aspirante 1");
console.log(sistema.asignar(carrera_admin, aspirante1));
console.log("Aspirante 2");
console.log(sistema.asignar(carrera_admin, aspirante2));
console.log("Aspirante 3");
console.log(sistema.asignar(carrera_admin, aspirante3));
console.log("Cupos restantes:", carrera_admin.cupos);
//# sourceMappingURL=proyecto.js.map