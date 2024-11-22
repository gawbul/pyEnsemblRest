import time

from pyensemblrest import EnsemblRest

# Setup a new EnsemblRest object
ensRest = EnsemblRest()

# Check the user agent
print(ensRest.get_user_agent())


# Archive
print(ensRest.getArchiveById(id="ENSG00000157764"))
print(ensRest.getArchiveByMultipleIds(id=["ENSG00000157764", "ENSG00000248378"]))
time.sleep(15)

# Comparative Genomics
print(ensRest.getCafeGeneTreeById(id="ENSGT00390000003602"))
print(ensRest.getCafeGeneTreeMemberBySymbol(species="human", symbol="BRCA2"))
print(ensRest.getCafeGeneTreeMemberById(species="human", id="ENSG00000167664"))
print(ensRest.getGeneTreeById(id="ENSGT00390000003602"))
print(ensRest.getGeneTreeMemberBySymbol(species="human", symbol="BRCA2"))
print(ensRest.getGeneTreeMemberById(species="human", id="ENSG00000167664"))
print(
    ensRest.getAlignmentByRegion(
        species="human",
        region="X:1000000..1000100:1",
        species_set_group="mammals",
    )
)
print(ensRest.getHomologyById(species="human", id="ENSG00000157764"))
print(ensRest.getHomologyBySymbol(species="human", symbol="BRCA2"))
time.sleep(15)

# Cross References
print(ensRest.getXrefsBySymbol(species="human", symbol="BRCA2"))
print(ensRest.getXrefsById(id="ENSG00000157764"))
print(ensRest.getXrefsByName(species="human", name="BRCA2"))
time.sleep(15)

# Information
print(ensRest.getInfoAnalysis(species="homo_sapiens"))
print(
    ensRest.getInfoAssembly(species="homo_sapiens", bands=1)
)  # bands is an optional parameter
print(ensRest.getInfoAssemblyRegion(species="homo_sapiens", region_name="X"))
ensRest.timeout = 300
print(ensRest.getInfoBiotypes(species="homo_sapiens"))  # this keeps timing out
ensRest.timeout = 60
print(ensRest.getInfoBiotypesByGroup(group="coding", object_type="gene"))
print(ensRest.getInfoBiotypesByName(name="protein_coding", object_type="gene"))
print(ensRest.getInfoComparaMethods())
print(ensRest.getInfoComparaSpeciesSets(methods="EPO"))
print(ensRest.getInfoComparas())
print(ensRest.getInfoData())
print(ensRest.getInfoEgVersion())
print(ensRest.getInfoExternalDbs(species="homo_sapiens"))
print(ensRest.getInfoDivisions())
print(ensRest.getInfoGenomesByName(name="arabidopsis_thaliana"))
print(ensRest.getInfoGenomesByAccession(accession="U00096"))
print(ensRest.getInfoGenomesByAssembly(assembly_id="GCA_902167145.1"))
print(ensRest.getInfoGenomesByDivision(division="EnsemblPlants"))
print(ensRest.getInfoGenomesByTaxonomy(taxon_name="Homo sapiens"))
print(ensRest.getInfoPing())
print(ensRest.getInfoRest())
print(ensRest.getInfoSoftware())
print(ensRest.getInfoSpecies())
print(ensRest.getInfoVariationBySpecies(species="homo_sapiens"))
print(ensRest.getInfoVariationConsequenceTypes())
print(
    ensRest.getInfoVariationPopulationIndividuals(
        species="human", population_name="1000GENOMES:phase_3:ASW"
    )
)
print(ensRest.getInfoVariationPopulations(species="homo_sapiens", filter="LD"))
time.sleep(15)

# Linkage Disequilibrium
print(
    ensRest.getLdId(
        species="homo_sapiens",
        id="rs56116432",
        population_name="1000GENOMES:phase_3:KHV",
        window_size=500,
        d_prime=1.0,
    )
)
print(ensRest.getLdPairwise(species="homo_sapiens", id1="rs6792369", id2="rs1042779"))
print(
    ensRest.getLdRegion(
        species="homo_sapiens",
        region="6:25837556..25843455",
        population_name="1000GENOMES:phase_3:KHV",
    )
)
time.sleep(15)

