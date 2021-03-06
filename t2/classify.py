#!/usr/bin/python3

from arguments import *
import core
import image
import utils

def process_dataset(args):
    training_header, training_set = utils.load_csv(args.input)
    if len(training_set) == 0:
        dataset.error("Invalid input: file does not exist or is empty.")
    
    test_set = []
    data = []
    if args.split:
        test_set = core.split_data(data=training_set, percentage=args.split)
    elif args.test_set:
        test_header, test_set = utils.load_csv(args.test_set)
        if len(test_set) == 0:
            dataset.error("Invalid test set: file does not exist or is empty.")
    elif not args.data:
        dataset.error("one of the arguments -d/--data -e/--test_set -s/--split is required")

    if args.data:
        data_header, data = utils.load_csv(args.data)

    # if len(args.category) > 1:
    #     categories = sorted(args.category)
    #     args.category = utils.aglutinate(training_header, categories)
    #     utils.aglutinate(training_set, categories)
    #     utils.aglutinate(test_set, categories)
    #     utils.aglutinate(data, categories)

    if args.ignore:
        utils.ignore_columns(training_set, args.ignore)
        utils.ignore_columns(test_set, args.ignore)
        utils.ignore_columns(data, args.ignore)
        for index in args.ignore:
            if index < args.category:
                args.category -= 1


    return (training_header, training_set, test_set, data)

def classify_dataset(args):
    header, training_set, test_set, data = process_dataset(args)
    params = {
        "algorithm": args.algorithm,
        "category": args.category,
        "k": args.knn if "knn" in args else 1,
        "zpa": args.zpa if "zpa" in args else 0,
        "zpd": args.zpd if "zpd" in args else 0,
        "zfa": args.zfa if "zfa" in args else 0,
        "zfd": args.zfd if "zfd" in args else 0,
    }
    (output, classifier) = core.IBL(training_set, test_set, data, **params)

    if len(output[1]) > 0:
        utils.save_csv(args.output, [header] + output[1])

    if args.show:
        if len(training_set[0]) == 3:
            core.plot(training_set, output[0], output[1], header, args.category)
        else:
            print("Cannot show non-2D data.")


def classify_spiral(args):
    header, training_set, data, size = core.process_spiral(args.spiral_type, args.grid_size, args.noise)
    test_set = []
    params = {
        "algorithm": args.algorithm,
        "category": 2,
        "k": args.knn if "knn" in args else 1,
        "zpa": args.zpa if "zpa" in args else 0,
        "zpd": args.zpd if "zpd" in args else 0,
        "zfa": args.zfa if "zfa" in args else 0,
        "zfd": args.zfd if "zfd" in args else 0,
    }
    (output, classifier) = core.IBL(training_set, test_set, data, **params)

    if args.algorithm == "IB3":
        descriptor = classifier.descriptor.data
    else:
        descriptor = classifier.descriptor

    core.save_spirals(training_set, output, args.output, size, args.show, descriptor, classifier.dropped)

def main():
    args = parser.parse_args()
    if args.data_type == "dataset":
        classify_dataset(args)
    else:
        classify_spiral(args)

if __name__ == "__main__":
    main()
