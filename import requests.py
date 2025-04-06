import requests

url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://pixabay.com/",
    "Origin": "https://pixabay.com",
    "Sec-Fetch-Dest": "audio",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "same-site"
}

response = requests.get(url, headers=headers, stream=True)

print(response.status_code)