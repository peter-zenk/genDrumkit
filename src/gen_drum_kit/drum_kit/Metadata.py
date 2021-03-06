'''
Created on Jun 15, 2020

@author: peter
'''
from dataclasses import dataclass


@dataclass
class Metadata():
    '''
    information about a drum kit
    '''
    version:     str = "0.0.0"
    title:       str = "title"
    image:       str = "path_to_image.png"
    description: str = "short_description"
    license:     str = "Creative Common"
    notes:       str = "long description"
    author:      str = "author_name"
    email:       str = "author_email"
    website:     str = "author_website"

    def __post_init__(self): 
        pass
