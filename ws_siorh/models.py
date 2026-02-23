from django.db import models

class PlantillaFin(models.Model):
    # --- Llave Primaria ---
    posicion = models.CharField(
        db_column='Posición', 
        max_length=255, 
        primary_key=True,
        verbose_name='Posición'
    )
    
    # --- Campos de la Tabla ---
    estado_nomina = models.CharField(db_column='Estado Nómina', max_length=255, blank=True, null=True, verbose_name='Estado de Nómina')
    num_empleado = models.CharField(db_column='Num Empleado', max_length=255, blank=True, null=True, verbose_name='Número de Empleado')
    rfc = models.CharField(db_column='RFC', max_length=255, blank=True, null=True, verbose_name='RFC')
    curp = models.CharField(db_column='CURP', max_length=255, blank=True, null=True, verbose_name='CURP')
    nombres = models.CharField(db_column='Nombres', max_length=255, blank=True, null=True)
    motivo = models.CharField(db_column='Motivo', max_length=255, blank=True, null=True)
    fecha_efectiva_personal = models.CharField(db_column='Fecha efectiva (Personal)', max_length=255, blank=True, null=True, verbose_name='Fecha Efectiva (Personal)')
    fecha_de_captura = models.CharField(db_column='Fecha de captura', max_length=255, blank=True, null=True, verbose_name='Fecha de Captura')
    qna = models.CharField(db_column='Qna#', max_length=255, blank=True, null=True, verbose_name='Quincena (Qna)')
    fecha_prevista_de_salida = models.CharField(db_column='Fecha prevista de salida', max_length=255, blank=True, null=True, verbose_name='Fecha Prevista de Salida')
    nj = models.CharField(db_column='NJ', max_length=255, blank=True, null=True, verbose_name='NJ')
    codigo_presupuestal = models.CharField(db_column='Código Presupuestal', max_length=255, blank=True, null=True, verbose_name='Código Presupuestal')
    nivel = models.CharField(db_column='Nivel', max_length=255, blank=True, null=True)
    escala = models.CharField(db_column='Escala', max_length=255, blank=True, null=True)
    smb = models.DecimalField(db_column='SMB', max_digits=12, decimal_places=2, blank=True, null=True, verbose_name='SMB')
    smn = models.DecimalField(db_column='SMN', max_digits=12, decimal_places=2, blank=True, null=True, verbose_name='SMN')
    partida = models.CharField(db_column='Partida', max_length=255, blank=True, null=True)
    tipo_de_contratacion = models.CharField(db_column='TIPO DE CONTRATACIÓN', max_length=255, blank=True, null=True, verbose_name='Tipo de Contratación')
    cd_un = models.CharField(db_column='Cd UN', max_length=255, blank=True, null=True, verbose_name='Código Unidad de Negocio')
    unidad_de_negocio = models.CharField(db_column='Unidad de Negocio', max_length=255, blank=True, null=True, verbose_name='Unidad de Negocio')
    cd_ua = models.CharField(db_column='Cd UA', max_length=255, blank=True, null=True, verbose_name='Código Unidad Administrativa')
    unidad_administrativa = models.CharField(db_column='Unidad Administrativa', max_length=255, blank=True, null=True, verbose_name='Unidad Administrativa')
    cd_pto_funcional = models.CharField(db_column='Cd Pto Funcional', max_length=255, blank=True, null=True, verbose_name='Código Puesto Funcional')
    nombre_puesto_funcional = models.CharField(db_column='Nombre Puesto Funcional', max_length=255, blank=True, null=True, verbose_name='Nombre Puesto Funcional')
    id_departamento = models.CharField(db_column='Id Departamento', max_length=255, blank=True, null=True, verbose_name='ID Departamento')
    departamento = models.CharField(db_column='Departamento', max_length=255, blank=True, null=True)
    dependencia_directa = models.CharField(db_column='Dependencia Directa', max_length=255, blank=True, null=True, verbose_name='Dependencia Directa')
    observaciones = models.CharField(db_column='OBSERVACIONES', max_length=255, blank=True, null=True)
    programa = models.CharField(db_column='Programa', max_length=255, blank=True, null=True)
    num_empleado1 = models.CharField(db_column='Num empleado1', max_length=255, blank=True, null=True, verbose_name='Num Empleado 1')
    posicion1 = models.CharField(db_column='Posición1', max_length=255, blank=True, null=True, verbose_name='Posición 1')
    especialidad = models.CharField(db_column='Especialidad', max_length=255, blank=True, null=True)
    entidad_federativa = models.CharField(db_column='Entidad Federativa', max_length=255, blank=True, null=True, verbose_name='Entidad Federativa')
    tipo_de_aduana = models.CharField(db_column='Tipo de Aduana', max_length=255, blank=True, null=True, verbose_name='Tipo de Aduana')
    ubicacion = models.CharField(db_column='Ubicación', max_length=255, blank=True, null=True)
    descripcion_ubicacion = models.CharField(db_column='Descripción ubicación', max_length=255, blank=True, null=True, verbose_name='Descripción de Ubicación')
    posicion_civil_sedena_semar = models.CharField(db_column='Posición _Civil / SEDENA / SEMAR', max_length=255, blank=True, null=True, verbose_name='Posición Civil/SEDENA/SEMAR')
    personal_militar_o_civil = models.CharField(db_column='Personal Militar o Civil', max_length=255, blank=True, null=True, verbose_name='Personal Militar o Civil')
    tipo_de_personal_sedena_semar = models.CharField(db_column='Tipo de personal SEDENA / SEMAR', max_length=255, blank=True, null=True, verbose_name='Tipo de Personal SEDENA/SEMAR')
    rango = models.CharField(db_column='Rango', max_length=255, blank=True, null=True)
    fecha_de_ingreso = models.CharField(db_column='Fecha de ingreso', max_length=255, blank=True, null=True, verbose_name='Fecha de Ingreso')
    dg_o_aduana_compactada = models.CharField(db_column='DG o Aduana compactada', max_length=255, blank=True, null=True, verbose_name='DG o Aduana Compactada')
    depuracion_vacancia = models.CharField(db_column='Depuración Vacancia', max_length=255, blank=True, null=True, verbose_name='Depuración Vacancia')
    proyecto_2025_shcp = models.CharField(db_column='Proyecto 2025 337 plazas para autorización SHCP', max_length=255, blank=True, null=True, verbose_name='Proyecto 2025 337 Plazas SHCP')
    plazas_propuestas_conversion = models.CharField(db_column='Plazas propuestas para conversión_ Eventuales y Permanenes P33 A', max_length=255, blank=True, null=True, verbose_name='Plazas Propuestas para Conversión')
    primer_escalon_reingresos_sedena = models.CharField(db_column='1er Escalón y 46 reingresos Sgtos SEDENA', max_length=255, blank=True, null=True, verbose_name='1er Escalón y 46 Reingresos SEDENA')
    validando_de_posicion_por_documento = models.CharField(db_column='Validando de posición por documento', max_length=255, blank=True, null=True, verbose_name='Validando Posición por Documento')
    reportada = models.CharField(db_column='Reportada', max_length=255, blank=True, null=True)
    foto = models.BinaryField(blank=True, null=True, verbose_name='Foto (BLOB)')
 

    class Meta:
        managed = False
        db_table = 'plantilla_fin'
        ordering = ['-smn']  # Ordena de mayor a menor por el campo 'smn'
        verbose_name = 'Plantilla de Personal'
        verbose_name_plural = 'Plantillas de Personal'

    def __str__(self):
        return f"{self.nombres} ({self.posicion})"


