# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/erik997/dev/python/dhooks-lite/venv/lib/python3.5/site-packages/dhooks_lite/client.py
# Compiled at: 2020-03-31 15:03:01
# Size of source mod 2**32: 5791 bytes
import logging, requests
logger = logging.getLogger(__name__)

class WebhookResponse:
    __doc__ = 'response from a Discord Webhook'

    def __init__(self, headers: dict, status_code: int, content: dict=None) -> None:
        self._headers = dict(headers)
        self._status_code = int(status_code)
        self._content = dict(content) if content else None

    @property
    def headers(self) -> dict:
        """response headers"""
        return self._headers

    @property
    def status_code(self) -> int:
        """HTTP status code of the response"""
        return self._status_code

    @property
    def content(self) -> dict:
        """content of the response, e.g. send report
        
        will be empty if not waited for response from Discord
        """
        return self._content

    @property
    def status_ok(self) -> bool:
        """whether the response was ok based on its HTTP status"""
        return self._status_code >= 200 and self._status_code <= 299


class Webhook:
    MAX_CHARACTERS = 2000

    def __init__(self, url: str, username: str=None,
                 avatar_url: str=None) -> None:
        """Initialize a Webhook object
        
        Parameters
        
        - url: Discord webhook url
        - username: Override default user name of the webhook
        - avatar_url: Override default avatar icon of the webhook with image URL

        """
        if not url:
            raise ValueError('url must be specified')
        self._url = url
        self._username = username
        self._avatar_url = avatar_url

    @property
    def url(self) -> str:
        return self._url

    @property
    def username(self) -> str:
        return self._username

    @property
    def avatar_url(self) -> str:
        return self._avatar_url

    def execute(self, content: str=None,
                embeds: list=None,
                tts: bool=None,
                username: str=None,
                avatar_url: str=None,
                wait_for_response: bool=False) -> WebhookResponse:
        """Posts a message to this webhook
        
        Parameters
        
        - content: Text of this message
            
        - embeds:List of Embed objects to be attached to this message
            
        - tts: Whether or not the message will use text-to-speech
            
        - username: Overrides default user name of the webhook
        
        - avatar_url: Override default avatar icon of the webhook with image URL
        
        - wait_for_response: Whether or not to wait for a send report 
        from Discord (defaults to ``False``). 
        
        Exceptions
                
        - ValueError: on invalid input

        - ConnectionError: on network issues
        
        - Timeout: if timeouts are exceeded

        - TooManyRedirects: if configured redirect limit is exceeded
        
        Returns
               
        - response from webhook as WebhookResponse object
         
        """
        if not content and not embeds:
            raise ValueError('need content or embeds')
        payload = dict()
        self._set_content(payload, content)
        self._set_embeds(payload, embeds)
        self._set_username(payload, username)
        self._set_avatar_url(payload, avatar_url)
        self._set_tts(payload, tts)
        logger.debug('Payload to %s: %s', self._url, payload)
        res = requests.post(url=self._url, params={'wait': wait_for_response}, json=payload)
        try:
            content_returned = res.json()
        except ValueError:
            content_returned = None

        response = WebhookResponse(headers=res.headers, status_code=res.status_code, content=content_returned)
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug('HTTP status code: %s', response.status_code)
            logger.debug('Response from Discord: %s', response.content)
        elif not response.status_ok:
            logger.warning('HTTP status code: %s', response.status_code)
        return response

    def _set_content(self, payload: dict, content: str) -> None:
        if content:
            content = str(content)
            if len(content) > self.MAX_CHARACTERS:
                raise ValueError('content exceeds {}'.format(self.MAX_CHARACTERS))
            payload['content'] = content

    def _set_embeds(self, payload: dict, embeds: list) -> None:
        if embeds:
            if not isinstance(embeds, list):
                raise TypeError('embeds must be of type list')
            for embed in embeds:
                if type(embed).__name__ != 'Embed':
                    raise TypeError('embeds elements must be of type Embed')

            payload['embeds'] = [x.to_dict() for x in embeds]

    def _set_username(self, payload: dict, username: str) -> None:
        if not username and self._username:
            username = self._username
        if username:
            payload['username'] = str(username)

    def _set_avatar_url(self, payload: dict, avatar_url: str) -> None:
        if not avatar_url and self._avatar_url:
            avatar_url = self._avatar_url
        if avatar_url:
            payload['avatar_url'] = str(avatar_url)

    def _set_tts(self, payload: dict, tts: bool) -> None:
        if tts:
            if not isinstance(tts, bool):
                raise TypeError('tts must be of type bool')
            payload['tts'] = tts