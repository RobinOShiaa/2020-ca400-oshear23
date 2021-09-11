import urllib.request
import csv
import time
import os
import re
DATE = '_' + '_'.join(time.strftime("%m/%d/%Y").split('/'))



THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(f'{THIS_FOLDER}','chromedriver.exe')

def dl_jpg(url, file_path, file_name):
    
    file_name = clean(file_name)
    full_path = file_path + file_name + '.jpg'


    try:
        urllib.request.urlretrieve(url, full_path)
    except(OSError):
        print(full_path)
        return 'error'

    while not os.path.exists(full_path):
        print(full_path)
        print('waiting')
        time.sleep(1)

    return full_path, file_name


def clean(file_name):
    file_name = re.sub('[!,#?;/®%&:*|"{}]'.format("'"), '', file_name).strip()
    print(file_name)
    return file_name



def to_csv(file_path,Data):

        with open(file_path, "w+", newline="") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(["Product", "Image_File_Path","Image_url"])
            for index in Data:
                    f.write("%s,%s,%s\n" % (index[0],index[1],index[2]))

