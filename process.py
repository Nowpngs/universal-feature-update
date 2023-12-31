from universal_feature_update import UniversalUpdateFeature

# process variables
# input path of the destination project
destination_project_path = ""

# input path of ssh key for the destination project (cd ~/.ssh/)
ssh_key_path = ""

# input feature name under the feature_xlsx directory in destination project folder
feature_name = "1.0.0-example_feature"


# run the process
UniversalUpdateFeature(
    destination_project_path=destination_project_path,
    ssh_key_path=ssh_key_path,
    feature_name=feature_name,
).process()
