from json_cfdi.wrappers.utils import Complex


class Emisor:
    def __init__(self, data):
        attrs = data.get("attributes")

        self.rfc = attrs.get("Rfc")
        self.nombre = attrs.get("Nombre")
        self.regimen_fiscal = attrs.get("RegimenFiscal")
        self.fac_atr_adquirente = attrs.get("FacAtrAdquirente")


class Receptor:
    def __init__(self, data):
        attrs = data.get("attributes")

        self.rfc = attrs.get("Rfc")
        self.nombre = attrs.get("Nombre")
        self.uso_cfdi = attrs.get("UsoCFDI")
        self.residencia_fiscal = attrs.get("ResidenciaFiscal")
        self.num_reg_id_trib = attrs.get("NumRegIdTrib")
        self.domicilio_fiscal_receptor = attrs.get("DomicilioFiscalReceptor")
        self.regimen_fiscal_receptor = attrs.get("RegimenFiscalReceptor")


class Complemento:
    """
    cfdi:Complemento > *

    Examples:
        In the XML:
            cfdi:Complemento
                > tfd:TimbreFiscalDigital
                > nomina12:Nomina
                > {any:any}

        As a model:
            cfdi.complemento.timbreFiscalDigital
            cfdi.complemento.nomina
            cfdi.complemento.{any}
    """

    def __init__(self, data):
        self.timbre_fiscal_digital = None
        self.nomina = None
        self.pagos = None

        if data.get("tfd:TimbreFiscalDigital"):
            from json_cfdi.wrappers.timbreFiscalDigital11 import TimbreFiscalDigital
            self.timbre_fiscal_digital = TimbreFiscalDigital(
                data.get("tfd:TimbreFiscalDigital")
            )

        if data.get("nomina12:Nomina"):
            from json_cfdi.wrappers.nomina12 import Nomina
            self.nomina = Nomina(data.get("nomina12:Nomina"))

        if data.get("pago20:Pagos"):
            from json_cfdi.wrappers.pagos20 import Pagos20 as Pagos
            self.pagos = Pagos(data.get("pago20:Pagos"))


class Taslado(Complex):
    def __init__(self, data):
        attrs = data.get("attributes")

        self.impuesto = attrs.get("Impuesto")
        self.tipo_factor = attrs.get("TipoFactor")
        self.tasa_o_cuota = self.float_or_none(attrs.get("TasaOCuota"))
        self.importe = self.float_or_none(attrs.get("Importe"))


class ConceptoTaslado(Complex):
    def __init__(self, data):
        attrs = data.get("attributes")

        self.base = self.float_or_none(attrs.get("Base"))
        self.impuesto = attrs.get("Impuesto")
        self.tipo_factor = attrs.get("TipoFactor")
        self.tasa_o_cuota = self.float_or_none(attrs.get("TasaOCuota"))
        self.importe = self.float_or_none(attrs.get("Importe"))


class Retencion(Complex):
    def __init__(self, data):
        attrs = data.get("attributes")

        self.impuesto = attrs.get("Impuesto")
        self.importe = self.float_or_none(attrs.get("Importe"))


class RetencionConcepto(Complex):
    def __init__(self, data):
        attrs = data.get("attributes")

        self.base = self.float_or_none(attrs.get("Base"))
        self.impuesto = attrs.get("Impuesto")
        self.tipo_factor = attrs.get("TipoFactor")
        self.tasa_o_cuota = self.float_or_none(attrs.get("TasaOCuota"))
        self.importe = self.float_or_none(attrs.get("Importe"))


class ConceptoImpuestos(Complex):
    """
    {
        cfdi:Impuestos: {
            cfdi:Traslados: {
                cfdi:Traslado: {} | []
            },
            cfdi:Retenciones {
                cfdi:Retencion: {} | []
            }
        }
    }
    """

    def __init__(self, data):
        self.traslados = self.children_as_list(
            data.get("cfdi:Traslados"),
            child="cfdi:Traslado",
            klass=ConceptoTaslado,
        )

        self.retenciones = self.children_as_list(
            data.get("cfdi:Retenciones"),
            child="cfdi:Retencion",
            klass=Retencion,
        )


