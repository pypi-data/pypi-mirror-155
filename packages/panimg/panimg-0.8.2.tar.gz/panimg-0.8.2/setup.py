# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['panimg',
 'panimg.contrib',
 'panimg.contrib.oct_converter',
 'panimg.contrib.oct_converter.image_types',
 'panimg.contrib.oct_converter.readers',
 'panimg.image_builders',
 'panimg.post_processors']

package_data = \
{'': ['*']}

install_requires = \
['Pillow',
 'SimpleITK>=2.0,!=2.1.1.1',
 'click',
 'construct',
 'openslide-python',
 'pydantic',
 'pydicom>=2.2',
 'pylibjpeg',
 'pylibjpeg-libjpeg',
 'pylibjpeg-openjpeg',
 'pylibjpeg-rle',
 'pyvips',
 'tifffile']

extras_require = \
{':python_version < "3.8"': ['numpy>=1.21,<2.0'],
 ':python_version >= "3.7" and python_version < "3.8"': ['setuptools'],
 ':python_version >= "3.8" and python_version < "4.0"': ['numpy>=1.22,<2.0']}

entry_points = \
{'console_scripts': ['panimg = panimg.cli:cli']}

setup_kwargs = {
    'name': 'panimg',
    'version': '0.8.2',
    'description': 'Conversion of medical images to MHA and TIFF.',
    'long_description': '# panimg\n\n[![CI](https://github.com/DIAGNijmegen/rse-panimg/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/DIAGNijmegen/rse-panimg/actions/workflows/ci.yml?query=branch%3Amain)\n[![PyPI](https://img.shields.io/pypi/v/panimg)](https://pypi.org/project/panimg/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/panimg)](https://pypi.org/project/panimg/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![DOI](https://zenodo.org/badge/344730308.svg)](https://zenodo.org/badge/latestdoi/344730308)\n\n**NOT FOR CLINICAL USE**\n\nConversion of medical images to MHA and TIFF.\nRequires Python 3.7, 3.8, 3.9 or 3.10.\n`libvips-dev` and `libopenslide-dev` must be installed on your system.\n\nUnder the hood we use:\n\n* `SimpleITK`\n* `pydicom`\n* `pylibjpeg`\n* `Pillow`\n* `openslide-python`\n* `pyvips`\n* `oct-converter`\n\n## Usage\n\n`panimg` takes a folder and tries to convert the containing files to MHA or TIFF.\nBy default, it will try to convert files from subdirectories as well.\nTo only convert files in the top level directory, set `recurse_subdirectories` to `False`.\nIt will try several strategies for loading the contained files, and if an image is found it will output it to the output folder.\nIt will return a structure containing information about what images were produced, what images were used to form the new images, image metadata, and any errors from any of the strategies.\n\n\n**NOTE: Alpha software, do not run this on folders you do not have a backup of.**\n\n```python\nfrom pathlib import Path\nfrom panimg import convert\n\nresult = convert(\n    input_directory=Path("/path/to/files/"),\n    output_directory=Path("/where/files/will/go/"),\n)\n```\n\n### Command Line Interface\n\n`panimg` is also accessible from the command line.\nInstall the package from pip as before, then you can use:\n\n**NOTE: Alpha software, do not run this on folders you do not have a backup of.**\n\n```shell\npanimg convert /path/to/files/ /where/files/will/go/\n```\n\nTo access the help test you can use `panimg -h`.\n\n### Supported Formats\n\n| Input                               | Output  | Strategy   | Notes                      |\n| ----------------------------------- | --------| ---------- | -------------------------- |\n| `.mha`                              | `.mha`  | `metaio`   |                            |\n| `.mhd` with `.raw` or `.zraw`       | `.mha`  | `metaio`   |                            |\n| `.dcm`                              | `.mha`  | `dicom`    |                            |\n| `.nii`                              | `.mha`  | `nifti`    |                            |\n| `.nii.gz`                           | `.mha`  | `nifti`    |                            |\n| `.nrrd`                             | `.mha`  | `nrrd`     | <sup>[1](#footnote1)</sup> |\n| `.e2e`                              | `.mha`  | `oct`      | <sup>[2](#footnote2)</sup> |\n| `.fds`                              | `.mha`  | `oct`      | <sup>[2](#footnote2)</sup> |\n| `.fda`                              | `.mha`  | `oct`      | <sup>[2](#footnote2)</sup> |\n| `.png`                              | `.mha`  | `fallback` | <sup>[3](#footnote3)</sup> |\n| `.jpeg`                             | `.mha`  | `fallback` | <sup>[3](#footnote3)</sup> |\n| `.tiff`                             | `.tiff` | `tiff`     |                            |\n| `.svs` (Aperio)                     | `.tiff` | `tiff`     |                            |\n| `.vms`, `.vmu`, `.ndpi` (Hamamatsu) | `.tiff` | `tiff`     |                            |\n| `.scn` (Leica)                      | `.tiff` | `tiff`     |                            |\n| `.mrxs` (MIRAX)                     | `.tiff` | `tiff`     |                            |\n| `.biff` (Ventana)                   | `.tiff` | `tiff`     |                            |\n\n<a name="footnote1">1</a>: Detached headers are not supported.\n\n<a name="footnote2">2</a>: Only OCT volume(s), no fundus image(s) will be extracted.\n\n<a name="footnote3">3</a>: 2D only, unitary dimensions\n\n#### Post Processors\n\nYou can also define a set of post processors that will operate on each output file.\nPost processors will not produce any new image entities, but rather add additional representations of an image, such as DZI or thumbnails.\nWe provide a `dzi_to_tiff` post processor that is enabled by default, which will produce a DZI file if it is able to.\nTo customise the post processors that run you can do this with\n\n```python\nresult = convert(..., post_processors=[...])\n```\n\nYou are able to run the post processors directly with\n\n```python\nfrom panimg import post_process\nfrom panimg.models import PanImgFile\n\nresult = post_process(image_files={PanImgFile(...), ...}, post_processors=[...])\n```\n\n#### Using Strategies Directly\n\nIf you want to run a particular strategy directly which returns a generator of images for a set of files you can do this with\n\n```python\nfiles = {f for f in Path("/foo/").glob("*.dcm") if f.is_file()}\n\ntry:\n    for result in image_builder_dicom(files=files):\n        sitk_image = result.image\n        process(sitk_image)  # etc. you can also look at result.name for the name of the file,\n                             # and result.consumed_files to see what files were used for this image\nexcept UnconsumedFilesException as e:\n    # e.errors is keyed with a Path to a file that could not be consumed,\n    # with a list of all the errors found with loading it,\n    # the user can then choose what to do with that information\n    ...\n```\n',
    'author': 'James Meakin',
    'author_email': 'panimg@jmsmkn.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DIAGNijmegen/rse-panimg',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
