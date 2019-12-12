from itertools import count

import pandas as pd

from rdflib import Graph, URIRef, Namespace, Literal

from roar import rdfSubject
from roar import Agent, Activity, Derivation
from roar import Document, Annotation, PersonObservation, PersonName, LocationObservation, ResourceSelection, FragmentSelector, TextualBody, Aggregation, WebResource
from roar import edm, roar, dc, oa, prov, dcterms, pnv

personCounter = count(1)
nsPersonObservation = Namespace(
    "https://data.create.humanities.uva.nl/datasets/kohier1674/observations/PersonObservation/"
)
nsLocationObservation = Namespace(
    "https://data.create.humanities.uva.nl/datasets/kohier1674/observations/LocationObservation/"
)
nsOccupationObservation = Namespace(
    "https://data.create.humanities.uva.nl/datasets/kohier1674/observations/OccupationObservation/"
)

AGENT = Agent(URIRef("https://www.leonvanwissen.nl/#me"),
              label=["Leon van Wissen"])
ACTIVITY = Activity(
    None,
    wasAssociatedWith=[AGENT],
    label=[Literal("OCR en correctie", lang='nl')],
    comment=[
        Literal(
            "De scans van inventarisnummer 5028:662A zijn geOCRd met Tesseract (5.0.0-alpha) en daarna semi-automatisch gecorrigeerd.",
            lang='nl')
    ])
DERIVATION = Derivation(None, hadActivity=ACTIVITY)


def main(csvfile):

    df = pd.read_csv(csvfile)
    df = df.where((pd.notnull(df)), None)

    g = rdfSubject.db = Graph(
        identifier="https://data.create.humanities.uva.nl/datasets/kohier1674/"
    )

    g.bind('edm', edm)
    g.bind('pnv', pnv)
    g.bind('roar', roar)
    g.bind('dc', dc)
    g.bind('dcterms', dcterms)
    g.bind('oa', oa)
    g.bind('prov', prov)

    images = set()
    for r in df.to_dict(orient='records'):

        scanName, _ = r['source'].split('_')
        pageNumber = int(scanName[-5:])

        document = Document(URIRef(f"#p{pageNumber}"))  #ProvidedCHO

        image = URIRef(r['source'].replace('txt', 'tif'))
        images.add(image)

        aggregation = Aggregation(URIRef(
            f"https://archief.amsterdam/archief/5028/662#p{pageNumber}"),
                                  aggregatedCHO=document)

        webResource = WebResource(
            URIRef(f"https://archief.amsterdam/archief/5028/662A#{scanName}"))

        aggregation.isShownAt = webResource

        annotation = Annotation(
            None,
            hasTarget=ResourceSelection(
                None,
                hasSource=document,
                hasSelector=FragmentSelector(
                    None,
                    conformsTo=URIRef("http://tools.ietf.org/rfc/rfc5147"),
                    value=f"line={r['lineNumber']}")),
            hasBody=TextualBody(None,
                                value=r['reference'],
                                language="nl",
                                format="text/html"),
            wasDerivedFrom=[image],
            qualifiedDerivation=DERIVATION)

        personNames = [
            PersonName(
                None,
                baseSurname=r['baseSurname'],
                givenName=r['givenName'],
                surnamePrefix=r['surnamePrefix'],
                disambiguatingDescription=r['disambiguatingDescription'],
                literalName=" ".join([
                    i for i in
                    [r['givenName'], r['surnamePrefix'], r['baseSurname']]
                    if i is not None
                ]))
        ]

        if r['altName']:
            personNames.append(PersonName(None, literalName=r['altName']))

        for name in personNames:
            name.label = name.literalName

        personObservation = PersonObservation(
            nsPersonObservation.term(str(next(personCounter))),
            hasName=personNames,
            documentedIn=document,
            locationInDocument=Literal(r['folio']) if r['folio'] else None,
            wasDerivedFrom=[annotation])

        personObservation.label = [i.literalName for i in personNames]

        if r['neighbourhood']:
            locationObservation = LocationObservation(
                nsLocationObservation.term(r['neighbourhood']),
                label=[r['neighbourhood']])

            personObservation.hasLocation = [locationObservation]

    DERIVATION.entity = sorted(images)

    return g


if __name__ == "__main__":
    g = main('data/records.csv')

    print("Serializing!")
    g.serialize('data/records.trig', format='trig')