class ConceptoCuentaPredial:
    def __init__(self, data):
        attrs = data.get("attributes")

        self.numero = attrs.get("Numero")


class ConceptoInformacionAduanera:
    def __init__(self, data):
        attrs = data.get("attributes")

        self.numero_pedimento = attrs.get("NumeroPedimento")


class ConceptoParte(Complex):
    def __init__(self, data):
        attrs = data.get("attributes")

        self.clave_prod_serv = attrs.get("ClaveProdServ")
        self.no_identificacion = attrs.get("NoIdentificacion")
        self.cantidad = self.float_or_none(attrs.get("Cantidad"))
        self.descripcion = attrs.get("Descripcion")
        self.unidad = attrs.get("Unidad")
        self.valor_unitario = self.float_or_none(attrs.get("ValorUnitario"))
        self.importe = self.float_or_none(attrs.get("Importe"))

        children = data.get("children")[0]
        self.informacion_aduanera = self.children_as_list(
            children,
            child="cfdi:InformacionAduanera",
            klass=ConceptoInformacionAduanera,
        )


class ACuentaTerceros:
    def __init__(self, data):
        attrs = data.get("attributes")

        self.rfc_a_cuenta_rerceros = attrs.get("RfcACuentaTerceros")
        self.nombre_a_cuenta_terceros = attrs.get("NombreACuentaTerceros")
        self.regimen_fiscal_a_cuenta_terceros = attrs.get("RegimenFiscalACuentaTerceros")
        self.domicilio_fiscal_a_cuenta_terceros = attrs.get(
            "DomicilioFiscalACuentaTerceros"
        )


class Concepto(Complex):
    def __init__(self, data):
        attrs = data.get("attributes")

        self.clave_prod_serv = attrs.get("ClaveProdServ")
        self.cantidad = self.float_or_none(attrs.get("Cantidad"))
        self.clave_unidad = attrs.get("ClaveUnidad")
        self.descripcion = attrs.get("Descripcion")
        self.valor_unitario = self.float_or_none(attrs.get("ValorUnitario"))
        self.importe = self.float_or_none(attrs.get("Importe"))
        self.no_identificacion = attrs.get("NoIdentificacion")
        self.unidad = attrs.get("Unidad")
        self.descuento = self.float_or_none(attrs.get("Descuento"))
        self.objeto_imp = attrs.get("ObjetoImp")

        self.impuestos = None
        self.a_cuenta_terceros = None
        self.complemento_concepto = None
        self.cuenta_predial = []
        self.informacion_aduanera = []
        self.parte = []

        if data.get("children") and len(data.get("children")) > 0:
            children = data.get("children")[0]

            if children.get("cfdi:Impuestos"):
                self.impuestos = ConceptoImpuestos(children.get("cfdi:Impuestos"))
            self.complemento_concepto = children.get("cfdi:ComplementoConcepto")
            if children.get("cfdi:CuentaPredial"):
                self.cuenta_predial = self.children_as_list(
                    children,
                    child="cfdi:CuentaPredial",
                    klass=ConceptoCuentaPredial,
                )
            if children.get("cfdi:ACuentaTerceros"):
                self.a_cuenta_terceros = ACuentaTerceros(
                    children.get("cfdi:ACuentaTerceros")
                )
            self.informacion_aduanera = self.children_as_list(
                children,
                child="cfdi:InformacionAduanera",
                klass=ConceptoInformacionAduanera,
            )
            self.parte = self.children_as_list(
                children, child="cfdi:Parte", klass=ConceptoParte
            )


