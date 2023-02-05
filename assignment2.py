import argparse
import urllib.request
import logging
import datetime

def downloadData(url):
    """Downloads the data"""
    with urllib.request.urlopen(url) as response:
        response = response.read().decode('utf-8')
    
    # return the data
    return response

def processData(file_content, logger):
    '''
    turning the file_content into a dictionary named personData
    with {id: (name,birthday)}
    '''
    # split the file_content into lines
    # skip the header line
    data_list = file_content.splitlines()
    data_list.pop(0)

    # creating the personData dictionary
    personData = {}
    for index, data in enumerate(data_list, start=2):
        [id, name, birthday] = data.split(',')
        try:
            [day,month,year] = birthday.split('/')
            birthday_date = datetime.datetime(int(year), int(month), int(day))
            personData[int(id)] = (name, birthday_date)
        except:
            logger.error("Error processing line #{} for ID #{}".format(index, id))
    # return the personData dictionary        
    return personData

def displayPerson(id, personData):
    '''
    takes an user id to look up the user's name and birthday
    display the user's id, name and birthday
    '''
    try:
        [name, birthday] = personData[id]
        print("Person #{} is {} with a birthday of {}".format(id, name, birthday.date()))
    except:
        print("No user found with that id")
    

def main(url):
    print(f"Running main with URL = {url}...")

    # downloading the content from the url
    data = downloadData(url)

    # logging
    assignment2 = logging.getLogger('assignment2')
    assignment2.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(message)s')
    file_handler = logging.FileHandler('errors.log')
    file_handler.setFormatter(formatter)
    assignment2.addHandler(file_handler)

    # creating a personData dictionary from the downloaded data
    personData = processData(data, assignment2)

    # prompt to enter user id and display the person's information
    # exit the promgram when id is invalid
    input_id = 1
    while input_id > 0:
        print('Please enter an id:')
        input_id = int(input())
        displayPerson(input_id, personData)
    print('Goodbye!')


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
