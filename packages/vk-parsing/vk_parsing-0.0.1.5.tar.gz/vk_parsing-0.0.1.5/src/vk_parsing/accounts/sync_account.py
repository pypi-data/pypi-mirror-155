from .account import ParsingAccount
from vk_parsing.exceptions import *
from vk_parsing.api import VkApiSimple
import os
import datetime
import time
import random

def forward(response):
    return response

class VkApiAccount(ParsingAccount):
    def __init__(self, login, token, cooldown, logger):
        self.vk_session = None
        self.last_access = None
        super().__init__(login, token, cooldown, logger)    

    def auth(self):
        self.vk_session = VkApiSimple(self.token)

    def check(self):
        if (self.vk_session == None):
            raise RuntimeError("Auth() was not called")
        self.can_single = True
        self.can_bucket = True
    
    def error_filter(self, ex):
        try:
            if ex.code in [5, 37]: # Errors that should stop parsing
                raise StopParsingError(f"Parsing stopped on account {self.login}, error: {str(ex)}")
            if not ex.code in [6, 9, 14, 29]: # Errors that should drop single account
                raise ex 
        except Exception: # HTTP error, just raise
            raise ex
        return

    def _obey_cooldown(self):
        if (self.last_access == None):
            self.last_access = datetime.datetime.now()
        now_time = datetime.datetime.now()
        difftime = now_time - self.last_access
        if (difftime.total_seconds() < self.cooldown):
            time.sleep(self.cooldown + self._exactly_small_random(self.cooldown) - difftime.total_seconds())
        self.last_access = datetime.datetime.now()

    def _exactly_small_random(self, core_value):
        return core_value / random.randint(1, 100)

    def method(self, method_name, method_args={}, callback=forward, callback_args=(), callback_kwargs={}):
        self._obey_cooldown()
        if (self.vk_session == None):
            raise RuntimeError("Auth() was not called")
        drop = False
        try:
            try:
                vk_response = self.vk_session.method(method_name, params=method_args)
            except Exception as ex:
                self.logger.debug(f"Error with {self.login}: {str(ex)}, trying again")
                self.error_filter(ex)
                self.logger.debug("This error passed filter, dropping account")
                drop = True
        except Exception as ex: # Case we raise the error
            self.logger.debug("This error didn't pass filter, raising this")
            raise
        if drop: # Case we drop the account
            raise BrokenAccountError("")
        try: # Case we call the callback
            return callback(vk_response, *callback_args, **callback_kwargs)
        except Exception as ex:
            self.logger.error(f"Error while calling callback: {str(ex)}")
            raise
