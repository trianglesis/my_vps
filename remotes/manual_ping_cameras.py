import django

django.setup()

import logging
import requests
from time import sleep
import datetime
import os

from PIL import Image
from io import BytesIO

from remotes.models import Options

log = logging.getLogger("dev")

perl_hostname = Options.objects.get(option_key__exact='perl_system_hostname').option_value
print(f"Using: {perl_hostname}")

skip_words = [
    'Forbidden',
    'Unauthorized',
    'HTTP/1.0 500',
    'HTTP/1.0 404',
    'Fatal error',
    'HTTP request failed',
]
PATH = os.path.abspath('D:\\Projects\\PycharmProjects\\my_vps\\y_devel\\CAM')
ANSWERS_LOG = os.path.join(PATH, 'answer_log.txt')
log.info(f'Save to: {PATH}')

for dvr in range(1, 50):
    for cam in range(1, 50):
        URL = f'{perl_hostname}cam.php?dvr={dvr}&cam={cam}'
        r = requests.get(URL)
        if r.status_code == 200:
            if not any(elem in r.text for elem in skip_words):
                print(f"Answer URL: {URL}")
                if r.content:
                    # image = Image.open(BytesIO(r.content))
                    img_bytes = BytesIO(r.content)
                    with Image.open(img_bytes).convert("RGB") as image:
                        print('Image opened')
                        # -{datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}
                        file_name = f"webcam__dvr={dvr}_cam={cam}.jpg"
                        save_to = os.path.join(PATH, file_name)
                        image.save(fp=save_to, format='JPEG')
            else:
                print(f"Skipping: dvr={dvr} cam={cam}")
                with open(ANSWERS_LOG, 'a', encoding='utf-8') as f:
                    f.write(f'Skipped: dvr={dvr} cam={cam} - {r.text}\n')
