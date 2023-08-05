# Mobilewalla Feature Serving SDK

## Getting started

```python
from mwfeatureserving import MwFeatureStore

mwfs = MwFeatureStore(mwfs_api_base_url='Mobilewalla Feature Machine Base URL', 
                      auth_key='Mobilewalla Feature Machine Auth Key')

# Example data retrieval call: 
online_features = mwfs.get_online_features_of_feature_group('Feature Group Name', 'Feature Group Version')
```

