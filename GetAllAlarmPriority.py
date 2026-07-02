import system

provider = "[default]VanguardOrganics"

print "TagPath,AlarmName,Priority"

def browseFolder(path):
    try:
        results = system.tag.browse(path)

        for result in results.getResults():

            fullPath = str(result["fullPath"])

            if result["hasChildren"]:
                browseFolder(fullPath)

            try:
                config = system.tag.getConfiguration(fullPath, False)

                if len(config) == 0:
                    continue

                tagConfig = config[0]

                if "alarms" in tagConfig:

                    alarms = tagConfig["alarms"]

                    for alarm in alarms:

                        alarmName = alarm.get("name", "")
                        priority = alarm.get("priority", "")

                        print '"%s","%s","%s"' % (
                            fullPath,
                            alarmName,
                            priority
                        )

            except Exception as e:
                print "Error reading %s : %s" % (fullPath, str(e))

    except Exception as e:
        print "Browse error on %s : %s" % (path, str(e))


browseFolder(provider)

print "Done."