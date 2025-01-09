def fetch_countries():
    response = requests.get('https://restcountries.com/v3.1/all?fields=name,flags,capital,population,continents,timezones,area,latlng')
    countries = response.json()

    for country_data in countries:
        Country.objects.update_or_create(
            name_common=country_data['name']['common'],
            defaults={
                'name_official': country_data['name']['official'],
                'capital': country_data['capital'][0] if country_data['capital'] else '',
                'lat': country_data['latlng'][0],
                'lng': country_data['latlng'][1],
                'area': country_data['area'],
                'population': country_data['population'],
                'timezone': country_data['timezones'][0] if country_data['timezones'] else '',
                'continent': country_data['continents'][0] if country_data['continents'] else '',
                'flag_png': country_data['flags']['png'],
                'flag_svg': country_data['flags']['svg'],
                'flag_alt': country_data['flags'].get('alt', '')
            }
        )