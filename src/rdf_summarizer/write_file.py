import re

def write_ontology(f):
    """
        Write ontology for smaller graph

        Parameters:
        -----------
            f: file
    """
    f.write("@prefix ngs: <https://ww.dcc.fc.up.pt/~up201605706/ngs#\n")
    f.write("@prefix xsd: <http://www.w3.org/2001/XMLSchema#>\n")
    f.write("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n\n")

    f.write("ngs:ReifiedTriple  rdfs:subClassOf rdf:Statement ;\n")
    f.write("                    rdfs:comment \"RDF statement about the reduced triple\" .\n\n")
    f.write("ngs:num_occurrences rdfs:domain ngs:ReifiedTriple ;\n")
    f.write("                    rdfs:range  xsd:integer ;\n")
    f.write("                    rdfs:comment \"Indicates how many originals triples are converted into the same reduced triple\" .\n\n")


def write_graph(file_name, results_triples):
    """
        Write smaller graph file

        Parameters:
        -----------
            file_name (str): graph name
            results_triples (dict): reduced triples
    """
    f = open("new_" + file_name + ".nt", "w")
    for sujeito in results_triples:
        for predicado in results_triples[sujeito]:
            for objeto in results_triples[sujeito][predicado]:
                f.write(str(sujeito) + " ")
                f.write(str(predicado) + " ")
                f.write(str(objeto) + "\n")
    f.close()


def write_statements(file_name, results_triples):
    """
        Write rdf statements

        Parameters:
        -----------
            file_name (str): graph name
            results_triples (dict): reduced triples
    """
    f = open("rdf_statements_" + file_name + ".nt", "w")
    write_ontology(f)
    
    num = 1
    for sujeito in results_triples:
        for predicado in results_triples[sujeito]:
            for objeto in results_triples[sujeito][predicado]:
                f.write("ngs:t" + str(num) + " rdf:type ngs:ReifiedTriple\n")
                f.write("ngs:t" + str(num) + " rdf:subject ngs:" + str(sujeito) + "\n")
                f.write("ngs:t" + str(num) + " rdf:predicate ngs:" + str(predicado) + "\n")

                if re.match("^xsd:", str(objeto)):
                    f.write("ngs:t" + str(num) + " rdf:object " + str(objeto) + "\n")
                else:
                    f.write("ngs:t" + str(num) + " rdf:object ngs:" + str(objeto) + "\n")
                
                f.write(
                    "ngs:t"
                    + str(num)
                    + " ngs:num_ocorrencias "
                    + str(results_triples[sujeito][predicado][objeto])
                )
                f.write("\n\n")
                num += 1
    f.close()
