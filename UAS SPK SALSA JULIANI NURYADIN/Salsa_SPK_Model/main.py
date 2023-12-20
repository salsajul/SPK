import sys
from colorama import Fore, Style
from models import Base, Laptop
from engine import engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from settings import NAMA_SCALE, HARGA_SCALE, PROSESOR_SCALE, RAM_SCALE, STORAGE_SCALE, BATERAI_SCALE,HARGA_SCALE,STORAGE_SCALE,HARGA_SCALE
session = Session(engine)

def create_table():
    Base.metadata.create_all(engine)
    print(f'{Fore.GREEN}[Success]: {Style.RESET_ALL}Database has created!')

class BaseMethod():

    def __init__(self):
        # 1-6
        self.raw_weight = {
            'Nama_Produk' : 2,
            'Harga_C1' : 1,
            'Prosesor_C2' : 6,
            'RAM_C3' : 5,
            'Storage_C4' : 3,
            'Baterai_C5' : 4
            }

    @property
    def weight(self):
        total_weight = sum(self.raw_weight.values())
        return {k: round(v/total_weight, 2) for k,v in self.raw_weight.items()}

    @property
    def data(self):
        query = select(Laptop)
        return [{'id': laptop.id, 
        'Nama_Produk': NAMA_SCALE[laptop.Nama_Produk], 
        'Harga_C1': HARGA_SCALE[laptop.Harga_C1], 
        'Prosesor_C2': PROSESOR_SCALE[laptop.Prosesor_C2], 
        'RAM_C3': RAM_SCALE[laptop.RAM_C3], 
        'Storage_C4': STORAGE_SCALE[laptop.Storage_C4], 
        'Baterai_C5': BATERAI_SCALE[laptop.Baterai_C5]} 
              for laptop in session.scalars(query)]
    

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
            nama.append(data['Nama_Produk'])
            harga.append(data['Harga_C1'])
            processor.append(data['Prosesor_C2'])
            ram.append(data['RAM_C3'])
            storage.append(data['Storage_C4'])
            baterai.append(data['Baterai_C5'])

        min_nama = min(nama)
        min_harga = min(harga)
        max_processor = max(processor)
        max_ram = max(ram)
        max_storage = max(storage)
        min_baterai = min(baterai)

        return [{
            'id': data['id'],
            'Nama_Produk': min_nama/data['Nama_Produk'], # cost
            'Harga_C1': min_nama/data['Harga_C1'], # cost
            'Prosesor_C2': data['Prosesor_C2']/max_processor, # benefit
            'RAM_C3': data['RAM_C3']/max_ram, # benefit
            'Storage_C4': data['Storage_C4']/max_storage, # benefit
            'Baterai_C5': min_baterai/data['Baterai_C5'], # cost
        } for data in self.data]

class WeightedProduct(BaseMethod):
    @property
    def calculate(self):
        weight = self.weight
        # calculate data and weight[WP]
        result =  {row['id']:
            round(
                row['Nama_Produk'] ** (-weight['Nama_Produk']) *
                row['Harga_C1'] ** (-weight['Harga_C1']) *
                row['Prosesor_C2'] ** weight['Prosesor_C2'] *
                row['RAM_C3'] ** weight['RAM_C3'] *
                row['Storage_C4'] ** weight['Storage_C4'] *
                row['Baterai_C5'] ** (-weight['Baterai_C5'])
                , 2)
            for row in self.normalized_data
        }
        # sorting
        return dict(sorted(result.items(), key=lambda x:x[1], reverse=True))


class SimpleAdditiveWeighting(BaseMethod):
    @property
    def calculate(self):
        weight = self.weight
        # calculate data and weight
        result =  {row['id']:
            round(row['Nama_Produk'] * weight['Nama_Produk'] +
            row['Harga_C1'] * weight['Harga_C1'] +
            row['Prosesor_C2'] * weight['Prosesor_C2'] +
            row['RAM_C3'] * weight['RAM_C3'] +
            row['Storage_C4'] * weight['Storage_C4'] +
            row['Baterai_C5'] * weight['Baterai_C5']
            , 2)
            for row in self.normalized_data
        }
        # sorting
        return dict(sorted(result.items(), key=lambda x:x[1]))

def run_saw():
    saw = SimpleAdditiveWeighting()
    print('result:', saw.calculate)

def run_wp():
    wp = WeightedProduct()
    print('result:', wp.calculate)
    pass

if len(sys.argv)>1:
    arg = sys.argv[1]

    if arg == 'create_table':
        create_table()
    elif arg == 'saw':
        run_saw()
    elif arg =='wp':
        run_wp()
    else:
        print('command not found')
