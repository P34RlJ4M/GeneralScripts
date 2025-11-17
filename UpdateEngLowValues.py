# Script to find all tags ending with _TM in [default]Papas_Tags folder
# and update their engHigh values to 3600

# Define the tag path to search
tagPath = "[default]Papas_Tags"

# Browse all tags in the folder recursively
tags = system.tag.browse(path=tagPath, filter={'recursive': True})

# Create a list to store matching tag paths
matchingTagPaths = []

# Iterate through all tags
for tag in tags.getResults():
    tagName = tag['name']
    fullPath = str(tag['fullPath'])  # Convert TagPath object to string

    # Check if tag name ends with _TM
    if tagName.endswith('_TM'):
        matchingTagPaths.append(fullPath)

# Print results header
print
"Found %d tags ending with '_TM':" % len(matchingTagPaths)
print
"-" * 80
print
"%-50s %-15s %-15s %-15s" % ("Tag Name", "Old engLow", "Old engHigh", "New engHigh")
print
"-" * 80

# List to store tag configurations for batch update
tagConfigsToUpdate = []

# Get detailed information for each matching tag
for tagPath in matchingTagPaths:
    try:
        # Read the current tag configuration
        tagConfigs = system.tag.readBlocking([tagPath + ".engLow", tagPath + ".engHigh"])

        engLow = tagConfigs[0].value if tagConfigs[0].quality.isGood() else 'N/A'
        oldEngHigh = tagConfigs[1].value if tagConfigs[1].quality.isGood() else 'N/A'
        newEngHigh = 3600

        # Print formatted output
        print
        "%-50s %-15s %-15s %-15s" % (tagPath, str(engLow), str(oldEngHigh), str(newEngHigh))

        # Prepare tag configuration for update
        tagConfig = {
            "tagPath": tagPath,
            "engHigh": newEngHigh
        }
        tagConfigsToUpdate.append(tagConfig)

    except Exception as e:
        print
        "%-50s ERROR: %s" % (tagPath, str(e))

# Confirm before updating
print
"\n" + "=" * 80
print
"Ready to update %d tags. Updating engHigh to 3600..." % len(tagConfigsToUpdate)
print
"=" * 80

# Update all tags
successCount = 0
errorCount = 0

for config in tagConfigsToUpdate:
    try:
        # Read the full tag configuration first
        tagConfig = system.tag.getConfiguration(config["tagPath"], False)[0]

        # Update only the engHigh property
        tagConfig['engHigh'] = config["engHigh"]

        # Extract the parent path and tag name
        pathParts = config["tagPath"].rsplit('/', 1)
        if len(pathParts) == 2:
            basePath = pathParts[0]
            tagConfig['name'] = pathParts[1]
        else:
            basePath = ""
            tagConfig['name'] = config["tagPath"]

        # Write the configuration back using the parent path as base
        result = system.tag.configure(basePath, [tagConfig], "o")

        if result and len(result) > 0:
            if str(result[0].getName()) == "Good":
                successCount += 1
            else:
                errorCount += 1
                print
                "Failed to update: %s - %s" % (config["tagPath"], str(result[0]))
        else:
            successCount += 1

    except Exception as e:
        errorCount += 1
        print
        "Error updating %s: %s" % (config["tagPath"], str(e))

# Print summary
print
"\n" + "=" * 80
print
"Update Complete!"
print
"Successfully updated: %d tags" % successCount
print
"Errors: %d tags" % errorCount
print
"=" * 80
