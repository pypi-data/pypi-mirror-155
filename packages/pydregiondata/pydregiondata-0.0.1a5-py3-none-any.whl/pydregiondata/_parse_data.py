import numpy as np
import xarray as xr
import pandas as pd
import os

def full_data_to_pandas(file_name):
    _path = os.path.join(os.path.dirname(os.path.abspath(__file__))
                         , "_ext", "_data", file_name + '.nc')
    dregion_xr = xr.load_dataarray(_path)
    states1 = pd.DataFrame()

    # добавление в словарь метода проведения
    messurment_dict = {file_name: dregion_xr.attrs['messurment']}
    messurment1 = pd.Series(messurment_dict)

    # добавление в словарь атрибута коцентрации
    units_dict = {file_name: dregion_xr.attrs['units']}
    units1 = pd.Series(units_dict)

    # добавление в словарь места проведения
    place_dict = {file_name: dregion_xr.attrs['place']}
    place1 = pd.Series(place_dict)

    # добавление в словарь времени проведения
    time_dict = {file_name: dregion_xr.time.values}
    time1 = pd.Series(time_dict)

    # добавление в словарь атрибутов времени проведения
    time_units_dict = {file_name: dregion_xr.attrs['time_units']}
    time1_units = pd.Series(time_units_dict)

    # добавление в словарь широты
    lat_dict = {file_name: dregion_xr.lat.values}
    lat1 = pd.Series(lat_dict)

    # добавление в словарь атрибутов широты
    lat_units_dict = {file_name: dregion_xr.attrs['lat_units']}
    lat1_units = pd.Series(lat_units_dict)

    # добавление в словарь долготы
    long_dict = {file_name: dregion_xr.long.values}
    long1 = pd.Series(long_dict)

    # добавление в словарь атрибутов долготы
    long_units_dict = {file_name: dregion_xr.attrs['long_units']}
    long1_units = pd.Series(long_units_dict)

    # добавление в словарь максимальной высоты
    alt_max_dict = {file_name: max(dregion_xr.alt.values)}
    alt1_max = pd.Series(alt_max_dict)

    # добавление в словарь минимальной высоты
    alt_min_dict = {file_name: min(dregion_xr.alt.values)}
    alt1_min = pd.Series(alt_min_dict)

    # добавление в словарь атрибутов высоты
    alt_units_dict = {file_name: dregion_xr.attrs['alt_units']}
    alt1_units = pd.Series(alt_units_dict)

    # добавление в словарь особенностей проведения
    special_dict = {file_name: dregion_xr.attrs['special']}
    special1 = pd.Series(special_dict)

    new_row = pd.DataFrame(
            {'messurment': messurment1, 'units': units1, 'place': place1, 'time': time1, 'time units': time1_units,
             'longtitude': long1, 'longtitude_units': long1_units, 'latitude': lat1, 'latitude_units': lat1_units,
             'alt_max': alt1_max, 'alt_min': alt1_min, 'alt_units': alt1_units, 'special': special1})
    states1 = pd.concat([states1,new_row])
    return states1

def full_data_from_csv(file_name):

    _path = os.path.join(os.path.dirname(os.path.abspath(__file__))
                         , "_ext", "_data_csv", file_name + '.csv')

    f1 = open(_path, 'r').readlines()
    a1 = []
    a2 = []

    for line in f1[1:]:
        fields = line.split(';')
        a1.append(fields[0])
        a2.append(fields[1])

    for line in f1[:1]:
        fields = line.split(';')
        messurment = fields[0]
        time_0 = fields[1]
        time_units = fields[2]
        place = fields[3]
        coords_unit = fields[4]
        lat_0 = fields[5]
        lat_units = fields[6]
        long_0 = fields[7]
        long_units = fields[8]
        alt_units = fields[9]
        units = fields[10]
        special_0 = fields[11]
        description = fields[12]

    alt = list([float(_) for _ in a1])

    param = list([float(_) for _ in a2])

    values = np.full(shape=(1, 1, 1, len(alt))
                     , fill_value=np.nan
                     , dtype=np.float64, order='F')

    time = [time_0]
    long = [long_0]
    lat = [lat_0]

    for i in range(len(param)):
        _ = float(param[i])
        values[0, 0, 0, i] = _

    dregion_xr = xr.DataArray(data=values
                              , coords=[time, long, lat, alt]
                              , dims=['time', 'long', 'lat', 'alt']
                              )

    dregion_xr.attrs['standard_name'] = 'D-region electron density file: ' + file_name
    dregion_xr.attrs['long_name'] = description
    dregion_xr.attrs['place'] = place
    dregion_xr.attrs['messurment'] = messurment
    dregion_xr.attrs['special'] = special_0
    dregion_xr.attrs['units'] = units
    dregion_xr.attrs['time_units'] = 'Data format d.m.yyyy h:m:s, ' + time_units
    dregion_xr.attrs['coord_units'] = 'Type of coordinates, ' + coords_unit
    dregion_xr.attrs['lat_units'] = 'latitude, deg. ' + lat_units
    dregion_xr.attrs['long_units'] = 'longtitude, deg.' + long_units
    dregion_xr.attrs['alt_units'] = "altitude above the Earth's surface, " + alt_units

    _path_save = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_ext", "_data", file_name + '.nc')
    dregion_xr.to_netcdf(path=_path_save)