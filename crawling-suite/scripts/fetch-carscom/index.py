import urllib3


def test_cars_website():
    http = urllib3.PoolManager()
    result = http.request('GET',
                          'https://www.cars.com/shopping/results/?stock_type=cpo&makes%5B%5D=&models%5B%5D=&list_price_max=&maximum_distance=all&zip=',
                          )
    print(result.data)


test_cars_website()
