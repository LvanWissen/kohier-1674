"""
ROAR ontology, plus several usefull classes from edm, schema, bio etc.
"""

from rdflib import Dataset, Graph, Namespace
from rdflib import XSD, RDF, RDFS, OWL
from rdflib import URIRef, BNode, Literal

from rdfalchemy.rdfSubject import rdfSubject
from rdfalchemy import rdfSingle, rdfMultiple, rdfContainer, rdfList

bio = Namespace("http://purl.org/vocab/bio/0.1/")
edm = Namespace("http://www.europeana.eu/schemas/edm/")
sem = Namespace("http://semanticweb.cs.vu.nl/2009/11/sem/")
rel = Namespace("http://purl.org/vocab/relationship/")
pnv = Namespace('https://w3id.org/pnv#')
skos = Namespace('http://www.w3.org/2004/02/skos/core#')
schema = Namespace('http://schema.org/')
dc = Namespace("http://purl.org/dc/elements/1.1/")
dcterms = Namespace("http://purl.org/dc/terms/")

AS = Namespace("http://www.w3.org/ns/activitystreams#")
oa = Namespace("http://www.w3.org/ns/oa#")
void = Namespace("http://rdfs.org/ns/void#")
foaf = Namespace("http://xmlns.com/foaf/0.1/")
prov = Namespace("http://www.w3.org/ns/prov#")
roar = Namespace("https://w3id.org/roar#")

PersonObservation = Namespace(
    "https://data.create.humanities.uva.nl/datasets/kohier1674/observations/PersonObservation/"
)
OccupationObservation = Namespace(
    "https://data.create.humanities.uva.nl/datasets/kohier1674/observations/OccupationObservation/"
)


class Entity(rdfSubject):
    rdf_type = prov.Entity

    locationInDocument = rdfSingle(roar.locationInDocument)
    name = rdfMultiple(schema.name)

    url = rdfSingle(schema.url)


# Void
class VoidDataset(rdfSubject):
    rdf_type = void.Dataset, schema.Dataset

    subset = rdfMultiple(void.subset)

    label = rdfMultiple(RDFS.label)
    name = rdfMultiple(schema.name)

    # db = ConjunctiveGraph

    about = rdfSingle(schema.about)
    url = rdfSingle(schema.url)

    title = rdfMultiple(dcterms.title)
    description = rdfMultiple(dcterms.description)
    creator = rdfMultiple(dcterms.creator)
    publisher = rdfMultiple(dcterms.publisher)
    contributor = rdfMultiple(dcterms.contributor)
    source = rdfSingle(dcterms.source)
    date = rdfSingle(dcterms.date)
    created = rdfSingle(dcterms.created)
    issued = rdfSingle(dcterms.issued)
    modified = rdfSingle(dcterms.modified)

    exampleResource = rdfSingle(void.exampleResource)
    vocabulary = rdfMultiple(void.vocabulary)
    triples = rdfSingle(void.triples)

    descriptionSchema = rdfMultiple(schema.description)
    isBasedOn = rdfSingle(schema.isBasedOn)

    dateCreated = rdfSingle(schema.dateCreated)

    distribution = rdfSingle(schema.distribution)
    licenseprop = rdfSingle(schema.license)

    alternateName = rdfMultiple(schema.alternateName)
    citation = rdfMultiple(schema.citation)

    keywords = rdfMultiple(schema.keywords)
    spatialCoverage = rdfSingle(schema.spatialCoverage)
    temporalCoverage = rdfSingle(schema.temporalCoverage)


class DataDownload(Entity):
    rdf_type = schema.DataDownload

    contentUrl = rdfSingle(schema.contentUrl)
    encodingFormat = rdfSingle(schema.encodingFormat)


# Prov


class Derivation(rdfSubject):
    rdf_type = prov.Derivation

    hadActivity = rdfSingle(prov.hadActivity, range_type=prov.Activity)
    entity = rdfMultiple(prov.entity, range_type=prov.Entity)


class Activity(rdfSubject):
    rdf_type = prov.Activity

    wasAssociatedWith = rdfSingle(prov.wasAssociatedWith,
                                  range_type=prov.Agent)
    qualifiedAssociation = rdfSingle(prov.qualifiedAssociation,
                                     range_type=prov.Association)

    comment = rdfSingle(RDFS.comment)


class Association(rdfSubject):
    rdf_type = prov.Association

    hadPlan = rdfSingle(prov.hadPlan, range_type=prov.Plan)
    agent = rdfSingle(prov.agent, range_type=prov.Agent)

    comment = rdfSingle(RDFS.comment)


class Plan(rdfSubject):
    rdf_type = prov.Plan

    comment = rdfSingle(RDFS.comment)


