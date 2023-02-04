# program to scrape google scholar with articles
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import re


# scrape the google scholar file
def extract_scholar_page_local(in_url, ilocal=True):

    # for local file
    if ilocal:
        with open(in_url, encoding="utf8") as fp:
            soup = BeautifulSoup(fp, 'html.parser')

    # for page on internet
    else:
        page = requests.get(in_url)
        soup = BeautifulSoup(page.text, 'html.parser')

    # create emply list to store the data
    ll_data = []

    # extract data
    for item in soup.find_all('div', class_='gs_ri'):
        try:
            try:

                # get the article name
                i_article = item.select('h3')[0].get_text()
                i_article = i_article.replace('[PDF][PDF] ', '')
                i_article = i_article.replace('[HTML][HTML] ', '')

                # get url
                i_url = item.select('a')[0]['href']

                # get the article year
                green_string = item.select_one('.gs_a').get_text()
                match = re.findall(r'\d{4}', green_string)
                match = list(set(match))
                i_year = (' '.join(match))

                # get the author
                i_author = green_string.split("-")[0]
                i_author = re.sub('[^A-Za-z0-9 ,]+', '', i_author)

                # journal
                i_journal = green_string.split("-")[1]
                i_journal = re.sub('[^A-Za-z0-9 ,]+', '', i_journal)

                # green_text
                i_green_text = re.sub('[^A-Za-z0-9 ,.]+', '', green_string)

                # scraped from
                scraped_from = in_url

                # append items
                # i_columns = ['article', 'author', 'year', 'journal', 'url', 'green_text']
                ll_data.append((
                    i_article,                       # article
                    i_author,                        # author': 4,
                    i_year,                          # year
                    i_journal,                       # journal': 5})
                    i_url,                           # url"
                    i_green_text,                    # green text in google
                    scraped_from,                    # scraped from url
                ))


                # soup_int = BeautifulSoup(item)
                # mydivs = soup.findAll('div')
                #
                # # mydivs = soup_int.find_all("div", {"class": "gs_a"})
                # print(mydivs)

            except Exception as e:
                # raise e
                print('error 1')

        except Exception as e:
            # raise e
            print('error 2')

    return ll_data

# Get the list of files
def get_files_to_scrape_local(ii_path):

    # Get a list of all items in the directory
    items_list = os.listdir(ii_path)

    # get only files
    file_list = [item for item in items_list if os.path.isfile(os.path.join(ii_path, item))]

    full_path_list = []

    # get the full path
    for i_file in file_list:
        # extract the data and put into list
        i_filepath = os.path.join(ii_path, i_file)
        full_path_list.append(i_filepath)

    return full_path_list

# get files to scrape internet
def get_files_to_scrape_internet(ii_path, ii_pages):

    full_path_list = []
    working_p = ii_path

    for x in range(ii_pages):
        if x == 0:
            x_prev = x
        else:
            x_prev = x - 1

        x_prev = x_prev * 10
        x_curr = x * 10

        x_prev_t = 'start=' + str(x_prev)
        x_curr_t = 'start=' + str(x_curr)

        # replace x_prev with x
        working_p = working_p.replace(x_prev_t, x_curr_t)

        full_path_list.append(working_p)

    return full_path_list




# get the list of urls to scrape
# Parameters
i_path_local    = r'C:\Users\Danie Smit\Documents\temp'
i_local = False
i_select_journal = 5
i_file_name_xlsx = 'data.xlsx'

# organisation OR organization OR company OR enterprise AND intext:"artificial intelligence" AND intext:"adoption" AND source:"European Journal of Information Systems"
# 69 entries
if i_select_journal == 1:
    i_path_internet = 'https://scholar.google.com/scholar?start=0&q=organisation+OR+organization+OR+company+OR+enterprise+AND+intext:%22artificial+intelligence%22+AND+intext:%22adoption%22+AND+source:%22European+Journal+of+Information+Systems%22&hl=en&as_sdt=0,5'
    i_pages = 8
    i_file_name_csv = 'data_1.csv'
    i_file_name_xlsx = 'data_1.xlsx'


# organisation OR organization OR company OR enterprise AND intext:"artificial intelligence" AND intext:"adoption" AND source:"Information Systems Journal"
# 42 entries
if i_select_journal == 2:
    i_path_internet = 'https://scholar.google.com/scholar?start=0&q=organisation+OR+organization+OR+company+OR+enterprise+AND+intext:%22artificial+intelligence%22+AND+intext:%22adoption%22+AND+source:%22Information+Systems+Journal%22&hl=en&as_sdt=0,5'
    i_pages = 5
    i_file_name_csv = 'data_2.csv'
    i_file_name_xlsx = 'data_2.xlsx'


