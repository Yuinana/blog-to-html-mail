import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import date
import json

# リンク一覧をスクレイピングし、リンクURLのリストとして出力

def return_soup(url):
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def return_scrape_pages(soup):
    link_lists = soup.select('a.entry-title-link')
    url_list = []
    for link_list in link_lists:
        url = link_list.get('href')
        url_list.append(url)
    return url_list

# リスト中のURLを開き、記事を見に行く
# 記事情報として、タイトル・ディスクリプション・ファイル名を辞書に格納する
# それぞれの記事情報をリストに格納する

def url_to_id(url):
    path = urlparse(url).path
    target = "/entry/"
    index = path.find(target)
    id = path[index+len(target):]
    return id

def make_article_dict(url_list):
    informations = []

    for url in url_list:
        id = url_to_id(url)
        article = return_soup(url)
        title = article.select_one('a.entry-title-link').text
        description = article.select_one('meta[name = "description"]').get('content')
        date_raw = article.select_one('.entry-header > .entry-date').text
        date = date_raw.strip()
        information = {
            'title' : title,
            'description' : description,
            'date' : date,
            'id' : id
        }
        informations.append(information)
    return informations

def main():
    index_url = "https://blog.pyq.jp/"
    soup = return_soup(index_url)
    url_list = return_scrape_pages(soup)
    informations = make_article_dict(url_list)

    today = date.today()
    str_today = today.strftime('%Y%m%d')
    file_name = 'informations_' + str_today
    json_path = 'json/' + file_name + '.json'

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(informations, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()
