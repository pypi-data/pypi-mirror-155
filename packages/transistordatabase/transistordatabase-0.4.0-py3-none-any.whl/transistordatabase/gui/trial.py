import transistordatabase as tdb


#t1 = tdb.import_json('/home/nikolasf/Downloads/TDB_MOSFETs/template_SCT3060AW7/Rohm_SCT3060AW7.json')
#t1 = tdb.import_json('/home/nikolasf/Downloads/TDB_MOSFETs/template_IPBE65R050CFD7A/Infineon_IPBE65R050CFD7A.json')

t1 = tdb.load('GaNSystems_GS66506T')
t1.export_datasheet()