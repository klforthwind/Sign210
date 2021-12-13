# sudo pip3 install python-dotenv
# pip3 install python-dotenv
from dotenv import load_dotenv
from os.path import getsize
from os.path import exists
import os

class Downloader():

    def __init__(self):
        if not exists(".env"):
            raise Exception(".env file not found")
        
        load_dotenv()
        self.PY_FILE_DIR = os.getenv('PY_FILE_DIR')

    def download_img(self, filename):
        os.system(f"curl {self.PY_FILE_DIR}/{filename} > {filename}")

    def download(self, filename):
        print(f"File {filename} - Starting Download!!")

        # curl latest file from server
        os.system(f"curl {self.PY_FILE_DIR}/{filename} > temp.py")

        # return on 404 not found
        with open("temp.py") as f:
            line = f.read()
            if "nginx" in line:
                print("404 File Downloaded - Server Down or Other Error?")
                return

        # verify filename exists (in order to diff it)
        if not exists(filename):
            os.system(f"touch {filename}")

        # obtain changes between latest and current file
        changes = os.popen(f"diff {filename} temp.py").read()
        
        # update on change
        if len(changes) != 0:
            print(f"File {filename} - Downloaded / Updated Successfully!!")
            os.system(f"cp temp.py {filename}")
        else:
            print(f"File {filename} - No Differences Detected!!")
        
        # clean up directory
        os.system("rm temp.py")
        print(f"File {filename} - Finished / Cleaned Up!!")
