import system
import time

# ============================================================
# LOGGER
# ============================================================
logger = system.util.getLogger(
    "ActivePipelineUpdater"
)

def log(msg):

    logger.warn(str(msg))
    print str(msg)

# ============================================================
# CONFIG
# ============================================================
base_folder = "[default]CowPleasant_Tags"

new_pipeline = (
    "Backend/RemoteNotify"
)

# ============================================================
# TAG LIST
# ============================================================
tagPaths = [
    "ESD_STA",
    "ESD_DG",
    "AT601_HH",
    "AT901_H2S_HH",
    "AT901_H2S_OOR",
    "AT901_LEL_HH",
    "AT901_LEL_HHH",
    "AT901_LEL_OOR",
    "AT902_H2S_HH",
    "AT902_H2S_OOR",
    "AT902_LEL_HH",
    "AT902_LEL_HHH",
    "AT902_LEL_OOR",
    "AT904_LEL_HH",
    "AT904_LEL_HHH",
    "AT904_LEL_OOR",
    "AT602_H2S_HH",
    "LIT201_LL",
    "LIT201_LP",
    "LIT201_HH",
    "LIT301_LLL",
    "LIT301_LP",
    "LIT301_HHH",
    "LIT401_LLL",
    "LIT401_LP",
    "LIT401_OOR",
    "LIT601_LL",
    "LIT601_OOR",
    "PT601_LL",
    "PT601_HH",
    "PT601_OOR",
    "PT602_LL",
    "PT602_HH",
    "PT602_OOR",
    "PT901_LL",
    "PT901_OOR",
    "TT301_LL",
    "TT301_HH",
    "CO102",
    "SD102",
    "HS102",
    "HS103",
    "GHT603_PR_OP_STS",
    "GLT603_VR_OP_STS",
    "HS201",
    "HS301",
    "LSHH201",
    "LSHH302",
    "LSHH401",
    "LSHH501",
    "GHT601_PR_OP_STS",
    "GLT601_VR_OP_STS",
    "GHT602_PR_OP_STS",
    "GLT602_VR_OP_STS",
    "UP_0ULF10CQ001",
    "UP_0UCH10AC001"
]


# ============================================================
# UPDATE ALARM PIPELINES
# ============================================================
def update_pipeline(tag_name):

    try:

        # ====================================================
        # BUILD FULL TAG PATH
        # ====================================================
        tag_path = (
            base_folder +
            "/" +
            str(tag_name)
        )

        log("------------------------------------------------")
        log("Checking tag:")
        log(tag_path)

        # ====================================================
        # VERIFY TAG EXISTS
        # ====================================================
        if not system.tag.exists(tag_path):

            return False, "TAG NOT FOUND"

        # ====================================================
        # READ CONFIGURATION
        # ====================================================
        config = system.tag.getConfiguration(
            tag_path,
            False
        )

        if not config:

            return False, "NO CONFIGURATION"

        tagConfig = config[0]

        # ====================================================
        # CHECK ALARMS
        # ====================================================
        alarms = tagConfig.get(
            "alarms",
            []
        )

        if len(alarms) == 0:

            return False, "NO ALARMS"

        log("Alarm count: %d" % len(alarms))

        # ====================================================
        # UPDATE ACTIVE PIPELINES
        # ====================================================
        updatedCount = 0

        for alarm in alarms:

            try:

                alarmName = alarm.get(
                    "name",
                    "UnnamedAlarm"
                )

                oldPipeline = alarm.get(
                    "activePipeline",
                    ""
                )

                log(
                    "Alarm: %s"
                    % alarmName
                )

                log(
                    "Old Pipeline: %s"
                    % oldPipeline
                )

                #
                # UPDATE ACTIVE PIPELINE
                #
                alarm["activePipeline"] = (
                    new_pipeline
                )

                log(
                    "New Pipeline: %s"
                    % new_pipeline
                )

                updatedCount += 1

            except Exception as e:

                log("FAILED TO UPDATE ALARM")
                log(str(e))

        # ====================================================
        # SAVE CONFIGURATION
        # ====================================================
        result = system.tag.configure(

            basePath=base_folder,

            tags=[tagConfig],

            collisionPolicy="o"
        )

        log("CONFIGURE RESULT:")
        log(str(result))

        return True, (
            "UPDATED %d ALARM(S)"
            % updatedCount
        )

    except Exception as e:

        import traceback

        log("EXCEPTION:")
        log(str(e))
        log(traceback.format_exc())

        return False, str(e)

# ============================================================
# START
# ============================================================
log("====================================================")
log("STARTING ACTIVE PIPELINE UPDATE")
log("====================================================")

log("Target tag count: %d" % len(tagPaths))

successCount = 0
failCount = 0

# ============================================================
# PROCESS TAGS
# ============================================================
for tagName in tagPaths:

    success, msg = update_pipeline(
        tagName
    )

    if success:

        log("SUCCESS: %s" % msg)

        successCount += 1

    else:

        log("FAILED: %s" % msg)

        failCount += 1

    #
    # Small delay for gateway breathing room
    #
    time.sleep(0.25)

# ============================================================
# SUMMARY
# ============================================================
log("")
log("====================================================")
log("UPDATE COMPLETE")
log("====================================================")

log("Successful Updates : %d" % successCount)
log("Failed Updates     : %d" % failCount)
log("Total Processed    : %d" % len(tagPaths))