class Agent(rdfSubject):
    rdf_type = prov.Agent


#############
# SAA Index #
#############


class Entity(rdfSubject):
    rdf_type = prov.Entity
    label = rdfMultiple(RDFS.label)
    comment = rdfMultiple(RDFS.comment)

    wasDerivedFrom = rdfMultiple(prov.wasDerivedFrom)
    qualifiedDerivation = rdfSingle(prov.qualifiedDerivation,
                                    range_type=prov.Derivation)

    inDataset = rdfSingle(void.inDataset)

    hasLocation = rdfMultiple(roar.hasLocation)

    documentedIn = rdfSingle(roar.documentedIn)

    identifier = rdfSingle(schema.identifier)


class Observation(Entity):
    rdf_type = roar.Observation

    locationInDocument = rdfSingle(roar.locationInDocument)


class Reconstruction(Entity):
    rdf_type = roar.Reconstruction

    sameAs = rdfSingle(schema.sameAs)


class ProvidedCHO(Entity):
    rdf_type = edm.ProvidedCHO


class WebResource(Entity):
    rdf_type = edm.WebResource


class Aggregation(Entity):
    rdf_type = edm.Aggregation

    aggregatedCHO = rdfSingle(edm.aggregatedCHO)

    hasView = rdfSingle(edm.hasView)
    isShownAt = rdfSingle(edm.isShownAt)
    isShownBy = rdfSingle(edm.isShownBy)


class Document(Entity):
    rdf_type = roar.Document, edm.ProvidedCHO
    identifier = rdfSingle(schema.identifier)

    language = rdfSingle(schema.isInLanguage)

    label = rdfMultiple(RDFS.label)

    onScan = rdfMultiple(roar.onScan)

    items = rdfList(AS.items)  # rdf:Collection
    prev = rdfSingle(AS.prev)
    next = rdfSingle(AS.next)


class Derivation(rdfSubject):
    rdf_type = prov.Derivation
    label = rdfMultiple(RDFS.label)
    comment = rdfMultiple(RDFS.comment)

    hadActivity = rdfSingle(prov.hadActivity)
    entity = rdfMultiple(prov.entity)


class Activity(rdfSubject):
    rdf_type = prov.Activity
    label = rdfMultiple(RDFS.label)
    comment = rdfMultiple(RDFS.comment)

    wasAssociatedWith = rdfMultiple(prov.wasAssociatedWith,
                                    range_type=prov.Agent)
    qualifiedAssociation = rdfSingle(prov.qualifiedAssociation,
                                     range_type=prov.Association)


class Agent(rdfSubject):
    rdf_type = prov.Agent
    label = rdfMultiple(RDFS.label)
    comment = rdfMultiple(RDFS.comment)


class StructuredValue(rdfSubject):
    value = rdfSingle(RDF.value)

    role = rdfSingle(roar.role)

    hasTimeStamp = rdfSingle(sem.hasTimeStamp)
    hasBeginTimeStamp = rdfSingle(sem.hasBeginTimeStamp)
    hasEndTimeStamp = rdfSingle(sem.hasEndTimeStamp)
    hasEarliestBeginTimeStamp = rdfSingle(sem.hasEarliestBeginTimeStamp)
    hasLatestBeginTimeStamp = rdfSingle(sem.hasLatestBeginTimeStamp)
    hasEarliestEndTimeStamp = rdfSingle(sem.hasEarliestEndTimeStamp)
    hasLatestEndTimeStamp = rdfSingle(sem.hasLatestEndTimeStamp)

    label = rdfMultiple(RDFS.label)


##########
# Person #
##########


class Person(Entity):
    rdf_type = schema.Person

    hasName = rdfMultiple(pnv.hasName, range_type=pnv.PersonName)  # resource

    label = rdfMultiple(RDFS.label)

    birth = rdfSingle(bio.birth)
    death = rdfSingle(bio.death)
    event = rdfMultiple(bio.event)

    birthDate = rdfSingle(schema.birthDate)
    birthPlace = rdfSingle(schema.birthPlace)
    deathDate = rdfSingle(schema.deathDate)
    deathPlace = rdfSingle(schema.deathPlace)

    gender = rdfSingle(schema.gender)

    mother = rdfSingle(bio.mother)
    father = rdfSingle(bio.father)
    child = rdfSingle(bio.child)

    spouse = rdfMultiple(schema.spouse)
    parent = rdfMultiple(schema.parent)
    children = rdfMultiple(schema.children)

    hasOccupation = rdfMultiple(schema.hasOccupation)

    address = rdfSingle(schema.address)
    homeLocation = rdfSingle(schema.homeLocation)

    depiction = rdfSingle(foaf.depiction)


