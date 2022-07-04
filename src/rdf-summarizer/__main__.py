from summarization import summarize

def main():
    file_name = re.split("^(.*)\.(\w+)$", sys.argv[1])[1]
    file_ext = re.split("^(.*)\.(\w+)$", sys.argv[1])[2]
    summarization(sys.argv[1], "")
