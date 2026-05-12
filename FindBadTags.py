import system

# ============================================================
# LOGGER
# ============================================================
logger = system.util.getLogger("BadQualityScan")

def log(msg):
    logger.warn(msg)
    print msg

# ============================================================
# CONFIG
# ============================================================
rootPath = "[default]"

# ============================================================
# STORAGE
# ============================================================
badTags = []

# ============================================================
# RECURSIVE BROWSE FUNCTION
# ============================================================
def browseTags(path):

    try:

        results = system.tag.browse(path)

        for result in results.getResults():

            try:

                tagPath = str(result["fullPath"])
                hasChildren = result["hasChildren"]

                #
                # Recurse folders
                #
                if hasChildren:

                    browseTags(tagPath)

                else:

                    #
                    # Read quality
                    #
                    qv = system.tag.readBlocking(
                        [tagPath]
                    )[0]

                    quality = qv.quality

                    #
                    # Check quality
                    #
                    if not quality.isGood():

                        badTags.append({
                            "path": tagPath,
                            "quality": str(quality)
                        })

                        log("BAD QUALITY:")
                        log("Path    : %s" % tagPath)
                        log("Quality : %s" % quality)
                        log("-----------------------------------")

            except Exception as e:

                log("ERROR PROCESSING TAG:")
                log(str(result))
                log(str(e))

    except Exception as e:

        log("ERROR BROWSING:")
        log(path)
        log(str(e))

# ============================================================
# START
# ============================================================
log("===================================================")
log("STARTING BAD QUALITY SCAN")
log("===================================================")

browseTags(rootPath)

# ============================================================
# SUMMARY
# ============================================================
log("===================================================")
log("SCAN COMPLETE")
log("===================================================")

log("Bad quality tag count: %d" % len(badTags))

if len(badTags) == 0:

    log("No bad quality tags found.")

else:

    log("===================================================")
    log("BAD QUALITY TAGS")
    log("===================================================")

    for tag in badTags:

        print "%s , %s" % (
            tag["path"],
            tag["quality"]
        )