class PersonObservation(Person, Observation):
    rdf_type = roar.PersonObservation


class PersonReconstruction(Person, Reconstruction):
    rdf_type = roar.PersonReconstruction


class LocationObservation(Observation):
    rdf_type = roar.LocationObservation

    hasPerson = rdfMultiple(roar.hasPerson)
    address = rdfSingle(schema.address)

    geoWithin = rdfSingle(schema.geoWithin)


class LocationReconstruction(Reconstruction):
    rdf_type = roar.LocationReconstruction


class PostalAddress(Entity):
    rdf_type = schema.PostalAddress

    streetAddress = rdfSingle(schema.streetAddress)
    addressRegion = rdfSingle(schema.addressRegion)
    postalCode = rdfSingle(schema.postalCode)
    disambiguatingDescription = rdfSingle(schema.disambiguatingDescription)


class PersonName(rdfSubject):
    rdf_type = pnv.PersonName
    label = rdfSingle(RDFS.label)

    literalName = rdfSingle(pnv.literalName)
    givenName = rdfSingle(pnv.givenName)
    surnamePrefix = rdfSingle(pnv.surnamePrefix)
    baseSurname = rdfSingle(pnv.baseSurname)

    prefix = rdfSingle(pnv.prefix)
    disambiguatingDescription = rdfSingle(pnv.disambiguatingDescription)
    patronym = rdfSingle(pnv.patronym)
    surname = rdfSingle(pnv.surname)

    nameSpecification = rdfSingle(pnv.nameSpecification)


class Occupation(rdfSubject):
    rdf_type = schema.Occupation
    label = rdfMultiple(RDFS.label)
    name = rdfMultiple(schema.name)

    occupationalCategory = rdfMultiple(schema.occupationalCategory,
                                       range_type=schema.CategoryCode)


class OccupationObservation(Entity):
    rdf_type = roar.OccupationObservation
    label = rdfMultiple(RDFS.label)
    name = rdfMultiple(schema.name)

    occupationalCategory = rdfMultiple(schema.occupationalCategory,
                                       range_type=schema.CategoryCode)


class CategoryCode(rdfSubject):
    rdf_type = schema.CategoryCode
    inCodeSet = rdfSingle(schema.inCodeSet, range_type=schema.CategoryCodeSet)
    codeValue = rdfSingle(schema.codeValue)

    label = rdfMultiple(RDFS.label)
    name = rdfMultiple(schema.name)


class CategoryCodeSet(rdfSubject):
    rdf_type = schema.CategoryCodeSet
    label = rdfMultiple(RDFS.label)
    name = rdfMultiple(schema.name)

    # {
    #     "@context": "http://schema.org/",
    #     "@type": "Occupation",
    #     "name": "Film actor",
    #     "occupationalCategory": {
    #         "@type": "CategoryCode",
    #         "inCodeSet": {
    #             "@type": "CategoryCodeSet",
    #             "name": "HISCO"
    #         },
    #         "codeValue": "17320",
    #         "name": "Actor"
    #     }
    # }


class Annotation(Entity):
    rdf_type = oa.Annotation
    hasTarget = rdfSingle(oa.hasTarget)

    bodyValue = rdfSingle(oa.bodyValue)
    hasBody = rdfSingle(oa.hasBody)  # or multiple?

    motivatedBy = rdfSingle(oa.motivatedBy)

    depiction = rdfSingle(foaf.depiction)


class SpecificResource(Entity):
    rdf_type = oa.SpecificResource

    hasSource = rdfSingle(oa.hasSource)
    hasSelector = rdfSingle(oa.hasSelector)
    hasState = rdfSingle(oa.hasState)
    hasPurpose = rdfSingle(oa.hasPurpose)


class Selector(Entity):
    rdf_type = oa.Selector


class FragmentSelector(Entity):
    rdf_type = oa.FragmentSelector

    conformsTo = rdfSingle(dcterms.conformsTo)
    value = rdfSingle(RDF.value)


class TextQuoteSelector(Entity):
    rdf_type = oa.TextQuoteSelector


class TextPositionSelector(Entity):
    rdf_type = oa.TextPositionSelector


class ResourceSelection(Entity):
    rdf_type = None

    hasSource = rdfSingle(oa.hasSource)
    hasSelector = rdfSingle(oa.hasSelector)
    hasState = rdfSingle(oa.hasState)


class TextualBody(Entity):
    rdf_type = oa.TextualBody

    value = rdfSingle(RDF.value)
    language = rdfSingle(dc.language)
    format = rdfSingle(dc.term('format'))
