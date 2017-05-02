import argparse
import requests
from lxml import html
from pprint import pprint

URL = 'http://stackoverflow.com/search?'


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tab', choices=['votes', 'relevance'], default='relevance')
    parser.add_argument('-p', '--pagesize', type=int, choices=[15, 30, 50], default=15)
    parser.add_argument('q', nargs='+')
    return parser


def get_result(params):
    page = requests.get(URL, params=params).text
    tree = html.fromstring(page)
    titles = tree.xpath("//div[@class='result-link']/span/a")
    titles = ((t.xpath('@title')[0], t.xpath('@href')[0]) for t in titles)
    seen = set()
    titles_distinct = []
    for t, h in titles:
        if t not in seen:
            seen.add(t)
            titles_distinct.append((t, h))
    return titles_distinct


def generate_html(result, args):
    name = '_'.join(keyword for keyword in args['q'])
    ext = '.html'
    filename = name + ext
    with open(filename, 'w') as f:
        for i, title in enumerate(result):
            f.write('<a href="http://stackoverflow.com{}">{}. {}</a></br>'.format(title[1], i + 1, title[0]))
            f.write('\n')


def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())
    params = {}
    for key, value in args.items():
        if isinstance(value, list):
            value = ' '.join(v for v in value)
        params[key] = value
    result = get_result(params)
    generate_html(result, args)
    pprint([t[0] for t in result])

if __name__ == '__main__':
    command_line_runner()