# En core/models.py, debajo de la clase PlantillaFin

class BajasFin(models.Model):
    # Django añadirá un campo 'id' como llave primaria automáticamente
    posicion = models.CharField(db_column='Posición', max_length=255, blank=True, null=True, verbose_name='Posición')
    estado_nomina = models.CharField(db_column='Estado Nómina', max_length=255, blank=True, null=True, verbose_name='Estado Nómina')
    id_empleado = models.CharField(db_column='Id Empleado', max_length=255, primary_key=True, verbose_name='ID Empleado')
    rfc = models.CharField(db_column='RFC', max_length=255, blank=True, null=True, verbose_name='RFC')
    curp = models.CharField(db_column='CURP', max_length=255, blank=True, null=True, verbose_name='CURP')
    nombre = models.CharField(db_column='Nombre', max_length=255, blank=True, null=True, verbose_name='Nombre')
    motivo = models.CharField(db_column='Motivo', max_length=255, blank=True, null=True, verbose_name='Motivo')
    fecha_efectiva_personal = models.CharField(db_column='Fecha efectiva (Personal)', max_length=255, blank=True, null=True, verbose_name='Fecha Efectiva (Personal)')
    fecha_de_captura = models.CharField(db_column='Fecha de captura', max_length=255, blank=True, null=True, verbose_name='Fecha de Captura')
    qna = models.CharField(db_column='Qna#', max_length=255, blank=True, null=True, verbose_name='Quincena (Qna)')
    codigo_presupuestal = models.CharField(db_column='Código Presupuestal', max_length=255, blank=True, null=True, verbose_name='Código Presupuestal')
    nivel = models.CharField(db_column='Nivel', max_length=255, blank=True, null=True, verbose_name='Nivel')
    partida = models.CharField(db_column='Partida', max_length=255, blank=True, null=True, verbose_name='Partida')
    tipo_de_contratacion = models.CharField(db_column='TIPO DE Contratación', max_length=255, blank=True, null=True, verbose_name='Tipo de Contratación')
    cd_un = models.CharField(db_column='Cd UN', max_length=255, blank=True, null=True, verbose_name='Cd UN')
    cd_ua = models.CharField(db_column='Cd UA', max_length=255, blank=True, null=True, verbose_name='Cd UA')
    unidad_administrativa = models.CharField(db_column='Unidad Administrativa', max_length=255, blank=True, null=True, verbose_name='Unidad Administrativa')
    cd_pto_funcional = models.CharField(db_column='Cd Pto Funcional', max_length=255, blank=True, null=True, verbose_name='Cd Pto Funcional')
    puesto_funcional = models.CharField(db_column='Puesto Funcional', max_length=255, blank=True, null=True, verbose_name='Puesto Funcional')
    foto = models.BinaryField(blank=True, null=True, verbose_name='Foto (BLOB)') # Cambiado a BinaryField para BLOB

    class Meta:
        managed = False
        db_table = 'bajas_fin'
        verbose_name = 'Baja de Personal'
        verbose_name_plural = 'Bajas de Personal'
        ordering = ['-fecha_de_captura'] # Ordena por fecha de captura descendente


