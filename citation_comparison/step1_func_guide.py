'''Description of step one'''

import json
import gzip
import os
import re
import pickle
from itertools import compress   # compress(list, boolean)
from collections import Counter
import numpy as np

# !pip install ijson
import ijson

def read_pwcjson(f_code, f_abs):
    """ Read two pwc datasets, one for paper's urls, the other for abstracts.
    Args:
        f_code: the filename for urls
        f_abs: the filename for abstracts
    Returns:
        paper_code: raw urls data
        paper_abs:  raw abstracts data
    """
    ## 1) whether the filename are in the dir
    if not os.path.isfile(f_code):
        raise ValueError("Input urls_text file does not exist: {0}.\
                          I'll quit now.".format(f_code))
    if not os.path.isfile(f_abs):
        raise ValueError("Input abstracts_text file does not exist: {0}.\
                          I'll quit now.".format(f_abs))
    ## 2) whether both filenames include ".json"
    if f_code[-5:]  != '.json':
        raise ValueError("Not correct json file in urls_text input file.")
    if f_abs[-5:]  != '.json':
        raise ValueError("Not correct json file in abstracts_text input file.")
    ## load the data
    with open(f_code, 'rb') as file:
        gzip_a = gzip.GzipFile(fileobj = file)         # unzip
        paper_code: list = json.load(gzip_a)    # read json fill
    with open(f_abs, 'rb') as file:
        gzip_a = gzip.GzipFile(fileobj = file)
        paper_abs: list = json.load(gzip_a)
    return (paper_code, paper_abs)

def process_pwc(paper_code, paper_abs, mention_paper=True):
    """
    Process pwc datasts using the following steps.
     1) process "paper_code": mentioned_in_paper" == True/False
     2) process "paper_code": remove duplicates
     3) merge "paper_code" with "paper_abs"
    Args:
        paper_code: raw urls' data
        paper_abs:  raw abstracts' data
    Returns:
        pwc_sub: merged (intersected) papers with url+abs
    """
    ### 1) process "paper_code": mentioned_in_paper" == True
    paper_code = [x for x in paper_code if x['mentioned_in_paper'] == mention_paper ]
    
    ### 2) process "paper_code": remove duplicates
    #print( len(paper_code) )
    paper_title = [x['paper_title'] for x in paper_code]
    #print( len(np.unique(paper_title)) )   
    title_index = []
    for title, count in Counter(paper_title).items():
        if count > 1:
            title_index.append(title)

    duplicated_items = []
    for title in title_index:
        item_l = []
        for item in paper_code:
            if item['paper_title'] == title:
                item_l.append(item)
        duplicated_items.append(item_l)
#     print("The number of unique titles in duplicated_items: ",
#           len(duplicated_items), '\n\t',
#           sorted(Counter([len(item) for item in duplicated_items]).items(),
#                  key=lambda x:x[0], reverse= True))

    ##Only extracted duplicated items with same github-parent url.
    ##for example, 'github/AAA/t1' and 'github/AAA/t2', 
    ##both have same parent "github/AAA"
    duplicated_items_clean = []
    for item in duplicated_items:
        item_repo = [re.search(r'github.com/(.*?)$', x['repo_url']).group(1) for x in item]
        item_repo = [x.split('/')[0] if len(x.split('/'))>0 else x for x in item_repo]
        if len(np.unique(item_repo)) == 1:
            item[0]['repo_url'] = 'https://github.com/' + item_repo[0]
            duplicated_items_clean.append(item[0])
#     print("The number of unique titles in duplicated_items_clean \
#           (not duplicated items here): \n\t",
#           len(duplicated_items_clean) )

    ##combine "paper_code_unique" and "duplicated_title_clean"
    ##  --> get "paper_code_upd"
    title_unique_index = [title for title, count in Counter(paper_title).items() 
                          if count == 1]
    paper_code_unique = [item for item in paper_code if item['paper_title']
                         in title_unique_index]
    # print(len(paper_code_unique))
    # generate "paper_code_upd"
    paper_code_upd = paper_code_unique + duplicated_items_clean

    ### 3) merge "paper_code" with "paper_abs"
    urls = [x['paper_url'] for x in paper_code_upd]
    pwc_sub = [item for item in paper_abs if item['paper_url'] in urls]