# Lookup
print(ensRest.getLookupById(id="ENSG00000157764"))
print(ensRest.getLookupByMultipleIds(ids=["ENSG00000157764", "ENSG00000248378"]))
print(ensRest.getLookupBySymbol(species="homo_sapiens", symbol="BRCA2", expand=1))
print(
    ensRest.getLookupByMultipleSymbols(
        species="homo_sapiens", symbols=["BRCA2", "BRAF"]
    )
)
time.sleep(15)

# Mapping
print(ensRest.getMapCdnaToRegion(id="ENST00000288602", region="100..300"))
print(ensRest.getMapCdsToRegion(id="ENST00000288602", region="1..1000"))
print(
    ensRest.getMapAssemblyOneToTwo(
        species="homo_sapiens",
        asm_one="GRCh37",
        region="X:1000000..1000100:1",
        asm_two="GRCh38",
    )
)
print(ensRest.getMapTranslationToRegion(id="ENSP00000288602", region="100..300"))
time.sleep(15)

# Ontologies and Taxonomy
print(ensRest.getAncestorsById(id="GO:0005667"))
print(ensRest.getAncestorsChartById(id="GO:0005667"))
print(ensRest.getDescendantsById(id="GO:0005667"))
print(ensRest.getOntologyById(id="GO:0005667"))
print(ensRest.getOntologyByName(name="transcription factor complex"))
print(ensRest.getTaxonomyClassificationById(id="9606"))
print(ensRest.getTaxonomyById(id="9606"))
print(ensRest.getTaxonomyByName(name="Homo%25"))
time.sleep(15)

# Overlap
print(ensRest.getOverlapById(id="ENSG00000157764", feature="gene"))
print(
    ensRest.getOverlapByRegion(
        species="homo_sapiens", region="X:1..1000:1", feature="gene"
    )
)
print(ensRest.getOverlapByTranslation(id="ENSP00000288602"))
time.sleep(15)

# Phenotype annotations
print(ensRest.getPhenotypeByAccession(species="homo_sapiens", accession="EFO:0003900"))
print(ensRest.getPhenotypeByGene(species="homo_sapiens", gene="ENSG00000157764"))
print(
    ensRest.getPhenotypeByRegion(species="homo_sapiens", region="9:22125500-22136000:1")
)
print(ensRest.getPhenotypeByTerm(species="homo_sapiens", term="coffee consumption"))
time.sleep(15)

# Regulation
print(
    ensRest.getRegulationBindingMatrix(
        species="homo_sapiens", binding_matrix="ENSPFM0001"
    )
)
time.sleep(15)

# Sequences
print(ensRest.getSequenceById(id="ENSG00000157764"))
print(ensRest.getSequenceByMultipleIds(ids=["ENSG00000157764", "ENSG00000248378"]))
print(
    ensRest.getSequenceByRegion(species="homo_sapiens", region="X:1000000..1000100:1")
)
print(
    ensRest.getSequenceByMultipleRegions(
        species="homo_sapiens",
        regions=["X:1000000..1000100:1", "ABBA01004489.1:1..100"],
    )
)
time.sleep(15)

# Transcript Haplotypes
print(ensRest.getTranscriptHaplotypes(species="homo_sapiens", id="ENST00000288602"))
time.sleep(15)

# VEP
print(
    ensRest.getVariantConsequencesByHGVSNotation(
        species="homo_sapiens", hgvs_notation="ENST00000366667:c.803C>T"
    )
)
print(
    ensRest.getVariantConsequencesByMultipleHGVSNotations(
        species="homo_sapiens",
        hgvs_notations=["ENST00000366667:c.803C>T", "9:g.22125504G>C"],
    )
)
print(ensRest.getVariantConsequencesById(species="homo_sapiens", id="rs56116432"))
print(
    ensRest.getVariantConsequencesByMultipleIds(
        species="homo_sapiens", ids=["rs56116432", "COSM476", "__VAR(sv_id)__"]
    )
)
print(
    ensRest.getVariantConsequencesByRegion(
        species="homo_sapiens", region="9:22125503-22125502:1", allele="C"
    )
)
print(
    ensRest.getVariantConsequencesByMultipleRegions(
        species="homo_sapiens",
        variants=[
            "21 26960070 rs116645811 G A . . .",
            "21 26965148 rs1135638 G A . . .",
        ],
    )
)
time.sleep(15)

