# Ignition Script: Update Alarm Pipelines for Specific Tags
import system
import time

# Target tag names (complete list)
target_tags = [
    'ESD_STA', 'ESD_DG',
    'AT901_H2S_HH', 'AT901_H2S_OOR', 'AT901_LEL_HH', 'AT901_LEL_HHH', 'AT901_LEL_OOR',
    'AT902_H2S_HH', 'AT902_H2S_OOR', 'AT902_LEL_HH', 'AT902_LEL_HHH', 'AT902_LEL_OOR',
    'AT903_H2S_HH', 'AT903_H2S_OOR', 'AT903_LEL_HH', 'AT903_LEL_HHH', 'AT903_LEL_OOR',
    'AT904_HH', 'AT904_HHH', 'AT904_OOR',
    'LIT201_LL', 'LIT201_LP', 'LIT201_HH',
    'LIT301_LLL', 'LIT301_LP', 'LIT301_HHH',
    'LIT302_LLL', 'LIT302_LP', 'LIT302_HHH',
    'LT502_LL', 'LT502_HH',
    'PT601_LL', 'PT601_HH', 'PT601_OOR',
    'PT602_LL', 'PT602_HH', 'PT602_OOR',
    'PT901_LL', 'PT901_OOR',
    'TT301_LL', 'TT301_HH', 'TT302_LL', 'TT302_HH',
    'AT601_HH', 'AT602_H2S_HH',
    'LIT401_LLL', 'LIT401_LP', 'LIT401_OOR',
    'LIT601_LL', 'LIT601_OOR',
    'PIT601_LLL', 'PIT601_LL', 'PIT601_OOR',
    'PIT602_LLL', 'PIT602_LL', 'PIT602_OOR',
    'PT603_LL', 'PT603_HH', 'PT603_OOR',
    'HS102', 'HS103', 'CO102', 'SD102',
    'V601_PR_OP_STS', 'V602_PR_OP_STS', 'V601_VR_OP_STS', 'V602_VR_OP_STS',
    'HS201', 'HS202', 'HS301',
    'LSHH201', 'LSHH302', 'LSHH304', 'LSHH401', 'LSHH501', 'LSHH507', 'LSHH562',
    'V603_PR_OP_STS', 'V604_PR_OP_STS', 'V603_VR_OP_STS', 'V604_VR_OP_STS',
    'V605_PR_OP_STS', 'V605_VR_OP_STS',
    'V90X_OFF',
    'DS1_MS1_H2S_HH', 'DS2_MS1_H2S_HH',
    'UP_0ULF10CQ001', 'UP_0UCH10AC001',
    'MR_HHV_LL', 'MR_HHV_HH', 'MR_CO2_HH', 'MR_O2_HH', 'MR_H2S_HH', 'MR_H2O_HH', 'MR_OUT_TEMP_HH'
]

base_folder = '[Schaendorf]Schaendorf_Tags'
new_pipeline = 'Schaendorf/Commissioning_Pipeline'


# Recursive tag search with exact name match
def find_tags(folder, targets, depth=0):
    if depth > 10:
        return {}
    found = {}
    try:
        results = system.tag.browse(folder, {"recursive": False}).getResults()
        for result in results:
            name = result['name']
            path = str(result['fullPath'])  # CONVERT TO STRING HERE
            tag_type = result['tagType']
            if name in targets:
                found[path] = name
            if tag_type in ['Folder', 'UdtInstance']:
                sub = find_tags(path, targets, depth + 1)
                found.update(sub)
    except Exception as e:
        print("Browse failed: {}".format(e))
    return found


# Update alarm pipelines for a single tag
def update_pipeline(tag_path):
    try:
        tag_path_str = str(tag_path)

        config = system.tag.getConfiguration(tag_path_str)
        if not config:
            return False, "No configuration found"

        alarms = config[0].get('alarms', [])
        if not alarms:
            return False, "No alarms to update"

        for alarm in alarms:
            alarm['activePipeline'] = new_pipeline

        base_path = tag_path_str.rsplit('/', 1)[0]

        result = system.tag.configure(
            basePath=base_path,
            tags=[config[0]],
            collisionPolicy='o'
        )

        return True, "Updated {} alarm(s)".format(len(alarms))

    except Exception as e:
        return False, str(e)


# Main execution
print("Starting alarm pipeline update for {} tags...".format(len(target_tags)))
found = find_tags(base_folder, target_tags)
print("Found {} matching tags.\n".format(len(found)))

success_count = 0
fail_count = 0

for path in sorted(found.keys()):
    print("Updating tag: {}".format(path))
    success, msg = update_pipeline(path)
    if success:
        print("  ✓ SUCCESS: {}".format(msg))
        success_count += 1
    else:
        print("  ✗ FAILED: {}".format(msg))
        fail_count += 1
    time.sleep(0.25)  # Optional delay for gateway breathing room

print("\nSUMMARY:")
print("  Updated: {}".format(success_count))
print("  Failed: {}".format(fail_count))
print("  Not Found: {}".format(len(target_tags) - len(found)))