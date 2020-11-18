##### Start command:   
python manage.py runserver

----
##### Routes
/records - returns list of records \
/records/{id} - returns certain record 

/record_types - returns list of record types(abstract=true to get abstract records) \
/record_types/{id} - returns certain record type(?abstract=true to get abstract record, ?fields=field_name1,field_name2,... to get certain fields)

/register/ \
/login/ \
/logout/

----
##### AbstractRecordType entity field values
+ "str"
+ "int"
+ "float"

