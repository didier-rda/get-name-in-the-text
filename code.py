import spacy
import os
import re
import sys
import subprocess
import pickle

def get_path_to_project_dir(os_getcwd):
    '''
    get the major project dirpath to model 
    '''
    req = r'\w*.{0,100}get-name-in-the-text'
    
    path = re.findall(req, os_getcwd)[0]    
    #path.replace('model-minutes-of-hearing-data-extraction')
    return path

def write_obj(obj_to_write, filename, path='/data/interim', type_ = '.bin'):
    project_root_path = get_path_to_project_dir(os.getcwd())
    full_path = project_root_path + '/' + path + '/' + filename + type_
    # open a file, where you ant to store the data
    file_obj = open(full_path, 'wb')
    pickle.dump(obj_to_write, file_obj)

def read_obj(filename,path='/data/interim', type_ ='.bin'):
    project_root_path = get_path_to_project_dir(os.getcwd())
    full_path = project_root_path + '/' + path + '/' + filename + type_
    if (os.path.isfile(full_path)):
        file_obj = open(full_path,'rb')           # dump information to that file
    else:
        print(f'file {full_path} dosent exist')
    return(pickle.load(file_obj))


def download_model_spacy(size='sm'):
    '''
    download from spacy portuguese repo.
    '''
    # download to model/spacy.bin
    cmd = 'python -m spacy download pt_core_news_' + size
    p = subprocess.Popen(cmd, stdin=None, stdout=None, shell=True).wait()
    if p == 0:
        print("\npt_core_news_"+ size + "successfully downloaded.\n")
    else:
        print("\nfailed to download pt_core_news_+size\n")

def load_model(filename='model_cnn_', size='sm', path='/models', type_= '.bin'):


    root_path = get_path_to_project_dir(os.getcwd())
    full_path = root_path + path + '/' + filename + size + type_

    if (os.path.isfile(full_path)):
        nlp = read_obj(filename + size, path='/data/model', type_=type_)
    else:
        nlp = spacy.load("pt_core_news_" + size)
        write_obj(nlp, filename + size, path='/data/model',type_=type_)

    return nlp
def get_name(str_):
#    nlp = spacy.load("pt_core_news_sm")
    nlp = load_model()
    doc = nlp(str_)
    set_names = set()
    for ent in doc.ents:
        if ent.label_ == 'PER':
            set_names.add(ent.text)
    return set_names

if __name__ == '__main__':
    #download_model_spacy()
    text = input('insert text:')
    print(f'found this Brazilian names:{get_name(text)}')
