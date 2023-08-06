from baraqdalib import Generator
from typing import Dict, List
from random import randrange
import random
import pkgutil
import json
import csv


class Cars:
    """Class Cars for generating vehicle infromation with using of statistical data from Poland to ensure propability of occurrence"""
    def __init__(self):
        self._car_generator = Generator()
        self._car: Dict[int, Dict[str]] = dict(dict())
        self._models: Dict[str, List[List[str]]] = dict(list(list()))

        self._filenames: List[str] = ['data/PL/cars/add_info_of_au.csv', 'data/PL/cars/add_info_of_vw.csv',
                                      'data/PL/cars/add_info_of_mb.csv', 'data/PL/cars/add_info_of_bmw.csv']
        self._vin_makers: Dict[str, list[str]] = {'MERCEDES-BENZ': ['VSC', 'WDB', 'WDC', 'WDD', 'WMX', 'W1K', 'W1N'],
                                                  'AUDI': ['TRU', 'WAU', 'WUA'],
                                                  'BMW': ['WBA', 'WBS', 'WBX', 'WBY', 'WB5'],
                                                  'VOLKSWAGEN': ['WVG', 'WVW']}
        self._body_type: Dict[str, str] = {'KARETA (SEDAN)': 'SEDAN', 'KOMBI': 'STATION WAGON', 'TERENOWY': 'SUV', 'HATCHBACK': 'HATCHBACK', 'INNY': 'DIFFERENT'}

        self._get_add_info_of_cars()

    def _get_add_info_of_cars(self):
        """Loading files with model for each car brand

        Parameters: None

        Return: None
        """
        for filename in self._filenames:
            models_file = pkgutil.get_data(__package__, filename)
            models = csv.reader(models_file.decode('utf-8').splitlines(), delimiter='\t')
            iterator = 0
            maker = ''
            temp_maker_letters = filename.split('.')[0][-2:]
            if temp_maker_letters == 'au':
                maker = 'AUDI'
            if temp_maker_letters == 'vw':
                maker = 'VOLKSWAGEN'
            if temp_maker_letters == 'mb':
                maker = 'MERCEDES-BENZ'
            if temp_maker_letters == 'mw':
                maker = 'BMW'
            self._models[maker] = {}
            for model in models:
                self._models[maker][iterator] = model
                iterator += 1

    def _toss_a_model(self, automaker: str):
        """Toss a model from specific brand

        Parameters:
        automaker (str):  Name of brand to toss from models from this brand

        Return:
        list (str):  Return list of attributes of tossed model
        """
        return self._models[automaker][randrange(0, len(self._models))]

    def _get_vin(self, automaker: str, production_year: str):
        """Create Vehcile Identification Number (VIN)

        Parameters:
        automaker (str):  Name of brand
        production_year (str)

        Return:
        str:  Return generated VIN
        """
        letters = 'ABCDEFGHJKLMNPRSTUVWXYZ'
        letters_nb = 'ABCDEFGHJKLMNPRSTUVWXYZ0123456789'
        nb_for_letter = [1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 7, 9, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8,
                         9]
        year_digits = 'ABCDEFGHJKLMNPRSTVWXY123456789'
        vin = ''

        temp_vin_maker_code = self._vin_makers[automaker]
        vin += random.choice(temp_vin_maker_code)  # 1-3 digits
        vin += ''.join(random.choices(letters_nb, k=6))  # 4-9 digits
        vin += year_digits[(int(production_year) - 1980) % len(year_digits)]  # 10 digit
        vin += random.choice(letters)  # 11 digit
        production_nb = str(randrange(1, 99999))
        vin += production_nb.rjust(5, '0')  # 12-16 digits
        check_sum = nb_for_letter[letters_nb.find(vin[0])] * 9 + nb_for_letter[letters_nb.find(vin[1])] * 8 \
                    + nb_for_letter[letters_nb.find(vin[2])] * 7 + nb_for_letter[letters_nb.find(vin[3])] * 6 \
                    + nb_for_letter[letters_nb.find(vin[4])] * 5 + nb_for_letter[letters_nb.find(vin[5])] * 4 \
                    + nb_for_letter[letters_nb.find(vin[6])] * 3 + nb_for_letter[letters_nb.find(vin[7])] * 2 \
                    + nb_for_letter[letters_nb.find(vin[8])] * 10 + nb_for_letter[letters_nb.find(vin[9])] * 9 \
                    + nb_for_letter[letters_nb.find(vin[10])] * 8 + nb_for_letter[letters_nb.find(vin[11])] * 7 \
                    + nb_for_letter[letters_nb.find(vin[12])] * 6 + nb_for_letter[letters_nb.find(vin[13])] * 5 \
                    + nb_for_letter[letters_nb.find(vin[14])] * 4 + nb_for_letter[letters_nb.find(vin[15])] * 3
        for i in range(0, 9):
            if (check_sum + (i * 2)) % 11 == i:
                vin += str(i)
                return vin

    def generate(self, lang: str = 'PL', count: int = 1):
        """Generating vehicles information

        Parameters:
        lang (str): Two letter shortcut for country name, default is 'PL'
        count (int):  Number how many complete information of vehicles should be generated

        Return:
        json:  Returns data in json format
        """
        generated_cars = self._car_generator.generate(lang=lang, data_type='cars', counter=count, sep='\t')

        for i in range(count):
            model = self._toss_a_model(generated_cars[i])
            self._car[i] = {
                'brand': generated_cars[i],
                'model': model[0],
                'type': model[1],
                'body': self._body_type[model[2]],
                'origin': model[3],
                'year_of_production': model[4],
                'engine_capacity': int(model[5].split('.')[0]),
                'engine_power': int(model[6].split('.')[0]),
                'nb_of_seats': model[7],
                'fuel_type': model[8],
                'vin': self._get_vin(generated_cars[i], model[4])
            }
        return json.dumps(self._car, indent=4, ensure_ascii=False)
