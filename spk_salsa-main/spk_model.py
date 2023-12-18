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
            'harga': HARGA_SCALE[laptop['harga']],
            'prosesor': PROSESOR_SCALE[laptop['prosesor']],
            'ram': RAM_SCALE[laptop['ram']],
            'storage': STORAGE_SCALE[laptop['storage']],
            'baterai': BATERAI_SCALE[laptop['baterai']]
        } for laptop in self.dataDict]

    @property
    def normalized_data(self):
        # x/max [benefit]
        # min/x [cost]
        nama = [] # min
        harga = [] # min
        prosesor = [] # max
        ram = [] # max
        storage = [] # max
        baterai = [] # max
        for data in self.data:
            nama.append(data['nama'])
            harga.append(data['harga'])
            prosesor.append(data['prosesor'])
            ram.append(data['ram'])
            storage.append(data['storage'])
            baterai.append(data['baterai'])

        min_nama = min(nama)
        min_harga = min(harga)
        max_prosesor = max(prosesor)
        max_ram = max(ram)
        max_storage = max(storage)
        max_baterai = max(baterai)

        return [
            {   'id': data['id'],
                'nama': data['nama']/min_nama, # cost
                'harga': data['harga']/min_harga, # cost
                'prosesor': data['prosesor']/max_prosesor, # benefit
                'ram': data['ram']/max_ram, # benefit
                'storage': data['storage']/max_storage, # benefit
                'baterai': data['baterai']/max_baterai # benefit
                }
            for data in self.data
        ]
 

class WeightedProduct(BaseMethod):
    def __init__(self, dataDict, setWeight:dict):
        super().__init__(data_dict=dataDict, **setWeight)
    @property
    def calculate(self):
        weight = self.weight
        result = {row['id']:
    round(
        row['nama'] ** weight['nama'] *
        row['harga'] ** weight['harga'] *
        row['prosesor'] ** weight['processor'] *
        row['ram'] ** weight['ram'] *
        row['storage'] ** weight['storage'] *
        row['baterai'] ** weight['baterai']
        , 2
    )
    for row in self.normalized_data}

        #sorting
        # return result
        return dict(sorted(result.items(), key=lambda x:x[1], reverse=True))