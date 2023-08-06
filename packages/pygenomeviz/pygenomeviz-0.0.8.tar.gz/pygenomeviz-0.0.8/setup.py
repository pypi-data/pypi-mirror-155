# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pygenomeviz']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.79,<2.0', 'matplotlib>=3.5.2,<4.0.0', 'numpy>=1.21,<2.0']

setup_kwargs = {
    'name': 'pygenomeviz',
    'version': '0.0.8',
    'description': 'A genome visualization python package for comparative genomics',
    'long_description': '# pyGenomeViz\n\n![Python3](https://img.shields.io/badge/Language-Python3-steelblue)\n![OS](https://img.shields.io/badge/OS-_Windows_|_Mac_|_Linux-steelblue)\n![License](https://img.shields.io/badge/License-MIT-steelblue)\n[![Latest PyPI version](https://img.shields.io/pypi/v/pygenomeviz.svg)](https://pypi.python.org/pypi/pygenomeviz)\n[![Bioconda](https://img.shields.io/conda/vn/bioconda/pygenomeviz.svg?color=green)](https://anaconda.org/bioconda/pygenomeviz)  \n\n## Overview\n\npyGenomeViz is a genome visualization python package for comparative genomics implemented in matplotlib.\nThis package is developed for the purpose of easily and beautifully plotting genomic\nfeatures and sequence similarity comparison links between multiple genomes.\nIt supports genome visualization of Genbank format file, and can be used to interactively plot\ngenome visualization figure on jupyter notebook, or for integration into a genome analysis pipeline.\n\nFor more information, please see full documentation [here](https://moshi4.github.io/pyGenomeViz/).\n\n## Installation\n\n`Python 3.7 or later` is required for installation.\n\n**Install PyPI package:**\n\n    pip install pygenomeviz\n\n**Install bioconda package:**\n\n    conda install -c conda-forge -c bioconda pygenomeviz\n\n## Examples\n\nJupyter notebooks containing code examples below is available [here](https://moshi4.github.io/pyGenomeViz/examples/basic_example/).\n\n### Basic Example\n\n#### Single Genome Track Visualization\n\n```python\nfrom pygenomeviz import GenomeViz\n\nname, genome_size = "Tutorial 01", 5000\ncds_list = ((100, 900, -1), (1100, 1300, 1), (1350, 1500, 1), (1520, 1700, 1), (1900, 2200, -1), (2500, 2700, 1), (2700, 2800, -1), (2850, 3000, -1), (3100, 3500, 1), (3600, 3800, -1), (3900, 4200, -1), (4300, 4700, -1), (4800, 4850, 1))\n\ngv = GenomeViz()\ntrack = gv.add_feature_track(name, genome_size)\nfor idx, cds in enumerate(cds_list, 1):\n    start, end, strand = cds\n    track.add_feature(start, end, strand, label=f"CDS{idx:02d}")\n\nfig = gv.plotfig()\n```\n\n![example01.png](https://raw.githubusercontent.com/moshi4/pyGenomeViz/main/docs/images/example01.png)\n\n#### Multiple Genome Track & Link Visualization\n\n```python\nfrom pygenomeviz import GenomeViz\n\ngenome_list = (\n    {"name": "genome 01", "size": 1000, "cds_list": ((150, 300, 1), (500, 700, -1), (750, 950, 1))},\n    {"name": "genome 02", "size": 1300, "cds_list": ((50, 200, 1), (350, 450, 1), (700, 900, -1), (950, 1150, -1))},\n    {"name": "genome 03", "size": 1200, "cds_list": ((150, 300, 1), (350, 450, -1), (500, 700, -1), (701, 900, -1))},\n)\n\ngv = GenomeViz(tick_style="axis")\nfor genome in genome_list:\n    name, size, cds_list = genome["name"], genome["size"], genome["cds_list"]\n    track = gv.add_feature_track(name, size)\n    for idx, cds in enumerate(cds_list, 1):\n        start, end, strand = cds\n        track.add_feature(start, end, strand, label=f"gene{idx:02d}", linewidth=1, labelrotation=0, labelvpos="top", labelhpos="center", labelha="center")\n\n# Add links between "genome 01" and "genome 02"\ngv.add_link(("genome 01", 150, 300), ("genome 02", 50, 200))\ngv.add_link(("genome 01", 700, 500), ("genome 02", 900, 700))\ngv.add_link(("genome 01", 750, 950), ("genome 02", 1150, 950))\n# Add links between "genome 02" and "genome 03"\ngv.add_link(("genome 02", 50, 200), ("genome 03", 150, 300), normal_color="skyblue", inverted_color="lime")\ngv.add_link(("genome 02", 350, 450), ("genome 03", 450, 350), normal_color="skyblue", inverted_color="lime")\ngv.add_link(("genome 02", 900, 700), ("genome 03", 700, 500), normal_color="skyblue", inverted_color="lime")\ngv.add_link(("genome 03", 900, 701), ("genome 02", 1150, 950), normal_color="skyblue", inverted_color="lime")\n\nfig = gv.plotfig()\n```\n\n![example02.png](https://raw.githubusercontent.com/moshi4/pyGenomeViz/main/docs/images/example02.png)\n\n### Practical Example\n\n#### Single Genome Track Visualization from Genbank file\n\n```python\nfrom pygenomeviz import Genbank, GenomeViz, load_dataset\n\n# Load single genbank file\ngbk_files, _ = load_dataset("escherichia_phage")\ngbk = Genbank(gbk_files[0])\n\n# Visualize genbank features\ngv = GenomeViz()\ntrack = gv.add_feature_track(gbk.name, gbk.genome_length)\ntrack.add_genbank_features(gbk)\n\nfig = gv.plotfig()\n```\n\n![example03.png](https://raw.githubusercontent.com/moshi4/pyGenomeViz/main/docs/images/example03.png)\n\n#### Multiple Genome Track & Link Visualization from Genbank files\n\n```python\nfrom pygenomeviz import Genbank, GenomeViz, load_dataset\n\ngv = GenomeViz(\n    feature_track_ratio=0.5,\n    link_track_ratio=1.0,\n    tick_track_ratio=0.5,\n    tick_style="bar",\n    align_type="center",\n)\n\ngbk_files, links = load_dataset("escherichia_phage")\nfor gbk_file in gbk_files:\n    gbk = Genbank(gbk_file)\n    track = gv.add_feature_track(gbk.name, gbk.genome_length)\n    track.add_genbank_features(gbk)\n\nfor link in links:\n    link_data1 = (link.ref_name, link.ref_start, link.ref_end)\n    link_data2 = (link.query_name, link.query_start, link.query_end)\n    gv.add_link(link_data1, link_data2, interpolation_value=link.identity, curve=True)\n\nfig = gv.plotfig()\n```\n\n![example04.png](https://raw.githubusercontent.com/moshi4/pyGenomeViz/main/docs/images/example04.png)\n\n### Customization Tips\n\nSince pyGenomeViz is implemented based on matplotlib, users can easily customize\nthe figure in the manner of matplotlib. Here are some tips for figure customization.\n\n- Add `GC content` & `GC skew` subtrack\n- Add annotation (Fill Box, ROI)\n- Add colorbar (Experimetal implementation)\n',
    'author': 'moshi4',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/moshi4/pyGenomeViz/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
