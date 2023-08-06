from json_cfdi.wrappers.utils import Complex


class SubContratacion(Complex):
    def __init__(self, data):
        attrs = data.get("attributes")

        self.rfc_labora = attrs.get("RfcLabora")
        self.porcentaje_tiempo = self.float_or_none(attrs.get("PorcentajeTiempo"))


class Receptor(Complex):
    def __init__(self, data):
        attrs = data.get("attributes")

        self.curp = attrs.get("Curp")
        self.num_seguridad_social = attrs.get("NumSeguridadSocial")
        self.fecha_inicio_rel_laboral = attrs.get("FechaInicioRelLaboral")
        self.antiguedad = attrs.get("Antigüedad")
        self.tipo_contrato = attrs.get("TipoContrato")
        self.sindicalizado = attrs.get("Sindicalizado")
        self.tipo_jornada = attrs.get("TipoJornada")
        self.tipo_regimen = attrs.get("TipoRegimen")
        self.num_empleado = attrs.get("NumEmpleado")
        self.departamento = attrs.get("Departamento")
        self.puesto = attrs.get("Puesto")
        self.riesgo_puesto = attrs.get("RiesgoPuesto")
        self.periodicidad_pago = attrs.get("PeriodicidadPago")
        self.banco = attrs.get("Banco")
        self.cuenta_bancaria = attrs.get("CuentaBancaria")
        self.salario_base_cot_apor = self.float_or_none(attrs.get("SalarioBaseCotApor"))
        self.salario_diario_integrado = self.float_or_none(
            attrs.get("SalarioDiarioIntegrado")
        )
        self.clave_ent_fed = attrs.get("ClaveEntFed")

        self.sub_contratacion = None

        children = data.get("children")[0]
        self.sub_contratacion = self.children_as_list(
            children, child="nomina12:SubContratacion", klass=SubContratacion
        )


class EntidadSNCF(Complex):
    def __init__(self, data):
        attrs = data.get("attributes")

        self.origen_recurso = attrs.get("OrigenRecurso")
        self.monto_recurso_propio = self.float_or_none(attrs.get("MontoRecursoPropio"))


class Emisor:
    def __init__(self, data):
        attrs = data.get("attributes")

        self.registro_patronal = attrs.get("RegistroPatronal")
        self.curp = attrs.get("Curp")
        self.rfc_patron_origen = attrs.get("RfcPatronOrigen")

        self.entidad_SNCF = None

        children = data.get("children")[0]
        if children.get("nomina12:EntidadSNCF"):
            self.entidad_SNCF = EntidadSNCF(children.get("nomina12:EntidadSNCF"))


class AccionesOTitulos(Complex):
    def __init__(self, data):
        attrs = data.get("attributes")

        self.valor_mercado = self.float_or_none(attrs.get("ValorMercado"))
        self.precio_al_otorgarse = self.float_or_none(attrs.get("PrecioAlOtorgarse"))


class HorasExtra(Complex):
    def __init__(self, data):
        attrs = data.get("attributes")

        self.dias = self.int_or_none(attrs.get("Dias"))
        self.tipo_horas = attrs.get("TipoHoras")
        self.horas_extra = self.int_or_none(attrs.get("HorasExtra"))
        self.importe_pagado = self.float_or_none(attrs.get("ImportePagado"))


class Percepcion(Complex):
    def __init__(self, data):
        attrs = data.get("attributes")

        self.clave = attrs.get("Clave")
        self.concepto = attrs.get("Concepto")
        self.importe_exento = self.float_or_none(attrs.get("ImporteExento"))
        self.importe_gravado = self.float_or_none(attrs.get("ImporteGravado"))
        self.tipo_percepcion = attrs.get("TipoPercepcion")

        self.acciones_o_titulos = None

        children = data.get("children")[0]
        if children.get("nomina12:AccionesOTitulos"):
            self.acciones_o_titulos = AccionesOTitulos(
                children.get("nomina12:AccionesOTitulos")
            )

        self.horas_extra = self.children_as_list(
            children, child="nomina12:HorasExtra", klass=HorasExtra
        )


class JubilacionPensionRetiro(Complex):
    def __init__(self, data):
        attrs = data.get("attributes")

        self.total_una_exhibicion = self.float_or_none(attrs.get("TotalUnaExhibicion"))
        self.ingreso_acumulable = self.float_or_none(attrs.get("IngresoAcumulable"))
        self.ingreso_no_acumulable = self.float_or_none(attrs.get("IngresoNoAcumulable"))


class Deduccion(Complex):
    def __init__(self, data):
        attrs = data.get("attributes")

        self.clave = attrs.get("Clave")
        self.concepto = attrs.get("Concepto")
        self.importe = self.float_or_none(attrs.get("Importe"))
        self.tipo_deduccion = attrs.get("TipoDeduccion")


class Deducciones(Complex):
    def __init__(self, data):
        attrs = data.get("attributes")

        self.total_impuestos_retenidos = self.float_or_none(
            attrs.get("TotalImpuestosRetenidos")
        )
        self.total_otras_deducciones = self.float_or_none(
            attrs.get("TotalOtrasDeducciones")
        )

        # getting nomina12:Deduccion
        children = data.get("children")[0]
        self.deducciones = self.children_as_list(
            children, child="nomina12:Deduccion", klass=Deduccion
        )


