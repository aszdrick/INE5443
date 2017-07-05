import argparse

def interval(value):
    ps = value.split("-")
    if len(ps) != 2:
        raise argparse.ArgumentParser()
    pv = tuple(map(lambda s: int(s), ps))
    if pv[0] > pv[1]:
        raise argparse.ArgumentParser()
    return pv

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

parser.add_argument(
    "-m",
    "--class_range",
    required=True
    type=interval,
    metavar="MIN_VALUE-MAX_VALUE",
    help="Minimum and maximum number of classes"
)

parser.add_argument(
    "-aw",
    "--average_weight",
    type=float,
    default=1,
    help="Mean/average weight"
)

parser.add_argument(
    "-sw",
    "--sd_weight",
    type=float,
    default=1,
    help="Standard deviation weight"
)
