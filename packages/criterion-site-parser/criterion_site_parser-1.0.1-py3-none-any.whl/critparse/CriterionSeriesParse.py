import requests
from bs4 import BeautifulSoup
from critparse import CriterionMovieParse
import argparse


def get_series_info(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    next_url = extract_next_url(soup)
    series_name, description = extract_series_name_and_description(soup)
    series = extract_episode_time_and_url(soup)
    while next_url:
        r = requests.get(next_url)
        soup = BeautifulSoup(r.content, 'html5lib')
        next_url = extract_next_url(soup)
        series += extract_episode_time_and_url(soup)
    return series_name, description, series


def extract_series_name_and_description(soup):
    ret_str = ["NoName", "unused", "NoDescription"]
    table = soup.find('div', attrs={'class': 'collection-details grid-padding-left'})
    if table:
        for string in table.stripped_strings:
            ret_str.append(string)
    return ret_str[0], ret_str[2]


def extract_next_url(soup):
    ret_str = None
    table = soup.find('div', attrs={'class': 'row loadmore'})
    if table:
        for item in table.findAll('a', attrs={'class': 'js-load-more-link'}):
            ret_str = "https://www.criterionchannel.com" + item['href']
    return ret_str


def extract_episode_time_and_url(soup):
    series = []
    table = soup.find('ul', attrs={'class': 'js-load-more-items-container'})
    for item in table.findAll('div', attrs={'class': 'grid-item-padding'}):
        movie = [item.a.text.strip(), item.a['href']]
        series.append(movie)
    return series


def main():
    args = process_args()
    if args.url:
        url = args.url
        series_name, description, extracted_episode_info = get_series_info(url)
        series_name = "Criterion:" + series_name
        print('Examined ' + url)
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print(series_name)
        print(description)
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print()
        print()
        i = 0
        for movie in extracted_episode_info:
            i += 1
            time, url = movie
            movie_parser = CriterionMovieParse.MovieParse(url)
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print(i)
            print(time)
            print(series_name)
            movie_parser.print_info(time)
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print()
            print()


def process_args():
    usage_desc = "This is how you use this thing"
    parser = argparse.ArgumentParser(description=usage_desc)
    parser.add_argument("url", help="URL to parse")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