#     print( len(pwc_sub) )
    return pwc_sub

def remove_index_abs(dblp_l):
    '''Remove 'index_abstracts' info'''
    for prefix, event, value in dblp_l:
        if prefix.startswith('item.indexed_abstract'):
            continue
        yield prefix, event, value
    
def read_dblpjson(file):
    """ Read large DBLP citation data (skip redundant abstracts info).
    Args:
        file_link: the file link of DBLP data
    Returns:
        dblp: raw dblp data without abstract info
    """
    #import ijson
    ### 1) read
    dta_dblp = ijson.parse(open(file, 'r', encoding="utf8"))
    ### 2) remove redundant abstracts info by applying func "remove_index_abs()"
#     dblp = remove_index_abs(dta_dblp)
    return remove_index_abs(dta_dblp)

def process_dblp(dblp):
    """ Process dblp data with the following steps. extract useful attributes,\ 
        such as "n_citation"..
    Args:
        dblp: raw dblp data without abstract info
    Returns:
        dblp_sub: processed dblp data with selected features
    """
    for prefix, event, value in dblp:
        if (prefix, event) == ('item', 'start_map'):
            yield prefix, event, value
    #   record = dict()

    ## extract: id, title, authors_name/id/org, venue_raw/id/type
    ##          year, n_citation,doc_type, publisher, volume, issue, doi,
    ##          fos_name/weight, references_item
    ## note: this raw data does not include "language" or "url"....
        elif (prefix, event) == ('item.id', 'number'):
            yield prefix, event, value
        elif prefix == 'item.title':
            yield prefix, event, value

        elif prefix == 'item.authors.item.name':
            yield prefix, event, value
        elif prefix == 'item.authors.item.id':
            yield prefix, event, value
        elif prefix == 'item.authors.item.org':
            yield prefix, event, value

        elif prefix == 'item.venue.raw':
            yield prefix, event, value
        elif prefix == 'item.venue.id':
            yield prefix, event, value
        elif prefix == 'item.venue.type':
            yield prefix, event, value

        elif prefix == 'item.year':
            yield prefix, event, value
        elif prefix == 'item.n_citation':
            yield prefix, event, value
        elif prefix == 'item.doc_type':
            yield prefix, event, value
        elif prefix == 'item.publisher':
            yield prefix, event, value
        elif prefix == 'item.volume':
            yield prefix, event, value
        elif prefix == 'item.issue':
            yield prefix, event, value
        elif prefix == 'item.doi':
            yield prefix, event, value

        elif prefix == 'item.fos.item.name':
            yield prefix, event, value
        elif prefix == 'item.fos.item.w':
            yield prefix, event, value

        elif prefix == 'item.references.item':
            yield prefix, event, value
#     return dblp_sub
### --> dblp_sub = process_dblp(dblp)

def lowercase_title(dblp_sub):
    '''Lowercase_title for dblp_sub'''
    for prefix, element, value in dblp_sub:
        if prefix == 'item.title':
            value = value.lower() if (value[-1] != '.') else value[:-1].lower()
        yield prefix, element, value
    