class MovPos(models.Model):

    n_pos_actual = models.CharField(
        db_column='Nº Pos Actual',
        max_length=255,
        primary_key=True,
        verbose_name='Número de Posición Actual'
    )
    f_efva = models.CharField(db_column='F Efva', max_length=255, blank=True, null=True, verbose_name='Fecha Efectiva')
    fecha_captura = models.CharField(db_column='Fecha Captura', max_length=255, blank=True, null=True)

    estado_psn = models.CharField(db_column='Estado Psn', max_length=255, blank=True, null=True, verbose_name='Estado de Posición')
    cd_motivo = models.CharField(db_column='Cd Motivo', max_length=255, blank=True, null=True, verbose_name='Código de Motivo')
    motivo = models.CharField(db_column='Motivo', max_length=255, blank=True, null=True)

    descr = models.CharField(db_column='Descr', max_length=255, blank=True, null=True, verbose_name='Descripción')
    unidad_de_negocio = models.CharField(db_column='Unidad de Negocio', max_length=255, blank=True, null=True)
    departamento = models.CharField(db_column='Cd Departamento', max_length=255, blank=True, null=True)
    ubicacion = models.CharField(db_column='Ubicación', max_length=255, blank=True, null=True)

    nivel_direc = models.CharField(db_column='Nvl Direc', max_length=255, blank=True, null=True, verbose_name='Nivel Dirección')
    nivel_ptal = models.CharField(db_column='Puesto Ptal', max_length=255, blank=True, null=True, verbose_name='Nivel Ptal')
    puesto = models.CharField(db_column='Nombre Puesto', max_length=255, blank=True, null=True, verbose_name='Puesto')

    class Meta:
        db_table = 'MOV_POS'
        managed = False
        verbose_name = 'Movimiento de Posición'
        verbose_name_plural = 'Historial de Posiciones (MOV_POS)'

    def __str__(self):
        return f"{self.n_pos_actual} - {self.estado_psn} ({self.fecha_captura})"


