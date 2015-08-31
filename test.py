import requests
from bs4 import BeautifulSoup

username = ""
password = ""

base_url = "https://instagram.com"
ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"  # noqa

headers = {
    'User-Agent': ua,
    'X-Instagram-AJAX': 1,
    'X-Requested-With': 'XMLHttpRequest'
}

headers = {
    'Accept-Language': 'en-US,en;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': ua,
    'Referer': '{0}/'.format(base_url),
    'Origin': base_url,
    'X-Instagram-AJAX': '1',
    'X-Requested-With': 'XMLHttpRequest',
}

client = requests.Session()

# Get CSRFToken
url = '{0}/accounts/login/'.format(base_url)
r = client.get(url=url, headers=headers)
headers['X-CSRFToken'] = r.cookies['csrftoken']

# Login
url = '{0}/accounts/login/ajax/'.format(base_url)
data = 'username={0}&password={1}'.format(username, password)
r = client.post(url=url, data=data, headers=headers)
headers.pop('X-CSRFToken')

# Get News Inbox
url = "http://instagram.com/api/v1/news/inbox/"
r = client.get(url)
# print r.text

# Parse
soup = BeautifulSoup(r.text, "html.parser")
activity = soup.find_all('li')

for li in activity:
    # print type(li)
    link = li.find('a')['href']
    caption = ' '.join(li.get_text().strip().split())
    classes = li.attrs['class']
    classes.remove('group')
    activity = classes[0].replace('-activity', '')

    print "*******"
    print activity
    print link
    print caption
