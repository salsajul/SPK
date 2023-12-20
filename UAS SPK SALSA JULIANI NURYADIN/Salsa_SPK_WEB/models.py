import numpy as np
import pandas as pd
from spk_model import WeightedProduct

class laptop():

    def __init__(self) -> None:
        self.laptop = pd.read_csv('data/spk_salsa_juliani_nuryadin.csv')
        self.laptop = np.array(self.laptop)

    @property
    def laptop_data(self):
        data = []
        for laptop in self.laptop:
            data.append({'id': laptop[0], 'nama': laptop[1]})
        return data

    @property
    def laptop_data_dict(self):
        data = {}
        for laptop in self.laptop:
            data[laptop[0]] = laptop[1] 
        return data

    def get_recs(self, kriteria:dict):
        wp = WeightedProduct(self.laptop.to_dict(orient="records"), kriteria)
        return wp.calculate

