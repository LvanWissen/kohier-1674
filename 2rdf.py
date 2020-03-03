import datetime
from itertools import count

import pandas as pd

from rdflib import Dataset, Graph, URIRef, Namespace, Literal, XSD, OWL

from roar import rdfSubject
from roar import Agent, Activity, Derivation
from roar import VoidDataset, DataDownload, Document, Annotation, PersonObservation, PersonName, LocationObservation, ResourceSelection, FragmentSelector, TextualBody, Aggregation, WebResource
from roar import edm, roar, dc, oa, prov, dcterms, pnv, schema, void, foaf

create = Namespace("https://data.create.humanities.uva.nl/")

personCounter = count(1)
nsPersonObservation = Namespace(
    "https://data.create.humanities.uva.nl/id/kohier1674/observations/PersonObservation/"
)
nsLocationObservation = Namespace(
    "https://data.create.humanities.uva.nl/id/kohier1674/observations/LocationObservation/"
)
nsOccupationObservation = Namespace(
    "https://data.create.humanities.uva.nl/id/kohier1674/observations/OccupationObservation/"
)

AGENT = Agent(URIRef("https://leonvanwissen.nl/me"), label=["Leon van Wissen"])
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


def main(csvfile, g):

    df = pd.read_csv(csvfile)
    df = df.where((pd.notnull(df)), None)

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

    return personObservation  # exampleResource


if __name__ == "__main__":

    ds = Dataset()
    g = rdfSubject.db = ds.graph(
        identifier="https://data.create.humanities.uva.nl/id/kohier1674/")

    exampleResource = main('data/records.csv', g)

    rdfSubject.db = ds

    description = """Van dit handgeschreven kohier (SAA inventarisnummer 5028:662) bestaat een getypte index op achternaam (SAA inventarisnummber 5028:662A). Hierin is de naam van een persoon, de relatie tot een andere persoon of groep (e.g. wed. van, of kinderen van), beroep en de woonwijk opgenomen. Ook is genoteerd op welk foliant de persoon beschreven is.

In totaal zijn 60 wijken beschreven in het kohier, aangegeven met cijfers. Daarna volgt een sectie van de 'Magistraten' (M), 'Joodse Natie' (J), 'Paden buijten de Stadt' (P1-P6), 'Officianten' (O), 'Regerende heeren' (R), 'Personen van andere Steden' (AS) en 'Testamenten' (T).

De wijkindeling correspondeert waarschijnlijk met die van een kaart uit 1766, vervaardigd door C. Philips Jacobsz. (1732-1789) en F.W. Greebe en is beschikbaar in de Beeldbank van het Stadsarchief, afbeelding 010001000849.

"""
    contributors = ""

    download = DataDownload(
        None,
        contentUrl=URIRef(
            "https://github.com/LvanWissen/kohier-1674/raw/master/data/kohier1674.trig"
        ),
        # name=Literal(),
        url=URIRef("https://github.com/LvanWissen/kohier-1674"),
        encodingFormat="application/trig")

    dataset = VoidDataset(
        URIRef("https://data.create.humanities.uva.nl/id/kohier1674/"),
        name=[
            Literal("Kohier van de 200ste penning, Amsterdam 1674", lang='nl')
        ],
        about=None,
        url=URIRef("https://github.com/LvanWissen/kohier-1674"),
        description=[Literal(description, lang='nl')],
        creator=[URIRef("https://leonvanwissen.nl/me")],
        publisher=[],
        contributor=[],
        source=None,
        date=Literal(datetime.datetime.now().isoformat(),
                     datatype=XSD.datetime),
        created=None,
        issued=None,
        modified=None,
        exampleResource=exampleResource,
        vocabulary=[URIRef("https://schema.org/")],
        triples=sum(1 for i in ds.graph(
            identifier="https://data.create.humanities.uva.nl/id/kohier1674/").
                    subjects()),
        temporalCoverage=Literal("1674", datatype=XSD.gYear, normalize=False),
        licenseprop=URIRef(
            "https://creativecommons.org/licenses/by-nc-sa/4.0/"),
        distribution=download)

    ds.bind('owl', OWL)
    ds.bind('create', create)
    ds.bind('schema', schema)
    ds.bind('void', void)
    ds.bind('foaf', foaf)
    ds.bind('edm', edm)
    ds.bind('pnv', pnv)
    ds.bind('roar', roar)
    ds.bind('dc', dc)
    ds.bind('dcterms', dcterms)
    ds.bind('oa', oa)
    ds.bind('prov', prov)

    print("Serializing!")
    ds.serialize('data/kohier1674.trig', format='trig')