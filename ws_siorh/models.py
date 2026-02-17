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
