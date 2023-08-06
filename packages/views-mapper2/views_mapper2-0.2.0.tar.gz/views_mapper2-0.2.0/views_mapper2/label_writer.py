"""
Small functions enabling ease of writing recursive mapping code
And simplifying the lookup and conversion of month and country ids
"""

from ingester3.ViewsMonth import ViewsMonth
from ingester3.Country import Country
import pycountry
from datetime import date


def vid2date(month_id):
    """
    Writes a label in standard year/month format from month_id
    :param month_id:
    :return: year/month date
    """
    year=str(ViewsMonth(month_id).year)
    month=str(ViewsMonth(month_id).month)
    return year+'/'+month

def date2id(date_string):
    """
    Writes month id from date, iso format
    :param date_string: date in iso format, e.g., '2010-04-01'
    :return: ViEWS month id
    """
    date_iso = date.fromisoformat(date_string)
    month_id = ViewsMonth.from_date(date_iso).id
    return month_id

def cid2name(country_id):
    """
    Function useful for labeling countries if needed by their name
    Create a string output name by country id
    Uses ingester3 Country as basis
    :param country_id: Views Country ID
    :return: name
    """
    name = print(Country(country_id).name)
    return name

def name2iso(country):
    """
    Creates a quick lookup of the ISO label for a country
    Contains soft search suggestion if the input is wrong
    :param name: name, please make sure to input in ''. e.g. 'England'
    :return: ISO code
    """
    try:
        output = pycountry.countries.get(name=country).alpha_3
    except AttributeError:
        try:
            output = 'no match, did you mean'+' ' + str(pycountry.countries.search_fuzzy(country)[0])
        except LookupError:
            output= 'check_spelling'
    return output

def name_mid2cid(country, month_id):
    """
    Quick lookup of the country id from name and month id
    :param country: Name of country, please enter as a string within '', e.g., 'England'
    :param month_id: ViEWS month ID
    :return: ViEWS country ID
    """
    try:
        output = Country.from_iso(pycountry.countries.get(name=country).alpha_3, month_id).id
    except AttributeError:
        try:
            output = 'no match, did you mean'+' ' + str(pycountry.countries.search_fuzzy(country)[0])
        except LookupError:
            output= 'check_spelling'
    return output

def name_date2cid(country, date_string):
    """
    Quick looks up of the country id from name and iso date
    :param country: name of the country, enter as string, e.g., 'England'
    :param date_string: date in iso format, enter as string, e.g., '2010-04-01'
    :return: ViEWS country ID
    """
    date_iso = date.fromisoformat(date_string)
    month_id = ViewsMonth.from_date(date_iso).id
    try:
        output = Country.from_iso(pycountry.countries.get(name=country).alpha_3, month_id)
    except AttributeError:
        try:
            output = 'no match, did you mean'+' ' + str(pycountry.countries.search_fuzzy(country)[0])
        except LookupError:
            output= 'check_spelling'
    return output