class SeparacionIndemnizacion(Complex):
    def __init__(self, data):
        attrs = data.get("attributes")

        self.total_pagado = self.float_or_none(attrs.get("TotalPagado"))
        self.num_axos_servicio = self.int_or_none(attrs.get("NumAñosServicio"))
        self.ultimo_sueldo_mens_ord = self.float_or_none(attrs.get("UltimoSueldoMensOrd"))
        self.ingreso_acumulable = self.float_or_none(attrs.get("IngresoAcumulable"))
        self.ingreso_no_acumulable = self.float_or_none(attrs.get("IngresoNoAcumulable"))


class Percepciones(Complex):
    def __init__(self, data):
        attrs = data.get("attributes")

        self.total_exento = self.float_or_none(attrs.get("TotalExento"))
        self.total_gravado = self.float_or_none(attrs.get("TotalGravado"))
        self.total_jubilacion_pension_retiro = self.float_or_none(
            attrs.get("TotalJubilacionPensionRetiro")
        )
        self.total_sueldos = self.float_or_none(attrs.get("TotalSueldos"))

        self.jubilacion_pension_retiro = None
        self.separacion_indemnizacion = None

        # percepciones
        children = data.get("children")[0]
        self.percepciones = self.children_as_list(
            children, child="nomina12:Percepcion", klass=Percepcion
        )

        # jubilacionPensionRetiro
        if children.get("nomina12:JubilacionPensionRetiro"):
            self.jubilacion_pension_retiro = JubilacionPensionRetiro(
                children.get("nomina12:JubilacionPensionRetiro")
            )

        # separacionIndemnizacion
        if children.get("nomina12:SeparacionIndemnizacion"):
            self.separacion_indemnizacion = SeparacionIndemnizacion(
                children.get("nomina12:SeparacionIndemnizacion")
            )


class SubsidioAlEmpleo(Complex):
    def __init__(self, data):
        attrs = data.get("attributes")

        self.subsidio_causado = self.float_or_none(attrs.get("SubsidioCausado"))


class CompensacionSaldosAFavor(Complex):
    def __init__(self, data):
        attrs = data.get("attributes")

        self.saldo_a_favor = self.float_or_none(attrs.get("SaldoAFavor"))
        self.axo = self.int_or_none(attrs.get("Año"))
        self.remanente_sal_fav = self.float_or_none(attrs.get("RemanenteSalFav"))


class OtroPago(Complex):
    def __init__(self, data):
        attrs = data.get("attributes")

        self.tipo_otro_pago = attrs.get("TipoOtroPago")
        self.clave = attrs.get("Clave")
        self.concepto = attrs.get("Concepto")
        self.importe = self.float_or_none(attrs.get("Importe"))

        self.subsidio_al_empleo = None
        self.compensacion_saldos_a_favor = None

        children = data.get("children")[0]
        if children.get("nomina12:SubsidioAlEmpleo"):
            self.subsidio_al_empleo = SubsidioAlEmpleo(
                children.get("nomina12:SubsidioAlEmpleo")
            )

        if children.get("nomina12:CompensacionSaldosAFavor"):
            self.compensacion_saldos_a_favor = CompensacionSaldosAFavor(
                children.get("nomina12:CompensacionSaldosAFavor")
            )


class Incapacidad(Complex):
    def __init__(self, data):
        attrs = data.get("attributes")

        self.dias_incapacidad = self.int_or_none(attrs.get("DiasIncapacidad"))
        self.tipo_incapacidad = attrs.get("TipoIncapacidad")
        self.importe_monetario = self.float_or_none(attrs.get("ImporteMonetario"))


class Nomina(Complex):
    supported_versions = ["1.2"]

    def __init__(self, raw_data):
        attrs = raw_data.get("attributes")

        self.version = attrs.get("Version")

        self.check_version()

        self.tipo_nomina = attrs.get("TipoNomina")

        self.fecha_pago = attrs.get("FechaPago")
        self.fecha_final_pago = attrs.get("FechaFinalPago")
        self.fecha_inicial_pago = attrs.get("FechaInicialPago")

        self.num_dias_pagados = self.float_or_none(attrs.get("NumDiasPagados"))
        self.total_percepciones = self.float_or_none(attrs.get("TotalPercepciones"))
        self.total_deducciones = self.float_or_none(attrs.get("TotalDeducciones"))
        self.total_otros_pagos = self.float_or_none(attrs.get("TotalOtrosPagos"))

        # getting children
        children = raw_data.get("children")[0]

        self.receptor = Receptor(children.get("nomina12:Receptor"))
        self.emisor = None
        self.percepciones = None
        self.deducciones = None

        if children.get("nomina12:Emisor"):
            self.emisor = Emisor(children.get("nomina12:Emisor"))

        if children.get("nomina12:Percepciones"):
            self.percepciones = Percepciones(children.get("nomina12:Percepciones"))

        if children.get("nomina12:Deducciones"):
            self.deducciones = Deducciones(children.get("nomina12:Deducciones"))

        self.otros_pagos = self.children_as_list(
            children.get("nomina12:OtrosPagos"),
            child="nomina12:OtroPago",
            klass=OtroPago,
        )

        self.incapacidades = self.children_as_list(
            children.get("nomina12:Incapacidades"),
            child="nomina12:Incapacidad",
            klass=Incapacidad,
        )

    def check_version(self):
        if self.version not in self.supported_versions:
            raise Exception(f"Version {self.version} not supported")
