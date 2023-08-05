import time
from datetime import datetime
import pandas as pd

from mwfeatureserving import config
from mwfeatureserving.mw_feature_store import MwFeatureStore
from mwfeatureserving.util import common_util
from mwfeatureserving.util import requests_util


def get_fv_detail(mwfs: MwFeatureStore, fg_name, fg_version):
    params = {
        "fgName": fg_name,
        "fgVersion": fg_version
    }
    return requests_util.get(mwfs.api_base_url + config.GET_FV_DETAIL_BY_FG_FV, params=params, auth_key=mwfs.auth_key)


def get_feature_groups_for_exp_id_itr(mwfs: MwFeatureStore, experiment_name: str, experiment_iteration_num: int):
    params = {
        "experimentName": experiment_name,
        "experimentIterationNo": experiment_iteration_num
    }
    return requests_util.get(mwfs.api_base_url + config.GET_FG_BY_EXP_ITR, params, auth_key=mwfs.auth_key)


def create_fv_with_gen_num(mwfs: MwFeatureStore, experiment_name: str, experiment_iteration_num: int,
                           feature_group_name: str,
                           feature_group_version: str, temp_fv_name: str):
    params = {
        "experimentName": experiment_name,
        "experimentIterationNo": experiment_iteration_num,
        "featureGroupName": feature_group_name,
        "featureGroupVersion": feature_group_version,
        "featureViewName": str(temp_fv_name)
    }
    return requests_util.post(mwfs.api_base_url + config.CREATE_FV_WITH_GEN_NUM, params, auth_key=mwfs.auth_key)


def get_repo_config_from_api(feast_wrapper_api_base,
                             config_api_path, auth_key=None):
    return requests_util.get(feast_wrapper_api_base + config_api_path, auth_key=auth_key)


def get_data_for_iteration(mwfs: MwFeatureStore, experiment_name: str, experiment_iteration_num: int,
                           feature_group_name: str,
                           feature_group_version: str, primary_keys: pd.core.frame.DataFrame = None):
    _tempFvName = time.time_ns()

    resp = create_fv_with_gen_num(mwfs, experiment_name, experiment_iteration_num, feature_group_name,
                                  feature_group_version, _tempFvName)

    _features = resp["features"]
    _fvName = resp["featureViewName"]
    _pks = resp["primaryKeys"]

    _featuresList = common_util.get_features_list(fv_name=_fvName, features=_features)

    _entityDf = primary_keys if primary_keys is not None else (
            "SELECT distinct " + common_util.get_primary_keys_str(_pks) + " FROM " + mwfs.spectrum_schema + ".fs_" + _fvName)

    _histFeaturesDf = mwfs.get_feature_store().get_historical_features(
        features=_featuresList,
        entity_df=_entityDf
    ).to_df()

    # Delete the temp Feature View
    delete_temp_fv(mwfs=mwfs, temp_fv_name=_fvName)

    return _histFeaturesDf


def delete_temp_fv(mwfs: MwFeatureStore, temp_fv_name: str):
    params = {
        "featureViewName": str(temp_fv_name)
    }
    return requests_util.delete(mwfs.api_base_url + config.GET_FV_DETAIL_BY_FG_FV, params, auth_key=mwfs.auth_key)
    pass


def create_fv_for_date_range(mwfs: MwFeatureStore, feature_group_name: str, feature_group_version: str,
                             start_date: datetime, end_date: datetime):
    params = {
        "feature_group_name": feature_group_name,
        "feature_group_version": feature_group_version,
        "start_date": start_date.strftime("%Y-%m-%d %H:%M:%S.%f"),
        "end_date": end_date.strftime("%Y-%m-%d %H:%M:%S.%f")
    }
    # print(params)
    url = mwfs.api_base_url + config.CREATE_FV_FOR_DATE_RANGE

    return requests_util.post(url, params, auth_key=mwfs.auth_key)


def get_data_of_feature_group_for_date_range(mwfs: MwFeatureStore, feature_group_name: str, feature_group_version: str,
                                             start_date: datetime, end_date: datetime,
                                             primary_keys: pd.DataFrame = None):
    resp = create_fv_for_date_range(mwfs, feature_group_name, feature_group_version, start_date, end_date)

    _features = resp["features"]
    _fvNames = resp["featureViewNames"]
    _pks = resp["primaryKeys"]

    union = pd.DataFrame()
    for _fvName in _fvNames:
        _featuresList = common_util.get_fv_features(fv_name=_fvName, features=_features)

        _entityDf = primary_keys if primary_keys is not None else (
                "SELECT distinct " + common_util.get_primary_keys_str(_pks) + " FROM " + mwfs.spectrum_schema + ".fs_" + _fvName)

        _histFeaturesDf = mwfs.get_feature_store().get_historical_features(
            features=_featuresList,
            entity_df=_entityDf
        ).to_df().drop_duplicates()

        # print("##################################")
        # print("##################################")
        # print("_histFeaturesDf - " + _fvName)
        # print(_histFeaturesDf)
        # print(_histFeaturesDf.to_dict('r'))

        union = pd.concat([union, _histFeaturesDf], ignore_index=True)

        # print("##################################")
        # print("##################################")
        # print("union - ")
        # print(union)
        # print(union.to_dict('r'))

        # Delete the temp Feature View
        delete_temp_fv(mwfs=mwfs, temp_fv_name=_fvName)

    return union
