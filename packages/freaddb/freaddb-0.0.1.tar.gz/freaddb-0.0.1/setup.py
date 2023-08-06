# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['freaddb']

package_data = \
{'': ['*']}

install_requires = \
['lmdb>=1.3.0,<2.0.0',
 'lz4>=4.0.1,<5.0.0',
 'msgpack>=1.0.4,<2.0.0',
 'numpy>=1.22.4,<2.0.0',
 'pyroaring>=0.3.3,<0.4.0',
 'tqdm>=4.64.0,<5.0.0',
 'ujson>=5.3.0,<6.0.0']

setup_kwargs = {
    'name': 'freaddb',
    'version': '0.0.1',
    'description': 'Fast Read DB',
    'long_description': '# FReadDB\n\nFast Read Database is implemented with LMDB (key-value database) as the underlying storage. We use this DB as a data storage, and RAM of [MTab system](https://mtab.kgraph.jp). \n\n## Installation\n\n```bash\npip install freaddb\n```\n\n## Usage\n\n```python\nfrom freaddb import config\nfrom freaddb.db_lmdb import DBSpec, FReadDB\n\n# Data file directory\ndata_file = "/tmp/freaddb/db_test_basic"\n\n# Define sub database schema\n# keys are strings, values are python objs and compress values \ndb_schema_0 = DBSpec(name="data0", integerkey=False, bytes_value=config.ToBytesType.OBJ, compress_value=True)\n\n# key are integers, values are python objects serialized with msgpack and no compress values\ndb_schema_1 = DBSpec(name="data1", integerkey=True, bytes_value=config.ToBytesType.OBJ)\n\n# key are strings, values are python objects serialized with pickle\ndb_schema_2 = DBSpec(name="data2", integerkey=False, bytes_value=config.ToBytesType.PICKLE)\n\n# key are strings, values are bytes\ndb_schema_3 = DBSpec(name="data3", integerkey=False, bytes_value=config.ToBytesType.BYTES)\n\n# key are integers, values are list integers serialized with numpy\ndb_schema_4 = DBSpec(name="data4", integerkey=False, bytes_value=config.ToBytesType.INT_NUMPY)\n\n# key are integers, values are list integers serialized with BITMAP\ndb_schema_5 = DBSpec(name="data5", integerkey=False, bytes_value=config.ToBytesType.INT_BITMAP)\n\n# Add 6 sub databases\ndata_schema = [db_schema_0, db_schema_1, db_schema_2, db_schema_3, db_schema_4, db_schema_5]\n\n\n# Example data\ndata = {\n        "data0": {"One": {1: "One"}, "Two": {2: "Two"}},\n        "data1": {1: "One", 2: "Two"},\n        "data2": {"One": 1, "Two": 2},\n        "data3": {"One": b"1", "Two": b"2"},\n        "data4": {i: list(range(i * 10)) for i in range(10, 20)},\n        "data5": {i: list(range(i * 10)) for i in range(10, 20)},\n    }\nto_list_data = {"data4", "data5"}\n\n# Create data with data_file, data_schema, and buffer is 1GB \ndb = FReadDB(db_file=data_file, db_schema=data_schema, buff_limit=config.SIZE_1GB)\n\n# Add data to FReadDB\nfor data_name, data_items in data.items():\n    for key, value in data_items.items():\n        db.add(data_name, key, value)\n        \n# Make sure save all buffer to disk\ndb.save_buff()\n\n# Access data\nsample = db.get_value("data1", 1)\nassert sample == "One"\n\nfor data_name, data_samples in data.items():\n    sample = db.get_values(data_name, list(data_samples.keys()))\n    if data_name in to_list_data:\n        sample = {k: list(v) for k, v in sample.items()}\n    assert sample == data_samples\n\n```\n',
    'author': 'Phuc Nguyen',
    'author_email': 'phucnt.ty@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/phucty/freaddb',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
