import system

# ============================================================
# OPC PATH VALIDATION SCRIPT
# ============================================================
#
# PURPOSE:
#   Searches recursively under:
#
#       [default]CowPleasant_Tags
#
#   For every tag name in tagNames.
#
#   For each matching tag:
#
#       1. Read the tag configuration.
#       2. Read opcItemPath.
#       3. Extract the text after the last "]".
#       4. Compare that value to the tag's actual name.
#
#   Example:
#
#       Tag Name:
#           HMI_DG1_FL_CY_SP
#
#       OPC Path:
#           ns=1;s=[CowPleasant_PLC]HMI_DG1_FL_CY_SP
#
#       Extracted OPC Name:
#           HMI_DG1_FL_CY_SP
#
#       Result:
#           PASS
#
#   Any mismatches are printed and logged.
#
# ============================================================

logger = system.util.getLogger("OPCPathValidation")

# ============================================================
# TAG LIST
# ============================================================

tagNames = [
    # Insert your tag names here
]

tagSet = set(tagNames)

# ============================================================
# STATISTICS
# ============================================================

stats = {
    "foldersVisited": 0,
    "tagsScanned": 0,
    "matchingTagsFound": 0,
    "mismatches": 0,
    "missingOpcPaths": 0,
    "errors": 0
}

# Keep track of every tag found so we can identify
# tags from the list that do not exist.
foundTags = set()

# ============================================================
# RECURSIVE BROWSE FUNCTION
# ============================================================

def browseFolder(path):

    stats["foldersVisited"] += 1

    logger.warn("")
    logger.warn("Browsing Folder: %s" % path)

    try:
        browseResults = system.tag.browse(path)

    except Exception as e:
        stats["errors"] += 1
        logger.error(
            "Browse failed for folder %s : %s"
            % (path, str(e))
        )
        return

    for result in browseResults.getResults():

        try:

            fullPath = str(result["fullPath"])
            name = str(result["name"])
            hasChildren = result.get("hasChildren", False)

            if hasChildren:
                browseFolder(fullPath)
                continue

            stats["tagsScanned"] += 1

            # Skip tags not in our validation list
            if name not in tagSet:
                continue

            foundTags.add(name)

            stats["matchingTagsFound"] += 1

            logger.warn(
                "FOUND MATCHING TAG: %s"
                % fullPath
            )

            print ""
            print "------------------------------------------------"
            print "FOUND TAG: %s" % name
            print "PATH     : %s" % fullPath

            # ==========================================
            # READ CONFIGURATION
            # ==========================================

            cfg = system.tag.getConfiguration(fullPath, False)

            if not cfg:

                stats["errors"] += 1

                logger.error(
                    "Unable to read configuration for %s"
                    % fullPath
                )

                print "ERROR: Unable to read configuration"

                continue

            cfg = cfg[0]

            opcPath = cfg.get("opcItemPath", "")

            print "OPC PATH : %s" % opcPath

            # ==========================================
            # OPC PATH CHECK
            # ==========================================

            if not opcPath:

                stats["missingOpcPaths"] += 1

                logger.warn(
                    "Missing OPC Path: %s"
                    % fullPath
                )

                print "RESULT   : MISSING OPC PATH"

                continue

            # Extract everything after the last ']'
            if "]" in opcPath:
                opcTagName = opcPath.split("]")[-1]
            else:
                opcTagName = opcPath

            print "EXPECTED : %s" % name
            print "ACTUAL   : %s" % opcTagName

            # ==========================================
            # COMPARISON
            # ==========================================

            if opcTagName != name:

                stats["mismatches"] += 1

                logger.error(
                    "OPC MISMATCH | Tag=%s | OPC=%s"
                    % (name, opcTagName)
                )

                print "RESULT   : FAILED"

            else:

                print "RESULT   : PASSED"

        except Exception as e:

            stats["errors"] += 1

            logger.error(
                "Exception processing tag %s : %s"
                % (fullPath, str(e))
            )

            print "ERROR: %s" % str(e)

# ============================================================
# SCRIPT START
# ============================================================

logger.warn("========================================")
logger.warn("OPC PATH VALIDATION STARTED")
logger.warn("========================================")

print ""
print "========================================"
print "OPC PATH VALIDATION STARTED"
print "========================================"

browseFolder("[default]CowPleasant_Tags")

# ============================================================
# TAGS NOT FOUND
# ============================================================

missingTags = sorted(list(tagSet - foundTags))

if missingTags:

    logger.warn("")
    logger.warn("TAGS NOT FOUND:")
    logger.warn("--------------------------------")

    print ""
    print "========================================"
    print "TAGS NOT FOUND"
    print "========================================"

    for tagName in missingTags:

        logger.warn(tagName)
        print tagName

# ============================================================
# SUMMARY
# ============================================================

print ""
print "========================================"
print "VALIDATION SUMMARY"
print "========================================"
print "Folders Visited : %d" % stats["foldersVisited"]
print "Tags Scanned    : %d" % stats["tagsScanned"]
print "Tags Found      : %d" % stats["matchingTagsFound"]
print "Mismatches      : %d" % stats["mismatches"]
print "Missing OPC     : %d" % stats["missingOpcPaths"]
print "Errors          : %d" % stats["errors"]

logger.warn("")
logger.warn("========================================")
logger.warn("VALIDATION SUMMARY")
logger.warn("========================================")
logger.warn("Folders Visited : %d" % stats["foldersVisited"])
logger.warn("Tags Scanned    : %d" % stats["tagsScanned"])
logger.warn("Tags Found      : %d" % stats["matchingTagsFound"])
logger.warn("Mismatches      : %d" % stats["mismatches"])
logger.warn("Missing OPC     : %d" % stats["missingOpcPaths"])
logger.warn("Errors          : %d" % stats["errors"])
logger.warn("========================================")