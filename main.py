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


def processFile(f: str) -> list:
    """Process a txt file (OCR result).
    
    Args:
        f (str): Filepath
    
    Returns:
        list: List of dictionaries with identified informational parts.
    """

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
                    d['personReference'], data[n - 1]['personReference'])

        # Try to parse the nameref
        for d in data:
            matches = parseNameRef(d['personReference'])

            if matches:
                d = {**d, **matches}
            records.append(d)

        # TODO
        # # Relatives and occupation
        # for d in records:
        #     if d['disambiguatingDescription']:

        #         # Are there references to relatives in the disambiguatingDescription?
        #         d['relatives'] = findRelatives(d['disambiguatingDescription'])

        #         # Occupations?
        #         d['occupation'] = findOccupation(
        #             d['disambiguatingDescription'])

        return records


def separate(text: str) -> tuple:
    """Try to separate a string into three columns by white space.
    
    Args:
        text (str): A line in the OCR text.
    
    Returns:
        tuple: Tuple of strings (personReference, neighbourhood, folio).
    """

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


def surnameFill(person: str, previousPerson: str) -> str:
    """Correct abbreviation " characters by looking at the previous mentioned person. 
    
    Args:
        person (str): A person reference (i.e. " , Jan)
        previousPerson ([str]): A person reference (i.e. Jansz, Jan)
    
    Returns:
        str: A corrected person reference
    """

    surname, _ = previousPerson.split(',', 1)
    surname = surname.strip()

    person = person.replace('" ', surname, 1)

    return person


def parseNameRef(reference: str, REGEX=REGEX) -> dict:
    """Use regex to filter out parts of a PersonName.
    
    Args:
        reference (str): A person reference (e.g. Jansen, Jan — metselaer)
        REGEX (re.Pattern): [description]. Defaults to REGEX.
    
    Returns:
        dict: Dictionary with keys givenName, surnamePrefix, baseSurname, 
        related, altName, disambiguatingDescription.
    """

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
        elif 'geboren' in result['givenName']:
            result['givenName'], result['altName'] = result['givenName'].split(
                ' geboren ')
        else:
            result['altName'] = None

        # de jonge / de oude
        if result['givenName'].strip().lower().endswith('de jonge') or result[
                'givenName'].strip().lower().endswith('de oude'):
            result['givenName'], jongoud, _ = re.split(r" (de jonge|de oude)",
                                                       result['givenName'],
                                                       maxsplit=1,
                                                       flags=re.IGNORECASE)
            jongoud = jongoud.strip()

            if jongoud and result['disambiguatingDescription']:
                result['disambiguatingDescription'] = ",".join(
                    [jongoud, result['disambiguatingDescription']])
            elif jongoud:
                result['disambiguatingDescription'] = jongoud

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


def findRelatives(description: str):
    pass


def findOccupation(description: str):
    pass


if __name__ == "__main__":
    d = main()

    import pandas as pd

    df = pd.DataFrame.from_records(d)

    df.to_csv('data/records.csv', index=False)