class Impuestos(Complex):
    def __init__(self, data):
        attrs = data.get("attributes")

        self.total_impuestos_trasladados = self.float_or_none(
            attrs.get("TotalImpuestosTrasladados")
        )
        self.total_impuestos_retenidos = self.float_or_none(
            attrs.get("TotalImpuestosRetenidos")
        )

        # getting children
        children = data.get("children")[0]

        self.retenciones = self.children_as_list(
            children.get("cfdi:Retenciones"),
            child="cfdi:Retencion",
            klass=Retencion,
        )

        self.traslados = self.children_as_list(
            children.get("cfdi:Traslados"),
            child="cfdi:Traslado",
            klass=Taslado,
        )


class CfdiRelacionados(Complex):
    def __init__(self, data):
        attrs = data.get("attributes")

        self.tipo_relacion = attrs.get("TipoRelacion")

        # children
        children = data.get("children")[0]
        self.cfdi_relacionados = self.children_as_list(
            children, child="cfdi:CfdiRelacionado", klass=CfdiRelacionado
        )


class CfdiRelacionado:
    def __init__(self, data):
        attrs = data.get("attributes")
        self.uuid = attrs.get("UUID")


class InformacionGlobal:
    def __init__(self, data):
        attrs = data.get("attributes")

        self.periodicidad = attrs.get("Periodicidad")
        self.meses = attrs.get("Meses")
        self.axo = attrs.get("Año")


class CFDI(Complex):
    """
    CFDI v4.0
    http://www.sat.gob.mx/cfd/4
    """

    supported_versions = ["4.0"]

    def __init__(self, raw_data):
        attrs = raw_data.get("attributes")

        self.schema_ocation = attrs.get("xsi:schemaLocation")
        self.version = attrs.get("Version")

        self.check_version()

        self.serie = attrs.get("Serie")
        self.folio = attrs.get("Folio")
        self.fecha = attrs.get("Fecha")
        self.sello = attrs.get("Sello")
        self.forma_pago = attrs.get("FormaPago")
        self.no_certificado = attrs.get("NoCertificado")
        self.certificado = attrs.get("Certificado")
        self.sub_total = self.float_or_none(attrs.get("SubTotal"))
        self.moneda = attrs.get("Moneda")
        self.total = self.float_or_none(attrs.get("Total"))
        self.tipo_de_comprobante = attrs.get("TipoDeComprobante")
        self.metodo_pago = attrs.get("MetodoPago")
        self.lugar_expedicion = attrs.get("LugarExpedicion")
        self.condiciones_de_pago = attrs.get("CondicionesDePago")
        self.descuento = self.float_or_none(attrs.get("Descuento"))
        self.tipo_cambio = self.float_or_none(attrs.get("TipoCambio"))
        self.confirmacion = attrs.get("Confirmacion")
        self.exportacion = attrs.get("Exportacion")

        self.informacion_global = None
        self.complemento = None
        self.impuestos = None
        self.addenda = None

        # getting children
        children = raw_data.get("children")[0]

        self.emisor = Emisor(children.get("cfdi:Emisor"))
        self.receptor = Receptor(children.get("cfdi:Receptor"))

        if children.get("cfdi:InformacionGlobal"):
            self.informacion_global = InformacionGlobal(
                children.get("cfdi:InformacionGlobal")
            )

        # getting conceptos
        self.conceptos = self.children_as_list(
            children.get("cfdi:Conceptos"),
            child="cfdi:Concepto",
            klass=Concepto,
        )

        if children.get("cfdi:Impuestos"):
            self.impuestos = Impuestos(children.get("cfdi:Impuestos"))

        # getting all complementos
        if children.get("cfdi:Complemento"):
            self.complemento = Complemento(children.get("cfdi:Complemento"))

        self.cfdi_relacionados = self.children_as_list(
            children, child="cfdi:CfdiRelacionados", klass=CfdiRelacionados
        )

        # it might require aditional configuration (location)
        self.addenda = children.get("cfdi:Addenda", None)

    def check_version(self):
        if self.version not in self.supported_versions:
            raise Exception(f"Version {self.version} not supported")
