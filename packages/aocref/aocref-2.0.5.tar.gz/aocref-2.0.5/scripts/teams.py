"""Query Liquipedia API for data updates."""
import logging
import json
import time
from collections import defaultdict

import pycountry
import requests
from ruamel.yaml import YAML
import wikitextparser as wtp

BLACKLIST = ['simtom']
LOGGER = logging.getLogger(__name__)
WAIT_SECS = 30
PAGE_SIZE = 500
SQUAD_CONDITIONS = [
    'Is number in roster::>0',
    'Is player::true',
    'Is active::true'
]
SQUAD_PROPS = [
    'Has id',
    'Has team'
]
PLAYER_CONDITIONS = [
    'Category:Age of Empires II Players',
    'Is player::true'
]
PLAYER_PROPS = [
    'Has pagename',
    'Has team'
]
HEADERS = {'User-Agent': 'https://github.com/SiegeEngineers/aoc-reference-data'}
API = "https://liquipedia.net/ageofempires/api.php"

def fetch(conditions, props):
    """Fetch data from liquipedia API."""
    output = defaultdict(set)
    offset = 0
    while True:
        LOGGER.info("querying liquipedia at offset %d", offset)
        url = 'https://liquipedia.net/ageofempires/api.php'
        resp = requests.get(url, params={
            'action': 'askargs',
            'format': 'json',
            'conditions': '|'.join(conditions),
            'printouts': '|'.join(props),
            'parameters': '|'.join([f'offset={offset}', f'limit={PAGE_SIZE}'])
        }, headers={
            'User-Agent': 'https://github.com/SiegeEngineers/aoc-reference-data'
        })

        try:
            data = resp.json()
        except json.decoder.JSONDecodeError:
            LOGGER.exception("failed to fetch: %s", resp.content)

        for result in data['query']['results'].values():
            record = result['printouts']
            # {'Has id': ['Ace'], 'Has team': [{'fulltext': 'InDuS', 'fullurl': 'https://liquipedia.net/ageofempires/InDuS', 'namespace': 0, 'exists': '1', 'displaytitle': ''}]}
            #name = record['Has id'][0]
            name = None
            if 'Has pagename' in record:
                name = record['Has pagename'][0]['displaytitle']
            elif 'Has id' in record:
                name = record['Has id'][0]
            if record['Has team'] and name:
                team = record['Has team'][0]['fulltext'].replace(" (team)", "")
                output[team].add(name)
            #url = record['Has pagename'][0]['fullurl']
            #output.append(dict(page=page, name=name, url=url))

        offset = data.get('query-continue-offset')
        if not offset:
            break
        time.sleep(WAIT_SECS)

    return output


def get_props(page, props):
    #LOGGER.info(f"getting props for {page}")
    resp = requests.get(API, params={
        'action': 'query',
        'prop': 'revisions',
        'titles': page,
        'rvslots': '*',
        'rvprop': 'content',
        'formatversion': 2,
        'format': 'json'
    }, headers=HEADERS)
    markup = resp.json()['query']['pages'][0]['revisions'][0]['slots']['main']['content']
    parsed = wtp.parse(markup)
    out = {}
    for tpl in parsed.templates:
        if tpl.name.strip() != 'Infobox player':
            continue
        for a in tpl.arguments:
            if a.name.strip() in props:
                out[a.name.strip()] = a.value.strip()
    return out


def find_new(result_data, player_data, last_id):
    seen = set([p['liquipedia'].lower().replace("_", " ").strip() for p in player_data if 'liquipedia' in p])
    seen |= set([p['name'].lower().replace("_", " ").strip() for p in player_data])
    for n in result_data:
        if n['name'].lower().replace("_", " ").strip() not in seen:
            props = get_props(n['page'], ['country', 'aoe2net_id'])
            if 'aoe2net_id' not in props or not props['aoe2net_id']:
                continue
            country_code = pycountry.countries.search_fuzzy(props['country'])[0].alpha_2.lower()
            last_id += 1
            if n['name'] in BLACKLIST:
                continue
            print(n['name'], country_code, props['aoe2net_id'])
            player_data.append(dict(
                name=n['name'],
                country=country_code,
                platforms=dict(
                    rl=[x.strip() for x in props['aoe2net_id'].split(',')]
                ),
                liquipedia=n['name'],
                id=last_id
            ))


def strip_leading_double_space(stream):
    if stream.startswith("  "):
        stream = stream[2:]
    return stream.replace("\n  ", "\n")


def main():
    logging.basicConfig(level=logging.INFO)

    yaml = YAML()
    yaml.indent(sequence=4, offset=2)
    yaml.preserve_quotes = True
    with open('data/players.yaml', 'r') as handle:
        player_data = yaml.load(handle)
    with open('data/teams.json', 'r') as handle:
        team_data = json.loads(handle.read())
    by_id = {}
    for t in team_data:
        by_id[t['id']] = t['name'].replace(" (team)", "")

    names = set()
    result_data = defaultdict(set)
    for p in player_data:
        names.add(p['name'].lower().replace('_', ''))
        if 'liquipedia' in p:
            names.add(p['liquipedia'].lower().replace('_', ''))
    LOGGER.info("starting data update")
    for x, y in fetch(SQUAD_CONDITIONS, SQUAD_PROPS).items():
        result_data[x] |= y
    time.sleep(WAIT_SECS)
    for x, y in fetch(PLAYER_CONDITIONS, PLAYER_PROPS).items():
        result_data[x] |= y
    for p in player_data:
        if 'team' in p and 'liquipedia' not in p:
            result_data[by_id[p['team']]].add(p['name'])
    td = []
    id = 1
    p2t = {}
    BLACKLIST = ['MMC eSports']
    for x, y in result_data.items():
        if x in BLACKLIST:
            continue
        tm = {f for f in y if f.lower().replace('_', '') in names}
        if tm:
            players = set()
            pns = set()
            for p in tm:
                ptrans = p.lower().replace('_', '')
                for pp in player_data:
                    if ptrans == pp['name'].lower().replace('_', '') or 'liquipedia' in pp and ptrans == pp['liquipedia'].lower().replace('_', ''):
                        pp['team'] = id
                        players.add(pp['id'])
                        pns.add(p)
            td.append(dict(
                name=x,
                players=list(players),
                id=id
            ))
            id += 1
            print(x)
            print('->', pns)
    with open('data/players.yaml', 'w') as handle:
        LOGGER.info("writing new players.yaml")
        yaml.dump(player_data, handle, transform=strip_leading_double_space)
    with open('data/teams.json', 'w') as handle:
        LOGGER.info("writing new teams.json")
        handle.write(json.dumps(td, indent=2))
    LOGGER.info("finished data update")

if __name__ == '__main__':
    main()
