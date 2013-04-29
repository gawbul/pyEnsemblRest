pyEnsemblRest
=============

```pyEnsemblRest``` is a simple Python wrapper around the EnsEMBL REST API

Installation
------------

    git clone git://github.com/gawbul/pyensemblrest.git
    cd pyensemblrest
    sudo python setup.py install

Usage
-----

To import an setup a new EnsemblRest object you should do the following:
	
	from ensemblrest import EnsemblRest
	ensemblrest = EnsemblRest()

To access the *Comparative Genomics* endpoints you can use the following methods:

	print ensemblrest.getGeneTreeById(id='ENSGT00390000003602')
	print ensemblrest.getGeneTreeByMemberId(id='ENSG00000157764')
	print ensemblrest.getGeneTreeByMemberSymbol(species='human', symbol='BRCA2')
	print ensemblrest.getHomologyById(id='ENSG00000157764')
	print ensemblrest.getHomologyById(species='human', symbol='BRCA2')

To access the *Cross References* endpoints you can use the following methods:

	print ensemblrest.getXrefsById(id='ENSG00000157764')

To access the *Information* endpoints you can use the following methods:

	print ensemblrest.getAssemblyInfo(species='human')
	print ensemblrest.getAssemblyInfoRegion(species='human', region_name='X')

	print ensemblrest.getInfoComparas()
	print ensemblrest.getInfoData()
	print ensemblrest.getInfoPing()
	print ensemblrest.getInfoRest()
	print ensemblrest.getInfoSoftware()
	print ensemblrest.getInfoSpecies()
