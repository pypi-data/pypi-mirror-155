from typing import Optional

import requests

from utils.md5 import MD5


class Notificator:
    class TokenType:
        RAW = 'raw'
        MD5 = 'md5'

    def __init__(self, username, token, token_type):
        self.host = 'https://notice.6-79.cn/'
        self.username = username
        self.token_type = token_type
        self.token = self.generate_token(token)

    def set_host(self, host: str):
        self.host = host
        if not self.host.endswith('/'):
            self.host += '/'

    def generate_token(self, token):
        if self.token_type == self.TokenType.RAW:
            return token
        if self.token_type == self.TokenType.MD5:
            return MD5.get(token)
        raise ValueError('unrecognized token type')

    def _send(self, data: dict, channel: str):
        del data['self']

        with requests.post(
            url=self.host + channel,
            json=data,
            headers=dict(
                Auth=f'{self.username}${self.token}',
            )
        ) as resp:
            return resp.json()

    def bark(
            self,
            uri: str,
            content: str,
            title: Optional[str] = None,
            sound: Optional[str] = None,
            icon: Optional[str] = None,
            group: Optional[str] = None,
            url: Optional[str] = None,
    ):
        return self._send(data=locals(), channel='bark')

    def sms(
            self,
            phone: str,
            content: str,
    ):
        return self._send(data=locals(), channel='sms')

    def mail(
            self,
            mail: str,
            content: str,
            subject: Optional[str] = None,
            appellation: Optional[str] = None,
    ):
        return self._send(locals(), channel='mail')
