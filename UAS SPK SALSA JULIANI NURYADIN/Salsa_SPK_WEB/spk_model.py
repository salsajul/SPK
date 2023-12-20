from settings import NAMA_SCALE, HARGA_SCALE, PROSESOR_SCALE, RAM_SCALE, STORAGE_SCALE, BATERAI_SCALE

class BaseMethod():

    def __init__(self, data_dict, **setWeight):

        self.dataDict = data_dict

        # 1-6 (Kriteria)
        self.raw_weight = {
            'nama' : 2,
            'harga' : 1,
            'processor' : 6,
            'ram' : 5,
            'storage' : 3,
            'baterai' : 4
        }

        if setWeight:
            for item in setWeight.items():
                temp1 = setWeight[item[0]] # value int
                temp2 = {v: k for k, v in setWeight.items()}[item[1]] # key str

                setWeight[item[0]] = item[1]
                setWeight[temp2] = temp1

    @property
    def weight(self):
        total_weight = sum(self.raw_weight.values())
        return {c: round(w/total_weight, 2) for c,w in self.raw_weight.items()}

    @property
    def data(self):
        return [{
            'id': laptop['id'],
            'nama': NAMA_SCALE[laptop['nama']],
            'harga': laptop['harga'],
            'prosesor': PROSESOR_SCALE[laptop['prosesor']],
            'ram': RAM_SCALE[laptop['ram']],
            'storage': laptop['storage'],
            'baterai': laptop['baterai']
        } for laptop in self.dataDict]

    @property
    def normalized_data(self):
        # x/max [benefit]
        # min/x [cost]

        nama = [] # min
        harga = [] # min
        processor = [] # max
        ram = [] # max
        storage = [] # max
        baterai = [] # min

        for data in self.data:
            nama.append(data['nama'])
            harga.append(data['harga'])
            processor.append(data['processor'])
            ram.append(data['ram'])
            storage.append(data['storage'])
            baterai.append(data['baterai'])

        min_nama = min(nama)
        min_harga = min(harga)
        max_processor = max(processor)
        max_ram = max(ram)
        max_storage = max(storage)
        min_baterai = min(baterai)

        return [{
            'id': data['id'],
            'nama': min_nama/data['nama'], # cost
            'harga': min_nama/data['harga'], # cost
            'processor': data['processor']/max_processor, # benefit
            'ram': data['ram']/max_ram, # benefit
            'storage': data['storage']/max_storage, # benefit
            'baterai': min_baterai/data['baterai'], # cost
        } for data in self.data]
 

class WeightedProduct(BaseMethod):
    def __init__(self, dataDict, setWeight:dict):
        super().__init__(data_dict=dataDict, **setWeight)

    @property
    def calculate(self):
        weight = self.weight
        # calculate data and weight[WP]
        result = {row['id']:
            round(
                row['nama'] ** (-weight['nama']) *
                row['harga'] ** (-weight['harga']) *
                row['processor'] ** weight['processor'] *
                row['ram'] ** weight['ram'] *
                row['storage'] ** weight['storage'] *
                row['baterai'] ** (-weight['baterai'])
                , 2
            )

            for row in self.normalized_data}
        #sorting
        # return result
        return dict(sorted(result.items(), key=lambda x:x[1]))
