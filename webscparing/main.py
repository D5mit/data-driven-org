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
i_path_internet = 'https://scholar.google.co.za/scholar?start=0&q=%22education+technology%22+%2B+%22design+science+research%22&hl=en&as_sdt=0,5&as_ylo=2018&as_yhi=2023&as_vis=1'
i_local = False
i_pages = 19

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
print('- i_local' + str(i_local))
print('- i_pages' + str(i_pages))

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

df.to_csv('data.csv', index=False)
df.to_excel('data.xlsx')
