
import json
from get_prefix import search_prefix


def create_first_json(g):
    """
    Create json file with prefixes of the graph file

    Parameters:
    -----------
        g (Graph): graph
    """
    new_prefixes = {}
    for ns_prefix, namespace in g.namespaces():
        key = ns_prefix
        if ns_prefix == '':
            i = namespace.rfind('/', 0, len(namespace)-1)
            key = namespace[i+1:len(namespace)-1]
        new_prefixes.update({key: namespace})

    out_json = json.dumps(new_prefixes, indent = 4)
    with open("graph_prefixes.json", "w") as f:
        f.write(out_json)


def create_new_json(inv_graph_prefix, results, t):
    """
    Create json file with new prefixes

    Parameters:
    -----------
        inv_graph_prefix (dict): prefixes and alias
        results: graph triples
        t (Trie): tree of prefixes
    """
    count_urls = {}
    for row in results:
        literal = False

        sujeito = row["s"]
        predicado = row["p"]
        objeto = row["o"]
        obj_datatype = row['dt']

        if sujeito[-1] == '#' or sujeito[-1] == '/':
            sujeito = sujeito[0:-1]
        
        if predicado[-1] == '#' or predicado[-1] == '/':
            predicado = predicado[0:-1]
        
        if obj_datatype is None:
            if objeto[-1] == '#' or objeto[-1] == '/':
                objeto = objeto[0:-1]

        i = sujeito.find('#')
        if i == -1:
            i = sujeito.rfind('/')
        url_s = sujeito[0:i+1]

        i = predicado.find('#')
        if i == -1:
            i = predicado.rfind('/')
        url_p = predicado[0:i+1]

        i = objeto.find('#')
        if i == -1:
            i = objeto.rfind('/')
        url_o = objeto[0:i+1]

        prefix_s = search_prefix(url_s, inv_graph_prefix, t)
        prefix_p = search_prefix(url_p, inv_graph_prefix, t)

        if obj_datatype is not None:
                literal = True
                prefix_o = "null"
        else:
                prefix_o = search_prefix(url_o, inv_graph_prefix, t)

        if prefix_s == "null":
            if url_s in count_urls:
                count_urls[url_s] += 1
            else:
                count_urls[url_s] = 1

        if prefix_p == "null":
            if url_p in count_urls:
                count_urls[url_p] += 1
            else:
                count_urls[url_p] = 1

        if prefix_o == "null" and not literal:
            if url_o in count_urls:
                count_urls[url_o] += 1
            else:
                count_urls[url_o] = 1      


    new_prefixes = {}
    prefix = ""
    for key in count_urls:
        value = count_urls[key]

        if value > 20:
            last = key.find('#')
            if last == -1:
                last = key.rfind('/')
            first = key.find('/', 0, last)
            second = key.find('/', first+1, last)
            prefix = key[second+1:last]
            prefix = prefix.replace('/', '_')

            new_prefixes.update({prefix: key})

    out_json = json.dumps(new_prefixes, indent = 4)
    with open("inferred_prefixes.json", "w") as f:
        f.write(out_json)
