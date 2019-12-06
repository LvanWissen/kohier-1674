import os
import re

TXTPATH = 'data/txt/'
REGEX = re.compile(
    r"""(?P<baseSurname>[^,\n]+), (?P<givenName>[^—\n]*)+? ?(?:(?P<surnamePrefix>(?:van der|van de|van|de|du|d')))? ?(?:—(?P<disambiguatingDescription>.*))?"""
)


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
        records = []

        # Try to cut the line in three parts: Nameref, Neighbourhood, Folio
        for n, line in enumerate(lines):
            line = line.strip()
            personReference, neighbourhood, folio = separate(line)

            if neighbourhood:
                neighbourhood = neighbourhood.replace(' ', '')

            data.append({
                'source': os.path.basename(f),
                'lineNumber': n,
                'reference': line,
                'personReference': personReference,
                'neighbourhood': neighbourhood,
                'folio': folio
            })

        # Correct the " abbreviation
        for n, d in enumerate(data):
            if d['personReference'].startswith('"'):
                d['personReference'] = surnameFill(
                    d['personReference'], data[n - 1]['personReference'], f)

        # Try to parse the nameref
        for d in data:
            matches = parseNameRef(d['personReference'])

            if matches:
                d = {**d, **matches}
            records.append(d)

        return records


def separate(text):

    text = text[::-1]

    try:
        folio, neighbourhood, personReference = re.split('\s\s+', text, 2)
    except:
        try:
            neighbourhood, personReference = re.split('\s\s+', text, 1)
            folio = None
        except:
            personReference = text
            neighbourhood = None
            folio = None

    personReference = personReference[::-1]
    if neighbourhood:
        neighbourhood = neighbourhood[::-1]
    if folio:
        folio = folio[::-1]

    return personReference, neighbourhood, folio


def surnameFill(person, previousPerson, f):

    surname, _ = previousPerson.split(',', 1)
    surname = surname.strip()

    person = person.replace('" ', surname, 1)

    return person


def parseNameRef(reference, REGEX=REGEX):

    matches = [m.groupdict() for m in REGEX.finditer(reference)]

    if matches:
        result = dict((k, v) for k, v in matches[0].items())

        if not result.get('givenName', None):
            return {
                'givenName': None,
                'surnamePrefix': None,
                'baseSurname': None,
                'related': None,
                'altName': None,
                'disambiguatingDescription': None
            }

        # someone else (+ huisvrouw)
        if ' + ' in result['givenName']:
            result['givenName'], result['related'] = result['givenName'].split(
                ' + ')
        else:
            result['related'] = None

        # geb. filter
        if 'geb.' in result['givenName']:
            result['givenName'], result['altName'] = result['givenName'].split(
                ' geb. ')
        else:
            result['altName'] = None

        # and filter out any surnamePrefix
        prefixes = {
            'van der', 'van de', 'van', 'de', 'du', "d'", 'ter', 'ten',
            'de la', 'la'
        }
        if len(set(result['givenName'].split()).intersection(prefixes)) > 0:
            name = re.split(r" (van der|van de|van|de la|la|de|du|d'|ter|ten)",
                            result['givenName'])

            if len(name) >= 4:
                # Fonseca, de Dias de
                *givenNames, result['surnamePrefix'], _ = name
                result['givenName'] = " ".join(i.strip() for i in givenNames)
            elif len(name) >= 2:
                result['givenName'], result['surnamePrefix'], _ = name
            elif len(name) == 1:
                result['surnamePrefix'] = name[0]

        else:
            result['surnamePrefix'] = None

        # any spaces left?
        result = {k: (v.strip() if v else v) for k, v in result.items()}

        return result


if __name__ == "__main__":
    d = main()

    import pandas as pd

    df = pd.DataFrame.from_records(d)

    df.to_csv('data/records.csv', index=False)
