"""BESTANDSINFORMATIE"""
#variabele: file_root
#uitleg:    Bestandspath van de map waarin zich de LOGI domeinen bevinden
#voorbeeld: "//epzlogi01t/Development"
#format:    "path"
file_root = "//epzlogi01t/Development"

#variabele: file_extension
#uitleg:    Bestandsextentie waarnaar gezocht moet worden in de opgegeven mappen
#voorbeeld: "*.lgx"
#format:    "bestandsextensie"
file_extension = "*.lgx"

#variabele: standard_path
#uitleg:    Standaard pad waarin de bestanden zich bevinden
#voorbeeld: "_Definitions/_Reports"
#format:    "path"
standard_path = "_Definitions/_Reports"

#variabele: settings_path
#uitleg:    Standaard pad waar de instellingenbestanden aanwezig zijn
#voorbeeld: "_Definitions/_Settings.lgx"
#format:    "path"
settings_path = "_Definitions/_Settings.lgx"

#variabele: exclude_files
#uitleg:    Bestanden die moeten worden overgeslagen per domein
#voorbeeld: {'domeinnaam': ['bestandsnaam1', 'bestandsnaam2']}
#format:    {'domein': ['bestandsnaam1', 'bestandsnaam2']}
exclude_files = {}

#variabele: include_domain
#uitleg:    Lijst van domeinen die moeten worden meegenomen. Leeg betekent alle domeinen.
#voorbeeld: ['domein1', 'domein2']
#format:    ['domein1', 'domein2']
include_domain = []


"""SERVERINFORMATIE"""
#variabele: serverinfo
#uitleg:    Dictionary van serverinformatie voor verschillende omgevingen
#voorbeeld: {'Omgeving1': ['server1', 'server2'], 'Omgeving2': ['server3']}
#format:    {'Omgeving': ['server1', 'server2']}
serverinfo = {'TEST_Omgeving': ['epzlogi01t'], 'ACCEPTATIE_Omgeving': ['epzlogi01a'], 'PRODUCTIE_Omgeving': ['reporting', 'reporting.epz.lan', 'epzlogi01p.epz.lan', 'epzlogi01p']}

#variabele: srv_1_env
#uitleg:    Omgevingsvariabele voor server 1
#voorbeeld: 'T'
#format:    'waarde'
srv_1_env = 'T'

#variabele: srv_1
#uitleg:    Naam van de server waar gegevens worden ingevoegd
#voorbeeld: 'epzsql03OT\OTDWH'
#format:    'servernaam'
srv_1 = 'epzsql03OT\OTDWH'

#variabele: srv_1_database
#uitleg:    Naam van de database op srv_1 waar gegevens worden ingevoegd
#voorbeeld: 'testgjh'
#format:    'databasenaam'
srv_1_database = 'testgjh'