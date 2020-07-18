import matplotlib.pyplot as plt
import json
import xml.etree.ElementTree as et
from json import JSONEncoder
from operator import itemgetter
from typing import NamedTuple, Dict, Iterable, Tuple

import click


class District(NamedTuple):
    id: int
    name: str
    candidates: Dict[str, int]
    data: 'DistrictData'


class DistrictData(NamedTuple):
    total: int
    received: int
    ahead: int
    inside: int
    outside: int
    unused: int
    moving: int
    stationary: int
    rejected: int
    accepted: int
    lost: int
    missing: int


@click.command()
@click.argument('data', type=click.File('r'))
@click.argument('mapping', type=click.File('r'))
def main(data, mapping):
    m = json.load(mapping)
    tree = et.parse(data)
    root = tree.getroot()
    districts = dict(parse(root, m))

    data = []
    for d in districts.values():
        votes = d.data.accepted + d.data.rejected
        putin = d.candidates['Путин Владимир Владимирович'] / votes
        data.append([votes / d.data.total, putin])

    data = sorted(data, key=itemgetter(0))
    x, y = zip(*data)
    click.echo(x)
    plt.plot(x, y)
    plt.savefig('plot.png')


def parse(root, mapping) -> Iterable[Tuple[str, District]]:

    for district in root:

        district_data: Dict[str, int] = {}
        district_candidates: Dict[str, int] = {}

        for item in district:
            names = item.findall('name')
            assert len(names) == 1, len(names)

            quantities = item.findall('quantity')
            assert len(quantities) == 1, len(quantities)

            fullname, value = names[0].text.strip(), int(quantities[0].text)
            if fullname in mapping['candidates']:
                district_candidates[fullname] = value
            else:
                district_data[mapping['data'][fullname]] = value

        attr = district.attrib
        yield attr['id'], District(
            id=int(attr['id']),
            name=attr['name'],
            candidates=district_candidates,
            data=DistrictData(**district_data),
        )
