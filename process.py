from universal_feature_update import UniversalUpdateFeature

# process variables
# input path of the destination project
destination_project_path = ""

# input path of ssh key (codium gitlab)
ssh_key_path = ""

# input feature name from the update_feature folder
feature_name = ""

# run the process
UniversalUpdateFeature(
    destination_project_path=destination_project_path,
    ssh_key_path=ssh_key_path,
    feature_name=feature_name,
)
