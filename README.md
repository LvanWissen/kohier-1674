# Kohier van de 200ste penning, Amsterdam 1674

| License     |                                                                                                                                                   |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Source code | [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)                                       |
| Data        | [![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/) |


## Introduction

Van dit handgeschreven kohier (SAA inventarisnummer [5028:662](https://archief.amsterdam/archief/5028/662/)) bestaat een getypte index op achternaam (SAA inventarisnummber [5028:662A](https://archief.amsterdam/archief/5028/662A/)). Hierin is de naam van een persoon, de relatie tot een andere persoon of groep (e.g. wed. van, of kinderen van), beroep en de woonwijk opgenomen. Ook is genoteerd op welk foliant de persoon beschreven is. 



### Wijkindeling
[![Wijkindeling 60 burgerwijken](https://images.memorix.nl/ams/thumb/250x250/b4b5cd12-031d-bc79-9c07-b6028472026b.jpg)](https://beeldbank.amsterdam.nl/afbeelding/010001000849)

In totaal zijn 60 wijken beschreven in het kohier, aangegeven met cijfers. Daarna volgt een sectie van de 'Magistraten' (M), 'Joodse Natie' (J), 'Paden buijten de Stadt' (P1-P6), 'Officianten' (O), 'Regerende heeren' (R), 'Personen van andere Steden' (AS) en 'Testamenten' (T). 

De wijkindeling correspondeert waarschijnlijk met die van een kaart uit 1766, vervaardigd door C. Philips Jacobsz. (1732-1789) en F.W. Greebe en is beschikbaar in de Beeldbank van het Stadsarchief, afbeelding [010001000849](https://beeldbank.amsterdam.nl/afbeelding/010001000849). 

### Digitalisering

Scans van zowel de index, als het kohier zelf zijn beschikbaar in de Beeldbank van het Stadsarchief Amsterdam. 

#### OCR

OCR met [Tesseract](https://github.com/tesseract-ocr/tesseract) (5.0.0-alpha) op afgeleide tiff's van [Scantailor](https://github.com/4lex4/scantailor-advanced) (Advanced 1.0.16). Zie [`/data/tif/`](https://github.com/LvanWissen/kohier-1674/tree/master/data/tif). 

#### Correctie

Semi-automatische verbetering van veelvoorkomende OCR-fouten (e.g. een '&' voor een '4'). Waar regels in het origineel afgebroken waren, zijn die in de tekstbestanden als één regel opgenomen. Elke regel kent drie kolommen, gescheiden door witruimte, met al dan niet een verdere verdeling in persoonsnaam en additionele informatie door een '—' teken. 

Persoonsnamen zijn verder uitgesplitst volgens PNV ([https://w3id.org/pnv#](https://w3id.org/pnv#)).

### Conversie naar RDF

De data uit de CSV is omgezet naar RDF volgens de ROAR ([https://w3id.org/roar#](https://w3id.org/roar#)) ontologie, met aanvullingen volgens PROV ([http://www.w3.org/ns/prov#](http://www.w3.org/ns/prov#)) OA ([http://www.w3.org/ns/oa#](http://www.w3.org/ns/oa#)) en EDM ([http://www.europeana.eu/schemas/edm/](http://www.europeana.eu/schemas/edm/)). Zie: [`/data/records.trig`](https://github.com/LvanWissen/kohier-1674/blob/master/data/records.trig). 

## Contact

[l.vanwissen@uva.nl](mailto:l.vanwissen@uva.nl)







