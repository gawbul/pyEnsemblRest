import collections
from typing import Any

import requests
from requests import Response
from requests.structures import CaseInsensitiveDict

class FakeResponse:
    headers: CaseInsensitiveDict[str] | dict[str, Any]
    status_code: int
    text: str
    def __init__(
        self,
        headers: CaseInsensitiveDict[str] | dict[str, Any],
        status_code: int,
        text: str,
    ) -> None: ...

class EnsemblRest:
    api_table: dict[str, Any]
    session_args: dict[str, Any]
    reqs_per_sec: int
    wall_time: float
    _request_timestamps: collections.deque[float]
    req_count: int
    last_req: float
    rate_reset: int | None
    rate_limit: int | None
    rate_remaining: int | None
    rate_period: int | None
    retry_after: float | None
    last_url: str
    last_headers: CaseInsensitiveDict[str] | dict[str, Any]
    last_params: dict[str, Any]
    last_data: Any
    last_method: str
    last_attempt: int
    last_response: Response | FakeResponse
    max_attempts: int
    timeout: int | float
    base_url: str
    session: requests.Session

    def __init__(self, api_table: dict[str, Any] = ..., **kwargs: Any) -> None: ...
    def register_api_func(self, api_call: str, api_table: dict[str, Any]) -> Any: ...
    def call_api_func(
        self, api_call: str, api_table: dict[str, Any], **kwargs: Any
    ) -> Any: ...
    def parseResponse(
        self, resp: Response | FakeResponse, content_type: str | dict[str, Any] = ...
    ) -> Any: ...
    def close(self) -> None: ...
    def __enter__(self) -> EnsemblRest: ...
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None: ...
    def get_user_agent(self) -> str: ...
    def getArchiveById(self, id: Any, **kwargs: Any) -> Any:
        """Uses the given identifier to return its latest version"""
        ...

    def getArchiveByMultipleIds(self, id: Any = ..., **kwargs: Any) -> Any:
        """Retrieve the latest version for a set of identifiers"""
        ...

    def getCafeGeneTreeById(self, id: Any, **kwargs: Any) -> Any:
        """Retrieves a cafe tree of the gene tree using the gene tree stable identifier"""
        ...

    def getCafeGeneTreeMemberBySymbol(
        self, species: Any, symbol: Any, **kwargs: Any
    ) -> Any:
        """Retrieves the cafe tree of the gene tree that contains the gene identified by a symbol"""
        ...

    def getCafeGeneTreeMemberById(self, species: Any, id: Any, **kwargs: Any) -> Any:
        """Retrieves the cafe tree of the gene tree that contains the gene / transcript / translation stable identifier in the given species"""
        ...

    def getGeneTreeById(self, id: Any, **kwargs: Any) -> Any:
        """Retrieves a gene tree for a gene tree stable identifier"""
        ...

    def getGeneTreeMemberBySymbol(
        self, species: Any, symbol: Any, **kwargs: Any
    ) -> Any:
        """Retrieves the gene tree that contains the gene identified by a symbol"""
        ...

    def getGeneTreeMemberById(self, species: Any, id: Any, **kwargs: Any) -> Any:
        """Retrieves the gene tree that contains the gene / transcript / translation stable identifier in the given species"""
        ...

    def getAlignmentByRegion(self, species: Any, region: Any, **kwargs: Any) -> Any:
        """Retrieves genomic alignments as separate blocks based on a region and species"""
        ...

    def getHomologyById(self, species: Any, id: Any, **kwargs: Any) -> Any:
        """Retrieves homology information (orthologs) by species and Ensembl gene id"""
        ...

    def getHomologyBySymbol(self, species: Any, symbol: Any, **kwargs: Any) -> Any:
        """Retrieves homology information (orthologs) by symbol"""
        ...

    def getXrefsBySymbol(self, species: Any, symbol: Any, **kwargs: Any) -> Any:
        """Looks up an external symbol and returns all Ensembl objects linked to it. This can be a display name for a gene/transcript/translation, a synonym or an externally linked reference. If a gene's transcript is linked to the supplied symbol the service will return both gene and transcript (it supports transient links)."""
        ...

    def getXrefsById(self, id: Any, **kwargs: Any) -> Any:
        """Perform lookups of Ensembl Identifiers and retrieve their external references in other databases"""
        ...

    def getXrefsByName(self, species: Any, name: Any, **kwargs: Any) -> Any:
        """Performs a lookup based upon the primary accession or display label of an external reference  and returning the information we hold about the entry"""
        ...

    def getInfoAnalysis(self, species: Any, **kwargs: Any) -> Any:
        """List the names of analyses involved in generating Ensembl data."""
        ...

    def getInfoAssembly(self, species: Any, **kwargs: Any) -> Any:
        """List the currently available assemblies for a species, along with toplevel sequences, chromosomes and cytogenetic bands."""
        ...

    def getInfoAssemblyRegion(
        self, species: Any, region_name: Any, **kwargs: Any
    ) -> Any:
        """Returns information about the specified toplevel sequence region for the given species."""
        ...

    def getInfoBiotypes(self, species: Any, **kwargs: Any) -> Any:
        """List the functional classifications of gene models that Ensembl associates with a particular species. Useful for restricting the type of genes/transcripts retrieved by other endpoints."""
        ...

    def getInfoBiotypesByGroup(
        self, group: Any, object_type: Any, **kwargs: Any
    ) -> Any:
        """Without argument the list of available biotype groups is returned. With :group argument provided, list the properties of biotypes within that group. Object type (gene or transcript) can be provided for filtering."""
        ...

    def getInfoBiotypesByName(self, name: Any, object_type: Any, **kwargs: Any) -> Any:
        """List the properties of biotypes with a given name. Object type (gene or transcript) can be provided for filtering."""
        ...

    def getInfoComparaMethods(self, **kwargs: Any) -> Any:
        """List all compara analyses available (an analysis defines the type of comparative data)."""
        ...

    def getInfoComparaSpeciesSets(self, methods: Any, **kwargs: Any) -> Any:
        """List all collections of species analysed with the specified compara method."""
        ...

    def getInfoComparas(self, **kwargs: Any) -> Any:
        """Lists all available comparative genomics databases and their data release. DEPRECATED: use info/genomes/division instead."""
        ...

    def getInfoData(self, **kwargs: Any) -> Any:
        """Shows the data releases available on this REST server. May return more than one release (unfrequent non-standard Ensembl configuration)."""
        ...

    def getInfoEgVersion(self, **kwargs: Any) -> Any:
        """Returns the Ensembl Genomes version of the databases backing this service"""
        ...

    def getInfoExternalDbs(self, species: Any, **kwargs: Any) -> Any:
        """Lists all available external sources for a species."""
        ...

    def getInfoDivisions(self, **kwargs: Any) -> Any:
        """Get list of all Ensembl divisions for which information is available"""
        ...

    def getInfoGenomesByName(self, name: Any, **kwargs: Any) -> Any:
        """Find information about a given genome"""
        ...

    def getInfoGenomesByAccession(self, accession: Any, **kwargs: Any) -> Any:
        """Find information about genomes containing a specified INSDC accession"""
        ...

    def getInfoGenomesByAssembly(self, assembly_id: Any, **kwargs: Any) -> Any:
        """Find information about a genome with a specified assembly"""
        ...

    def getInfoGenomesByDivision(self, division: Any, **kwargs: Any) -> Any:
        """Find information about all genomes in a given division. May be large for Ensembl Bacteria."""
        ...

    def getInfoGenomesByTaxonomy(self, taxon_name: Any, **kwargs: Any) -> Any:
        """Find information about all genomes beneath a given node of the taxonomy"""
        ...

    def getInfoPing(self, **kwargs: Any) -> Any:
        """Checks if the service is alive."""
        ...

    def getInfoRest(self, **kwargs: Any) -> Any:
        """Shows the current version of the Ensembl REST API."""
        ...

    def getInfoSoftware(self, **kwargs: Any) -> Any:
        """Shows the current version of the Ensembl API used by the REST server."""
        ...

    def getInfoSpecies(self, **kwargs: Any) -> Any:
        """Lists all available species, their aliases, available adaptor groups and data release."""
        ...

    def getInfoVariationBySpecies(self, species: Any, **kwargs: Any) -> Any:
        """List the variation sources used in Ensembl for a species."""
        ...

    def getInfoVariationConsequenceTypes(self, **kwargs: Any) -> Any:
        """Lists all variant consequence types."""
        ...

    def getInfoVariationPopulationIndividuals(
        self, species: Any, population_name: Any, **kwargs: Any
    ) -> Any:
        """List all individuals for a population from a species"""
        ...

    def getInfoVariationPopulations(self, species: Any, **kwargs: Any) -> Any:
        """List all populations for a species"""
        ...

    def getLdId(
        self, species: Any, id: Any, population_name: Any, **kwargs: Any
    ) -> Any:
        """Computes and returns LD values between the given variant and all other variants in a window centered around the given variant. The window size is set to 500 kb."""
        ...

    def getLdPairwise(self, species: Any, id1: Any, id2: Any, **kwargs: Any) -> Any:
        """Computes and returns LD values between the given variants."""
        ...

    def getLdRegion(
        self, species: Any, region: Any, population_name: Any, **kwargs: Any
    ) -> Any:
        """Computes and returns LD values between all pairs of variants in the defined region."""
        ...

    def getLookupById(self, id: Any, **kwargs: Any) -> Any:
        """Find the species and database for a single identifier e.g. gene, transcript, protein"""
        ...

    def getLookupByMultipleIds(self, ids: Any = ..., **kwargs: Any) -> Any:
        """Find the species and database for several identifiers. IDs that are not found are returned with no data."""
        ...

    def getLookupBySymbol(self, species: Any, symbol: Any, **kwargs: Any) -> Any:
        """Find the species and database for a symbol in a linked external database"""
        ...

    def getLookupByMultipleSymbols(
        self, species: Any, symbols: Any = ..., **kwargs: Any
    ) -> Any:
        """Find the species and database for a set of symbols in a linked external database. Unknown symbols are omitted from the response."""
        ...

    def getMapCdnaToRegion(self, id: Any, region: Any, **kwargs: Any) -> Any:
        """Convert from cDNA coordinates to genomic coordinates. Output reflects forward orientation coordinates as returned from the Ensembl API."""
        ...

    def getMapCdsToRegion(self, id: Any, region: Any, **kwargs: Any) -> Any:
        """Convert from CDS coordinates to genomic coordinates. Output reflects forward orientation coordinates as returned from the Ensembl API."""
        ...

    def getMapAssemblyOneToTwo(
        self, species: Any, asm_one: Any, region: Any, asm_two: Any, **kwargs: Any
    ) -> Any:
        """Convert the co-ordinates of one assembly to another"""
        ...

    def getMapTranslationToRegion(self, id: Any, region: Any, **kwargs: Any) -> Any:
        """Convert from protein (translation) coordinates to genomic coordinates. Output reflects forward orientation coordinates as returned from the Ensembl API."""
        ...

    def getAncestorsById(self, id: Any, **kwargs: Any) -> Any:
        """Reconstruct the entire ancestry of a term from is_a and part_of relationships"""
        ...

    def getAncestorsChartById(self, id: Any, **kwargs: Any) -> Any:
        """Reconstruct the entire ancestry of a term from is_a and part_of relationships."""
        ...

    def getDescendantsById(self, id: Any, **kwargs: Any) -> Any:
        """Find all the terms descended from a given term. By default searches are conducted within the namespace of the given identifier"""
        ...

    def getOntologyById(self, id: Any, **kwargs: Any) -> Any:
        """Search for an ontological term by its namespaced identifier"""
        ...

    def getOntologyByName(self, name: Any, **kwargs: Any) -> Any:
        """Search for a list of ontological terms by their name"""
        ...

    def getTaxonomyClassificationById(self, id: Any, **kwargs: Any) -> Any:
        """Return the taxonomic classification of a taxon node"""
        ...

    def getTaxonomyById(self, id: Any, **kwargs: Any) -> Any:
        """Search for a taxonomic term by its identifier or name"""
        ...

    def getTaxonomyByName(self, name: Any, **kwargs: Any) -> Any:
        """Search for a taxonomic id by a non-scientific name"""
        ...

    def getOverlapById(self, id: Any, **kwargs: Any) -> Any:
        """Retrieves features (e.g. genes, transcripts, variants and more) that overlap a region defined by the given identifier."""
        ...

    def getOverlapByRegion(self, species: Any, region: Any, **kwargs: Any) -> Any:
        """Retrieves features (e.g. genes, transcripts, variants and more) that overlap a given region."""
        ...

    def getOverlapByTranslation(self, id: Any, **kwargs: Any) -> Any:
        """Retrieve features related to a specific Translation as described by its stable ID (e.g. domains, variants)."""
        ...

    def getPhenotypeByAccession(
        self, species: Any, accession: Any, **kwargs: Any
    ) -> Any:
        """Return phenotype annotations for genomic features given a phenotype ontology accession"""
        ...

    def getPhenotypeByGene(self, species: Any, gene: Any, **kwargs: Any) -> Any:
        """Return phenotype annotations for a given gene."""
        ...

    def getPhenotypeByRegion(self, species: Any, region: Any, **kwargs: Any) -> Any:
        """Return phenotype annotations that overlap a given genomic region."""
        ...

    def getPhenotypeByTerm(self, species: Any, term: Any, **kwargs: Any) -> Any:
        """Return phenotype annotations for genomic features given a phenotype ontology term"""
        ...

    def getRegulationBindingMatrix(
        self, species: Any, binding_matrix: Any, **kwargs: Any
    ) -> Any:
        """Return the specified binding matrix"""
        ...

    def getSequenceById(self, id: Any, **kwargs: Any) -> Any:
        """Request multiple types of sequence by stable identifier. Supports feature masking and expand options."""
        ...

    def getSequenceByMultipleIds(self, ids: Any = ..., **kwargs: Any) -> Any:
        """Request multiple types of sequence by a stable identifier list."""
        ...

    def getSequenceByRegion(self, species: Any, region: Any, **kwargs: Any) -> Any:
        """Returns the genomic sequence of the specified region of the given species. Supports feature masking and expand options."""
        ...

    def getSequenceByMultipleRegions(
        self, species: Any, regions: Any = ..., **kwargs: Any
    ) -> Any:
        """Request multiple types of sequence by a list of regions."""
        ...

    def getTranscriptHaplotypes(self, species: Any, id: Any, **kwargs: Any) -> Any:
        """Computes observed transcript haplotype sequences based on phased genotype data"""
        ...

    def getVariantConsequencesByHGVSNotation(
        self, species: Any, hgvs_notation: Any, **kwargs: Any
    ) -> Any:
        """Fetch variant consequences based on a HGVS notation"""
        ...

    def getVariantConsequencesByMultipleHGVSNotations(
        self, species: Any, hgvs_notations: Any = ..., **kwargs: Any
    ) -> Any:
        """Fetch variant consequences for multiple HGVS notations"""
        ...

    def getVariantConsequencesById(self, species: Any, id: Any, **kwargs: Any) -> Any:
        """Fetch variant consequences based on a variant identifier"""
        ...

    def getVariantConsequencesByMultipleIds(
        self, species: Any, ids: Any = ..., **kwargs: Any
    ) -> Any:
        """Fetch variant consequences for multiple ids"""
        ...

    def getVariantConsequencesByRegion(
        self, species: Any, region: Any, allele: Any, **kwargs: Any
    ) -> Any:
        """Fetch variant consequences"""
        ...

    def getVariantConsequencesByMultipleRegions(
        self, species: Any, variants: Any = ..., **kwargs: Any
    ) -> Any:
        """Fetch variant consequences for multiple regions"""
        ...

    def getVariationRecoderById(self, species: Any, id: Any, **kwargs: Any) -> Any:
        """Translate a variant identifier, HGVS notation or genomic SPDI notation to all possible variant IDs, HGVS and genomic SPDI"""
        ...

    def getVariationRecoderByMultipleIds(
        self, species: Any, ids: Any = ..., **kwargs: Any
    ) -> Any:
        """Translate a list of variant identifiers, HGVS notations or genomic SPDI notations to all possible variant IDs, HGVS and genomic SPDI"""
        ...

    def getVariationById(self, species: Any, id: Any, **kwargs: Any) -> Any:
        """Uses a variant identifier (e.g. rsID) to return the variation features including optional genotype, phenotype and population data"""
        ...

    def getVariationByPMCID(self, species: Any, pmcid: Any, **kwargs: Any) -> Any:
        """Uses a variant identifier (e.g. rsID) to return the variation features including optional genotype, phenotype and population data"""
        ...

    def getVariationByPMID(self, species: Any, pmid: Any, **kwargs: Any) -> Any:
        """Uses a variant identifier (e.g. rsID) to return the variation features including optional genotype, phenotype and population data"""
        ...

    def getVariationByMultipleIds(
        self, species: Any, ids: Any = ..., **kwargs: Any
    ) -> Any:
        """Uses a list of variant identifiers (e.g. rsID) to return the variation features including optional genotype, phenotype and population data"""
        ...

    def getGA4GHBeacon(self, **kwargs: Any) -> Any:
        """Return Beacon information"""
        ...

    def getGA4GHBeaconQuery(
        self,
        alternateBases: Any,
        assemblyId: Any,
        referenceBases: Any,
        referenceName: Any,
        start: Any,
        **kwargs: Any,
    ) -> Any:
        """Return the Beacon response for allele information"""
        ...

    def postGA4GHBeaconQuery(
        self,
        alternateBases: Any = ...,
        assemblyId: Any = ...,
        end: Any = ...,
        referenceBases: Any = ...,
        referenceName: Any = ...,
        start: Any = ...,
        variantType: Any = ...,
        **kwargs: Any,
    ) -> Any:
        """Return the Beacon response for allele information"""
        ...

    def getGA4GHFeaturesById(self, id: Any, **kwargs: Any) -> Any:
        """Return the GA4GH record for a specific sequence feature given its identifier"""
        ...

    def searchGA4GHFeatures(
        self,
        end: Any = ...,
        referenceName: Any = ...,
        start: Any = ...,
        featureSetId: Any = ...,
        parentId: Any = ...,
        **kwargs: Any,
    ) -> Any:
        """Return a list of sequence annotation features in GA4GH format"""
        ...

    def searchGA4GHCallset(
        self,
        variantSetId: Any = ...,
        name: Any = ...,
        pageToken: Any = ...,
        pageSize: Any = ...,
        **kwargs: Any,
    ) -> Any:
        """Return a list of sets of genotype calls for specific samples in GA4GH format"""
        ...

    def getGA4GHCallsetById(self, id: Any, **kwargs: Any) -> Any:
        """Return the GA4GH record for a specific CallSet given its identifier"""
        ...

    def searchGA4GHDatasets(
        self, pageToken: Any = ..., pageSize: Any = ..., **kwargs: Any
    ) -> Any:
        """Return a list of datasets in GA4GH format"""
        ...

    def getGA4GHDatasetsById(self, id: Any, **kwargs: Any) -> Any:
        """Return the GA4GH record for a specific dataset given its identifier"""
        ...

    def searchGA4GHFeaturesets(
        self,
        datasetId: Any = ...,
        pageToken: Any = ...,
        pageSize: Any = ...,
        **kwargs: Any,
    ) -> Any:
        """Return a list of feature sets in GA4GH format"""
        ...

    def getGA4GHFeaturesetsById(self, id: Any, **kwargs: Any) -> Any:
        """Return the GA4GH record for a specific featureSet given its identifier"""
        ...

    def getGA4GHVariantsById(self, id: Any, **kwargs: Any) -> Any:
        """Return the GA4GH record for a specific variant given its identifier."""
        ...

    def searchGA4GHVariantAnnotations(
        self,
        variantAnnotationSetId: Any = ...,
        effects: Any = ...,
        end: Any = ...,
        pageSize: Any = ...,
        pageToken: Any = ...,
        referenceId: Any = ...,
        referenceName: Any = ...,
        start: Any = ...,
        **kwargs: Any,
    ) -> Any:
        """Return variant annotation information in GA4GH format for a region on a reference sequence"""
        ...

    def searchGA4GHVariants(
        self,
        variantSetId: Any = ...,
        callSetIds: Any = ...,
        referenceName: Any = ...,
        start: Any = ...,
        end: Any = ...,
        pageToken: Any = ...,
        pageSize: Any = ...,
        **kwargs: Any,
    ) -> Any:
        """Return variant call information in GA4GH format for a region on a reference sequence"""
        ...

    def searchGA4GHVariantsets(
        self,
        datasetId: Any = ...,
        pageToken: Any = ...,
        pageSize: Any = ...,
        **kwargs: Any,
    ) -> Any:
        """Return a list of variant sets in GA4GH format"""
        ...

    def getGA4GHVariantsetsById(self, id: Any, **kwargs: Any) -> Any:
        """Return the GA4GH record for a specific VariantSet given its identifier"""
        ...

    def searchGA4GHReferences(
        self,
        referenceSetId: Any = ...,
        md5checksum: Any = ...,
        accession: Any = ...,
        pageToken: Any = ...,
        pageSize: Any = ...,
        **kwargs: Any,
    ) -> Any:
        """Return a list of reference sequences in GA4GH format"""
        ...

    def getGA4GHReferencesById(self, id: Any, **kwargs: Any) -> Any:
        """Return data for a specific reference in GA4GH format by id"""
        ...

    def searchGA4GHReferencesets(
        self,
        accession: Any = ...,
        pageToken: Any = ...,
        pageSize: Any = ...,
        **kwargs: Any,
    ) -> Any:
        """Return a list of reference sets in GA4GH format"""
        ...

    def getGA4GHReferencesetsById(self, id: Any, **kwargs: Any) -> Any:
        """Return data for a specific reference set in GA4GH format"""
        ...

    def searchGA4GHVariantAnnotationsets(
        self,
        variantSetId: Any = ...,
        pageToken: Any = ...,
        pageSize: Any = ...,
        **kwargs: Any,
    ) -> Any:
        """Return a list of annotation sets in GA4GH format"""
        ...

    def getGA4GHVariantAnnotationsetsById(self, id: Any, **kwargs: Any) -> Any:
        """Return meta data for a specific annotation set in GA4GH format"""
        ...
