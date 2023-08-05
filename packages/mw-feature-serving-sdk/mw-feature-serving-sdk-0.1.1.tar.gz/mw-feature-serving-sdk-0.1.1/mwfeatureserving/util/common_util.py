from typing import Dict


def get_features_list(fv_name: str, features: Dict):
    _featuresList = []
    for i in range(len(features)):
        _featureName = features[i]["name"]
        _featuresList.append(fv_name + ":" + _featureName)

    return _featuresList

def get_fv_features(fv_name: str, features: list):
    _featuresList = []
    for _featureName in features:
        _featuresList.append(fv_name + ":" + _featureName)

    return _featuresList


def get_primary_keys_str(primary_keys: list):
    _primaryKeysList = []
    _primaryKeysList.extend(primary_keys)
    _primaryKeysList.append("event_timestamp")
    _pkList = ", ".join(_primaryKeysList)
    return _pkList
