from citation_comparison import read_PWCjson
import pytest
import numpy as np


'''
The test script will have 6 functions, each testing different functionality of the read_PWCjson function. When testing, 6 tests will be performed and if all goes according to plan, testing should result in 4 tests passed.
'''


@pytest.mark.load_missing
def test_file_load_missing_url_file():
    '''Test if the function raises the exception if nonexisting URL_file name is passed as parameter.'''

    with pytest.raises(ValueError) as excinfo:
        read_PWCjson.read_PWCjson("non-existing_file.json", "abstracts.json")

    assert "urls_text file does not exist" in str(excinfo.value)


@pytest.mark.load_missing
def test_file_load_missing_abs_file():
    ''' Test if the function raises the exception if nonexisting ABSTRACT_file name is passed as parameter. '''
    
    with pytest.raises(ValueError) as excinfo:
        read_PWCjson.read_PWCjson('urls.json', "non-existing_file.json")

    assert "abstracts_text file does not exist" in str(excinfo.value)


@pytest.mark.name_json
def test_file_name_json_url_file():
    # Test if the URL_file name is ".json" format
    with pytest.raises(ValueError) as excinfo:
      	read_PWCjson.read_PWCjson("urls.txt", 'abstracts.json')
    assert "Not correct json file in urls_text" in str(excinfo.value)


@pytest.mark.name_json
def test_file_name_json_abs_file():
    # Test if the Abstract_file name is ".json" format
    with pytest.raises(ValueError) as excinfo:
	      read_PWCjson.read_PWCjson('urls.json', 'abstracts.txt')
    assert "Not correct json file in abstracts_text" in str(excinfo.value)



@pytest.mark.file_good
def test_file_return_good():
    # Test if the URL_file//Abs_file has enough rows
    paper_code, paper_abs = read_PWCjson.read_PWCjson('urls.json', 'abstracts.json')
    assert (len(paper_code) > 30000) & (len(paper_abs) > 50000)
        # there should be 37,480 rows for URL_file
        # there should be 133,824 rows for abs_file
     
  
@pytest.mark.file_list
def test_file_return_list():
    # Test if the returned URL_file/Abs_file  is "list" 
    paper_code, paper_abs = read_PWCjson.read_PWCjson("urls.json", "abstracts.json")
    assert (type(paper_code) == list) & (type(paper_abs) == list)
        
       

