# coding=utf-8
# 从数据源同步到本地

import requests
import json
from conf import source_list

headers = {
    'User-Agent': 'okhttp/3.12.11'
}


def get_redirect(url):
    res = requests.get(url, headers=headers, allow_redirects=False)
    return res.headers["Location"]


def get_conf(url):
    response = requests.get(url, headers=headers)
    json_text = response.content.decode("utf-8")
    res = ""
    for line in json_text.split("\r\n"):
        if not line.strip().startswith("//"):
            res += line.strip()
    try:
        res_json = json.loads(res)
        remove_keys(res_json)
        res = json.dumps(res_json, indent=4, ensure_ascii=False)
        # print(res)
        return res
    except Exception as e:
        print("json 解析失败", e)
        return ""


def get_git_conf(url):
    response = requests.get(url)
    res = response.json()
    res_json = json.loads(res["payload"]["blob"]["rawBlob"])
    remove_keys(res_json)
    res = json.dumps(res_json, indent=4, ensure_ascii=False)
    return res


def remove_keys(result):
    key_list = ["warningText"]
    for key in key_list:
        if key in result:
            result.pop(key)


def write_file(name, data):
    with open('./json/{}.json'.format(name), 'w') as f:
        f.write(data)


def main():
    for template in source_list:
        result = ""
        url = template["url"]
        print("开始同步 - {}".format(template["desc"]))
        if template["allow_redirect"]:
            url = get_redirect(url)
        if template["from"] == "api":
            result = get_conf(url)
        elif template["from"] == "git":
            result = get_git_conf(url)
        if result:
            write_file(template["name"], result)


if __name__ == '__main__':
    main()
