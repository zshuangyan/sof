import argparse
import requests
from lxml import html
from collections import namedtuple
from colorama import Fore

from .util import remove_duplicate_item
from .draw import output

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
    output("GET: %s" % res.url, color=Fore.WHITE)
    page = res.content
    tree = html.fromstring(page)
    answers = tree.xpath("//div[@class='result-link']/*/a")
    answers = [Answer(t.xpath('@title')[0], t.xpath('@href')[0]) for t in answers]
    distinct_answers = remove_duplicate_item(answers, key=lambda x: x.title)
    return distinct_answers


def parse_answer(answer: Answer, base_url: str):
    # Todo: 处理不包含#的情况
    if "#" not in answer.href:
        contents = "can not resolve when answer id not in href"
        output(contents, color=Fore.RED)
        print()
        return
    url, idt = answer.href.split("#")
    url = base_url + url
    output("%s (%s): " % (answer.title, url), width=150, color=Fore.YELLOW)
    page = requests.get(url).content
    tree = html.fromstring(page)
    post_xpath = "//div[@id='answer-%s']//div[@class='post-text']" % idt
    childs = tree.xpath(post_xpath)[0]
    contents = '\n'.join([child.text for child in childs.iter() if child.text])
    output(contents, color=Fore.GREEN)
    print()


def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())
    params = {}
    for key, value in args.items():
        if isinstance(value, list):
            value = ' '.join(value)
        params[key] = value
    answers = get_answers(params)
    output("Total Answer num: %s\n" % len(answers), color=Fore.BLUE)
    for answer in answers:
        output("Answer:", color=Fore.YELLOW)
        parse_answer(answer, base_url="http://stackoverflow.com")


if __name__ == '__main__':
    command_line_runner()
