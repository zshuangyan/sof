import requests
import argparse
from lxml import html
import pprint

url = 'http://stackoverflow.com/search?'
keys = ['tab', 'pagesize', 'q']
params = dict.fromkeys(keys)

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--tab', choices=['votes', 'relevance'], default='relevance')
parser.add_argument('-p', '--pagesize', type=int, choices=[15, 30, 50], default=15)
parser.add_argument('q', nargs='+')
args = parser.parse_args()
for key, value in vars(args).items():
    if isinstance(value, list):
        value = ' '.join(v for v in value)
    params[key] = value

page = requests.get(url, params=params)
tree = html.fromstring(page.text)
titles = tree.xpath("//div[@class='result-link']/span/a/@title")
seen = set()
titles_distinct = []
for t in titles:
    if t not in seen:
        seen.add(t)
        titles_distinct.append(t)

name = '_'.join(keyword for keyword in args.q)
ext = '.html'
filename = name + ext
with open(filename, 'w') as f:
    for i, title in enumerate(titles_distinct):
        f.write('<p>{}. {}</p>'.format(i+1, title))
        f.write('\n')
pprint.pprint(titles_distinct)
import requests
import argparse
from lxml import html
import pprint

url = 'http://stackoverflow.com/search?'
keys = ['tab', 'pagesize', 'q']
params = dict.fromkeys(keys)

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--tab', choices=['votes', 'relevance'], default='relevance')
parser.add_argument('-p', '--pagesize', type=int, choices=[15, 30, 50], default=15)
parser.add_argument('q', nargs='+')
args = parser.parse_args()
for key, value in vars(args).items():
    if isinstance(value, list):
        value = ' '.join(v for v in value)
    params[key] = value

page = requests.get(url, params=params)
tree = html.fromstring(page.text)
titles = tree.xpath("//div[@class='result-link']/span/a")
titles = ((t.xpath('@title')[0], t.xpath('@href')[0]) for t in titles)
seen = set()
titles_distinct = []
for t, h in titles:
    if t not in seen:
        seen.add(t)
        titles_distinct.append((t, h))

name = '_'.join(keyword for keyword in args.q)
ext = '.html'
filename = name + ext
with open(filename, 'w') as f:
    for i, title in enumerate(titles_distinct):
        f.write('<a href="http://stackoverflow.com{}">{}. {}</a></br>'.format(title[1], i+1, title[0]))
        f.write('\n')

