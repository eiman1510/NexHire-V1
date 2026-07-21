import importlib

features = {
    "candidate:apply_job": "v1",
    "candidate:candidate_info": "v1",
    "candidate:job_handler": "v1",
    "candidate:signup": "v1",
    "hr:application_handler": "v1",
    "hr:job_handler": "v1",
    "hr:signup": "v1",
    "login": "v1",
}


def load_function(feature_key, module_name, function_name):
    version = features.get(feature_key)

    if not version:
        raise ValueError(f"No version configured for {feature_key}")

    if feature_key == "login":
        package_name = "features.login"
    else:
        section, feature = feature_key.split(":", 1)
        package_name = f"features.{section}.{feature}"

    module = importlib.import_module(
        f".{version}.{module_name}",
        package=package_name
    )

    return getattr(module, function_name)