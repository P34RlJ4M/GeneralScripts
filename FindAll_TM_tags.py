# Script to find all tags ending with _TM in [default]Papas_Tags folder

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
"%-50s %-15s %-15s" % ("Tag Name", "engLow", "engHigh")
print
"-" * 80

# Get detailed information for each matching tag
for tagPath in matchingTagPaths:
    try:
        # Read the tag configuration as JSON
        tagConfigs = system.tag.readBlocking([tagPath + ".engLow", tagPath + ".engHigh"])

        engLow = tagConfigs[0].value if tagConfigs[0].quality.isGood() else 'N/A'
        engHigh = tagConfigs[1].value if tagConfigs[1].quality.isGood() else 'N/A'

        # Print formatted output
        print
        "%-50s %-15s %-15s" % (tagPath, str(engLow), str(engHigh))

    except Exception as e:
        print
        "%-50s ERROR: %s" % (tagPath, str(e))

# Return the list if you need to use it further
# return matchingTagPaths