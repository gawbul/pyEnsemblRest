from typing import Any

from . import __version__

# Set Ensembl REST URL
ensembl_default_url = "https://rest.ensembl.org"

# Ensembl API lookup table
# Specifies the functions relevant to the Ensembl REST server
ensembl_api_table: dict[str, Any] = {
    # Archive
    "getArchiveById": {
        "doc": "Uses the given identifier to return its latest version",
        "url": "/archive/id/{{id}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getArchiveByMultipleIds": {
        "doc": "Retrieve the latest version for a set of identifiers",
        "url": "/archive/id",
        "method": "POST",
        "content_type": "application/json",
        "post_parameters": ["id"],
    },
    # Comparative Genomics
    "getCafeGeneTreeById": {
        "doc": "Retrieves a cafe tree of the gene tree using the gene tree stable identifier",
        "url": "/cafe/genetree/id/{{id}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getCafeGeneTreeMemberBySymbol": {
        "doc": "Retrieves the cafe tree of the gene tree that contains the gene identified by a symbol",
        "url": "/cafe/genetree/member/symbol/{{species}}/{{symbol}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getCafeGeneTreeMemberById": {
        "doc": "Retrieves the cafe tree of the gene tree that contains the gene / transcript / translation stable identifier in the given species",
        "url": "/cafe/genetree/member/id/{{species}}/{{id}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getGeneTreeById": {
        "doc": "Retrieves a gene tree for a gene tree stable identifier",
        "url": "/genetree/id/{{id}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getGeneTreeMemberBySymbol": {
        "doc": "Retrieves the gene tree that contains the gene identified by a symbol",
        "url": "/genetree/member/symbol/{{species}}/{{symbol}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getGeneTreeMemberById": {
        "doc": "Retrieves the gene tree that contains the gene / transcript / translation stable identifier in the given species",
        "url": "/genetree/member/id/{{species}}/{{id}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getAlignmentByRegion": {
        "doc": "Retrieves genomic alignments as separate blocks based on a region and species",
        "url": "/alignment/region/{{species}}/{{region}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getHomologyById": {
        "doc": "Retrieves homology information (orthologs) by species and Ensembl gene id",
        "url": "/homology/id/{{species}}/{{id}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getHomologyBySymbol": {
        "doc": "Retrieves homology information (orthologs) by symbol",
        "url": "/homology/symbol/{{species}}/{{symbol}}",
        "method": "GET",
        "content_type": "application/json",
    },
    # Cross References
    "getXrefsBySymbol": {
        "doc": """Looks up an external symbol and returns all Ensembl objects linked to it. """
        """This can be a display name for a gene/transcript/translation, """
        """a synonym or an externally linked reference. """
        """If a gene's transcript is linked to the supplied symbol """
        """the service will return both gene and transcript (it supports transient links).""",
        "url": "/xrefs/symbol/{{species}}/{{symbol}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getXrefsById": {
        "doc": "Perform lookups of Ensembl Identifiers and retrieve their external references in other databases",
        "url": "/xrefs/id/{{id}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getXrefsByName": {
        "doc": """Performs a lookup based upon the primary accession or display label of an external reference  """
        """and returning the information we hold about the entry""",
        "url": "/xrefs/name/{{species}}/{{name}}",
        "method": "GET",
        "content_type": "application/json",
    },
    # Information
    "getInfoAnalysis": {
        "doc": "List the names of analyses involved in generating Ensembl data.",
        "url": "/info/analysis/{{species}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getInfoAssembly": {
        "doc": """List the currently available assemblies for a species, along with toplevel sequences, """
        """chromosomes and cytogenetic bands.""",
        "url": "/info/assembly/{{species}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getInfoAssemblyRegion": {
        "doc": "Returns information about the specified toplevel sequence region for the given species.",
        "url": "/info/assembly/{{species}}/{{region_name}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getInfoBiotypes": {
        "doc": """List the functional classifications of gene models that Ensembl associates with a particular species. """
        """Useful for restricting the type of genes/transcripts retrieved by other endpoints.""",
        "url": "/info/biotypes/{{species}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getInfoBiotypesByGroup": {
        "doc": """Without argument the list of available biotype groups is returned. With :group argument provided, list the properties of biotypes within that group. """
        """Object type (gene or transcript) can be provided for filtering.""",
        "url": "/info/biotypes/groups/{{group}}/{{object_type}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getInfoBiotypesByName": {
        "doc": """List the properties of biotypes with a given name. """
        """Object type (gene or transcript) can be provided for filtering.""",
        "url": "/info/biotypes/name/{{name}}/{{object_type}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getInfoComparaMethods": {
        "doc": "List all compara analyses available (an analysis defines the type of comparative data).",
        "url": "/info/compara/methods",
        "method": "GET",
        "content_type": "application/json",
    },
    "getInfoComparaSpeciesSets": {
        "doc": "List all collections of species analysed with the specified compara method.",
        "url": "/info/compara/species_sets/{{methods}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getInfoComparas": {
        "doc": """Lists all available comparative genomics databases and their data release. """
        """DEPRECATED: use info/genomes/division instead.""",
        "url": "/info/comparas",
        "method": "GET",
        "content_type": "application/json",
    },
    "getInfoData": {
        "doc": """Shows the data releases available on this REST server. """
        """May return more than one release (unfrequent non-standard Ensembl configuration).""",
        "url": "/info/data",
        "method": "GET",
        "content_type": "application/json",
    },
    "getInfoEgVersion": {
        "doc": "Returns the Ensembl Genomes version of the databases backing this service",
        "url": "/info/eg_version",
        "method": "GET",
        "content_type": "application/json",
    },
    "getInfoExternalDbs": {
        "doc": "Lists all available external sources for a species.",
        "url": "/info/external_dbs/{{species}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getInfoDivisions": {
        "doc": "Get list of all Ensembl divisions for which information is available",
        "url": "/info/divisions",
        "method": "GET",
        "content_type": "application/json",
    },
    "getInfoGenomesByName": {
        "doc": "Find information about a given genome",
        "url": "/info/genomes/{{name}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getInfoGenomesByAccession": {
        "doc": "Find information about genomes containing a specified INSDC accession",
        "url": "/info/genomes/accession/{{accession}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getInfoGenomesByAssembly": {
        "doc": "Find information about a genome with a specified assembly",
        "url": "/info/genomes/assembly/{{assembly_id}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getInfoGenomesByDivision": {
        "doc": "Find information about all genomes in a given division. May be large for Ensembl Bacteria.",
        "url": "/info/genomes/division/{{division}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getInfoGenomesByTaxonomy": {
        "doc": "Find information about all genomes beneath a given node of the taxonomy",
        "url": "/info/genomes/taxonomy/{{taxon_name}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getInfoPing": {
        "doc": "Checks if the service is alive.",
        "url": "/info/ping",
        "method": "GET",
        "content_type": "application/json",
    },
    "getInfoRest": {
        "doc": "Shows the current version of the Ensembl REST API.",
        "url": "/info/rest",
        "method": "GET",
        "content_type": "application/json",
    },
    "getInfoSoftware": {
        "doc": "Shows the current version of the Ensembl API used by the REST server.",
        "url": "/info/software",
        "method": "GET",
        "content_type": "application/json",
    },
    "getInfoSpecies": {
        "doc": "Lists all available species, their aliases, available adaptor groups and data release.",
        "url": "/info/species",
        "method": "GET",
        "content_type": "application/json",
    },
    "getInfoVariationBySpecies": {
        "doc": "List the variation sources used in Ensembl for a species.",
        "url": "/info/variation/{{species}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getInfoVariationConsequenceTypes": {
        "doc": "Lists all variant consequence types.",
        "url": "/info/variation/consequence_types",
        "method": "GET",
        "content_type": "application/json",
    },
    "getInfoVariationPopulationIndividuals": {
        "doc": "List all individuals for a population from a species",
        "url": "/info/variation/populations/{{species}}/{{population_name}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getInfoVariationPopulations": {
        "doc": "List all populations for a species",
        "url": "/info/variation/populations/{{species}}",
        "method": "GET",
        "content_type": "application/json",
    },
    # Linkage Disequilibrium
    "getLdId": {
        "doc": """Computes and returns LD values between the given variant and all other variants """
        """in a window centered around the given variant. The window size is set to 500 kb.""",
        "url": "/ld/{{species}}/{{id}}/{{population_name}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getLdPairwise": {
        "doc": "Computes and returns LD values between the given variants.",
        "url": "/ld/{{species}}/pairwise/{{id1}}/{{id2}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getLdRegion": {
        "doc": "Computes and returns LD values between all pairs of variants in the defined region.",
        "url": "/ld/{{species}}/region/{{region}}/{{population_name}}",
        "method": "GET",
        "content_type": "application/json",
    },
    # Lookup
    "getLookupById": {
        "doc": "Find the species and database for a single identifier e.g. gene, transcript, protein",
        "url": "/lookup/id/{{id}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getLookupByMultipleIds": {
        "doc": """Find the species and database for several identifiers. """
        """IDs that are not found are returned with no data.""",
        "url": "/lookup/id",
        "method": "POST",
        "content_type": "application/json",
        "post_parameters": ["ids"],
    },
    "getLookupBySymbol": {
        "doc": "Find the species and database for a symbol in a linked external database",
        "url": "/lookup/symbol/{{species}}/{{symbol}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getLookupByMultipleSymbols": {
        "doc": """Find the species and database for a set of symbols in a linked external database. """
        """Unknown symbols are omitted from the response.""",
        "url": "/lookup/symbol/{{species}}",
        "method": "POST",
        "content_type": "application/json",
        "post_parameters": ["symbols"],
    },
    # Mapping
    "getMapCdnaToRegion": {
        "doc": """Convert from cDNA coordinates to genomic coordinates. """
        """Output reflects forward orientation coordinates as returned from the Ensembl API.""",
        "url": "/map/cdna/{{id}}/{{region}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getMapCdsToRegion": {
        "doc": """Convert from CDS coordinates to genomic coordinates. """
        """Output reflects forward orientation coordinates as returned from the Ensembl API.""",
        "url": "/map/cds/{{id}}/{{region}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getMapAssemblyOneToTwo": {
        "doc": "Convert the co-ordinates of one assembly to another",
        "url": "/map/{{species}}/{{asm_one}}/{{region}}/{{asm_two}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getMapTranslationToRegion": {
        "doc": """Convert from protein (translation) coordinates to genomic coordinates. """
        """Output reflects forward orientation coordinates as returned from the Ensembl API.""",
        "url": "/map/translation/{{id}}/{{region}}",
        "method": "GET",
        "content_type": "application/json",
    },
    # Ontologies and Taxonomy
    "getAncestorsById": {
        "doc": "Reconstruct the entire ancestry of a term from is_a and part_of relationships",
        "url": "/ontology/ancestors/{{id}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getAncestorsChartById": {
        "doc": "Reconstruct the entire ancestry of a term from is_a and part_of relationships.",
        "url": "/ontology/ancestors/chart/{{id}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getDescendantsById": {
        "doc": """Find all the terms descended from a given term. """
        """By default searches are conducted within the namespace of the given identifier""",
        "url": "/ontology/descendants/{{id}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getOntologyById": {
        "doc": "Search for an ontological term by its namespaced identifier",
        "url": "/ontology/id/{{id}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getOntologyByName": {
        "doc": "Search for a list of ontological terms by their name",
        "url": "/ontology/name/{{name}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getTaxonomyClassificationById": {
        "doc": "Return the taxonomic classification of a taxon node",
        "url": "/taxonomy/classification/{{id}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getTaxonomyById": {
        "doc": "Search for a taxonomic term by its identifier or name",
        "url": "/taxonomy/id/{{id}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getTaxonomyByName": {
        "doc": "Search for a taxonomic id by a non-scientific name",
        "url": "/taxonomy/name/{{name}}",
        "method": "GET",
        "content_type": "application/json",
    },
    # Overlap
    "getOverlapById": {
        "doc": """Retrieves features (e.g. genes, transcripts, variants and more) """
        """that overlap a region defined by the given identifier.""",
        "url": "/overlap/id/{{id}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getOverlapByRegion": {
        "doc": """Retrieves features (e.g. genes, transcripts, variants and more) """
        """that overlap a given region.""",
        "url": "/overlap/region/{{species}}/{{region}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getOverlapByTranslation": {
        "doc": """Retrieve features related to a specific Translation as described """
        """by its stable ID (e.g. domains, variants).""",
        "url": "/overlap/translation/{{id}}",
        "method": "GET",
        "content_type": "application/json",
    },
    # Phenotype annotations
    "getPhenotypeByAccession": {
        "doc": "Return phenotype annotations for genomic features given a phenotype ontology accession",
        "url": "/phenotype/accession/{{species}}/{{accession}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getPhenotypeByGene": {
        "doc": "Return phenotype annotations for a given gene.",
        "url": "/phenotype/gene/{{species}}/{{gene}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getPhenotypeByRegion": {
        "doc": "Return phenotype annotations that overlap a given genomic region.",
        "url": "/phenotype/region/{{species}}/{{region}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getPhenotypeByTerm": {
        "doc": "Return phenotype annotations for genomic features given a phenotype ontology term",
        "url": "/phenotype/term/{{species}}/{{term}}",
        "method": "GET",
        "content_type": "application/json",
    },
    # Regulation
    "getRegulationBindingMatrix": {
        "doc": "Return the specified binding matrix",
        "url": "/species/{{species}}/binding_matrix/{{binding_matrix}}/",
        "method": "GET",
        "content_type": "application/json",
    },
    # Sequences
    "getSequenceById": {
        "doc": """Request multiple types of sequence by stable identifier. """
        """Supports feature masking and expand options.""",
        "url": "/sequence/id/{{id}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getSequenceByMultipleIds": {
        "doc": "Request multiple types of sequence by a stable identifier list.",
        "url": "/sequence/id",
        "method": "POST",
        "content_type": "application/json",
        "post_parameters": ["ids"],
    },
    "getSequenceByRegion": {
        "doc": """Returns the genomic sequence of the specified region of the given species. """
        """Supports feature masking and expand options.""",
        "url": "/sequence/region/{{species}}/{{region}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getSequenceByMultipleRegions": {
        "doc": "Request multiple types of sequence by a list of regions.",
        "url": "/sequence/region/{{species}}",
        "method": "POST",
        "content_type": "application/json",
        "post_parameters": ["regions"],
    },
    # Transcript Haplotypes
    "getTranscriptHaplotypes": {
        "doc": "Computes observed transcript haplotype sequences based on phased genotype data",
        "url": "/transcript_haplotypes/{{species}}/{{id}}",
        "method": "GET",
        "content_type": "application/json",
    },
    # VEP
    "getVariantConsequencesByHGVSNotation": {
        "doc": "Fetch variant consequences based on a HGVS notation",
        "url": "/vep/{{species}}/hgvs/{{hgvs_notation}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getVariantConsequencesByMultipleHGVSNotations": {
        "doc": "Fetch variant consequences for multiple HGVS notations",
        "url": "/vep/{{species}}/hgvs/",
        "method": "POST",
        "content_type": "application/json",
        "post_parameters": ["hgvs_notations"],
    },
    "getVariantConsequencesById": {
        "doc": "Fetch variant consequences based on a variant identifier",
        "url": "/vep/{{species}}/id/{{id}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getVariantConsequencesByMultipleIds": {
        "doc": "Fetch variant consequences for multiple ids",
        "url": "/vep/{{species}}/id",
        "method": "POST",
        "content_type": "application/json",
        "post_parameters": ["ids"],
    },
    "getVariantConsequencesByRegion": {
        "doc": "Fetch variant consequences",
        "url": "/vep/{{species}}/region/{{region}}/{{allele}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getVariantConsequencesByMultipleRegions": {
        "doc": "Fetch variant consequences for multiple regions",
        "url": "/vep/{{species}}/region",
        "method": "POST",
        "content_type": "application/json",
        "post_parameters": ["variants"],
    },
    # Variation
    "getVariationRecoderById": {
        "doc": """Translate a variant identifier, HGVS notation or genomic SPDI notation """
        """to all possible variant IDs, HGVS and genomic SPDI""",
        "url": "/variant_recoder/{{species}}/{{id}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getVariationRecoderByMultipleIds": {
        "doc": """Translate a list of variant identifiers, HGVS notations or genomic SPDI """
        """notations to all possible variant IDs, HGVS and genomic SPDI""",
        "url": "/variant_recoder/{{species}}",
        "method": "POST",
        "content_type": "application/json",
        "post_parameters": ["ids"],
    },
    "getVariationById": {
        "doc": """Uses a variant identifier (e.g. rsID) to return the variation features """
        """including optional genotype, phenotype and population data""",
        "url": "/variation/{{species}}/{{id}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getVariationByPMCID": {
        "doc": """Uses a variant identifier (e.g. rsID) to return the variation features """
        """including optional genotype, phenotype and population data""",
        "url": "/variation/{{species}}/pmcid/{{pmcid}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getVariationByPMID": {
        "doc": """Uses a variant identifier (e.g. rsID) to return the variation features """
        """including optional genotype, phenotype and population data""",
        "url": "/variation/{{species}}/pmid/{{pmid}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getVariationByMultipleIds": {
        "doc": """Uses a list of variant identifiers (e.g. rsID) to return the variation features """
        """including optional genotype, phenotype and population data """,
        "url": "/variation/{{species}}",
        "method": "POST",
        "content_type": "application/json",
        "post_parameters": ["ids"],
    },
    # Variation GA4GH
    "getGA4GHBeacon": {
        "doc": "Return Beacon information",
        "url": "/ga4gh/beacon",
        "method": "GET",
        "content_type": "application/json",
    },
    "getGA4GHBeaconQuery": {
        "doc": "Return the Beacon response for allele information",
        "url": "/ga4gh/beacon/query?"
        "alternateBases={{alternateBases}};"
        "assemblyId={{assemblyId}};"
        "end={{end}};"
        "referenceBases={{referenceBases}}"
        "referenceName={{referenceName}}"
        "start={{start}}"
        "variantType={{variantType}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "postGA4GHBeaconQuery": {
        "doc": "Return the Beacon response for allele information",
        "url": "/ga4gh/beacon/query?",
        "method": "POST",
        "content_type": "application/json",
        "post_parameters": [
            "alternateBases"
            "assemblyId"
            "end"
            "referenceBases"
            "referenceName"
            "start"
            "variantType",
        ],
    },
    "getGA4GHFeaturesById": {
        "doc": "Return the GA4GH record for a specific sequence feature given its identifier",
        "url": "/ga4gh/features/{{id}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "searchGA4GHFeatures": {
        "doc": "Return a list of sequence annotation features in GA4GH format",
        "url": "/ga4gh/features/search",
        "method": "POST",
        "content_type": "application/json",
        "post_parameters": [
            "end",
            "referenceName",
            "start",
            "featureSetId",
            "parentId",
        ],
    },
    "searchGA4GHCallset": {
        "doc": "Return a list of sets of genotype calls for specific samples in GA4GH format",
        "url": "/ga4gh/callsets/search",
        "method": "POST",
        "content_type": "application/json",
        "post_parameters": ["variantSetId", "name", "pageToken", "pageSize"],
    },
    "getGA4GHCallsetById": {
        "doc": "Return the GA4GH record for a specific CallSet given its identifier",
        "url": "/ga4gh/callsets/{{id}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "searchGA4GHDatasets": {
        "doc": "Return a list of datasets in GA4GH format",
        "url": "/ga4gh/datasets/search",
        "method": "POST",
        "content_type": "application/json",
        "post_parameters": ["pageToken", "pageSize"],
    },
    "getGA4GHDatasetsById": {
        "doc": "Return the GA4GH record for a specific dataset given its identifier",
        "url": "/ga4gh/datasets/{{id}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "searchGA4GHFeaturesets": {
        "doc": "Return a list of feature sets in GA4GH format",
        "url": "/ga4gh/featuresets/search",
        "method": "POST",
        "content_type": "application/json",
        "post_parameters": ["datasetId", "pageToken", "pageSize"],
    },
    "getGA4GHFeaturesetsById": {
        "doc": "Return the GA4GH record for a specific featureSet given its identifier",
        "url": "/ga4gh/featuresets/{{id}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "getGA4GHVariantsById": {
        "doc": "Return the GA4GH record for a specific variant given its identifier.",
        "url": "/ga4gh/variants/{{id}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "searchGA4GHVariantAnnotations": {
        "doc": "Return variant annotation information in GA4GH format for a region on a reference sequence",
        "url": "/ga4gh/variantannotations/search",
        "method": "POST",
        "content_type": "application/json",
        "post_parameters": [
            "variantAnnotationSetId",
            "effects",
            "end",
            "pageSize",
            "pageToken",
            "referenceId",
            "referenceName",
            "start",
        ],
    },
    "searchGA4GHVariants": {
        "doc": "Return variant call information in GA4GH format for a region on a reference sequence",
        "url": "/ga4gh/variants/search",
        "method": "POST",
        "content_type": "application/json",
        "post_parameters": [
            "variantSetId",
            "callSetIds",
            "referenceName",
            "start",
            "end",
            "pageToken",
            "pageSize",
        ],
    },
    "searchGA4GHVariantsets": {
        "doc": "Return a list of variant sets in GA4GH format",
        "url": "/ga4gh/variantsets/search",
        "method": "POST",
        "content_type": "application/json",
        "post_parameters": ["datasetId", "pageToken", "pageSize"],
    },
    "getGA4GHVariantsetsById": {
        "doc": "Return the GA4GH record for a specific VariantSet given its identifier",
        "url": "/ga4gh/variantsets/{{id}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "searchGA4GHReferences": {
        "doc": "Return a list of reference sequences in GA4GH format",
        "url": "/ga4gh/references/search",
        "method": "POST",
        "content_type": "application/json",
        "post_parameters": [
            "referenceSetId",
            "md5checksum",
            "accession",
            "pageToken",
            "pageSize",
        ],
    },
    "getGA4GHReferencesById": {
        "doc": "Return data for a specific reference in GA4GH format by id",
        "url": "/ga4gh/references/{{id}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "searchGA4GHReferencesets": {
        "doc": "Return a list of reference sets in GA4GH format",
        "url": "/ga4gh/referencesets/search",
        "method": "POST",
        "content_type": "application/json",
        "post_parameters": ["accession", "pageToken", "pageSize"],
    },
    "getGA4GHReferencesetsById": {
        "doc": "Return data for a specific reference set in GA4GH format",
        "url": "/ga4gh/referencesets/{{id}}",
        "method": "GET",
        "content_type": "application/json",
    },
    "searchGA4GHVariantAnnotationsets": {
        "doc": "Return a list of annotation sets in GA4GH format",
        "url": "/ga4gh/variantannotationsets/search",
        "method": "POST",
        "content_type": "application/json",
        "post_parameters": ["variantSetId", "pageToken", "pageSize"],
    },
    "getGA4GHVariantAnnotationsetsById": {
        "doc": "Return meta data for a specific annotation set in GA4GH format",
        "url": "/ga4gh/variantannotationsets/{{id}}",
        "method": "GET",
        "content_type": "application/json",
    },
}

# Define HTTP status codes
ensembl_http_status_codes: dict[int, Any] = {
    200: (
        "OK",
        "Request was a success. Only process data from the service when you receive this code",
    ),
    400: (
        "Bad Request",
        "Occurs during exceptional circumstances such as the service is unable to find an ID. "
        "Check if the response Content-type or Accept was JSON. "
        "If so the JSON object is an exception hash with the message keyed under error",
    ),
    403: (
        "Forbidden",
        "You are submitting far too many requests and have been temporarily forbidden access to the service. "
        "Wait and retry with a maximum of 15 requests per second.",
    ),
    404: ("Not Found", "Indicates a badly formatted request. Check your URL"),
    408: ("Timeout", "The request was not processed in time. Wait and retry later"),
    415: (
        "Unsupported Media Type",
        "The server is refusing to service the request "
        "because the entity of the request is in a format not supported "
        "by the requested resource for the requested method",
    ),
    429: (
        "Too Many Requests",
        "You have been rate-limited; wait and retry. "
        "The headers X-RateLimit-Reset, X-RateLimit-Limit and X-RateLimit-Remaining will inform you "
        "of how long you have until your limit is reset and what that limit was. "
        "If you get this response and have not exceeded your limit then check "
        "if you have made too many requests per second.",
    ),
    500: (
        "Internal Server Error",
        "This error is not documented. Maybe there is an error in user input or "
        "the REST server could have problems. Try to do the query with curl. "
        "If your data input and query are correct, contact the Ensembl team",
    ),
    503: (
        "Service Unavailable",
        "The service is temporarily down; retry after a pause",
    ),
}

# Set the user agent
ensembl_user_agent = "pyEnsemblRest v" + __version__
ensembl_header = {"User-Agent": ensembl_user_agent}
ensembl_content_type = "application/json"

# Define known errors
ensembl_known_errors = [
    "something bad has happened",
    "Something went wrong while fetching from LDFeatureContainerAdaptor",
    "%s timeout" % ensembl_user_agent,
]
