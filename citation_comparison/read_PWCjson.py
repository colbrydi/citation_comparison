import json
import gzip
import os


def read_PWCjson(f_code, f_abs):
    """ Read two pwc datasets, one for paper's urls, the other for abstracts.
    
    Args:
    	f_code: the filename for urls
    	f_abs:	the filename for abstracts
    Returns:
    	paper_code: raw urls data
    	paper_abs:  raw abstracts data
    """
    
    ## 1) whether the filename are in the dir
    if not os.path.isfile(f_code):
      raise ValueError("Input urls_text file does not exist: {0}. I'll quit now.".format(f_code))
    
    if not os.path.isfile(f_abs):
      raise ValueError("Input abstracts_text file does not exist: {0}. I'll quit now.".format(f_abs))
    
    ## 2) whether both filenames include ".json" 
    if f_code[-5:]  != '.json':
    	raise ValueError("Not correct json file in urls_text input file.")
    if f_abs[-5:]  != '.json':
    	raise ValueError("Not correct json file in abstracts_text input file.")
    
    ## load the data
    with open(f_code, 'rb') as f:
    	gzip_a = gzip.GzipFile(fileobj = f)         # unzip
    	paper_code: list = json.load(gzip_a)    # read json file

    with open(f_abs, 'rb') as f:
      gzip_a = gzip.GzipFile(fileobj = f)         
      paper_abs: list = json.load(gzip_a)
    
    return (paper_code, paper_abs)