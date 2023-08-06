from apafib.config import DATALINK, datasets
import pandas as pd
from sklearn.utils import Bunch

def fetch_apa_data(name, version, target_column, return_X_y=False, as_frame=True):
    """_summary_

    Args:
        name (_type_): _description_
        version (_type_): _description_
        target_column (_type_): _description_
        return_X_y (bool, optional): _description_. Defaults to True.
        as_frame (bool, optional): _description_. Defaults to False.
    """
    if name not in datasets:
        raise NameError("Dataset is not valid")
    maxver, fname = datasets[name]
    if version > maxver:
        raise NameError("Invalid version")

    fname+=f"{version}"
    data = pd.read_csv(f"{DATALINK}/{fname}.csv", header=0, delimiter=',',decimal='.')

    if type(target_column) is list:
        for t in target_column:
            if t not in data.columns:
                raise NameError('Target column invalid')  
    else:
        if target_column not in data.columns:
            raise NameError('Target column invalid')

    data_X = data.loc[:,~data.columns.isin(target_column)].copy()
    data_y = data.loc[:, target_column].copy()

    if return_X_y:
        return (data_X.to_numpy(), data_y.to_numpy())

    b = Bunch()
    b['data'] = data_X if as_frame else data_X.to_numpy()
    b['target'] = data_y if as_frame else data_y.to_numpy()
    b['feature_names'] = data_X.columns 
    b['target_names'] = data_y.columns 
    if as_frame:
        b['frame'] = data.copy()

    return b







    