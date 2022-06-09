import json
import multiprocessing
import requests

request_url = 'https://www.coinbase.com/api/v2/assets/search?base=USD&country=RU&filter=all&include_prices=true&limit=50&order=asc'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15'
}


def get_pages_count():
    result = requests.get(url=f'{request_url}&page=1', headers=headers).json()
    pages_count = result['pagination']['total_pages']
    return pages_count


def get_data(i):
    data = {}
    result = requests.get(url=f'{request_url}&page={i}', headers=headers).json()

    for wallet in result['data']:
        try:
            name = wallet['name']
            price = float(wallet['latest'])
            change = wallet['latest_price']['percent_change']['week'] * 100
            data[name] = {
                'price': price,
                'change': change
            }
        except Exception as ex:
            print(f'{name}: {ex}')

    print(f'Parsed {i} page...')
    return data


def main():
    pages_count = get_pages_count()
    with multiprocessing.Pool(multiprocessing.cpu_count() * 8) as process:
        data = process.map(get_data, [i for i in range(1, pages_count + 1)])
    full_data = data[0]
    for elem in data[1::]:
        full_data.update(elem)

    with open('crypto_data.json', 'w') as f:
        json.dump(full_data, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
