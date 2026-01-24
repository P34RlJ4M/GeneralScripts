# Script to generate history provider path
# Run this in the Script Console in Ignition Designer
# THE RIGHT COMBINATION FOR THE DATASOURCE AND DBTYPE WILL NEED TO BE FOUND. DBTYPE IS USUALLY THE REALTIME/HISTORICAL TAG PROVIDER

print "=== History Provider Path Generator ==="
print ""

# Configuration
historyProvider = "TAGHISTORIAN"
datasource = "schaendorf"
dbType = "schaendorf"

# Generate the path
path = "histprov:%s:/drv:%s:%s:/" % (historyProvider, dbType, datasource)

print "CONFIGURATION:"
print "  History Provider: %s" % historyProvider
print "  Datasource: %s" % datasource
print "  Database Type: %s" % dbType
print ""
print "POWER CHART HISTORY PROVIDER PATH:"
print ""
print path
print ""