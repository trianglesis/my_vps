from __future__ import absolute_import, unicode_literals

import logging
import requests
import PIL
from PIL import Image, ImageEnhance
import io
from time import sleep

from django.template import loader

from core.helpers.mailing import Mails

from core.setup_logic import Credentials
from core.security import DjangoCreds

from remotes.models import PerlCameras, Options, PerlButtons

log = logging.getLogger("core")

skip_words = [
    'Forbidden',
    'Unauthorized',
    'HTTP/1.0 500',
    'HTTP/1.0 404',
    'Fatal error',
    'HTTP request failed',
]


def request_image(cam_url, caller='nobody'):
    log.debug(f"2.0 Requesting image content by url: {cam_url} by: {caller}")
    r = requests.get(cam_url)
    if r.status_code == 200:
        if not any(elem in r.text for elem in skip_words):
            if r.content:
                log.debug(f"2.1 Successful request pic URL: {cam_url}")
                return r.content
    elif r.status_code == 404:
        log.error(f"2.1 Unsuccessful request pic URL: {cam_url} - 404! Exit")
        return b''
    log.debug(f"2.2 Unsuccessful request pic URL: {cam_url}, will return empty bytecode and retry")
    return b''


def save_image(runs, cam_url, images, content, image_enhance):
    stop = 3
    runs += 1
    log.debug(f"3.1 Save image attempt: {runs}")
    if runs > stop:
        log.debug(f"3.4 Last attempt to save image: {runs} full stop at: {stop}")
        pass
    else:
        img_bytes = io.BytesIO(content)
        try:
            log.debug(f"3.2 Save image attempt: {runs} try save!")
            image = PIL.Image.open(img_bytes).convert("RGB")
            wpercent = (image_enhance['basewidth'] / float(image.width))
            hsize = int((float(image.height) * float(wpercent)))
            image = image.resize((image_enhance['basewidth'], hsize), Image.ANTIALIAS)
            image = ImageEnhance.Color(image).enhance(image_enhance['color'])
            image = ImageEnhance.Brightness(image).enhance(image_enhance['brightness'])
            image = ImageEnhance.Contrast(image).enhance(image_enhance['contrast'])
            image = ImageEnhance.Sharpness(image).enhance(image_enhance['sharpness'])
            images.append(image)
        except PIL.UnidentifiedImageError as e:
            sleep(0.5)
            log.error(f"3.3 Cannot save image: {cam_url}, attempt: {runs}, Exception caught: {e}")
            content = request_image(cam_url, caller=f'exception, run:{runs}')
            save_image(runs, cam_url, images, content, image_enhance)


def camera_shot(element, perl_hostname, image_enhance, basewidth=None):
    images = []

    if not basewidth:
        basewidth = image_enhance.get(option_key__exact='ImageEnhance.image.basewidth').option_value

    color = image_enhance.get(option_key__exact='ImageEnhance.Color').option_value
    brightness = image_enhance.get(option_key__exact='ImageEnhance.Brightness').option_value
    contrast = image_enhance.get(option_key__exact='ImageEnhance.Contrast').option_value
    sharpness = image_enhance.get(option_key__exact='ImageEnhance.Sharpness').option_value

    image_enhance = dict(
        basewidth=int(basewidth),
        color=float(color),
        brightness=float(brightness),
        contrast=float(contrast),
        sharpness=float(sharpness),
    )

    log.info(f"Image enhancements: color: {color} brightness: {brightness} contrast: {contrast} sharpness: {sharpness} basewidth: {basewidth}")

    if hasattr(element, 'assigned_buttons'):
        # element.assigned_buttons.all()
        for camera in element.assigned_buttons.all():
            runs = 0
            # cam_url = f"{perl_hostname}cam.php?dvr=12&cam=47"
            cam_url = f"{perl_hostname}cam.php?dvr={camera.dvr}&cam={camera.cam}"
            log.debug(f"1.0 Requesting camera content: {cam_url}")
            content = request_image(cam_url, caller='initial')
            log.debug(f"3.0 Save image or check if save-able content: {cam_url}")
            save_image(runs, cam_url, images, content, image_enhance)
            log.debug(f"4.0 Finishing job for this image and run forward! {cam_url}")
    elif element.dvr and element.cam:
        log.info(f"Making snapshot for single camera: {element.description}")
        runs = 0
        # cam_url = f"{perl_hostname}cam.php?dvr=12&cam=47"
        cam_url = f"{perl_hostname}cam.php?dvr={element.dvr}&cam={element.cam}"
        log.debug(f"1.0 Requesting camera content: {cam_url}")
        content = request_image(cam_url, caller='initial')
        log.debug(f"3.0 Save image or check if save-able content: {cam_url}")
        save_image(runs, cam_url, images, content, image_enhance)
        log.debug(f"4.0 Finishing job for this image and run forward! {cam_url}")
    else:
        log.error(f"Else")

    return images


def make_snap_send_email_routine(**kwargs):
    dom = kwargs.get('dom')
    gate = kwargs.get('gate')
    mode = kwargs.get('mode')

    dvr = kwargs.get('dvr')
    cam = kwargs.get('cam')

    username = kwargs.get('username')
    send_to = kwargs.get('send_to')

    fake = kwargs.get('fake', None)
    snap = kwargs.get('snap', None)

    button = None
    camera = None
    perl_hostname = Options.objects.get(option_key__exact='perl_system_hostname').option_value
    image_enhance = Options.objects.filter(option_key__startswith='ImageEnhance')

    if snap:
        template = loader.get_template('emails/maked_snap.html')
        camera = PerlCameras.objects.get(
            dvr__exact=dvr,
            cam__exact=cam
        )
        subject = f'Remote snapshot: {camera.description}'
        images = camera_shot(camera, perl_hostname, image_enhance)
    elif fake:
        log.debug(f"Running fake!!! Only snap, do not open that door")
        template = loader.get_template('emails/maked_snap.html')
        button = PerlButtons.objects.get(
            dom__exact=dom,
            gate__exact=gate,
            mode__exact=mode
        )
        subject = f'FAKE: Remote snapshot: {button.description}'
        images = camera_shot(button, perl_hostname, image_enhance)
    else:
        template = loader.get_template('emails/pushed_button.html')
        button = PerlButtons.objects.get(
            dom__exact=dom,
            gate__exact=gate,
            mode__exact=mode
        )
        subject = f'Remote open: {button.description}'
        images = camera_shot(button, perl_hostname, image_enhance)

    mail_html = template.render(dict(
        subject=subject,
        button=button,
        camera=camera,
        username=username,
        hostname=Credentials.SITE,
    ))

    log.debug(f"subject: {subject}, bcc: {DjangoCreds.mails['admin']}, send_to: {send_to}")

    Mails().short(
        subject=subject,
        mail_html=mail_html,
        images=images,
        send_to=send_to,
        bcc=DjangoCreds.mails['admin'],
    )
    return True
