class TimbreFiscalDigital:
    def __init__(self, data):
        """
        Timbre Fiscal Digital (TFD)
        * v1.0
        * v1.1
        https://www.sat.gob.mx/TimbreFiscalDigital
        """
        attrs = data.get("attributes")

        self.schema_location = attrs.get("xsi:schemaLocation")
        self.rfc_prov_certif = attrs.get("RfcProvCertif")
        self.version = attrs.get("Version")
        self.uuid = attrs.get("UUID")
        self.fecha_timbrado = attrs.get("FechaTimbrado")
        self.sello_cfd = attrs.get("SelloCFD")
        self.no_certificado_sat = attrs.get("NoCertificadoSAT")
        self.sello_sat = attrs.get("SelloSAT")

        # timbreFiscalDigital v1.1 only
        self.leyenda = attrs.get("Leyenda")
