import requests
from askdata.askdata_client import *

### function for testing login
def test_login(username, password, domain):
    url = "https://api.askdata.com/security/domain/" + domain + "/oauth/token"

    payload = "grant_type=password&username=" + username + "&password=" + password

    headers = {'authority': "api.askdata.com",
               'accept': "application/json, text/plain, */*",
               'accept-language': "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7,ar;q=0.6",
               'authorization': "Basic c21hcnRhZ2VudDpzbWFydGFnZW50", 'content-type': "application/x-www-form-urlencoded", 
               'origin': "https://app.askdata.com",
               'referer': "https://app.askdata.com/",
               'sec-ch-ua-mobile': "?1",
               'sec-ch-ua-platform': "Android", 
               'sec-fetch-dest': "empty", 
               'sec-fetch-mode': "cors", 
               'sec-fetch-site': "same-site", 
               'user-agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Mobile Safari/537.36"}

    response = requests.request("POST", url, data=payload, headers=headers)

    return response
    
    
### function for testing authentication    
def run_authentication_test(credentials_to_test):
    
    global message_body, total_passed, total_failed
    
    message_body = ""

    message_body += "<h1>Authentication Testing</h1> Tests passed: xxxxx/" + str(len(credentials_to_test.keys())) + " ------- Fails: yyyy %" + "\n \n "

    total_passed, total_failed, test_passed, test_failed = 0, 0, 0, 0


    for user in credentials_to_test:

        psw = credentials_to_test[user][0]

        domain = credentials_to_test[user][1]


        try:
            assert test_login(user, psw, domain).status_code == 200

            message_body += "<br><b style='color:green;'>Login Successful</b> for " + user + " in domain " + credentials_to_test[user][1] + " \n "

            test_passed += 1
            
            total_passed += 1

        except AssertionError:

            message_body += "<br><b style='color:red;'>Login Failed</b> for " + user + " in domain " + credentials_to_test[user][1]

            test_failed += 1
            
            total_failed += 1
            

    message_body = message_body.replace("xxxxx", str(test_passed)).replace("yyyy", str(round(test_failed*100 / (test_failed + test_passed), 2)))
    

    return message_body


def get_message_body():
    
    return message_body



## initialize testing for specific Agent given the previous credentials tested
def initialize_agent_test(username = '', password = '', token = None, agent_slug = ''):
    
    global message_body, agent_id, test_passed, test_failed, glob_token
    
    
    test_passed, test_failed = 0, 0
    
    if token:
        askdata = Askdata(token = token, env = 'prod')
        
        glob_token = token
        
    else:
        askdata = Askdata(username = username, password = password, env = 'prod')
            
        glob_token = test_login(username, password, "askdata").json()["access_token"]

    agent = askdata.agent(agent_slug)

    agent_name = agent._agent_name

    agent_id = agent._agentId

    message_body = get_message_body()

    message_body += "<h2>AGENT {}</h2> \n <i>https://app.askdata.com/{}</i> <b>id</b>: {} <br>Tests passed: xxxxx ------- Fails: yyyy % \n \n ".format(agent_name, agent_slug, agent_id)
    
    return message_body
    
    
def get_agent_id():
    
    return agent_id

def get_test_passed():
    
    return test_passed

def get_test_failed():
    
    return test_failed

def get_total_passed():
    
    return total_passed

def get_total_failed():
    
    return total_failed

def get_glob_token():
    
    return glob_token
    
### function for running queries


def run_query(token, agent_id, query):
    
    url = "https://api.askdata.com/smartfeed/askdata/preflight"

    querystring = {"agentId": agent_id, "lang":"en"}

    payload = "{\"text\":\"" + query + " \"}"

    headers = {'authority': "api.askdata.com", 'accept': "application/json, text/plain, */*", 
               'accept-language': "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7,ar;q=0.6", 'authorization': "Bearer " + token,      
               'content-type': "application/json",      
               'origin': "https://app.askdata.com",      
               'referer': "https://app.askdata.com/",      
               'sec-ch-ua-mobile': "?1",      
               'sec-ch-ua-platform': "Android",      
               'sec-fetch-dest': "empty",      
               'sec-fetch-mode': "cors",      
               'sec-fetch-site': "same-site",      
               'user-agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Mobile Safari/537.36"}


    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

    return response
  
    
    
#check the number of cards
def num_of_cards(response): 
    
    return (len(response.json()))


#check the component type in a specific position
def check_component(response, comp = 0):
    
    return response.json()[0]['attachment']['body'][comp]['component_type']


#check the name of the column in a table component in a specific position
def check_col_names(response, comp = 0):
    
    return set(response.json()[0]['attachment']['body'][comp]['details']['columns'])


#check column filtered and its value in a specific position (i.e. country in Italy)
def check_filter(response, comp = 0, filter_number = 0):
    
    return response.json()[0]['attachment']['body'][comp]['details']['filters'][filter_number]['field'], response.json()[0]['attachment']['body'][comp]['details']['filters'][filter_number]['operator'], response.json()[0]['attachment']['body'][comp]['details']['filters'][filter_number]['values']




## run the query test

def run_test(#username = '', password = '', token = '', 
             query = '',
             
            n_cards = None, check_component_types = None, 
             check_table_columns = None, check_filters_existance = None 
           
            ):
    
    global message_body, test_passed, test_failed, total_passed, total_failed, glob_token
    
    agent_id = get_agent_id()
    
    message_body = get_message_body()
    
    total_passed = get_total_passed()
    
    total_failed = get_total_failed()
    
    test_passed = get_test_passed()
    
    test_failed = get_test_failed()
    
    '''
    if token == '':
    
        token = test_login(username, password, "askdata").json()["access_token"]
    '''
    
    glob_token = get_glob_token()
    
    response = run_query(glob_token, agent_id, query)
    
    #this print is helpful for debugging code00
    #print(response.json()[0]['attachment']['body'])
    
    try:
        assert response.status_code == 200
        
        print('Response 200')
        
        if n_cards:
        
            assert num_of_cards(response) == n_cards
            
            print('Number of cards expected passed')
        
        
        if check_component_types:
            
            for position, component in enumerate(check_component_types):
                
                assert check_component(response, position) == component
                
            print('Check for Components type passed')
            
                
        if check_table_columns:
            
            for position, columns in enumerate(check_table_columns):
                
                if columns != []:
                
                    assert check_col_names(response, position) == set(columns)               
            
            print('Check for column names in table passed')
            
    
        if check_filters_existance:
            
            for position, filters in enumerate(check_filters_existance):
                
                if filters != []:
                    
                    for filter_number, f in enumerate(filters):
                        
                        
                    
                        assert check_filter(response, position, filter_number) == f
                
            print('Check for filters passed')
            
            
        message_body += "<br><b style='color:green;'>Test Successful</b> for query: {}".format(query)
        
        test_passed += 1
        
        total_passed += 1
        
        print('All Check Passed')
        
        
    except AssertionError:
    
        message_body += "<br><b style='color:red;'>Test Failed</b> for query: {}".format(query)
    
        test_failed += 1
        
        total_failed += 1
        
        print('Test Failed')
        
    
    
    return message_body


## finalize agent test message body

def finalize_agent_test():
    
    global test_passed, test_failed, message_body
    
    test_passed = get_test_passed()

    test_failed = get_test_failed()
    
    message_body = get_message_body()
    
    message_body = message_body.replace("xxxxx", str(test_passed) + "/" + str((test_failed + test_passed)) ).replace("yyyy", str(round(test_failed*100, 2) / (test_failed + test_passed)))
    
    return message_body
