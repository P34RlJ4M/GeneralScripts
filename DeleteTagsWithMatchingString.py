# Script to delete tags ending with _FLT_TM in [default]GreenMeadows_Tags

def findAndDeleteTagsEndingWith(tagPath, suffix):
    """
    Recursively search for and delete tags ending with a specific suffix
    """
    deletedTags = []
    failedTags = []

    try:
        # Browse the tags at this path
        tags = system.tag.browse(tagPath, {'recursive': False})

        for tag in tags:
            tagName = str(tag['name'])
            fullPath = str(tag['fullPath'])
            tagType = str(tag['tagType'])

            # Check if this is a folder and recurse into it
            if tagType == 'Folder' or tagType == 'UdtInstance':
                # Recursively search in this folder/UDT
                deleted, failed = findAndDeleteTagsEndingWith(fullPath, suffix)
                deletedTags.extend(deleted)
                failedTags.extend(failed)

            # Check if tag name ends with the suffix
            if tagName.endswith(suffix):
                try:
                    # Delete the tag - pass as string in a list
                    system.tag.deleteTags([fullPath])
                    deletedTags.append(fullPath)
                    print
                    "DELETED: " + fullPath
                except Exception as e:
                    failedTags.append({'path': fullPath, 'error': str(e)})
                    print
                    "FAILED to delete " + fullPath + ": " + str(e)

    except Exception as e:
        print
        "Error browsing path " + str(tagPath) + ": " + str(e)

    return deletedTags, failedTags


# Main execution
print
"=" * 80
print
"WARNING: This script will DELETE all tags ending with '_FLT_TM'"
print
"=" * 80
print
""

# Set to True to proceed with deletion
CONFIRM_DELETE = True

if not CONFIRM_DELETE:
    print
    "SAFETY CHECK: Set CONFIRM_DELETE = True to proceed with deletion"
    print
    "Script aborted - no tags were deleted"
else:
    print
    "Searching and deleting tags ending with '_FLT_TM' in [default]GreenMeadows_Tags..."
    print
    ""

    # Search and delete starting from the root of the tag provider
    basePath = "[default]GreenMeadows_Tags"
    deletedTags, failedTags = findAndDeleteTagsEndingWith(basePath, "_FLT_TM")

    # Display summary
    print
    ""
    print
    "=" * 80
    print
    "DELETION SUMMARY"
    print
    "=" * 80

    if deletedTags:
        print
        "Successfully deleted " + str(len(deletedTags)) + " tag(s):"
        for i, tagPath in enumerate(deletedTags, 1):
            print
            "  " + str(i) + ". " + tagPath
    else:
        print
        "No tags were deleted"

    if failedTags:
        print
        ""
        print
        "Failed to delete " + str(len(failedTags)) + " tag(s):"
        for i, item in enumerate(failedTags, 1):
            print
            "  " + str(i) + ". " + item['path']
            print
            "     Error: " + item['error']

    print
    ""
    print
    "=" * 80
    print
    "Deletion complete!"
    print
    "=" * 80