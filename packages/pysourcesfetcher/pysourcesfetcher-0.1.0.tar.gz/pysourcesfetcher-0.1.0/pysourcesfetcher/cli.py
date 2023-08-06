"""Console script for pysourcesfetcher."""
# import argparse
import fire
import sys

from pysourcesfetcher.pysourcesfetcher import pysourcesinfo

def main():
    """Console script for pysourcesfetcher."""
    fire.Fire(pysourcesinfo)
    return 0
    #parser = argparse.ArgumentParser()
    #parser.add_argument('_', nargs='*')
    #args = parser.parse_args()

    #print("Arguments: " + str(args._))
    #print("Replace this message by putting your code into "
    #      "pysourcesfetcher.cli.main")
    

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
