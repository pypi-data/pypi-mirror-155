import requests
import pandas as pd
import dask.dataframe as dd
from .base import bucket_name, Base
from .dataset import DatasetManager
import io
import time

def append_slash(txt):
    if txt[-1] != '/':
        txt += '/'
    return txt

class DataNode(DatasetManager):
    def write(self, ddf=None, df=None, directory=None, name=None, description="", replace=None, profiling=False, **kwargs):
        if (ddf is None) and (df is None):
            raise Exception(f"Please input ddf(dask dataframe) or df(pandas dataframe), got {type(ddf) or type(df)}")
        if (type(ddf) != dd.DataFrame) and (type(df) != pd.DataFrame):
            raise Exception("Invalid type expect ddf(dask dataframe) or df(pandas dataframe)")
        if name == None or type(name) != str:
            raise Exception(f"Please input data name, but got {type(name)}")
        if description=="":
            description = f"data {name}"
            
        name = f'{name}.parquet'
        replace = self._check_fileExists(directory, name)
        
        _res = requests.post(f'{self._discovery_api}/file/', headers=self._jwt_header,
                                json={
                                    "name": name,
                                    "description": description,
                                    "directory": directory,
                                    "is_use": False,
                                    "replace": replace
                                }
                            )
        if _res.status_code != 201:
            raise Exception(f"can not create directory in discovery {_res.json()}")
        meta = _res.json()
        _df_ddf = ddf if type(ddf) == dd.DataFrame else df
        _df_ddf.to_parquet(f"s3://{bucket_name}/{meta['key']}",
            storage_options=self._storage_options,
            **kwargs
        )
        
        # create profiling & data dict
        if profiling:
            for _ in range(5):
                _res = requests.get(f"{self._discovery_api}/file/{meta['id']}/", headers=self._jwt_header)
                if _res.status_code != 200:
                    time.sleep(2)
                else:
                    break
            requests.get(f"{self._discovery_api}/file/{meta['id']}/createDatadict/", headers=self._jwt_header)
            requests.get(f"{self._discovery_api}/file/{meta['id']}/createProfileling/", headers=self._jwt_header)
            
        return {
            'sucess': True,
            'file_id': meta['id'],
            'path': meta['key']
        }
    
    def get_file(self, file_id=None):
        _res = requests.get(f"{self._discovery_api}/file/{file_id}/", headers=self._jwt_header)
        if _res.status_code != 200:
            txt = _res.json() if _res.status_code < 500 else " "
            raise Exception(f"Some thing wrong, {txt}")
        meta = _res.json()
        
        try:
            response = self.client.get_object(bucket_name=bucket_name, object_name=meta['s3_key'])
        except Exception as e:
            raise e
        else:
            return io.BytesIO(response.data)
        
    
    def read_ddf(self, file_id=None):
        _res = requests.get(f"{self._discovery_api}/file/{file_id}/", headers=self._jwt_header)
        if _res.status_code != 200:
            txt = _res.json() if _res.status_code < 500 else " "
            raise Exception(f"Some thing wrong, {txt}")
        meta = _res.json()
        meta.update({
            'key': append_slash(meta['s3_key'])
        })
        _f_type = meta['type']['name']
        if _f_type == "parquet":
            return dd.read_parquet(f"s3://{bucket_name}/{meta['key']}", storage_options=self._storage_options)
        elif _f_type == "csv":
            return dd.read_csv(f"s3://{bucket_name}/{meta['key']}", storage_options=self._storage_options)
        return Exception(f"Can not read file extension {_f_type}, support [parquet, csv]")
        
    def read_df(self, file_id=None):
        _res = requests.get(f"{self._discovery_api}/file/{file_id}/", headers=self._jwt_header)
        if _res.status_code != 200:
            txt = _res.json() if _res.status_code < 500 else " "
            raise Exception(f"Some thing wrong, {txt}")
        meta = _res.json()
        meta.update({
            'key': append_slash(meta['s3_key'])
        })
        _f_type = meta['type']['name']
        if _f_type == "parquet":
            return pd.read_parquet(f"s3://{bucket_name}/{meta['key']}", storage_options=self._storage_options)
        elif _f_type == "csv":
            return pd.read_csv(f"s3://{bucket_name}/{meta['key']}", storage_options=self._storage_options)
        return Exception(f"Can not read file extension {_f_type}, support [parquet, csv]")