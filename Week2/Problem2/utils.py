import numpy as np

def save_as_csv(csv_name: str, data: list):
    """save list data as csv file

    Arguments
    csv_name [str]: csv name finished with .csv
    data [list(list|tuple)]: 2d list data
    """
    assert csv_name[-4:] == ".csv"

    np.savetxt(csv_name, data, delimiter=", ", fmt="% s")