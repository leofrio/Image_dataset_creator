
import os
from platform import architecture 
from  bs4 import * 
import requests 
import json 
import re 
import shutil
import urllib.request 
import math 
import string as String  
olddirectory=os.path.dirname(os.path.realpath(__file__)) + '/datasets'
print('this is the directory current')
print(olddirectory)
ds_name=input("choose the name of the new dataset you are creating/want to use \n")
directory=os.path.join(olddirectory,ds_name)
print(directory)
usr_agent = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/105.0.5195.127 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}
letters=list(String.ascii_lowercase) 

def getdata(url): 
    r = requests.get(url,stream=True) 
    return r.text  

def download_image(url, file_path, file_name):
    fname=file_name + '.jpg' 
    full_path = os.path.join(file_path,fname)
    
    urllib.request.urlretrieve(url, full_path)


GOOGLE_IMAGE = \
    'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'
if not os.path.exists(directory): 
    os.makedirs(directory) 
    print('directory %s was sucessfully created and its located at %s' % (ds_name,directory))  
while True: 
    print('current dataset: %s' % ds_name)
    amt_folders=len(os.listdir(directory))  
    amt_img_each_folder=0 
    if amt_folders != 0: 
        amt_img_each_folder=len(os.listdir(os.path.join(directory,os.listdir(directory)[0])))
    action=input('''what do you want to do? choose one of the following: \n 
    0-create new dataset from 0 using google image search \n 
    1-add new folders named with the new google image searches you want to add \n  
    2- see a dataset you've created \n 
    3-create new dataset/change directory to another dataset \n
    4-alter size of images for dataset \n
    5-exit \n 
    please type the number corresponding to what you want to do \n''') 
    if action == '0': 
        desired=input('alright! now type all the searches you want to do separated by comma(ex: Luffy,Goku) \n') 
        desired=desired.split(',')  
        desired=list(map(lambda a: a.lstrip(),desired))
        desired=list(map(lambda a: a.rstrip(),desired))
        desired=list(map(lambda a: a.replace(" ",'_'),desired))
        n_images=int(input('how many images do you want?'))
        for wsearch in desired:  
            current_dic= os.path.join(directory,wsearch.lower())
            if not os.path.exists(current_dic): 
                os.makedirs(current_dic)  
            if len(os.listdir(current_dic)) == n_images: 
                continue  
            wsearch=wsearch.replace("_"," ")
            search_url=getdata(GOOGLE_IMAGE + 'q=' +wsearch)
            amount_of_times=math.ceil(n_images/20.0) 
            if amount_of_times > 26: 
                amount_of_times=26 
            search_urls=[] 
            counter=0
            search_urls.append(search_url) 
            limit_reached=False
            for i in range(0,amount_of_times): 
                search_urls.append(getdata(GOOGLE_IMAGE + 'q=' +wsearch + ' %c' % letters[i])) 
            search_urls.pop(1)
            for variations in search_urls:
                soup=BeautifulSoup(variations,'html.parser')  
                imglist=[] 
                for item in soup.select('img',limit=n_images):
                    imglist.append(item['src']) 
                imglist.pop(0)
                for image in imglist: 
                    name=wsearch +str(counter)
                    download_image(image,current_dic,name) 
                    counter += 1 
                    if counter == n_images: 
                        limit_reached=True 
                        break
                if limit_reached: 
                    break;
    elif action == '1': 
        if len(os.listdir(directory)) ==0: 
            print('you havent added anything to this directory yet!') 
            continue
        desired=input('alright! now type the new searches you want to add, the number of images will be the same as the other searches \n') 
        desired=desired.split(',') 
        desired=list(map(lambda a: a.lstrip(),desired))
        desired=list(map(lambda a: a.rstrip(),desired))
        desired=list(map(lambda a: a.replace(" ",'_'),desired))
        n_images=len(os.listdir(os.path.join(directory,os.listdir(directory)[0])))
        for wsearch in desired: 
            current_dic= os.path.join(directory,wsearch.lower())
            if not os.path.exists(current_dic): 
                os.makedirs(current_dic)  
            if len(os.listdir(current_dic)) == n_images: 
                continue  
            wsearch=wsearch.replace("_"," ")
            search_url=getdata(GOOGLE_IMAGE + 'q=' +wsearch)
            amount_of_times=math.ceil(n_images/20.0) 
            if amount_of_times > 26: 
                amount_of_times=26 
            search_urls=[] 
            counter=0
            search_urls.append(search_url) 
            limit_reached=False
            for i in range(0,amount_of_times): 
                search_urls.append(getdata(GOOGLE_IMAGE + 'q=' +wsearch + ' %c' % letters[i])) 
            search_urls.pop(1)
            for variations in search_urls:
                soup=BeautifulSoup(variations,'html.parser')  
                imglist=[] 
                for item in soup.select('img',limit=n_images):
                    imglist.append(item['src']) 
                imglist.pop(0)
                for image in imglist: 
                    name=wsearch +str(counter)
                    download_image(image,current_dic,name) 
                    counter += 1 
                    if counter == n_images: 
                        limit_reached=True 
                        break
                if limit_reached: 
                    break; 
    elif action == '2': 
        print(
    '''current dataset: %s \n  
    path to dataset: %s
    amount of sub-folders: %d \n 
    amount of images in each folders %d \n  
    total files: %d  
    total_size: %s''' % (ds_name,directory,amt_folders,amt_img_each_folder,amt_folders*amt_img_each_folder,os.path.getsize(directory))) 
    elif action == '3': 
        ds_name=input("choose the name of the new dataset you are creating/want to use\n") 
        olddirectory='datasets' 
        directory=os.path.join(olddirectory,ds_name) 
        if not os.path.exists(directory): 
            os.makedirs(directory)
            print('Directory %s at path %s was just created!' % (ds_name,directory))
        print("directory changed to %s at path %s " % (ds_name,directory))  
    elif action == '4':
        if len(os.listdir(directory)) == 0:
            print('No subfolders available in the current dataset.')
            continue

        # Find the subfolder with the least number of images
        min_images_folder = min(os.listdir(directory), key=lambda subfolder: len(os.listdir(os.path.join(directory, subfolder))))

        # Get the number of images in the subfolder with the least images
        min_images_count = len(os.listdir(os.path.join(directory, min_images_folder)))

        # Set all other subfolders to have the same number of images
        for subfolder in os.listdir(directory):
            if subfolder != min_images_folder:
                current_subfolder = os.path.join(directory, subfolder)

                # Get the current number of images in the subfolder
                current_images_count = len(os.listdir(current_subfolder))

                # Remove excess images
                if current_images_count > min_images_count:
                    excess_images = current_images_count - min_images_count
                    for i in range(excess_images):
                        os.remove(os.path.join(current_subfolder, os.listdir(current_subfolder)[i]))

        print('All subfolders now have the same number of images as the one with the least images (%d).' % min_images_count)
    elif action == '5': 
        break;  