# Variation
print(ensRest.getVariationRecoderById(species="homo_sapiens", id="rs56116432"))
print(
    ensRest.getVariationRecoderByMultipleIds(
        species="homo_sapiens", ids=["rs56116432", "rs1042779"]
    )
)
print(ensRest.getVariationById(species="homo_sapiens", id="rs56116432"))
print(ensRest.getVariationByPMCID(species="homo_sapiens", pmcid="PMC5002951"))
print(ensRest.getVariationByPMID(species="homo_sapiens", pmid="26318936"))
print(
    ensRest.getVariationByMultipleIds(
        species="homo_sapiens", ids=["rs56116432", "COSM476", "__VAR(sv_id)__"]
    )
)
time.sleep(15)

# Variation GA4GH
print(ensRest.getGA4GHBeacon())
print(
    ensRest.getGA4GHBeaconQuery(
        alternateBases="C",
        assemblyId="GRCh38",
        end="23125503",
        referenceBases="G",
        referenceName="9",
        start="22125503",
        variantType="DUP",
    )
)
print(
    ensRest.postGA4GHBeaconQuery(
        alternateBases="C",
        assemblyId="GRCh38",
        end="23125503",
        referenceBases="G",
        referenceName="9",
        start="22125503",
        variantType="DUP",
    )
)
print(ensRest.getGA4GHFeaturesById(id="ENST00000408937.7"))
ensRest.timeout = 180
print(
    ensRest.searchGA4GHFeatures(
        parentId="ENST00000408937.7",
        featureSetId="",
        featureTypes=["cds"],
        end=220023,
        referenceName="X",
        start=197859,
        pageSize=1,
    )
)  # this keeps timing out
ensRest.timeout = 60
print(ensRest.searchGA4GHCallset(variantSetId=1, pageSize=2))
print(ensRest.getGA4GHCallsetById(id="1"))
print(ensRest.searchGA4GHDatasets(pageSize=3))
print(ensRest.getGA4GHDatasetsById(id="6e340c4d1e333c7a676b1710d2e3953c"))
print(ensRest.searchGA4GHFeaturesets(datasetId="Ensembl"))
print(ensRest.getGA4GHFeaturesetsById(id="Ensembl"))
print(ensRest.getGA4GHVariantsById(id="1:rs1333049"))
print(
    ensRest.searchGA4GHVariantAnnotations(
        variantAnnotationSetId="Ensembl",
        referenceId="9489ae7581e14efcad134f02afafe26c",
        start=25221400,
        end=25221500,
        pageSize=1,
    )
)
print(
    ensRest.searchGA4GHVariants(
        variantSetId=1,
        referenceName=22,
        start=25455086,
        end=25455087,
        pageToken="",
        pageSize=1,
    )
)
print(
    ensRest.searchGA4GHVariantsets(
        datasetId="6e340c4d1e333c7a676b1710d2e3953c", pageToken="", pageSize=2
    )
)
print(ensRest.getGA4GHVariantsetsById(id=1))
print(ensRest.searchGA4GHReferences(referenceSetId="GRCh38", pageSize=10))
print(ensRest.getGA4GHReferencesById(id="9489ae7581e14efcad134f02afafe26c"))
print(ensRest.searchGA4GHReferencesets())
print(ensRest.getGA4GHReferencesetsById(id="GRCh38"))
print(ensRest.searchGA4GHVariantAnnotationsets(variantSetId="Ensembl"))
print(ensRest.getGA4GHVariantAnnotationsetsById(id="Ensembl"))
time.sleep(15)
