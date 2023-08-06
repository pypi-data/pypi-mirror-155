import unittest
from easysparql import easysparql, cacher, easysparqlclass
import hashlib
import os


ENDPOINT = "https://dbpedia.org/sparql"
albert_uri = "http://dbpedia.org/resource/Albert_Einstein"
albert_name = "Albert Einstein"
scientist = "http://dbpedia.org/ontology/Scientist"
foaf_name = "http://xmlns.com/foaf/0.1/name"
isaac_name = "Isaac Newton"
isaac_uri = "http://dbpedia.org/resource/Isaac_Newton"
cacher = cacher.Cacher(".cache")


class TestCache(unittest.TestCase):

    def test_cache(self):
        query = """
            select distinct ?s where{
                ?s ?p "%s"%s
            }
        """ % (isaac_name, "@en")

        fname = hashlib.blake2b(str.encode(query)).hexdigest()+".txt"
        cache_f_path = os.path.join(".cache", fname)
        if os.path.exists(cache_f_path):
            os.remove(cache_f_path)

        results = easysparql.run_query(query=query, endpoint=ENDPOINT)
        data = [r['s']['value'] for r in results]
        self.assertIn(isaac_uri, data)
        self.assertFalse(os.path.exists(cache_f_path))
        self.assertIsNone(cacher.get_cache_if_any(query))
        cacher.write_to_cache(query, [[isaac_uri]], keys=['s'])
        data = cacher.get_cache_if_any(query)
        self.assertIsNotNone(data)
        self.assertEqual(isaac_uri, data[0][0])

    def test_empty_cache(self):
        query = """
                    select distinct ?s where{
                        ?s ?p "%s"%s
                    }
                """ % (albert_name+"NOT FOUND NAME", "@en")

        fname = hashlib.blake2b(str.encode(query)).hexdigest() + ".txt"
        cache_f_path = os.path.join(".cache", fname)
        if os.path.exists(cache_f_path):
            os.remove(cache_f_path)

        results = easysparql.run_query(query=query, endpoint=ENDPOINT)
        # data = [r['s']['value'] for r in results]
        self.assertEqual(results, [])
        # self.assertIsNone(results)
        self.assertFalse(os.path.exists(cache_f_path))
        self.assertIsNone(cacher.get_cache_if_any(query))
        cacher.write_results_to_cache(query, [])
        data = cacher.get_cache_if_any(query)
        self.assertIsNotNone(data)

    def test_empty_cache_usage(self):
        query = """
                    select distinct ?s where{
                        ?s ?p "%s"%s
                    }
                """ % (albert_name+"NOT FOUND and and", "@en")
        e = easysparqlclass.EasySparql(endpoint=ENDPOINT, lang_tag="@en", cache_dir=".cache")
        fname = hashlib.blake2b(str.encode(query)).hexdigest() + ".txt"
        cache_f_path = os.path.join(".cache", fname)
        if os.path.exists(cache_f_path):
            os.remove(cache_f_path)
        rows = [['s'], ['not found 1'], ['not found 2']]
        e.cacher.write_to_cache(query, rows, keys=[])
        self.assertTrue(os.path.exists(cache_f_path))
        result = e.run_query(query)
        data = [r['s']['value'] for r in result]
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0], rows[1][0])
        self.assertEqual(data[1], rows[2][0])


if __name__ == '__main__':
    unittest.main()
