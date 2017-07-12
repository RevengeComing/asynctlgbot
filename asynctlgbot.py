import concurrent.futures
import functools
import asyncio

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


def generate_button(self, button_text, request_contact=False, request_location=False):
    return {
        'text':button_text,
        'request_contact':request_contact,
        'request_location':request_location
    }

class Telegram():
    unauth_url = "https://api.telegram.org/bot{token}/"

    def __init__(self, token, loop=None, requests_workers=12):
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=requests_workers)
        self.token = token
        self.loop = loop or asyncio.get_event_loop()
        self.base_url = "%s{method_name}" % (self.unauth_url.format(token=token))

    def set_event_loop(self, loop):
        self.loop = loop

    def get_updates(self):
        api_url = self.base_url.format(method_name='deleteWebhook')
        resp = requests.get(api_url)
        resp = resp.json()
        api_url = self.base_url.format(method_name='getUpdates')
        resp = requests.get(api_url)
        resp = resp.json()

    async def set_webhook(self, url, certificate=None, max_connections='100',
            allowed_updates=["message", "edited_channel_post", "callback_query"]):
        api_url = self.base_url.format(method_name='setWebhook')
        fields = {
            "url": url,
            "max_connections": max_connections,
            "allowed_updates": allowed_updates
        }
        if certificate:
            fields['certificate'] = (certificate, open(certificate, 'rb'), 'text/plain')
        multipart_data = MultipartEncoder(fields=fields)
        response = await self.post(api_url, data=multipart_data,
                      headers={'Content-Type': multipart_data.content_type})
        return response

    async def get_webhook_info(self):
        api_url = self.base_url.format(method_name='getWebhookInfo')
        resp = await self.get(api_url)
        resp = resp.json()
        if resp['ok'] != True:
            Exception("Something went wrong to get webhook info...")
        else:
            print(resp)

    async def send_message(self, chat_id, text, rply_msg_id=None,
            reply_markup={'remove_keyboard':True}):
        api_url = self.base_url.format(method_name='sendMessage')
        json_data = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': "HTML",
            'reply_markup': reply_markup,
        }
        if rply_msg_id:
            json_data['reply_to_message_id'] = rply_msg_id
        resp = await self.post(api_url, json=json_data)

    async def send_photo(self, chat_id, photo, caption=None,
            reply_markup={'remove_keyboard':True}):
        api_url = self.base_url.format(method_name='sendPhoto')
        json_data = {
            'chat_id': chat_id,
            'photo': photo,
            'reply_markup': reply_markup,
            'parse_mode': 'HTML'
        }
        if caption:
            json_data['caption'] = caption
        resp = await self.post(api_url, json=json_data)

    async def get(self, url, data=None, json=None, params=None, loop=None, headers={}):
        if not loop:
            loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor,
            functools.partial(requests.get, url,data=data,
                              json=json, params=params, headers=headers))

    async def post(self, url, file=False, data=None, json=None,
                   params=None, loop=None, headers={}):
        if not loop:
            loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, 
            functools.partial(requests.post, url, data=data,
                              json=json, params=params, headers=headers))
