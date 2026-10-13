import system
import os

# ============================================
# CONFIGURATION
# ============================================

year = 2026
month = 9

fileName = "AlarmHistory_September_2026.csv"

desktopPath = os.path.join(
    os.path.expanduser("~"),
    "Desktop"
)

filePath = os.path.join(desktopPath, fileName)

# ============================================
# DATE RANGE
# ============================================

startDate = system.date.getDate(year, month - 1, 1)
endDate = system.date.addMonths(startDate, 1)

# ============================================
# EXPORT
# ============================================

headers = [
    "EventTime",
    "EventType",
    "Source",
    "DisplayPath",
    "Name",
    "Priority"
]

rows = []

currentDate = startDate

try:

    print("Starting September 2026 Alarm Export")

    while currentDate.before(endDate):

        nextDate = system.date.addDays(currentDate, 1)

        # Query one day
        results = system.alarm.queryJournal(
            startDate=currentDate,
            endDate=nextDate,
            state=[0],
            maxReturnSize=100000
        )

        print("{} - Retrieved {} alarms".format(
            system.date.format(currentDate, "yyyy-MM-dd"),
            len(results)
        ))

        for event in results:

            eventTime = event.get("EventTime")
            eventType = event.get("EventType")
            source = event.get("Source")
            displayPath = event.get("DisplayPath")
            name = event.get("Name")
            priority = event.get("Priority")

            rows.append([
                str(eventTime) if eventTime is not None else "",
                str(eventType) if eventType is not None else "",
                str(source) if source is not None else "",
                str(displayPath) if displayPath is not None else "",
                str(name) if name is not None else "",
                str(priority) if priority is not None else ""
            ])

        currentDate = nextDate

    # ============================================
    # CREATE CSV
    # ============================================

    dataset = system.dataset.toDataSet(headers, rows)

    csvData = system.dataset.toCSV(dataset, True)

    system.file.writeFile(filePath, csvData)

    print("")
    print("===================================")
    print("EXPORT COMPLETE")
    print("===================================")
    print("Total Alarm Activations: {}".format(len(rows)))
    print("File: {}".format(filePath))

except Exception as e:

    print("EXPORT FAILED")
    print(str(e))