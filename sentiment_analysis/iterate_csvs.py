import os
import csv
from do_sentiment_analysis import analyze

def get_list_of_csv_files(folder_paths):
    csv_files = []
    for folder in folder_paths:
        for root, _, files in os.walk(folder):
            for file in files:
                if os.path.splitext(file)[1] == '.csv':
                    # analyze(os.path.join(root, file))
                    csv_files.append(os.path.join(root,file))
                    # csv_files.append(file)
    return csv_files

if __name__ == '__main__':
    # csv_files = get_list_of_csv_files(["../data", "../general_news_data", "../NewsData"])
    # for file in csv_files:
    #     analyze(file)
    analyze("../final_kaggle_data.csv")