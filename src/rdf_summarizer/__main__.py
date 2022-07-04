from .summarization import summarize

def main():
    # TODO complain if not enough arguments
    if len(sys.argv) > 1:
        file_name = re.split("^(.*)\.(\w+)$", sys.argv[1])[1]
        file_ext = re.split("^(.*)\.(\w+)$", sys.argv[1])[2]
        summarize(sys.argv[1], "")

if __name__ == "__main__":
    main()
