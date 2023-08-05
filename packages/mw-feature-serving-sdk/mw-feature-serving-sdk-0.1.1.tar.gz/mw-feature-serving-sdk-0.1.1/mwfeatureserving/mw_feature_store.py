import logging
from datetime import datetime

import pandas
from feast import FeatureStore

from mwfeatureserving import config
import mwfeatureserving.services.mwfs_api as mwfs_api
from mwfeatureserving.util import repo_config_util
from mwfeatureserving.util import requests_util


class MwFeatureStore:
    mwfs = None
    api_base_url = None
    repo_config = None
    workspace_id = None  # Stubbed variable for when we need workspace-id to interact with UI.
    auth_key = None
    spectrum_schema = None

    def __init__(self, mwfs_api_base_url=None,
                 auth_key=None, lazy=False):
        MwFeatureStore.__instance = self

        if mwfs_api_base_url is None or auth_key is None:
            raise Exception(
                "Mobilewalla Feature Store Base API URL and the corresponding Auth-Key are required. " +
                "Please login to Mobilewalla Feature Machine to get these details.")

        self.api_base_url = mwfs_api_base_url
        self.auth_key = auth_key

        if not lazy:
            self.get_feature_store()

    def get_repo_config_from_api(self):
        if self.repo_config is None:
            _repoConfig = mwfs_api.get_repo_config_from_api(feast_wrapper_api_base=self.api_base_url,
                                                            config_api_path=config.GET_REPO_CONFIG,
                                                            auth_key=self.auth_key)
            # logging.info("Created RepoConfig object: {}".format(_repoConfig))
            self.repo_config = repo_config_util.get_mwfs_repo_config(_repoConfig['repo'])
            self.spectrum_schema = _repoConfig['spectrum_schema']
        return self.repo_config

    def get_feature_store(self):
        if self.mwfs is None:
            if self.repo_config is None:
                self.mwfs = FeatureStore(config=self.get_repo_config_from_api())
            else:
                self.mwfs = FeatureStore(config=self.repo_config)
        return self.mwfs

    def get_feature_groups_for_iteration(self, experiment_name: str, experiment_iteration_num: int):
        return mwfs_api.get_feature_groups_for_exp_id_itr(self, experiment_name, experiment_iteration_num)

    def get_data_for_iteration(self, experiment_name: str, experiment_iteration_num: int, feature_group_name: str,
                               feature_group_version: str, primary_keys: pandas.core.frame.DataFrame):
        return mwfs_api.get_data_for_iteration(self, experiment_name, experiment_iteration_num,
                                               feature_group_name, feature_group_version,
                                               primary_keys)

    def get_data_of_feature_group_for_date_range(self, feature_group_name: str, feature_group_version: str,
                                                 start_date: datetime, end_date: datetime,
                                                 primary_keys: pandas.core.frame.DataFrame = None):

        return mwfs_api.get_data_of_feature_group_for_date_range(self, feature_group_name, feature_group_version,
                                                                 start_date, end_date, primary_keys)

    def get_online_features_of_feature_group(self, feature_group_name, feature_group_version, primary_keys):
        params = {
            "fgName": feature_group_name,
            "fgVersion": feature_group_version
        }
        resp = requests_util.get(self.api_base_url + config.GET_FV_DETAIL_BY_FG_FV, params, auth_key=self.auth_key)
        _fv_name = resp["featureViewName"]
        _features = resp["features"]

        featuresList = []
        for i in range(len(_features)):
            featureName = _features[i]["name"]
            featuresList.append(_fv_name + ":" + featureName)

        # print(_fv_name)
        # print(featuresList)
        #
        # print("Retrieving data from online store...")
        # feature store
        fs = FeatureStore(config=self.repo_config)

        online_features = fs.get_online_features(
            features=featuresList, entity_rows=primary_keys.to_dict('records'),
        )

        return online_features.to_df()
