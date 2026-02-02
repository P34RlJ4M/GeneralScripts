# Run this in the Script Console (Gateway scope)
import system

SOURCE_FOLDER = "[default]Carsada_Tags"
DEST_FOLDER   = "[default]BadTags"

def browse_all_tags(path):
    """Recursively gather all tag paths under a given folder."""
    tag_list = []
    try:
        results = system.tag.browse(path, {"recursive": False}).getResults()
        for result in results:
            full_path = str(result['fullPath'])
            tag_type = result['tagType']
            if tag_type == 'Folder':
                tag_list.extend(browse_all_tags(full_path))
            else:
                tag_list.append(full_path)
    except Exception as e:
        print("Browse failed at {}: {}".format(path, e))
    return tag_list

def move_bad_tags():
    bad_tags = []
    all_tags = browse_all_tags(SOURCE_FOLDER)
    print("Scanned {} tags under {}".format(len(all_tags), SOURCE_FOLDER))

    # Check tag qualities
    quality_results = system.tag.readBlocking(all_tags)
    for tag_path, tag_value in zip(all_tags, quality_results):
        if not tag_value.quality.isGood():
            bad_tags.append(tag_path)

    print("Found {} bad quality tags.".format(len(bad_tags)))

    # Move each bad tag
    for tag_path in bad_tags:
        try:
            config = system.tag.getConfiguration(tag_path, False)[0]
            tag_name = config['name']
            relative_path = tag_path.replace(SOURCE_FOLDER + "/", "")
            dest_path = "{}/{}".format(DEST_FOLDER, relative_path.rsplit('/', 1)[-1])

            # Make sure destination folder exists
            dest_folder = DEST_FOLDER
            system.tag.configure(dest_folder, [], "m")  # No-op to force folder creation if needed

            # Create tag in new location
            system.tag.configure(dest_folder, [config], collisionPolicy="o")
            print("Moved: {} → {}".format(tag_path, dest_path))

            # Delete original tag
            system.tag.removeTag(tag_path)

        except Exception as e:
            print("Failed to move {}: {}".format(tag_path, e))

# Run it
move_bad_tags()
