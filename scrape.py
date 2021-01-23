# coding:utf-8
import requests
from bs4 import BeautifulSoup
import re
from datetime import date
import json

# リンク一覧をスクレイピングし、リンクURLのリストとして出力

def scrape_html(url):    
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def make_article_list(soup):
    link_lists = soup.select('a.entry-title-link')
    url_list = []
    for link_list in link_lists:
        url = link_list.get('href')
        url_list.append(url)
    return url_list

# リスト中のURLを開き、記事を見に行く
# 記事情報として、タイトル・ディスクリプション・ファイル名を辞書に格納する
# それぞれの記事情報をリストに格納する

def make_article_dict(url_list):
    article_informations = []

    for url in url_list:
        article = scrape_html(url)
        article_title = article.select_one('a.entry-title-link').text
        article_description = article.select_one('meta[name = "description"]').get('content')
        article_date_row = article.select_one('.entry-header > .entry-date').text
        article_date = article_date_row.replace('\n', '')
        article_id = re.sub('^https:\/\/blog\.pyq\.jp\/entry\/', '', url)
        article_information = {
            'title' : article_title,
            'description' : article_description,
            'date' : article_date,
            'id' : article_id,
        }
        article_informations.append(article_information)
    return article_informations

if __name__ == "__main__":
    index_url = "https://blog.pyq.jp/"
    soup = scrape_html(index_url)
    url_list = make_article_list(soup)
    article_informations = make_article_dict(url_list)

    today = date.today()
    str_today = today.strftime('%Y%m%d')
    file_name = 'article_informations_' + str_today
    json_path = 'json/' + file_name + '.json'

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(article_informations, f, indent=4)




