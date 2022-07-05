import re
import json
import time
import sys
import rdflib as rdf
from os import path
from .prefixes import search_prefix, create_trie, infer_common_namespaces, extract_namespace_declarations
from .write_file import write_graph, write_statements


start_time = time.time()
local_time = time.ctime(start_time)
print("%s" % local_time)


def update_dict(results_triples, s, p, o):
    """
    Add new triple to the dictionary

    Parameters:
    -----------
        results_triples (dict): reduced triples: {s: {p: {o: count}}}
        s (str): subject url
        p (str): predicate url
        o (str): object url
    """
    new_results = {p: {o: 1}}
    if s in results_triples:
        predicado, objeto = False, False

        for pred in results_triples[s]:
            if pred == p:
                predicado = True
                for obj in results_triples[s][pred]:
                    if obj == o:
                        objeto = True
                        break
                if not objeto:
                    results_triples[s][pred][o] = 1
                else:
                    results_triples[s][pred][o] += 1
                break

        if not predicado:
            results_triples[s].update(new_results)

    else:
        results_triples[s] = new_results


def summarize(graph, string):
    """
    Summarize graph

    Parameters:
    -----------
        graph (Graph): graph to be summarized
        string (str): if normalize literals, the literals are converted
    """

    file_name = re.split("^(.*)\.(\w+)$", graph)[1]
    file_ext = re.split("^(.*)\.(\w+)$", graph)[2]

    if not path.exists(graph):
        print(f'Cannot find file {graph}', file=sys.stderr)
        sys.exit(1)

    normalize = False
    if string == "normalize literals":
        normalize = True

    print(f"processing {graph}")

    g = rdf.Graph().parse(graph)
    print("--- %s seconds after parse---" % (time.time() - start_time))
    results = g.query(
    """
        select ?s ?p ?o ?dt
        where {
            ?s ?p ?o .
            bind (datatype(?o) as ?dt)
        }
        order by ?s ?p ?o ?dt
    """
    )
    print("--- %s seconds after query---" % (time.time() - start_time))

    # prefixes of graph file
    extract_namespace_declarations(g)
    print("--- %s seconds after creation of first json---" % (time.time() - start_time))

    f = open("graph_prefixes.json")
    graph_prefixes = json.load(f)
    f.close()

    f = open("prefixcc.json")
    prefixcc = json.load(f)
    f.close()

    graph_prefix = {**prefixcc, **graph_prefixes}
    inv_graph_prefix = { v:k for k,v in graph_prefix.items() }

    t1 = create_trie(graph_prefix)

    infer_common_namespaces(inv_graph_prefix, results, t1)
    print(
        "--- %s seconds after creation of second json---" % (time.time() - start_time)
    )

    f = open("inferred_prefixes.json")
    inferred_prefixes = json.load(f)
    f.close()

    graph_prefix_new = {**inferred_prefixes, **prefixcc, **graph_prefixes}
    inv_graph_prefix_new = { v:k for k,v in graph_prefix_new.items() }

    t = create_trie(graph_prefix_new)

    results_triples = {}
    total = len(results)
    print(f"--- will process {total} triples")
    for count, row in enumerate(results):
        if count % 10000 == 0:
            print(
                f"Processed {str(count)} triples ({round((count*100)/total, 2)}%) in {str(time.time() - start_time)}"
            )

        literal = False
        suj_blank = False
        obj_blank = False

        sujeito = row["s"]
        predicado = row["p"]
        objeto = row["o"]
        obj_datatype = row["dt"]

        if type(sujeito) == 'rdf.term.BNode':
            suj_blank = True
        if type(objeto) == 'rdf.term.BNode':
            obj_blank = True

        if obj_blank:
            prefix_o = "bnode"
        else:
            if normalize:
                if obj_datatype is not None:
                    literal = True
                    prefix_o = "null"
                    i = obj_datatype.find("#")
                    obj_datatype = obj_datatype[i + 1 :]
                else:
                    prefix_o = search_prefix(objeto, inv_graph_prefix_new, t)
            else:
                prefix_o = search_prefix(objeto, inv_graph_prefix_new, t)

        if suj_blank:
            prefix_s = "bnode"
        else:
            prefix_s = search_prefix(sujeito, inv_graph_prefix_new, t)

        prefix_p = search_prefix(predicado, inv_graph_prefix_new, t)


        nt_subject = str(sujeito) if prefix_s == "null" else prefix_s
        nt_predicate = str(predicado) if prefix_p == "null" else prefix_p

        if prefix_o == "null":
            if literal:
                nt_object = str(obj_datatype)
            else:
                nt_object = str(objeto)
        else:
            nt_object = prefix_o

        update_dict(results_triples, nt_subject, nt_predicate, nt_object)
    

    print(results_triples)
    print("--- %s seconds after for---" % (time.time() - start_time))

    write_graph(file_name, results_triples)
    print("--- %s seconds after writing smaller graph---" % (time.time() - start_time))

    write_statements(file_name, results_triples)
    print("--- %s seconds after writing rdf statements---" % (time.time() - start_time))

    local_time = time.ctime(time.time())
    print("%s" % local_time)


