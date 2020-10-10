# coding=utf-8

def Read_PWCjson(f_code, f_abs):
    """ Read two pwc datasets, one for paper's urls, the other for abstracts.
    
    Args:
    	f_code: the file link for urls
    	f_abs:	the file link for abstracts
    Returns:
    	paper_code: raw urls' data
    	paper_abs:  raw abstracts' data
    """
    #return(paper_code, paper_abs)

def process_PWC( paper_code, paper_abs ):
    """ 
	Process pwc datasts using the following steps.
     1) process "paper_code": mentioned_in_paper" == True
     2) process "paper_code": remove duplicates
     3) merge "paper_code" with "paper_abs"
    
    Args:
        paper_code: raw urls' data
        paper_abs:  raw abstracts' data
        
    Returns:
        pwc_sub: merged (intersected) papers with url+abs
    """
    #return pwc_sub
    

def Read_DBLPjson(file):
    """ Read large DBLP citation data (skip redundant abstracts info).
    
    Args: 
        file: the file link of DBLP data
    
    Returns:
        dblp: raw dblp data without abstract info
    """
    #return dblp


def process_DBLP( dblp ):
    """ Process dblp data with the following steps.
    1) extract useful attributes, such as "n_citation".. 
    
    Args:
        dblp: raw dblp data without abstract info
    
    Returns:
        dblp_sub: processed dblp data with selected features
    """
    #return dblp_sub

def merge_PWC_DBLP(pwc_sub, dblp_sub):
    """ Left join paper_code_abs with dblp_sub using common ("title" & "year").
    
    Args:
        pwc_sub: processed dataset 1 (papers with url+abs)
        dblp_sub: processed dataset 2 (dblp_with selected features)

    Returns:
        pwc_dblp_trt: cleaned treatment data (with urls)
    """
    #return pwc_dblp_trt

def gen_Control(paper_code, paper_abs, dblp):
    """ Generate control group.
    
    Args:
        paper_code: raw urls' data
        paper_abs:  raw abstracts' data
        dblp: raw dblp data without abstract info
        
    Returns:
        pwc_dblp_con: cleaned controled data (without urls)
    """
    #return pwc_dblp_con


def matching(pwc_dblp_trt, pwc_dblp_con):
    """ For each treated item in "pwc_dblp_trt". 
        select a matched item as control
   
    Args:
        pwc_dblp_trt: cleaned treatment data (with urls)
        pwc_dblp_con: cleaned controled data (without urls)
    
    Returns:
        matched_dta: the dataset with treated and control items.
    """
    #return matched_dta

