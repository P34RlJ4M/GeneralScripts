import system

# ============================================================
# LOGGER
# ============================================================
logger = system.util.getLogger(
    "CowPleasantActivePipelineAudit"
)

def log(msg):

    logger.warn(str(msg))
    print str(msg)

# ============================================================
# CONFIG
# ============================================================
rootFolder = "[default]CowPleasant_Tags"

# ============================================================
# INSERT OPC TAG LIST HERE
# ============================================================
tagPaths = [
    "ns=1;s=[CowPleasant_Tags]ESD_STA",
    "ns=1;s=[CowPleasant_Tags]ESD_DG",
    "ns=1;s=[CowPleasant_Tags]AT601_HH",
    "ns=1;s=[CowPleasant_Tags]AT901_H2S_HH",
    "ns=1;s=[CowPleasant_Tags]AT901_H2S_OOR",
    "ns=1;s=[CowPleasant_Tags]AT901_LEL_HH",
    "ns=1;s=[CowPleasant_Tags]AT901_LEL_HHH",
    "ns=1;s=[CowPleasant_Tags]AT901_LEL_OOR",
    "ns=1;s=[CowPleasant_Tags]AT902_H2S_HH",
    "ns=1;s=[CowPleasant_Tags]AT902_H2S_OOR",
    "ns=1;s=[CowPleasant_Tags]AT902_LEL_HH",
    "ns=1;s=[CowPleasant_Tags]AT902_LEL_HHH",
    "ns=1;s=[CowPleasant_Tags]AT902_LEL_OOR",
    "ns=1;s=[CowPleasant_Tags]AT904_LEL_HH",
    "ns=1;s=[CowPleasant_Tags]AT904_LEL_HHH",
    "ns=1;s=[CowPleasant_Tags]AT904_LEL_OOR",
    "ns=1;s=[CowPleasant_Tags]AT602_H2S_HH",
    "ns=1;s=[CowPleasant_Tags]LIT201_LL",
    "ns=1;s=[CowPleasant_Tags]LIT201_LP",
    "ns=1;s=[CowPleasant_Tags]LIT201_HH",
    "ns=1;s=[CowPleasant_Tags]LIT301_LLL",
    "ns=1;s=[CowPleasant_Tags]LIT301_LP",
    "ns=1;s=[CowPleasant_Tags]LIT301_HHH",
    "ns=1;s=[CowPleasant_Tags]LIT401_LLL",
    "ns=1;s=[CowPleasant_Tags]LIT401_LP",
    "ns=1;s=[CowPleasant_Tags]LIT401_OOR",
    "ns=1;s=[CowPleasant_Tags]LIT601_LL",
    "ns=1;s=[CowPleasant_Tags]LIT601_OOR",
    "ns=1;s=[CowPleasant_Tags]PT601_LL",
    "ns=1;s=[CowPleasant_Tags]PT601_HH",
    "ns=1;s=[CowPleasant_Tags]PT601_OOR",
    "ns=1;s=[CowPleasant_Tags]PT602_LL",
    "ns=1;s=[CowPleasant_Tags]PT602_HH",
    "ns=1;s=[CowPleasant_Tags]PT602_OOR",
    "ns=1;s=[CowPleasant_Tags]PT901_LL",
    "ns=1;s=[CowPleasant_Tags]PT901_OOR",
    "ns=1;s=[CowPleasant_Tags]TT301_LL",
    "ns=1;s=[CowPleasant_Tags]TT301_HH",
    "ns=1;s=[CowPleasant_Tags]CO102",
    "ns=1;s=[CowPleasant_Tags]SD102",
    "ns=1;s=[CowPleasant_Tags]HS102",
    "ns=1;s=[CowPleasant_Tags]HS103",
    "ns=1;s=[CowPleasant_Tags]GHT603_PR_OP_STS",
    "ns=1;s=[CowPleasant_Tags]GLT603_VR_OP_STS",
    "ns=1;s=[CowPleasant_Tags]HS201",
    "ns=1;s=[CowPleasant_Tags]HS301",
    "ns=1;s=[CowPleasant_Tags]LSHH201",
    "ns=1;s=[CowPleasant_Tags]LSHH302",
    "ns=1;s=[CowPleasant_Tags]LSHH401",
    "ns=1;s=[CowPleasant_Tags]LSHH501",
    "ns=1;s=[CowPleasant_Tags]GHT601_PR_OP_STS",
    "ns=1;s=[CowPleasant_Tags]GLT601_VR_OP_STS",
    "ns=1;s=[CowPleasant_Tags]GHT602_PR_OP_STS",
    "ns=1;s=[CowPleasant_Tags]GLT602_VR_OP_STS",
    "ns=1;s=[CowPleasant_Tags]UP_0ULF10CQ001",
    "ns=1;s=[CowPleasant_Tags]UP_0UCH10AC001"
]


# ============================================================
# START
# ============================================================
log("====================================================")
log("STARTING ACTIVE PIPELINE AUDIT")
log("====================================================")

print ""
print "Tag Name,Exists,Alarm Name,Priority,Active Pipeline"
print "------------------------------------------------------------------------"

# ============================================================
# PROCESS TAGS
# ============================================================
for opcItem in tagPaths:

    try:

        # ====================================================
        # EXTRACT TAG NAME
        # ====================================================
        tagName = opcItem.split("]")[-1]

        # ====================================================
        # BUILD IGNITION TAG PATH
        # ====================================================
        tagPath = rootFolder + "/" + tagName

        # ====================================================
        # CHECK IF TAG EXISTS
        # ====================================================
        exists = system.tag.exists(tagPath)

        if not exists:

            print "%s,NOT FOUND,N/A,N/A,N/A" % tagName
            continue

        # ====================================================
        # GET TAG CONFIGURATION
        # ====================================================
        config = system.tag.getConfiguration(
            tagPath,
            False
        )

        if not config:

            print "%s,FOUND,NO CONFIG,N/A,N/A" % tagName
            continue

        tagConfig = config[0]

        # ====================================================
        # GET ALARMS
        # ====================================================
        alarms = tagConfig.get(
            "alarms",
            []
        )

        if len(alarms) == 0:

            print "%s,FOUND,NO ALARMS,N/A,N/A" % tagName
            continue

        # ====================================================
        # PROCESS ALARMS
        # ====================================================
        for alarm in alarms:

            try:

                alarmName = alarm.get(
                    "name",
                    "UnnamedAlarm"
                )

                priority = alarm.get(
                    "priority",
                    "N/A"
                )

                #
                # ACTIVE PIPELINE
                #
                activePipeline = alarm.get(
                    "activePipeline",
                    "NO ACTIVE PIPELINE"
                )

                if activePipeline == "":
                    activePipeline = "NO ACTIVE PIPELINE"

                print "%s,FOUND,%s,%s,%s" % (
                    tagName,
                    alarmName,
                    priority,
                    activePipeline
                )

            except Exception as e:

                print "%s,FOUND,ERROR,%s,N/A" % (
                    tagName,
                    str(e)
                )

    except Exception as e:

        print "%s,ERROR,%s,N/A,N/A" % (
            opcItem,
            str(e)
        )

# ============================================================
# END
# ============================================================
log("====================================================")
log("ACTIVE PIPELINE AUDIT COMPLETE")
log("====================================================")