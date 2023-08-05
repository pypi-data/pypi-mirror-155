from django.utils.translation import gettext_lazy as _

import pycountry


def country_choices():
    for country in get_countries():
        yield country.alpha_2, _(country.name)


def get_countries():
    prefix_list = []
    countries_list = []
    for country in pycountry.countries:
        # Put the UK and ROI as the first item on the list.
        if country.alpha_2 == "GB":
            prefix_list.insert(0, country)
        elif country.alpha_2 == "IE":
            prefix_list.append(country)
        else:
            countries_list.append(country)
    countries_list.sort(key=lambda c: c.name)
    return prefix_list + countries_list
