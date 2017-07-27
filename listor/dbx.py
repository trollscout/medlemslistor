'''
Created on 26 juli 2017

@author: hakan
'''

import dropbox
import os

OAUTH_KEY = os.getenv('DBX_OAUTHKEY', 'P_f0hApputAAAAAAAAABxl2HC2JCkUP6lkYH3btQxjlhXT-Cve8xg-IRzNB4qJaq')
BASE_DIR = "/Aktuella kontakt- och e-postlistor/"

def save_file(fname, data):
        dbx = dropbox.Dropbox(OAUTH_KEY)
        dbx.files_upload(data, BASE_DIR+fname, dropbox.files.WriteMode.overwrite, mute=True)
