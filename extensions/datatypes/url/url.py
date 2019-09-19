import re
from arches.app.models.system_settings import settings
from arches.app.datatypes.base import BaseDataType

from rdflib import ConjunctiveGraph as Graph, Namespace
from rdflib.namespace import RDF, RDFS, XSD, DC, DCTERMS
archesproject = Namespace(settings.ARCHES_NAMESPACE_FOR_DATA_EXPORT)
cidoc_nm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")

details = {
    'datatype': 'url',
    'iconclass': 'fa fa-location-arrow',
    'modulename': 'datatypes.py',
    'classname': 'URLDataType',
    'defaultwidget': 'urldatatype',
    'defaultconfig': None,
    'configcomponent': None,
    'configname': None,
    'isgeometric': False,
    'issearchable': True
}


class URLDataType(BaseDataType):
    """
    URL Datatype to store an optionally labelled hyperlink to a (typically) external resource
    """

    URL_REGEX = re.compile(r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)")

    def validate(self, value, row_number=None, source=None):
        errors = []
        try:
            if value.get('url') is not None:
                # check URL conforms to URL structure
                url_test = self.URL_REGEX.match(value['url'])
                if url_test is None:
                    raise Exception
        except:
            errors.append({
                'type': 'ERROR',
                'message': 'datatype: {0} value: {1} {2} {3} - {4}. {5}'.format(
                    self.datatype_model.datatype,
                    value,
                    source,
                    row_number,
                    'this is not a valid HTTP/HTTPS URL',
                    'This data was not imported.'
                )
            })
        return errors

    def append_to_document(self, document, nodevalue, nodeid, tile, provisional=False):
        if nodevalue.get('url') is not None:
            if nodevalue.get('url_label') is not None:
                val = {'string': nodevalue['url_label'],
                       'nodegroup_id': tile.nodegroup_id,
                       'provisional': provisional}
                document['strings'].append(val)

            # FIXME: URLs searchable?
            # val = {'string': nodevalue['url'], 'nodegroup_id': tile.nodegroup_id, 'provisional': provisional}
            document['strings'].append(val)

    def get_search_terms(self, nodevalue, nodeid=None):
        terms = []
        if nodevalue.get('url') is not None:
            if nodevalue.get('url_label') is not None:
                if settings.WORDS_PER_SEARCH_TERM == None or  \
                    (len(nodevalue['url_label'].split(' ')) < settings.WORDS_PER_SEARCH_TERM):
                    terms.append(nodevalue['url_label'])
            # terms.append(nodevalue['url'])       FIXME: URLs searchable?
        return terms

    def append_search_filters(self, value, node, query, request):
        # Match the label in the same manner as a String datatype
        try:
            if value['val'] != '':
                match_type = 'phrase_prefix' if '~' in value['op'] else 'phrase'
                match_query = Match(field='tiles.data.%s' % (str(node.pk)), query=value['val'], type=match_type)
                if '!' in value['op']:
                    query.must_not(match_query)
                    query.filter(Exists(field="tiles.data.%s" % (str(node.pk))))
                else:
                    query.must(match_query)
        except KeyError, e:
            pass

    def is_a_literal_in_rdf(self):
        return False

    def to_rdf(self, edge_info, edge):
        # returns an in-memory graph object, containing the domain resource, its
        # type and the string as a string literal
        g = Graph()
        if edge_info['range_tile_data'] is not None and \
            edge_info['range_tile_data'].get('url') is not None:
            g.add((edge_info['d_uri'], RDF.type, URIRef(edge.domainnode.ontologyclass)))
            g.add((edge_info['d_uri'], URIRef(edge.ontologyproperty), URIRef(
                edge_info['range_tile_data']['url'])))
            if edge_info['range_tile_data'].get('url_label') is not None:
                g.add((URIRef(edge_info['range_tile_data']['url'])), RDFS.label, Literal(
                    edge_info['range_tile_data']['url_label'])
                )
        return g

    def from_rdf(self, json_ld_node):
        """
        The json-ld representation of this datatype should look like the following (once expanded)

        [
          {
            "http://some/kind/of/property": [
              {
                "@value": "Link to spectro report"
              }
            ],
            "@id": "https://host/url/to/link"
          }
        ]
        """

        value = {}
        try:
            # assume single URL for this datatype
            url_node = json_ld_node[0]
            value['url'] = url_node['@id']
            value['url_label'] = None
            if "http://www.w3.org/2000/01/rdf-schema#label" in url_node:
                value['url_label'] = url_node["http://www.w3.org/2000/01/rdf-schema#label"]["@value"]
        except (IndexError, AttributeError, KeyError) as e:
            return None