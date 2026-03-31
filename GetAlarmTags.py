def browse_tags_recursive(base_path):
    results = system.tag.browse(base_path)

    for result in results.getResults():
        full_path = str(result['fullPath'])
        has_children = result['hasChildren']
        tag_type = str(result['tagType'])

        try:
            # Only process Atomic Tags
            if tag_type == "AtomicTag":
                config = system.tag.getConfiguration(full_path, False)

                if config and 'alarms' in config[0]:
                    alarms = config[0]['alarms']

                    for alarm in alarms:
                        alarm_name = alarm.get('name', 'UnnamedAlarm')
                        priority = alarm.get('priority', 'Unknown')

                        print
                        "Tag: {0} | Alarm: {1} | Priority: {2}".format(
                            full_path, alarm_name, priority
                        )

            # Recurse into folders
            if has_children:
                browse_tags_recursive(full_path)

        except Exception as e:
            print
            "Error processing {0}: {1}".format(full_path, str(e))


# Start browsing from your folder
browse_tags_recursive("[default]VanguardOrganics")
