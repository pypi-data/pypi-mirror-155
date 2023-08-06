import requests

def get_my_ip():
    return requests.get('https://api.ipify.org').text

def main():
    print(get_my_ip())

if __name__ == '__main__':
    main()
