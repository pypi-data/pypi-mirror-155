from SPARQLWrapper import SPARQLWrapper, JSON
import logging

try:
    basestring
except:
    basestring = str


def get_logger(name, level=logging.INFO):
    # logging.basicConfig(level=logging.DEBUG)
    # logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=level)
    logger = logging.getLogger(name)
    return logger


logger = get_logger(__name__, level=logging.INFO)


def run_query(query, endpoint):
    """
    :param query: raw SPARQL query
    :param endpoint: endpoint source that hosts the data
    :return: query result as a dict
    """
    sparql = SPARQLWrapper(endpoint=endpoint)
    sparql.setQuery(query=query)
    # sparql.setMethod("POST")
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
        if len(results["results"]["bindings"]) > 0:
            return results["results"]["bindings"]
        else:
            logger.debug("returns 0 rows")
            logger.debug("query: <%s>" % str(query).strip())
            return []
    except Exception as e:
        logger.warning(str(e))
        logger.warning("sparql error: $$<%s>$$" % str(e))
        logger.warning("query: $$<%s>$$" % str(query))
        return None


def get_class_properties(endpoint=None, class_uri=None, min_num=30):
    """
    :param endpoint:
    :param class_uri:
    :return:
    """

    if class_uri is None:
        print("get_class_properties> class_uri should not be None")
        raise Exception("class_uri is missing")
    class_uri_stripped = get_url_stripped(class_uri)
    query = """
                SELECT ?p (count(distinct ?s) as ?num)
                WHERE {
                    ?s a <%s>.
                    ?s ?p[]
                }
                group by ?p
                order by desc(?num)
            """ % class_uri_stripped
    results = run_query(query=query, endpoint=endpoint)
    properties = []
    if results:
        # print(results)
        # for r in results:
        #     print(r)
        #     print(r['p']['value'])
        #     print(r['num']['value'])
        properties = [r['p']['value'] for r in results if int(r['num']['value']) >= min_num]
    return properties


def get_entities(subject_name, endpoint, language_tag=None):
    """
    assuming only in the form of name@en. To be extended to other languages and other types e.g. name^^someurltype
    :param subject_name:
    :param endpoint
    :return:
    """
    if language_tag is None:
        query = """
            select distinct ?s where{
                ?s ?p "%s"@en
            }
        """ % (subject_name)
    else:
        query = """
            select distinct ?s where{
                ?s ?p "%s"%s
            }
        """ % (subject_name, language_tag)

    results = run_query(query=query, endpoint=endpoint)
    entities = []
    if results:
        entities = [r['s']['value'] for r in results]
    return entities


def get_classes(entity_uri, endpoint):
    """
    :param entity: entity url without <>
    :param endpoint:
    :return:
    """
    query = """
        select distinct ?c where{
        <%s> a ?c
        }
    """ % entity_uri
    results = run_query(query=query, endpoint=endpoint)
    classes = []
    if results:
        classes = [r['c']['value'] for r in results]
    return classes


def get_parents_of_class(class_uri, endpoint):
    """
    get the parent class of the given class, get the first results in case of multiple ones
    :param class_uri:
    :param endpoint:
    :return:
    """
    query = """
    select distinct ?c where{
    <%s> rdfs:subClassOf ?c.
    }
    """ % class_uri
    results = run_query(query=query, endpoint=endpoint)
    classes = []
    if results:
        classes = [r['c']['value'] for r in results]
    return classes


def get_subjects(class_uri, endpoint):
    """
    Get subjects of a given class
    :param class_uri:
    :param endpoint:
    :return:
    """
    query = """ select ?s
    where{
        ?s a <%s>        
    }
    """ % (class_uri)
    results = run_query(query, endpoint)
    subjects = []
    if results:
        subjects = [r['s']['value'] for r in results]
    return subjects


def get_properties_of_subject(subject_uri, endpoint):
    """
    Get properties of a given subject
    :param subject_uri:
    :param endpoint:
    :return:
    """
    query = """
        select distinct ?p
        where{
            <%s> ?p ?o.
        }
    """ % (subject_uri)

    results = run_query(query, endpoint)
    properties = []
    if results:
        properties = [r['p']['value'] for r in results]
    return properties


# The below two functions are copied from oeg-upm/ttla
# and are slighly updated
def get_numerics_from_list(nums_str_list, num_perc):
    """
    :param nums_str_list: list of string or numbers or a mix
    :param num_perc: the percentage of numbers to non-numbers
    :return: list of numbers or None if less than {num_perc}% are numbers
    """
    nums = []
    for c in nums_str_list:
        n = get_num(c)
        if n is not None:
            nums.append(n)
    if len(nums) < len(nums_str_list) / 2:
        return None
    return nums


def get_num(num_or_str):
    """
    :param num_or_str:
    :return: number or None if it is not a number
    """
    if isinstance(num_or_str, (int, float)):
        return num_or_str
    elif isinstance(num_or_str, basestring):
        if '.' in num_or_str or ',' in num_or_str or num_or_str.isdigit():
            try:
                return float(num_or_str.replace(',', ''))
            except Exception as e:
                return None
    return None


def get_entities_and_classes(subject_name, attributes, endpoint):
    """
    :param subject_name:
    :param attributes:
    :param endpoint: the SPARQL endpoint
    :return:
    """
    inner_qs = []
    csubject = clean_text(subject_name)
    for attr in attributes:
        cattr = clean_text(attr)
        q = """
            {
                ?s rdfs:label "%s"@en.
                ?s ?p "%s"@en.
                ?s a ?c.
            } UNION {
                ?s rdfs:label "%s"@en.
                ?s ?p ?e.
                ?e rdfs:label "%s"@en.
                ?s a ?c.
            }
        """ % (csubject, cattr, csubject, cattr)
        inner_qs.append(q)

    inner_q = "UNION".join(inner_qs)

    query = """
        select distinct ?s ?c where{
            %s
        }
    """ % (inner_q)
    results = run_query(query=query, endpoint=endpoint)
    try:
        entity_class_pair = [(r['s']['value'], r['c']['value']) for r in results]
    except:
        entity_class_pair = []
    return entity_class_pair


def clean_text( text):
    ctext = text.replace('"', '')
    ctext = ctext.replace("'", "")
    ctext = ctext.strip()
    return ctext


def get_url_stripped(uri):
    """
    :param uri:  <uri> or uri
    :return: uri
    """
    uri_stripped = uri.strip()
    if uri_stripped[0] == "<":
        uri_stripped = uri_stripped[1:]
    if uri_stripped[-1] == ">":
        uri_stripped = uri_stripped[:-1]
    return uri_stripped