# organisation OR organization OR company OR enterprise AND intext:"artificial intelligence" AND intext:"adoption" AND source:"Information Systems Research"
if i_select_journal == 3:
    i_path_internet = 'https://scholar.google.com/scholar?start=0&q=organisation+OR+organization+OR+company+OR+enterprise+AND+intext:%22artificial+intelligence%22+AND+intext:%22adoption%22+AND+source:%22Information+Systems+Research%22&hl=en&as_sdt=0,5'
    i_pages = 21    # 213 lots of suplicates with MISQ
    i_file_name_csv = 'data_3.csv'
    i_file_name_xlsx = 'data_3.xlsx'


# organisation OR organization OR company OR enterprise AND intext:"artificial intelligence" AND intext:"adoption" AND source:"Journal of the Association for Information Systems"
if i_select_journal == 4:
    i_path_internet = 'https://scholar.google.com/scholar?start=0&q=organisation+OR+organization+OR+company+OR+enterprise+AND+intext:%22artificial+intelligence%22+AND+intext:%22adoption%22+AND+source:%22Journal+of+the+Association+for+Information+Systems%22&hl=en&as_sdt=0,5'
    i_pages = 9   # 87
    i_file_name_csv = 'data_4.csv'
    i_file_name_xlsx = 'data_4.xlsx'


# organisation OR organization OR company OR enterprise AND intext:"artificial intelligence" AND intext:"adoption" AND source:"Journal of Information Technology" - source:"International Journal of Information Technology" - source: "Journal of Information Technology &" - source:"Journal of Information Technology and"
if i_select_journal == 5:
    i_path_internet = 'https://scholar.google.co.za/scholar?start=0&q=organisation+OR+organization+OR+company+OR+enterprise+AND+intext:%22artificial+intelligence%22+AND+intext:%22adoption%22+AND+source:%22Journal+of+Information+Technology%22&hl=en&as_sdt=0,5&as_vis=1'
    i_pages = 36 #80
    i_file_name_csv = 'data_5.csv'
    i_file_name_xlsx = 'data_5.xlsx'

# organisation OR organization OR company OR enterprise AND intext:"artificial intelligence" AND intext:"adoption" AND source:"Journal of Management information systems"
if i_select_journal == 6:
    i_path_internet = 'https://scholar.google.com/scholar?start=0&q=organisation+OR+organization+OR+company+OR+enterprise+AND+intext:%22artificial+intelligence%22+AND+intext:%22adoption%22+AND+source:%22Journal+of+Management+information+systems%22&hl=en&as_sdt=0,5'
    i_pages = 10  # 94
    i_file_name_csv = 'data_6.csv'
    i_file_name_xlsx = 'data_6.xlsx'

# organisation OR organization OR company OR enterprise AND intext:"artificial intelligence" AND intext:"adoption" AND source:"Journal of Strategic Information Systems"
if i_select_journal == 7:
    i_path_internet = 'https://scholar.google.com/scholar?start=0&q=organisation+OR+organization+OR+company+OR+enterprise+AND+intext:%22artificial+intelligence%22+AND+intext:%22adoption%22+AND+source:%22Journal+of+Strategic+Information+Systems%22&hl=en&as_sdt=0,5'
    i_pages = 4     #35
    i_file_name_csv = 'data_7.csv'
    i_file_name_xlsx = 'data_7.xlsx'

# organisation OR organization OR company OR enterprise AND intext:"artificial intelligence" AND intext:"adoption" AND source:"MIS quarterly"
if i_select_journal == 8:
    i_path_internet = 'https://scholar.google.com/scholar?start=0&q=organisation+OR+organization+OR+company+OR+enterprise+AND+intext:%22artificial+intelligence%22+AND+intext:%22adoption%22+AND+source:%22MIS+quarterly%22&hl=en&as_sdt=0,5'
    i_pages = 10    #105
    i_file_name_csv = 'data_8.csv'
    i_file_name_xlsx = 'data_8.xlsx'



# get local or global file
if i_local:
    i_files = get_files_to_scrape_local(i_path_local)
else:
    i_files = get_files_to_scrape_internet(i_path_internet, i_pages)

i_columns = ['article', 'author', 'year', 'journal', 'url', 'green_text', 'scraped_from']
l_data = []
df = pd.DataFrame(l_data, columns=[i_columns])

print('Parameters:')
print('- i_path_local = ' + i_path_local)
print('- i_path_internet = ' + i_path_internet)
print('- i_local = ' + str(i_local))
print('- i_pages = ' + str(i_pages))
print('- i_file_name_xlsx = ' + i_file_name_xlsx)

print('Start Scraping...')

# scrape fhe files
for i_file in i_files:

    print('- File:' + i_file)

    # scrape the file
    l_data = extract_scholar_page_local(i_file, i_local)

    # Create a DataFrame from the list and specify the columns names
    new_df = pd.DataFrame(l_data, columns=[i_columns])

    # Create a DataFrame from the list and specify the columns names
    df = pd.concat([df, new_df], ignore_index=True)

print('Number of articles extracted ' + str(len(df)))

df.to_excel(i_file_name_xlsx)


