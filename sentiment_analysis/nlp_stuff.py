import csv
import os
from nltk.sentiment import SentimentIntensityAnalyzer
import pprint
import yaml
import copy
import time
from textblob import TextBlob
USING_TEXTBLOB = True

def prettyprint(data : list) -> None:
    pp = pprint.PrettyPrinter()
    pp.pprint(data)

def dictprint(data : dict) -> None:
    print(yaml.dump(data, default_flow_style=False))

def get_list_of_csv_files(folder_paths : list) -> list:
    csv_files = []
    for folder in folder_paths:
        for root, _, files in os.walk(folder):
            for file in files:
                if os.path.splitext(file)[1] == '.csv':
                    # analyze(os.path.join(root, file))
                    csv_files.append(os.path.join(root,file))
                    # csv_files.append(file)
    return csv_files

def analyze_sentiment_nltk(text : str) -> str:
    sia = SentimentIntensityAnalyzer()
    scores = sia.polarity_scores(text)
    return str(scores['compound'])

def analyze_sentiment_TextBlob(text: str) -> str:
    return TextBlob(text).sentiment.polarity

def sd_destpath(filepath : str) -> str:
    splitext = os.path.splitext(os.path.basename(filepath))
    destpath = os.path.join(os.path.dirname(filepath), splitext[0] + '_nlp' + splitext[1])
    # print(destpath)
    return destpath

# dict: {date: [  
#                  {category: , headline_score: , snippet_score: },... ]}

def get_category(filename : str) -> str:
    return os.path.basename(os.path.dirname(filename))

def process_news(csv_file : str, data : dict) -> dict:
    print("Processing: " + csv_file)
    file = open(csv_file, 'r')
    csv_reader = csv.reader(file)
    columns = next(csv_reader)
    category = get_category(csv_file)
    # snippet_there = 'snippet' in columns
    # headline_there = 'headline' in columns
    # headline_index = columns.index('headline') if headline_there else columns.index('sentiment')
    headline_index = columns.index('headline')
    date_index = columns.index('date')
    # if snippet_there:
    #     snippet_index = columns.index('snippet')
    for row in csv_reader:
        headline = row[headline_index]
        date = row[date_index]
        data[date] = data.get(date, [])
        # if headline_there:
        headline_score = analyze_sentiment_nltk(headline)
        if USING_TEXTBLOB:
            headline_score2 = analyze_sentiment_TextBlob(headline)
            news_data = {'category': category, 'headline_score': headline_score, 'headline_score2': headline_score2}
        else:
            news_data = {'category': category, 'headline_score': headline_score}
        # else:
            # headline_score = row[headline_index]
            # if USING_TEXTBLOB:
            #     headline_score2 = row[headline_index]
            #     news_data = {'category': category, 'headline_score': headline_score, 'headline_score2': headline_score}
            # else:
            #     news_data = {'category': category, 'headline_score': headline_score}
        data[date].append(news_data)
    return data

def process_all_news(csv_list : list) -> dict:
    data = {}
    for csv_file in csv_list:
        data = process_news(csv_file, data)
    return data

def process_nlp_data(data : dict) -> dict:
    all_categories = ['ALB', 'CBAK', 'ENS', 'LAC', 'SQM', 'TIA', 'lithium']
    processed_data = {}
    for date, articles in data.items():
        headline_score = {x:0.0 for x in all_categories}
        if USING_TEXTBLOB:
            headline_score2 = {x:0.0 for x in all_categories}
        counts = {x:0 for x in all_categories}
        for article in articles:
            headline_score[article['category']] += float(article['headline_score'])
            if USING_TEXTBLOB:
                headline_score2[article['category']] += float(article['headline_score2'])
            counts[article['category']] += 1.0

        for cat in all_categories:
            headline_score[cat] /= max(counts[cat], 1)
            if USING_TEXTBLOB:
                headline_score2[cat] /= max(counts[cat], 1)
        if USING_TEXTBLOB:
            processed_data[date] = [str(x) for x in headline_score.values()] + [str(x) for x in headline_score2.values()]
        else:
            processed_data[date] = [str(x) for x in headline_score.values()]
    return processed_data

def do_nlp_stuff(stock_data_file : str, root_folder : str) -> None:
    nlp_files = get_list_of_csv_files([root_folder])
    nlp_data = process_all_news(nlp_files)
    print("Sentiment scores generated for all textual data. Averaging to get single score per date...")
    nlp_data = process_nlp_data(nlp_data)
    print("NLP Scores Preprocessing done...")
    # dictprint(nlp_data)
    # return
    sdread = open(stock_data_file, 'r')
    sd_csv_read = csv.reader(sdread, delimiter = ',')
    sdwrite = open(sd_destpath(stock_data_file), 'w')
    sd_csv_write = csv.writer(sdwrite, delimiter = ',')
    columns = next(sd_csv_read)
    all_categories = ['ALB', 'CBAK', 'ENS', 'LAC', 'SQM', 'TIA', 'lithium']
    new_columns1 = [x + '_sentiment_nltk' for x in all_categories]
    for col in new_columns1:
        assert col in columns
    date_index = columns.index('Date')
    if USING_TEXTBLOB:
        new_columns2 = [x + '_sentiment_TextBlob' for x in all_categories]
        # sd_csv_write.writerow(columns + new_columns + new_columns2)
        sd_csv_write.writerow(columns)
        new_columns = new_columns1 + new_columns2
        zeros = [0.0 for _ in new_columns]
    else:
        # sd_csv_write.writerow(columns + new_columns)
        sd_csv_write.writerow(columns)
        new_columns = new_columns1
        zeros = [0.0 for _ in new_columns]
    for row in sd_csv_read:
        date = row[date_index]
        nlp_row = (nlp_data[date] if date in nlp_data.keys() else copy.deepcopy(zeros))
        for index, col in enumerate(new_columns):
            row[columns.index(col)] = nlp_row[index]
        # sd_csv_write.writerow(row + nlp_row)
        sd_csv_write.writerow(row)
    sdread.close()
    sdwrite.close()

def trial():
    file = 'all_data/lithium/twittersentiment.csv'
    # data = {'something':['other', 'something'], 'new' : 'data'}
    # prettyprint(data)
    
    # return
    # file = 'all_data/ENS/GlobeNewswireENS_fixed.csv'
    read = open(file, 'r', encoding='utf-8-sig')
    csv_reader = csv.reader(read)
    columns = next(csv_reader)
    print(columns)
    print('date' in columns)
    print(columns.index('date'))
    write_file = open(file, 'w')
    csv_writer =  csv.writer(write_file)
    csv_writer.writerow(columns)
    for row in csv_reader:
        csv_writer.writerow(row)
    write_file.close()
    read.close()
    pass

if __name__  == '__main__':
    start_time = time.time()
    # stock_data_file = '../StockData/main_ds.csv'
    stock_data_file = '../StockData/main_ds_nlp_weather.csv'
    root_folder = 'all_data/'
    # trial()
    # sd_destpath(stock_data_file)
    # sdwrite = open(sd_destpath(stock_data_file), 'w')
    # analyze_sentiment_TextBlob("This is extremely bad!")
    do_nlp_stuff(stock_data_file, root_folder)
    print("--- %s seconds ---" % (time.time() - start_time))