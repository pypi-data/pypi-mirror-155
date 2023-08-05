from feast.repo_config import RepoConfig


def get_mwfs_repo_config(repo_config: dict):
    _repoConfigParsed = RepoConfig.parse_obj(repo_config)
    return _repoConfigParsed


# def get_mwfs_repo_config_as_dict(repo_config):
#     _mwfsConfig = {}
#
#     for key, value in os.environ.items():
#         if key.startswith("mwfs_config_"):
#             path = key.split("__")
#
#             ref = _mwfsConfig
#             for part in path[1:-1]:
#                 ref[part] = part in ref and ref[part] or {}
#                 ref = ref[part]
#             ref[path[-1]] = value  # take the last part of key and set the value
#
#     return _mwfsConfig
