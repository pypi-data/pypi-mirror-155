# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysmi',
 'pysmi.borrower',
 'pysmi.codegen',
 'pysmi.lexer',
 'pysmi.parser',
 'pysmi.reader',
 'pysmi.scripts',
 'pysmi.searcher',
 'pysmi.writer']

package_data = \
{'': ['*']}

install_requires = \
['ply>=3.11,<4.0', 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['mibcopy = pysmi.scripts.mibcopy:start',
                     'mibdump = pysmi.scripts.mibdump:start']}

setup_kwargs = {
    'name': 'pysnmp-pysmi',
    'version': '1.1.10',
    'description': '',
    'long_description': '\nSNMP MIB parser\n---------------\n\n[![Python Versions](https://img.shields.io/pypi/pyversions/pysnmp-pysmi.svg)](https://pypi.org/project/pysnmp-pysmi/)\n[![Build status](https://travis-ci.org/etingof/pysmi.svg?branch=master)](https://secure.travis-ci.org/etingof/pysmi)\n[![Coverage Status](https://img.shields.io/codecov/c/github/pysnmp/pysmi.svg)](https://codecov.io/github/pysnmp/pysmi)\n[![GitHub license](https://img.shields.io/badge/license-BSD-blue.svg)](https://raw.githubusercontent.com/pysnmp/pysmi/main/LICENSE.rst)\n\nPySMI is a pure-Python implementation of\n[SNMP SMI](https://en.wikipedia.org/wiki/Management_information_base) MIB parser.\nThis tool is designed to turn ASN.1 MIBs into various formats. As of this moment,\nJSON and [pysnmp](https://github.com/etingof/pysnmp) modules can be generated\nfrom ASN.1 MIBs.\n\nFeatures\n--------\n\n* Understands SMIv1, SMIv2 and de-facto SMI dialects\n* Turns MIBs into pysnmp classes and JSON documents\n* Maintains an index of MIB objects over many MIB modules\n* Automatically pulls ASN.1 MIBs from local directories, ZIP archives,\n  HTTP and FTP servers\n* 100% Python, works with Python 2.4 up to Python 3.7\n\nRendered PySMI documentation can be found at [pysmi site](http://snmplabs.com/pysmi).\n\nHow to use PySMI\n----------------\n\nIf you are using pysnmp, you might never notice pysmi presence - pysnmp\ncalls pysmi for MIB download and compilation behind the scenes (you can\nstill can do that manually by invoking *mibdump.py* tool).\n\nTo turn ASN.1 MIB into a JSON document, call *mibdump.py* tool like this:\n\n```\n$ mibdump.py --generate-mib-texts  --destination-format json IF-MIB\nSource MIB repositories: file:///usr/share/snmp/mibs, https://pysnmp.github.io/mibs/asn1/@mib@\nBorrow missing/failed MIBs from: http://pysnmp.github.io/json/fulltexts/@mib@\nExisting/compiled MIB locations: \nCompiled MIBs destination directory: .\nMIBs excluded from code generation: RFC-1212, RFC-1215, RFC1065-SMI, RFC1155-SMI,\nRFC1158-MIB, RFC1213-MIB, SNMPv2-CONF, SNMPv2-SMI, SNMPv2-TC, SNMPv2-TM\nMIBs to compile: IF-MIB\nDestination format: json\nParser grammar cache directory: not used\nAlso compile all relevant MIBs: yes\nRebuild MIBs regardless of age: yes\nDo not create/update MIBs: no\nByte-compile Python modules: no (optimization level no)\nIgnore compilation errors: no\nGenerate OID->MIB index: no\nGenerate texts in MIBs: yes\nKeep original texts layout: no\nTry various filenames while searching for MIB module: yes\nCreated/updated MIBs: IANAifType-MIB, IF-MIB, SNMPv2-MIB\nPre-compiled MIBs borrowed: \nUp to date MIBs: SNMPv2-CONF, SNMPv2-SMI, SNMPv2-TC\nMissing source MIBs: \nIgnored MIBs: \nFailed MIBs: \n```\n\nJSON document build from\n[IF-MIB module](https://pysnmp.github.io/mibs/asn1IF-MIB)\nwould hold information such as:\n\n```\n   {\n      "ifMIB": {\n          "name": "ifMIB",\n          "oid": "1.3.6.1.2.1.31",\n          "class": "moduleidentity",\n          "revisions": [\n            "2007-02-15 00:00",\n            "1996-02-28 21:55",\n            "1993-11-08 21:55"\n          ]\n        },\n      ...\n      "ifTestTable": {\n        "name": "ifTestTable",\n        "oid": "1.3.6.1.2.1.31.1.3",\n        "nodetype": "table",\n        "class": "objecttype",\n        "maxaccess": "not-accessible"\n      },\n      "ifTestEntry": {\n        "name": "ifTestEntry",\n        "oid": "1.3.6.1.2.1.31.1.3.1",\n        "nodetype": "row",\n        "class": "objecttype",\n        "maxaccess": "not-accessible",\n        "augmention": {\n          "name": "ifTestEntry",\n          "module": "IF-MIB",\n          "object": "ifEntry"\n        }\n      },\n      "ifTestId": {\n        "name": "ifTestId",\n        "oid": "1.3.6.1.2.1.31.1.3.1.1",\n        "nodetype": "column",\n        "class": "objecttype",\n        "syntax": {\n          "type": "TestAndIncr",\n          "class": "type"\n        },\n        "maxaccess": "read-write"\n      },\n      ...\n   }\n```\n\nIn general, converted MIBs capture all aspects of original (ASN.1) MIB contents\nand layout. The snippet above is just a partial example, but here is the\ncomplete [IF-MIB.json](http://pysnmp.github.io/json/fulltexts/IF-MIB.json)\nfile.\n\nBesides one-to-one MIB conversion, PySMI library can produce JSON index to\nfacilitate fast MIB information lookup across large collection of MIB files.\nFor example, JSON index for\n[IP-MIB.json](http://pysnmp.github.io/json/asn1/IP-MIB),\n[TCP-MIB.json](http://pysnmp.github.io/json/asn1/TCP-MIB) and\n[UDP-MIB.json](http://pysnmp.github.io/json/asn1/UDP-MIB)\nmodules would keep information like this:\n\n```\n   {\n      "compliance": {\n         "1.3.6.1.2.1.48.2.1.1": [\n           "IP-MIB"\n         ],\n         "1.3.6.1.2.1.49.2.1.1": [\n           "TCP-MIB"\n         ],\n         "1.3.6.1.2.1.50.2.1.1": [\n           "UDP-MIB"\n         ]\n      },\n      "identity": {\n          "1.3.6.1.2.1.48": [\n            "IP-MIB"\n          ],\n          "1.3.6.1.2.1.49": [\n            "TCP-MIB"\n          ],\n          "1.3.6.1.2.1.50": [\n            "UDP-MIB"\n          ]\n      },\n      "oids": {\n          "1.3.6.1.2.1.4": [\n            "IP-MIB"\n          ],\n          "1.3.6.1.2.1.5": [\n            "IP-MIB"\n          ],\n          "1.3.6.1.2.1.6": [\n            "TCP-MIB"\n          ],\n          "1.3.6.1.2.1.7": [\n            "UDP-MIB"\n          ],\n          "1.3.6.1.2.1.49": [\n            "TCP-MIB"\n          ],\n          "1.3.6.1.2.1.50": [\n            "UDP-MIB"\n          ]\n      }\n   }\n```\n\nWith this example, *compliance* and *identity* keys point to\n*MODULE-COMPLIANCE* and *MODULE-IDENTITY* MIB objects, *oids*\nlist top-level OIDs branches defined in MIB modules. Full index\nbuild over thousands of MIBs could be seen\n[here](http://pysnmp.github.io/json/index.json).\n\nThe PySMI library can automatically fetch required MIBs from HTTP, FTP sites\nor local directories. You could configure any MIB source available to you (including\n[https://pysnmp.github.io/mibs/asn1](https://pysnmp.github.io/mibs/asn1)) for that purpose.\n\nHow to get PySMI\n----------------\n\nThe pysmi package is distributed under terms and conditions of 2-clause\nBSD [license](http://snmplabs.com/pysmi/license.html). Source code is freely\navailable as a GitHub [repo](https://github.com/pysnmp/pysmi).\n\nYou could `pip install pysnmp-pysmi` or download it from [PyPI](https://pypi.org/project/pysnmp-pysmi/).\n\nIf something does not work as expected,\n[open an issue](https://github.com/pysnmp/pysmi/issues) at GitHub or\npost your question [on Stack Overflow](http://stackoverflow.com/questions/ask).\n\nCopyright (c) 2015-2020, [Ilya Etingof](mailto:etingof@gmail.com).\nAll rights reserved.\n',
    'author': 'rfaircloth-splunk',
    'author_email': 'rfaircloth@splunk.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pysnmp/pysmi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
