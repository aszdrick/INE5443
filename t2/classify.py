#!/usr/bin/python3

from arguments import *
import core
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
    elif args.data:
        data_header, data = utils.load_csv(args.data)
    else:
        dataset.error("one of the arguments -d/--data -e/--test_set -s/--split is required")

    if args.ignore:
        utils.ignore_columns(training_set, args.ignore)
        utils.ignore_columns(test_set, args.ignore)
        utils.ignore_columns(data, args.ignore)
        for index in args.ignore:
            if index < args.category:
                args.category -= 1

    return (training_header, training_set, test_set, data)

if __name__ == "__main__":
    args = parser.parse_args()
    if args.data_type == "dataset":
        header, training_set, test_set, data = process_dataset(args)
        params = {
            "algorithm": args.algorithm,
            "category": args.category
        }
        output = core.IBL(training_set, test_set, data, **params)
    else:
        header, training_set, data, size = core.process_spiral(args.spiral_type, args.grid_size, args.noise)
        test_set = []
        params = {
            "algorithm": args.algorithm,
            "category": 2
        }
        output = core.IBL(training_set, test_set, data, **params)
        import image
        image.save(
            positions=[(x[0], x[1]) for x in training_set],
            colors=[utils.hex_to_tuple(x[2]) for x in training_set],
            width=size,
            height=size,
            path=args.output + "_original.png",
            show=args.show
        )

        image.save(
            positions=[(x[0], x[1]) for x in output],
            colors=[utils.hex_to_tuple(x[2]) for x in output],
            width=size,
            height=size,
            path=args.output + ".png",
            show=args.show
        )
