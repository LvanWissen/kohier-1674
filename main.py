import os
import re

TXTPATH = 'data/txt/'


def main():

    d = []

    for f in sorted(os.listdir(TXTPATH)):
        d += processFile(os.path.join(TXTPATH, f))

    return d


def processFile(f):

    with open(f, encoding='utf-8') as infile:

        next(infile)  # skip the header (Naam, wijk, fol.)

        lines = infile.readlines()

        data = []
        for n, line in enumerate(lines):
            line = line.strip()
            person, neighbourhood, folio = separate(line)

            data.append({
                'source': os.path.basename(f),
                'lineNumber': n,
                'reference': line,
                'person': person,
                'neighbourhood': neighbourhood,
                'folio': folio
            })

        for n, d in enumerate(data):
            if d['person'].startswith('"'):
                d['person'] = surnameFill(d['person'], data[n - 1]['person'],
                                          f)

        return data


def separate(text):

    text = text[::-1]

    try:
        folio, neighbourhood, person = re.split('\s\s+', text, 2)
    except:
        try:
            neighbourhood, person = re.split('\s\s+', text, 1)
            folio = None
        except:
            person = text
            neighbourhood = None
            folio = None

    person = person[::-1]
    if neighbourhood:
        neighbourhood = neighbourhood[::-1]
    if folio:
        folio = folio[::-1]

    return person, neighbourhood, folio


def surnameFill(person, previousPerson, f):

    surname, _ = previousPerson.split(',', 1)
    surname = surname.strip()

    person = person.replace('" ', surname, 1)

    return person


if __name__ == "__main__":
    d = main()

    import pandas as pd

    df = pd.DataFrame.from_records(d)

    df.to_csv('data/records.csv', index=False)
