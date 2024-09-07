import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# File paths
CHANNELS_FILE = 'channels.txt'
VALID_CHANNELS_FILE = 'valid_channels.txt'

# Banner
BANNER = """\n\n\x1b[96m\t████████╗ ██████╗      ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗\n\t╚══██╔══╝██╔════╝     ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝\n\t   ██║   ██║  ███╗    ██║     ███████║█████╗  ██║     █████╔╝ \n\t   ██║   ██║   ██║    ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ \n\t   ██║   ╚██████╔╝    ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗\n\t   ╚═╝    ╚═════╝      ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝\n\n"""

# User-Agent header
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0'

def read_channels():
    with open(CHANNELS_FILE, 'r') as file:
        return file.read().splitlines()

def write_valid_channel(link):
    with open(VALID_CHANNELS_FILE, 'a+') as file:
        file.write(link + "\n")

def check_channel(link):
    headers = {'User-Agent': USER_AGENT}
    try:
        response = requests.get(link, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            page_image = soup.find('img', class_='tgme_page_photo_image')
            page_extra = soup.find('div', class_='tgme_page_extra')
            if page_image and page_extra:
                subscriber_count = page_extra.text
                channel_name = soup.find('div', class_='tgme_page_title').text.strip()
                print(f"\x1b[97m[TG CHECK] \x1b[97m{link}:\x1b[92m valid\x1b[97m:\x1b[96m {channel_name}\x1b[97m (\x1b[94m{subscriber_count}\x1b[97m)")
                write_valid_channel(link)
                return True
            else:
                print(f"\x1b[97m[TG CHECK] \x1b[97m{link}:\x1b[91m invalid\x1b[97m")
                return False
    except Exception as e:
        print(f"\x1b[97m[TG CHECK] \x1b[97m{link}:\x1b[91m error\x1b[97m:\x1b[91m {e}\x1b[97m")
        return False

def main():
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(check_channel, read_channels())

if __name__ == '__main__':
    print(BANNER)
    main()
