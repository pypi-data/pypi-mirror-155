# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['csvy']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0']

setup_kwargs = {
    'name': 'pycsvy',
    'version': '0.2.0',
    'description': 'Python reader/writer for CSV files with YAML header information.',
    'long_description': '# CSVY for Python\n\n[![Test and build](https://github.com/ImperialCollegeLondon/csvy/actions/workflows/ci.yml/badge.svg)](https://github.com/ImperialCollegeLondon/csvy/actions/workflows/ci.yml)\n[![PyPI version shields.io](https://img.shields.io/pypi/v/pycsvy.svg)](https://pypi.python.org/pypi/pycsvy/)\n[![PyPI status](https://img.shields.io/pypi/status/pycsvy.svg)](https://pypi.python.org/pypi/pycsvy/)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pycsvy.svg)](https://pypi.python.org/pypi/pycsvy/)\n[![PyPI license](https://img.shields.io/pypi/l/pycsvy.svg)](https://pypi.python.org/pypi/pycsvy/)\n[![codecov](https://codecov.io/gh/ImperialCollegeLondon/pycsvy/branch/develop/graph/badge.svg?token=N03KYNUD18)](https://codecov.io/gh/ImperialCollegeLondon/pycsvy)\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/8d1b791b315f4814a128d94483499561)](https://www.codacy.com/gh/ImperialCollegeLondon/pycsvy/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ImperialCollegeLondon/pycsvy&amp;utm_campaign=Badge_Grade)\n\nCSV is a popular format for storing tabular data used in many disciplines. Metadata\nconcerning the contents of the file is often included in the header, but it rarely\nfollows a format that is machine readable - sometimes is not even human readable! In\nsome cases, such information is provided in a separate file, which is not ideal as it is\neasy for data and metadata to get separated.\n\nCSVY is a small Python package to handle CSV files in which the metadata in the header\nis formatted in YAML. It supports reading/writing tabular data contained in numpy\narrays, pandas DataFrames and nested lists, as well as metadata using a standard python\ndictionary. Ultimately, it aims to incorporate information about the [CSV\ndialect](https://specs.frictionlessdata.io/csv-dialect/) used and a [Table\nSchema](https://specs.frictionlessdata.io/table-schema/) specifying the contents of each\ncolumn to aid the reading and interpretation of the data.\n\n## Instalation\n\n\'pycsvy\' is available in PyPI therefore its installation is as easy as:\n\n```bash\npip install pycsvy\n```\n\nIn order to support reading into `numpy` arrays or into `pandas` DataFrames, you will\nneed to install those two packages, too.\n\n## Usage\n\nIn the simplest case, to save some data contained in `data` and some metadata contained\nin a `metadata` dictionary into a CSVY file `important_data.csv` (the extension is not\nrelevant), just do the following:\n\n```python\nimport csvy\n\ncsvy.write("important_data.csv", data, metadata)\n```\n\nThe resulting file will have the YAML-formatted header in between `---` markers with,\noptionally, a comment character starting each header line. It could look something like\nthe following:\n\n```text\n---\nname: my-dataset\ntitle: Example file of csvy\ndescription: Show a csvy sample file.\nencoding: utf-8\nschema:\n  fields:\n  - name: Date\n    type: object\n  - name: WTI\n    type: number\n---\nDate,WTI\n1986-01-02,25.56\n1986-01-03,26.00\n1986-01-06,26.53\n1986-01-07,25.85\n1986-01-08,25.87\n```\n\nFor reading the information back:\n\n```python\nimport csvy\n\n# To read into a numpy array\ndata, metadata = csvy.read_to_array("important_data.csv")\n\n# To read into a pandas DataFrame\ndata, metadata = csvy.read_to_dataframe("important_data.csv")\n```\n\nThe appropriate writer/reader will be selected based on the type of `data`:\n\n- numpy array: `np.savetxt` and `np.loadtxt`\n- pandas DataFrame: `pd.DataFrame.to_csv` and `pd.read_csv`\n- nested lists:\' `csv.writer` and `csv.reader`\n\nOptions can be passed to the tabular data writer/reader by setting the `csv_options`\ndictionary. Likewise you can set the `yaml_options` dictionary with whatever options you\nwant to pass to `yaml.safe_load` and `yaml.safe_dump` functions, reading/writing the\nYAML-formatted header, respectively.\n\nFinally, you can control the character(s) used to indicate comments by setting the\n`comment` keyword when writing a file. By default, there is no character (""). During reading, the comment character is found atomatically.\n',
    'author': 'Diego Alonso Álvarez',
    'author_email': 'd.alonso-alvarez@imperial.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ImperialCollegeLondon/pycsvy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
