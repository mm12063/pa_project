from nltk.sentiment import SentimentIntensityAnalyzer
import os
import csv

## Note that NLTK sentiment scores are as follows:
## negative, neutral, postive, compound
## where negative, neutral and positive scores sum up to 1 with none being negative
## and compound score is in range [-1, 1]
##
## So, the sentiment scores for the headlines (and snippets) are stored in the following format:
## negative|neutral|positive|compound

HEADLINE = 'headline'
SNIPPET = 'snippet'

def analyze_sentiment(text : str) -> str:
    sia = SentimentIntensityAnalyzer()
    scores = sia.polarity_scores(text)
    return '|'.join([str(score) for score in scores.values()])

def setup_destination_folder(file_path: str) -> str:
    directory_path = os.path.split(file_path)[0]
    directory_path = os.path.join(directory_path, 'sentimentally')
    os.makedirs(directory_path, exist_ok = True)
    return os.path.join(directory_path, os.path.basename(file_path))

def analyze(file_path):
    print("current file: " + os.path.basename(file_path))
    write_file_path = setup_destination_folder(file_path)
    file = open(file_path, 'r')
    write_file = open(write_file_path, 'w')
    csv_writer = csv.writer(write_file, delimiter=',')
    csv_reader = csv.reader(file, delimiter=',')
    columns = next(csv_reader)
    print("columns: " + str(columns))
    global HEADLINE, SNIPPET
    HEADLINE = 'headline'
    SNIPPET = 'snippet'
    if HEADLINE not in columns:
        print("No \'headline\' column exists!!!!")
        HEADLINE = 'title'
        SNIPPET = 'summary'
    headline_index = columns.index(HEADLINE)
    snippet_there = SNIPPET in columns
    snippet_index = columns.index(SNIPPET) if snippet_there else -1
    write_row = columns + ['headline_sentiment']
    write_row += ['snippet_sentiment'] if snippet_there else []
    csv_writer.writerow(write_row)
    for row in csv_reader:
        headline = row[headline_index]
        headline_sentiment = analyze_sentiment(headline)
        write_row = row + [headline_sentiment]
        write_row += [analyze_sentiment(row[snippet_index])] if snippet_there else []
        csv_writer.writerow(write_row)
    write_file.close()
    file.close()
        


if __name__ == '__main__':
    analyze("../general_news_data/theGuardian/data.csv")