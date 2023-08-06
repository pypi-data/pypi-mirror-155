# easysparql
A python wrapper to easily query knowledge graphs with SPARQL

[![Build Status](https://ahmad88me.semaphoreci.com/badges/easysparql.svg)](https://ahmad88me.semaphoreci.com/projects/easysparql)
[![codecov](https://codecov.io/gh/oeg-upm/easysparql/branch/master/graph/badge.svg)](https://codecov.io/gh/oeg-upm/easysparql)

[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)


# Install

## via setuptools
```python setup.py ```

## via pip
```pip install easysparql```

## Run tests
```python -m unittest discover```


# Functions
* `run_query`: run a sparql query.
* `get_entities`: get candidate entities of the given name (exact match).
* `get_classes`: get classes of a given entity.
* `get_parents_of_class`: get direct parent classes of a given class.
* `get_subjects`: Get the number of subjects of a given class.
* `get_properties_of_subject`: Get the properties of a given subject.
* `get_numerics_from_list`: Get the numbers from a list of strings and numbers (if they are more that the provided percentage).
* `get_num`: Get the number of a given number/string or None (if it was not a number).


# Example
```
from easysparql import easysparql

DBPEDIA_ENDPOINT = "https://dbpedia.org/sparql"

albert_uri = "http://dbpedia.org/resource/Albert_Einstein"
albert_name = "Albert Einstein"
scientist = "http://dbpedia.org/ontology/Scientist"
foaf_name = "http://xmlns.com/foaf/0.1/name"


classes = easysparql.get_classes(albert_uri, DBPEDIA_ENDPOINT)

entities = easysparql.get_entities(albert_name, DBPEDIA_ENDPOINT, "@en")

parents = easysparql.get_parents_of_class(scientist, DBPEDIA_ENDPOINT)

query = "select distinct ?Concept where {[] a ?Concept} LIMIT 100"
results = easysparql.run_query(query, DBPEDIA_ENDPOINT)

subjects = easysparql.get_subjects(class_uri=scientist, endpoint=DBPEDIA_ENDPOINT)

properties = easysparql.get_properties_of_subject(subject_uri=albert_uri, endpoint=DBPEDIA_ENDPOINT)

a =  ["1.2","2","4","3",3,6,"a","b", "ccc", "1jasdf"]
nums = easysparql.get_numerics_from_list(a, 0.5)

```

