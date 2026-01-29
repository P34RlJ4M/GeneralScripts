# Script to generate history provider path
# Run this in the Script Console in Ignition Designer
# THE RIGHT COMBINATION FOR THE DATASOURCE AND DBTYPE WILL NEED TO BE FOUND. DBTYPE IS USUALLY THE REALTIME/HISTORICAL TAG PROVIDER
# histprov:${databaseName}:/drv:${gatewayName}:${tagProvider}:/tag:${pathToTag}
print "=== History Provider Path Generator ==="
print ""

# Configuration
historyProvider = "TAGHISTORIAN"
tagProvider = "schaendorf"
gatewayName = "schaendorf"

# Generate the path
path = "histprov:%s:/drv:%s:%s:/" % (historyProvider, gatewayName, tagProvider)

print "CONFIGURATION:"
print "  History Provider: %s" % historyProvider
print "  Tag Provider: %s" % tagProvider
print "  Gateway Name: %s" % gatewayName
print ""
print "POWER CHART HISTORY PROVIDER PATH:"
print ""
print path
print ""