from nbformat import write
import requests
from pprint import pprint
import time
import yaml
from yaml.loader import SafeLoader
import csv

def filter_articles(json_file: dict, document_list: list) -> list:
    docs = json_file['response']['docs']
    for doc in docs:
        newdoc = dict()
        newdoc['idx'] = len(document_list)
        newdoc['headline'] = doc.get('headline', {}).get('main', "NOTHING_FOUND").replace(',','')
        newdoc['date'] = doc.get('pub_date', "NOTHING_FOUND")
        newdoc['snippet'] = doc.get('snippet', "NOTHING_FOUND").replace(',','')
        newdoc['source'] = doc.get('source', "NOTHING_FOUND")
        document_list.append(newdoc)
    return document_list

def write_to_file(document_list, file_name):
    with open(file_name, 'w') as f:
        f.write("idx,headline,date,snippet,source\n")
        wstr = ''
        for doc in document_list:
            wstr = str(doc['idx']) + ","
            wstr += str(doc['headline']) + ","
            wstr += str(doc['date']) + ","
            wstr += str(doc['snippet']) + ","
            wstr += str(doc['source']) + "\n"
            f.write(wstr)

if __name__ == '__main__':
    with open('config.yaml') as f:
        data = yaml.load(f, Loader=SafeLoader)
        apikey = data['NYTIMES_API_KEY']
    document_list = []

    query = "lithium"
    begin_date = "20150101"  # YYYYMMDD
    end_date = "20220701" # YYYYMMDD
    filter_query = "\"body:(\"lithium\" \"mining\")\""  # http://www.lucenetutorial.com/lucene-query-syntax.html
    page = "0"  # <0-100>
    sort = "oldest"  # newest, oldest, relevance

    query_url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?" \
                f"q={query}" \
                f"&api-key={apikey}" \
                f"&begin_date={begin_date}" \
                f"&end_date={end_date}" \
                f"&fq={filter_query}" \
                f"&page={page}" \
                f"&sort={sort}"

    r = requests.get(query_url)
    json_file = r.json()
    page_count = int(int(json_file['response']['meta']['hits']) / 10)
    print(f"page count: {page_count}")

    for page_index in range(0, page_count + 1):
        query_url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?" \
                f"q={query}" \
                f"&api-key={apikey}" \
                f"&begin_date={begin_date}" \
                f"&end_date={end_date}" \
                f"&fq={filter_query}" \
                f"&page={page_index}" \
                f"&sort={sort}"
        r = requests.get(query_url)
        print(f"query of page {page_index} done")
        json_file = r.json()
        document_list = filter_articles(json_file, document_list)
        # break
        time.sleep(8)
    
    print(len(document_list))
    write_to_file(document_list, 'data.csv')