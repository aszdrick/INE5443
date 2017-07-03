import argparse

parser = argparse.ArgumentParser(description="Tree Clustering data analyser")

parser.add_argument(
    "-o",
    "--output",
    type=str,
    default="out",
    metavar="FILE",
    help="Save classified data as <FILE>.csv"
)

parser.add_argument(
    "-i",
    "--input",
    type=str,
    required=True,
    metavar="FILE",
    help="Filename of the dataset"
)

parser.add_argument(
    "-l",
    "--linkage",
    choices=["complete", "average", "nearest"],
    default="average",
    metavar="TYPE",
    help="Type of linkage to construct dendrogram"
)