# Formalising PPSR for effective re-use

## Motivation

PPSR has been described as a set of attributes for a flat schema @  

[[https://www.wilsoncenter.org/article/ppsr-core-metadata-standards]]

a formalisation of PPSR is planned but not yet published:

[[https://github.com/CitSciAssoc/DMWG-PPSR-Core]]

and 

[[https://www.cs-eu.net/news/wg-5-deliverable-citizen-science-ontology]]


The immediate goal of a formalisation is to support automation of activities like validation, configuration, presenting forms and providing discoverable explanations of meaning.

There is however another set of critical requirements for a formalisation:
1) allowing publication of "alignment" models with other standards - such as Darwin Core, DCAT, ISO19115 etc. 
2) providing the ability to describe simplified profiles of PPSR for particular uses. 

Without such profiles and known mappings to standards the chances of creating a ecosystem of PPSR based descriptions that can be effectively combined is slim. This is backed by the experience of GEOSS in trying to combine multiple catalogs of ISO19115 based metadata, where each community has used general fields in different ways or using undocumented or incompatible content values. The solution in GEOSS is an elaborate infrastructure (the Data Access Broker) painstakingly developed over many years and providing limited semantic enhancement of the collection of metadata.

Citizen science has the opportunity and need to create a much richer, yet simpler, set of profiles for different sub-communities to declare directly useful descriptions, rather than attempting to retro-fit meaning to heterogeneous and ad-hoc attempts.

## Modularity

PPSR has been described as multiple modules already:
""PPSR-Core is a set of global, transdisciplinary data and metadata standards describing contextualized details about PPSR projects (Project Data Model, or PDM), datasets (Dataset Data Model, or DDM), and data (Observation Data Model, or ODM). These standards are united, supported, and underlined by a common framework, the PPSR-Core common data model (CDM), " [[https://github.com/CitSciAssoc/DMWG-PPSR-Core/wiki/About-the-PPSR-Core#what-is-the-ppsr-core]]

The Observation Data model (ODM) relates to a wider set of metadata requirements, and experience at the OGC suggests that a range of related models are required to express observations:
* what is being measured (observable parameters, units of measure)
* how it is measured (observation process, sensor types, computational models etc)
* how the observation process is configured (parameters)
* geometric models relating sensor placement to actual observed features ("sensor models")
* data quality (limits of detection, error rates, level of validation)
* provenance (chains of processing between original observation and data products)

It is evident that there is thus a wide range of metadata required to meet requirements for citizen science outputs to be understood across project boundaries and over time. It will be impossible to create a "perfect" model for all such metadata in one step.

Thus there is a requirement for a systematic approach to modularity so that metadata requirements can be addressed incrementally, and changes to more experimental modules dont impact established cores once implemented. This is a concept called "encapsulation" and is critical to developing a sustainable information ecosystem that can evolve in a controlled and transparent way.

The net result of these concerns is thus that the PPSR modules should be described in separately managed artefacts that can be stablised independently.

## Approach

A JSON schema has been proposed for the full PPSR model for data encoded in JSON syntax. JSON-LD provides an alternative method for explaining the semantics of JSON attributes - unfortunately these approaches overlap but they are not fundamentally inconsistent.

Thus the approach is to break the PPSR model in modules, each module with set of convenient forms to support usage:
* JSON schema
* JSON context
* JSON data examples
* Spreadsheet
* SKOS terminology description (a standard for sharing definitions)
* OWL/RDF data model
* SHACL constraints language (for validation and annotation)
* Alignment ontologies mapping to well known standards.



## Plan
1) initially create a module for the "Project Data Model" and the relevant artefacts
2) publish SKOS version of property definitions on OGC definitions server
3) describe an example profile (or hierarchy) specialising this core (and publish this description as RDF at OGC)

## Resources

https://w3c.github.io/wot-thing-description/ontology/jsonschema.html





