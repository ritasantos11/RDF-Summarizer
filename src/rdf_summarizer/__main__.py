from .summarization import summarize
import sys

def main():
    if len(sys.argv) < 1:
    	print("Need the graph file as argument")
    if len(sys.argv) > 1:
        summarize(sys.argv[1], "normalize literals")

if __name__ == "__main__":
    main()
