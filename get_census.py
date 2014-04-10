import requests
import csv


def build_api_query(get_param, spatial_param, key, dataset="2011/acs5"):
    """builds a valid api query given key, dataset, get, and spatial/for"""

    root = "http://api.census.gov/data/"
    #add a dataset
    query = root + dataset + '?'
    #add a key
    query = query + "key=" + key
    #add the get
    query = query + "&get=" + get_param
    #add the spatial
    query = query + "&for=" + spatial_param

    return query


def get_tract_data(key, state_code, county_code):
    """gets tract data from the census"""

    #build up the spatial param from state and county code
    spatial = "tract:*&in=state:" + state_code + "+county:" + county_code

    query = build_api_query(
        get_param="B19013_001E,B06009_001E,B06009_005E",
        spatial_param=spatial,
        key=key
    )
    return query


def main():

    with open("api_key.txt", "r") as api_file:
        api_key = api_file.readlines()

    #read our csv into a list of dicts
    rpa = []
    with open('countyFIPS.csv', 'rb') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)
        headers = next(reader)
        for row in reader:
            #make a dict
            internal_dict = dict(zip(headers, row))
            #append to the list
            rpa.append(internal_dict)

    #loop over counties and build api query
    for co in rpa:
        valid_query = get_tract_data(
            state_code=co['STFIPS'],
            county_code=co['countyFIPS'],
            key=api_key[0]
        )
        print valid_query
        r = requests.get(valid_query)
        resp = r.json()
        #TODO: loop over tracts in response and handle data
        for tract in resp:
            print tract

if __name__ == '__main__':
    main()