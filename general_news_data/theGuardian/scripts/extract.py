


from nbformat import write
import requests
from pprint import pprint
import time
import yaml
from yaml.loader import SafeLoader
import csv
# http://content.guardianapis.com/tags?q=apple&section=technology&show-references=all

# section = "science"
# query_url = f"https://api.nytimes.com/svc/topstories/v2/{section}.json?api-key={apikey}"
# query_url = f"https://api.nytimes.com/svc/archive/v1/2015/2.json?api-key={apikey}"

def filter_articles(json_file: dict, document_list: list) -> list:
    docs = json_file['response']['results']
    for doc in docs:
        newdoc = dict()
        newdoc['idx'] = len(document_list)
        newdoc['headline'] = doc.get('webTitle', "NOTHING_FOUND")
        newdoc['date'] = doc.get('webPublicationDate', "NOTHING_FOUND")
        # newdoc['snippet'] = doc.get('snippet', "NOTHING_FOUND")
        newdoc['source'] = "The Guardian"
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
            # wstr += str(doc['snippet']) + ","
            wstr += str(doc['source']) + "\n"
            f.write(wstr)

if __name__ == '__main__':
    with open('config.yaml') as f:
        data = yaml.load(f, Loader=SafeLoader)
        apikey = data['THEGUARDIAN_API_KEY']
    document_list = []


    # query = "(hurricane OR storm)"
    query = "lithium"
    # query_fields = "body"
    # section = "business"  # https://open-platform.theguardian.com/documentation/section
    # tag = "world/extreme-weather"  # https://open-platform.theguardian.com/documentation/tag
    from_date = "2015-01-01"
    query_url = f"https://content.guardianapis.com/search?" \
                f"api-key={apikey}" \
                f"&q={query}" \
                f"&from-date={from_date}" \
                f"&page=1"
                # f"&query-fields={query_fields}" \
                # f"§ion={section}" \
                # f"&show-fields=headline,byline,starRating,shortUrl"
                # f"&tag={tag}" \
    
    # query_url = f"http://content.guardianapis.com/tags?api-key={apikey}"
    r = requests.get(query_url)
    json_file = r.json()
    # pprint(json_file)
    page_count = int(json_file['response']['pages'])
    print(f"page count: {page_count}")
    for page_index in range(1, page_count + 1):
        query_url = f"https://content.guardianapis.com/search?" \
                f"api-key={apikey}" \
                f"&q={query}" \
                f"&from-date={from_date}" \
                f"&page={page_index}"
        r = requests.get(query_url)
        print(f"query of page {page_index} done")
        json_file = r.json()
        document_list = filter_articles(json_file, document_list)
        # break
        time.sleep(8)
    # exit()
    

    
    
    print(len(document_list))
    write_to_file(document_list, 'data.csv')