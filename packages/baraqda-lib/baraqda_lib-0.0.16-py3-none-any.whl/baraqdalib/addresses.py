from baraqdalib import Generator
import csv
import random
from typing import Dict
import pkgutil


class Addresses:
    """Class Addresses for generating polish fake address but with true distribution"""
    def __init__(self):
        self._postal_codes: Dict[str] = dict()
        self._streets: Dict[str] = dict()
        self._cities: Dict[Dict[str]] = dict(dict())

        self._set_cities()
        self._set_streets()
        self._set_postal_codes()

    def _set_cities(self):
        """Get cities names  from file cities.csv and save in self._cities dict

        Parameters : None

        Returns: None
        """
        cities_file = pkgutil.get_data(__package__, 'data/PL/cities.csv')
        cities_file = csv.DictReader(cities_file.decode('utf-8-sig').splitlines(), delimiter=';')

        for row in cities_file:
            city = {row['SYM']: row['NAZWA']}
            self._cities.update(city)

    def _set_streets(self):
        """Get street names from file streets.csv and save in self._streets dict

        Parameters : None

        Returns: None
        """
        streets_file = pkgutil.get_data(__package__, 'data/PL/streets.csv')
        streets_file = csv.DictReader(streets_file.decode('utf-8-sig').splitlines(), delimiter=';')

        for street in streets_file:
            streets = {street['SYM']: list()}
            self._streets.update(streets)

        streets_file = pkgutil.get_data(__package__, 'data/PL/streets.csv')
        streets_file = csv.DictReader(streets_file.decode('utf-8-sig').splitlines(), delimiter=';')

        for street in streets_file:
            self._streets[street['SYM']].append(str(street['CECHA']+' '+street['NAZWA_2']+' '+street['NAZWA_1']).replace('  ', ' '))

    def _set_postal_codes(self):
        """Get postal codes from file postal_codes.csv and save in self._postal_code dict

        Parameters : None

        Returns: None
        """
        postal_codes_file = pkgutil.get_data(__package__, 'data/PL/postal_codes.csv')
        postal_codes_file = csv.DictReader(postal_codes_file.decode('utf-8-sig').splitlines(), delimiter=';')

        for postal_code in postal_codes_file:
            city = {postal_code['MIEJSCOWOŚĆ']: list()}
            self._postal_codes.update(city)

        postal_codes_file = pkgutil.get_data(__package__, 'data/PL/postal_codes.csv')
        postal_codes_file = csv.DictReader(postal_codes_file.decode('utf-8-sig').splitlines(), delimiter=';')

        for postal_code in postal_codes_file:
            self._postal_codes[postal_code['MIEJSCOWOŚĆ']].append(postal_code['KOD POCZTOWY'])

    def generate(self, lang: str = 'PL'):
        """ Generating address with city, street, street number,  and postal code

        Parameters:
        lang (str): Default is 'PL'. By this argument you can choose from which country addresses should be generated.

        Returns:
        Dict(): returning generated address in dictionary for easy access

        """
        address_generator = Generator()
        city = str(address_generator.generate(lang, 'cities_pops', 1, '\t')[0])
        sym = self._get_sym_city(city)
        street = self._get_streets(str(sym))
        postal_code = self._get_postal_code(city)
        address = {'street': street, 'city': city, 'postal_code': postal_code}
        return address

    def _get_sym_city(self, city: str):
        """Searching for city in cities and returning sym (identifier)

        Parameters:
        city (str): name of city for searching

        Returns:
        str : return sym for searching city
        """
        return list(self._cities.keys())[list(self._cities.values()).index(city)]

    def _get_postal_code(self, city: str):
        """Search and return postal code for a given city

        Parameters:
        city (str): Name of the city

        Returns:
        str: Returns postal code
        """
        city.replace('-', ' ')
        return random.choice(self._postal_codes[city])

    def _get_streets(self, city_sym: str):
        """ Generate random street for given city sym (identifier) that is in this city.

        Parameters:
        city_sym (str): number of city syn

        Returns:
        str: returns random street
        """
        try:
            streets = self._streets[city_sym]
            return random.choice(streets) + ' ' + str((round(random.lognormvariate(1.6, 2)) + 1) % 200)
        except KeyError:
            rand_sym = random.choice(list(self._streets.keys()))
            streets = self._streets[rand_sym]
            return random.choice(streets) + ' ' + str((round(random.lognormvariate(1.6, 2)) + 1) % 200)
