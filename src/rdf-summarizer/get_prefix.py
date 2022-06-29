
# funcoes auxiliares

from trie import Trie


def create_trie(json_file):
    """
    Creates a trie

    Parameters:
    -----------
        json_file (dict): prefixes to insert in trie
    """
    t = Trie()
    for key in json_file:
        t.insert(json_file[key])
    return t  


def search_prefix(url, inv_json, t):
    """
    Searches url in json file

    Parameters:
    -----------
        url (str): url to be found

    Returns:
        alias associated with the url or null if not found
    """
    prefix = t.search(url)
    if prefix != "":
        return inv_json.get(prefix)
    return "null"
