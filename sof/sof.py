import argparse
import requests
from lxml import html

from .util import Answer

URL = 'http://stackoverflow.com/search?'


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tab', choices=['votes', 'relevance'], default='votes')
    parser.add_argument('-p', '--pagesize', type=int, choices=[15, 30, 50], default=15)
    parser.add_argument('q', nargs='+')
    return parser


def get_answers(params):
    res = requests.get(URL, params=params)
    print(res.url)
    page = res.content
    tree = html.fromstring(page)
    answers = tree.xpath("//div[@class='result-link']/*/a")
    answers = [Answer(t.xpath('@title')[0], t.xpath('@href')[0]) for t in answers]
    seen = set()
    distinct_answers = []
    for answer in answers:
        if answer.title not in seen:
            seen.add(answer.title)
            distinct_answers.append(answer)
    return distinct_answers


def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())
    params = {}
    for key, value in args.items():
        if isinstance(value, list):
            value = ' '.join(value)
        params[key] = value
    answers = get_answers(params)
    for answer in answers:
        print("标题: %s\n链接: %s" % (answer.title, answer.href))


if __name__ == '__main__':
    command_line_runner()
