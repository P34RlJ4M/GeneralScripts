# Update history provider to Historian for all tags in tag_paths
# Script Console

tag_paths = [
    # paste your tag_paths list here
]

new_provider = "Historian"

success_count = 0
skipped_count = 0
error_count   = 0

for tag_path in tag_paths:
    try:
        # Split full path into parent and tag name
        last_slash = tag_path.rfind("/")
        parent_path = tag_path[:last_slash]
        tag_name    = tag_path[last_slash + 1:]

        configs = system.tag.getConfiguration(tag_path, False)
        if not configs:
            print("SKIP (no config): " + tag_path)
            skipped_count += 1
            continue

        cfg = configs[0]

        if not cfg.get('historyEnabled', False):
            print("SKIP (history not enabled): " + tag_path)
            skipped_count += 1
            continue

        cfg['name']            = tag_name
        cfg['historyProvider'] = new_provider

        system.tag.configure(parent_path, [cfg], "m")
        print("OK: " + tag_path)
        success_count += 1

    except Exception as e:
        print("ERROR: {} - {}".format(tag_path, str(e)))
        error_count += 1

print("")
print("=" * 50)
print("Done.  Success: {}  Skipped: {}  Errors: {}".format(success_count, skipped_count, error_count))