import os
import re
import requests
import time
from bs4 import BeautifulSoup as BS 


from .static import StaticSpell
from .dynamic import DynamicSpell

def WebSpell(url, **kwargs):
    if 'browser' in kwargs or 'ghost' in kwargs:
        ghost = kwargs['ghost'] if 'ghost' in kwargs else False
        browser = kwargs['browser'] if 'browser' in kwargs else 'chrome'
        driver_path = kwargs['driver_path'] if 'driver_path' in kwargs else None
        return DynamicSpell(url=url, driver_path=driver_path, ghost=ghost, browser=browser)
    else:
        return StaticSpell(url=url)

# class WebSpell:
#     # Initializes a StaticSpell (requests) or DynamicSpell (selenium)
#     def __init__(self, url, **kwargs):
#         self.url = url
#         self.keys = kwargs
#         return self.cast()

#     def cast(self):

            

        


