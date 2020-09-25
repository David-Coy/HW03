import numpy as np

#url = 'https://gt.bootcampcontent.com/GT-Coding-Boot-Camp/gt-atl-data-pt-09-2020-u-c/raw/master/02-Homework/03-Python/Instructions/PyPoll/Resources/election_data.csv'
#pd.set_option("display.max_rows", None, "display.max_columns", None)
#url = 'https://gt.bootcampcontent.com/GT-Coding-Boot-Camp/gt-atl-data-pt-09-2020-u-c/raw/master/02-Homework/03-Python/Instructions/PyPoll/Resources/election_data.csv?raw=true'
#pd.read_csv(url, error_bad_lines=False)

#ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDMnij/JtZA6P6t4npEiM7wcjj3Lt7xYFNGsQnXrGHf4vpHwMHkiZe865guadpmLJYUhDoTxdn2TSXfEcPHq5vSG1lJweqj31M9/tg+F2oTm1y/JKMhoFNSpaxlaqRibZ1lle8IaG/BCZML/zxHm442skqy3w0rz5HD+ydAhPO1I4g7nI8n28Ok5vThFad4qYISIw3PiU70wGZSxueoDP5ejr6MJ4G8peALn24ZFqSvhIeyDpAv4URd6kKPLVBCOcTZSLSRXBQWXRrWFxPzqeqo2mzxVESfOaja1N61WfPNZVRVgVkk5HASvtj7pEVWb7xQ4BarIp4S5P3uasvtwRab071K61XUsuAQ88D1oXIZ+D9xNoQlA4Lr6UTks3c7ebv4QItX106wc7YTr5O/o90DdVxJQzZlTHTXbbtzRAXu9MGWG+Arxpm6a/xr1T8yNfMeOzLqVhjIYXyqgpMg4A9BiThZS5QXdnq+6CKHCkkCPscTSxKNZfoo1oZFZYTMtS2CIx2FNMvoctkP+GpTytjlbWYUAMYM4h223bCtywhLjAJZV3ZnpCOX7IPuYI9fTVNVOWk5Z0DwNvnx8hAqO3kgxBkr+qwsFWW97BLDAwz71v2nshm1bJ+UrS2vCSNZRh39CcaSuWhhNZ0Qj1udA/niYHdhTp7JINmbvjm2Svvkfw== davidcoy@ptotonmail.com


import re
import sys
import requests
import gitlab


URL = 'https://gitlab.com'
SIGN_IN_URL = 'https://gitlab.com/users/sign_in'
LOGIN_URL = 'https://gitlab.com/users/sign_in'

session = requests.Session()

#sign_in_page = session.get(SIGN_IN_URL).content
sign_in_page = session.get(SIGN_IN_URL).text
for l in sign_in_page.split('\n'):
    m = re.search('name="authenticity_token" value="([^"]+)"', l)
    if m:
        break

d = None
if m:
    token = m.group(1)

if not token:
    print('Unable to find the authenticity token')
    sys.exit(1)

data = {'user[login]': 'davidcoy@protonmail.com',
        'user[password]': 'e4svummyFootbag!',
        'authenticity_token': PCgwzKvL-QnCBg1eqsQQ}
r = session.post(LOGIN_URL, data=data)
if r.status_code != 200:
    print('Failed to log in')
    sys.exit(1)

gl = gitlab.Gitlab(URL, api_version=4, session=session)