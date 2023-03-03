# 从喵影视更新数据源

import requests
import json

url = "http://miaotvs.cn/meow"

headers = {
    'User-Agent': 'okhttp/3.12.11'
}


def get_redirect():
    res = requests.get(url, headers=headers, allow_redirects=False)
    return res.headers["Location"]


def get_conf():
    host = get_redirect()
    response = requests.get(host, headers=headers)
    json_text = response.text
    res = ""
    for line in json_text.split("\r\n"):
        if not line.strip().startswith("//"):
            res += line.strip()
    res = json.dumps(json.loads(res), indent=4, ensure_ascii=False)
    print(res)
    return res


def write_file(data):
    with open('source.json', 'w') as f:
        f.write(data)


if __name__ == '__main__':
    d = get_conf()
    write_file(d)
