
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
    f.write("@prefix ngs: <https://ww.dcc.fc.up.pt/~up201605706/ngs#\n\n")
    num = 1
    for sujeito in results_triples:
        for predicado in results_triples[sujeito]:
            for objeto in results_triples[sujeito][predicado]:
                f.write("ngs:t" + str(num) + " rdf:type rdf:statement\n")
                f.write("ngs:t" + str(num) + " rdf:subject ngs:" + str(sujeito) + "\n")
                f.write(
                    "ngs:t" + str(num) + " rdf:predicate ngs:" + str(predicado) + "\n"
                )
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