class Familiar(models.Model):
    id = models.AutoField(primary_key=True)

    hr_id_persona = models.CharField(db_column='HR_ID_PERSONA', max_length=255, blank=True, null=True)
    emplid = models.CharField(db_column='EMPLID', max_length=255, blank=True, null=True, db_index=True)
    hr_curp = models.CharField(db_column='HR_CURP', max_length=255, blank=True, null=True)

    hr_nombre = models.CharField(db_column='HR_NOMBRE', max_length=255, blank=True, null=True)
    last_name100 = models.CharField(db_column='LAST_NAME100', max_length=255, blank=True, null=True)
    hr_secnd_last_name = models.CharField(db_column='HR_SECND_LAST_NAME', max_length=255, blank=True, null=True)

    parentesco = models.CharField(db_column='PARENTESCO', max_length=255, blank=True, null=True)
    mismo_domicilio = models.CharField(db_column='MISMO_DOMICILIO', max_length=255, blank=True, null=True)

    correo_electronico = models.CharField(db_column='CORREO_ELECTRÓNICO', max_length=255, blank=True, null=True)

    tel_particular = models.CharField(db_column='TELÉFONO_PARTICULAR', max_length=255, blank=True, null=True)
    tel_celular = models.CharField(db_column='TELÉFONO_CELULAR', max_length=255, blank=True, null=True)

    codigo_postal = models.CharField(db_column='CODIGO_POSTAL', max_length=255, blank=True, null=True)
    colonia = models.CharField(db_column='COLONIA', max_length=255, blank=True, null=True)
    asentamiento = models.CharField(db_column='ASENTAMIENTO', max_length=255, blank=True, null=True)

    pais = models.CharField(db_column='PAIS', max_length=255, blank=True, null=True)
    entidad = models.CharField(db_column='ENTIDAD', max_length=255, blank=True, null=True)
    municipio = models.CharField(db_column='MUNICIPIO', max_length=255, blank=True, null=True)

    ciudad = models.CharField(db_column='CIUDAD', max_length=255, blank=True, null=True)
    ciudad_1 = models.CharField(db_column='CIUDAD_1', max_length=255, blank=True, null=True)
    ciudad_2 = models.CharField(db_column='CIUDAD_2', max_length=255, blank=True, null=True)

    sexo = models.CharField(db_column='SEXO', max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'FAMILIAR'


class Domicilio(models.Model):
    no_empleado = models.TextField(db_column='NO_EMPLEADO', primary_key=True)
    hr_id_persona = models.TextField(db_column='HR_ID_PERSONA', blank=True, null=True)
    position_nbr = models.TextField(db_column='POSITION_NBR', blank=True, null=True)
    nombre_completo = models.TextField(db_column='NOMBRE_COMPLETO', blank=True, null=True)
    rfc = models.TextField(db_column='RFC', blank=True, null=True)
    curp = models.TextField(db_column='CURP', blank=True, null=True)

    puesto_estructural = models.TextField(db_column='PUESTO_ESTRUCTURAL', blank=True, null=True)
    puesto_funcional = models.TextField(db_column='PUESTO_FUNCIONAL', blank=True, null=True)
    puesto = models.TextField(db_column='PUESTO', blank=True, null=True)

    escolaridad_tipo = models.TextField(db_column='ESCOLARIDAD_TIPO', blank=True, null=True)
    escolaridad_nivel = models.TextField(db_column='ESCOLARIDAD_NIVRL', blank=True, null=True)
    escolaridad_area = models.TextField(db_column='ESCOLARIDAD_AREA', blank=True, null=True)
    carrera = models.TextField(db_column='CARRERA', blank=True, null=True)
    centro_escolar = models.TextField(db_column='CENTRO_ESCOLAR', blank=True, null=True)

    humanos_status = models.TextField(db_column='HUMANOS_STATUS', blank=True, null=True)
    estatus_nomina = models.TextField(db_column='ESTATUS_NOMINA', blank=True, null=True)

    phone = models.TextField(db_column='PHONE', blank=True, null=True)
    phone1 = models.TextField(db_column='PHONE1', blank=True, null=True)

    calle = models.TextField(db_column='CALLE', blank=True, null=True)
    hr_numero_exterior = models.TextField(db_column='HR_NUMERO_EXTERIOR', blank=True, null=True)
    hr_numero_interior = models.TextField(db_column='HR_NUMERO_INTERIOR', blank=True, null=True)
    postal = models.TextField(db_column='POSTAL', blank=True, null=True)
    colonia = models.TextField(db_column='COLONIA', blank=True, null=True)
    hr_municipio = models.TextField(db_column='HR_MUNICIPIO', blank=True, null=True)
    estado = models.TextField(db_column='ESTADO', blank=True, null=True)

    email_addr2 = models.TextField(db_column='EMAIL_ADDR2', blank=True, null=True)
    email_addr = models.TextField(db_column='EMAIL_ADDR', blank=True, null=True)

    deptid = models.TextField(db_column='DEPTID', blank=True, null=True)
    unidad_administrativa = models.TextField(db_column='UNIDAD_ADMINISTRATIVA', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'domicilios'


class Movimiento(models.Model):
    llave = models.CharField(db_column='LLAVE', max_length=255, primary_key=True)

    posicion = models.CharField(db_column='Posición', max_length=255, blank=True, null=True)
    id_empl = models.CharField(db_column='Id_empl', max_length=255, blank=True, null=True)
    nombre = models.CharField(db_column='Nombre', max_length=255, blank=True, null=True)
    paterno = models.CharField(db_column='Paterno', max_length=255, blank=True, null=True)
    apellido_materno = models.CharField(db_column='Apellido Matern', max_length=255, blank=True, null=True)

    accion = models.CharField(db_column='Acción', max_length=255, blank=True, null=True)
    accion_nombre = models.CharField(db_column='Acción (Nombre)', max_length=255, blank=True, null=True)
    motivo = models.CharField(db_column='Motivo', max_length=255, blank=True, null=True)
    motivo_nombre = models.CharField(db_column='Motivo (Nombre)', max_length=255, blank=True, null=True)

    fecha_efectiva = models.CharField(db_column='F/Efva', max_length=255, blank=True, null=True)
    sec = models.CharField(db_column='Sec', max_length=255, blank=True, null=True)
    fecha_captura = models.CharField(db_column='F/Captura', max_length=255, blank=True, null=True)

    est_hr = models.CharField(db_column='Est HR', max_length=255, blank=True, null=True)
    estado_pago = models.CharField(db_column='Estado Pago', max_length=255, blank=True, null=True)
    partida_ptal = models.CharField(db_column='Ptda Ptal', max_length=255, blank=True, null=True)

    un = models.CharField(db_column='UN', max_length=255, blank=True, null=True)
    u_admva = models.CharField(db_column='U/Admva', max_length=255, blank=True, null=True)
    id_depto = models.CharField(db_column='Id/Depto', max_length=255, blank=True, null=True)
    depnd_drt = models.CharField(db_column='Depnd Drt', max_length=255, blank=True, null=True)

    plan_sal = models.CharField(db_column='Plan Sal', max_length=255, blank=True, null=True)
    grado = models.CharField(db_column='Grado', max_length=255, blank=True, null=True)
    esc = models.CharField(db_column='Esc', max_length=255, blank=True, null=True)
    puesto_ptal = models.CharField(db_column='Puesto Ptal', max_length=255, blank=True, null=True)
    nivel_tabular = models.CharField(db_column='Nivel Tabular', max_length=255, blank=True, null=True)
    gp_pago = models.CharField(db_column='Gp Pago', max_length=255, blank=True, null=True)
    prog_beneficios = models.CharField(db_column='Prog Beneficios', max_length=255, blank=True, null=True)

    sal_base = models.CharField(db_column='Sal Base', max_length=255, blank=True, null=True)
    cd_puesto = models.CharField(db_column='Cd Puesto', max_length=255, blank=True, null=True)
    ubicacion = models.CharField(db_column='Ubicación', max_length=255, blank=True, null=True)
    id_estbl = models.CharField(db_column='ID Estbl', max_length=255, blank=True, null=True)

    slda_prevista = models.CharField(db_column='Slda Prevista', max_length=255, blank=True, null=True)
    fh_ult_actz = models.CharField(db_column='F/H Últ Actz', max_length=255, blank=True, null=True)
    por = models.CharField(db_column='Por', max_length=255, blank=True, null=True)
    ult_inicio = models.CharField(db_column='Últ Inicio', max_length=255, blank=True, null=True)
    f_inicial = models.CharField(db_column='F/Inicial', max_length=255, blank=True, null=True)
    gp_trabajo = models.CharField(db_column='Gp Trabajo', max_length=255, blank=True, null=True)
    grupo_cd_sal = models.CharField(db_column='Grupo Cd Sal', max_length=255, blank=True, null=True)
    antig_empr = models.CharField(db_column='Antig Empr', max_length=255, blank=True, null=True)

    rfc = models.CharField(db_column='RFC', max_length=255, blank=True, null=True)
    curp = models.CharField(db_column='CURP', max_length=255, blank=True, null=True)
    id_persona = models.CharField(db_column='Id Persona', max_length=255, blank=True, null=True)
    descr_larga = models.CharField(db_column='Descr Larga', max_length=255, blank=True, null=True)
    niv_jerarquico = models.CharField(db_column='Niv# Jerarquico', max_length=255, blank=True, null=True)
    descr_larga1 = models.CharField(db_column='Descr Larga1', max_length=255, blank=True, null=True)
    genero = models.CharField(db_column='Género', max_length=255, blank=True, null=True)
    fecha_entrada = models.CharField(db_column='Fecha Entrada', max_length=255, blank=True, null=True)
    f_posicion = models.CharField(db_column='F Posición', max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'MOV_TOTAL'
