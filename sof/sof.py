import argparse
import requests
from lxml import html
from collections import namedtuple

from .util import remove_duplicate_item

Answer = namedtuple("Answer", ["title", "href"])

URL = 'http://stackoverflow.com/search?'


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tab', choices=['votes', 'relevance'], default='votes')
    parser.add_argument('-p', '--pagesize', type=int, choices=[15, 30, 50], default=15)
    parser.add_argument('q', nargs='+')
    return parser


def get_answers(params):
    res = requests.get(URL, params=params)
    print("GET: %s" % res.url)
    page = res.content
    tree = html.fromstring(page)
    answers = tree.xpath("//div[@class='result-link']/*/a")
    answers = [Answer(t.xpath('@title')[0], t.xpath('@href')[0]) for t in answers]
    distinct_answers = remove_duplicate_item(answers, key=lambda x: x.title)
    return distinct_answers


def parse_answer(answer: Answer, base_url: str):
    url, idt = answer.href.split("#")
    url = base_url + url
    print("%s(%s): " % (answer.title, url))
    page = requests.get(url).content
    tree = html.fromstring(page)
    post_xpath = "//div[@id='answer-%s']//div[@class='post-text']" % idt
    childs = tree.xpath(post_xpath)[0]
    contents = '\n'.join([child.text for child in childs.iter() if child.text])
    print("%s%s\n" % (''.join(contents[:500]), "..." if len(contents) > 500 else ""))


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
        print("Answers:\n")
        parse_answer(answer, base_url="http://stackoverflow.com")


if __name__ == '__main__':
    command_line_runner()
