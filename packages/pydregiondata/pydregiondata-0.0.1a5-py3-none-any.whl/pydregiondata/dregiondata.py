import numpy as np
import xarray as xr
import pandas as pd
import os
from _parse_data import full_data_to_pandas

def get_description():  # получить описание хаарэя
    states2 = pd.DataFrame()
    path3 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_ext", "_data")
    for i in range(len([name for name in os.listdir(path3)])):
        states2 = pd.concat([states2, full_data_to_pandas('0000'+str(i))])
    return states2

def get_data(name):# получить  хаарэя
    _path = os.path.join(os.path.dirname(os.path.abspath(__file__))
                         , "_ext", "_data", name + '.nc')
    return xr.load_dataarray(_path)

def license(): # пользователю показывают лицензию
    """
    :return: the license notice the package is distributed under.
    """
    return """ 
        Copyright (c) 2022 Ekaterina Shvets
       pydregiondata package is Licensed under the Apache License, Version 2.0 (the "License");
       you may not use this file except in compliance with the License.
       You may obtain a copy of the License at
    
         http://www.apache.org/licenses/LICENSE-2.0
    
       Unless required by applicable law or agreed to in writing, software
       distributed under the License is distributed on an "AS IS" BASIS,
       WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
       See the License for the specific language governing permissions and
       limitations under the License.its license
       """


print(get_description())