def match_title_id(pwc_title, dblp_sub_lt):
    '''Match titles in pwc_sub with dblp data'''
       
    record = dict()
    author_name = []
    author_id = []
    author_org = []

    fos_name = []
    fos_w = []
    ref = []
    # default
    title_match = False

    for prefix, event, value in dblp_sub_lt:
        if (prefix, event) == ('item', 'start_map'):
            ## return results only if "title_match" == True
            if title_match:
                record['authors_name'] = author_name
                record['authors_id'] = author_id
                record['authors_org'] = author_org
                record['fos_name'] = fos_name
                record['fos_w'] = fos_w
                record['ref'] = ref  # references_item
                yield record

            record = dict()
            author_name = []
            author_id = []
            author_org = []

            fos_name = []
            fos_w = []
            ref = []  # references_item

        elif prefix == 'item.id':
            record['id'] = value
    
        elif prefix == 'item.title':
            ## filter title in pwc_title
            if value in pwc_title:
                title_match = True
                record['title'] = value
            else:
                title_match = False
                continue   # --> use "continue" not "break" !!
            # end of filter/match title

        elif prefix == 'item.authors.item.name':
            author_name.append(value)
        elif prefix == 'item.authors.item.id':
            author_id.append(value)
        elif prefix == 'item.authors.item.org':
            author_org.append(value )
      
        elif prefix == 'item.venue.raw':
            record['venue_raw'] = value
        elif prefix == 'item.venue.id':
            record['venue_id'] = value
        elif prefix == 'item.venue.type':
            record['venue_type'] = value
      
        elif prefix == 'item.year':
            record['year'] = value
        elif prefix == 'item.n_citation':
            record['n_citation'] = value
        elif prefix == 'item.doc_type':
            record['doc_type'] = value
        elif prefix == 'item.publisher':
            record['publisher'] = value
        elif prefix == 'item.volume':
            record['volume'] = value
        elif prefix == 'item.issue':
            record['issue'] = value
        elif prefix == 'item.doi':
            record['doi'] = value

        elif prefix == 'item.fos.item.name':
            fos_name.append(value)
        elif prefix == 'item.fos.item.w':
            fos_w.append(value)

        elif prefix == 'item.references.item':
            ref.append(value)
            
   
            
## NOT BE USED!
def merge_pwc_dblp(pwc_sub_trt, dblp_match_cs):
    """ Left join pwc_sub with dblp_sub using common ("title" & "year").
    Args:
        pwc_sub_trt: processed dataset 1 (papers with url+abs), either trt or control
        dblp_match_cs: processed dataset 2 (dblp_with selected features with MATCH titles 
                     in pwc_sub)
    Returns:
        match_trt: cleaned treatment data (with urls)
    """
    
    ## lowercase title for "paper_code_abs_upd"
    for item in pwc_sub_trt:
        if item['title'][-1] != '.':
            item['title'] = item['title'].lower()
        else:
            item['title'] = item['title'][:-1].lower()

    ## match -- get "match_trt"
    match_trt = []
    for code in pwc_sub_trt:  # code: pwc data feature
        for cite in dblp_match_cs:   # cite: citation data feature
            if code['title'] == cite['title']:
                if int(code['date'][:4]) == cite['year']:
                    cite_sub = { key:value for key,value in cite.items()
                                if key in ['id', 'n_citation', 'doc_type', 'publisher',
                                           'volume','issue','doi', 'venue_raw',
                                           'venue_id','venue_type', 'authors_name', 
                                           'authors_id','authors_org',
                                           'fos_name', 'fos_w', 'ref']}
                    match_trt.append( {**code , **cite_sub} )
                    break
    
    ## clean "venue_raw"
    for item in match_trt:
        if 'venue_raw' in item.keys():
            if item['venue_raw'][:7] == 'arXiv: ':
                item['venue_raw'] = item['venue_raw'][7:]
    ### save "match_trt" !!!!
#     with open('match_trt.pkl', 'wb') as out:
#         pickle.dump(match_trt, out)
    return match_trt


# def gen_control(paper_code, paper_abs, dblp):
#     """Generate control group.
#     Args:
#         paper_code: raw urls' data
#         paper_abs:  raw abstracts' data
#         dblp: raw dblp data without abstract info
#     Returns:
#         pwc_dblp_con: cleaned controled data (without urls)
#     """
#     #return pwc_dblp_con
    
