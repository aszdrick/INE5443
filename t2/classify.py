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
    elif args.data:
        data_header, data = utils.load_csv(args.data)
    else:
        dataset.error("one of the arguments -d/--data -e/--test_set -s/--split is required")

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

if __name__ == "__main__":
    args = parser.parse_args()
    if args.data_type == "dataset":
        header, training_set, test_set, data = process_dataset(args)
        params = {
            "algorithm": args.algorithm,
            "category": args.category
        }
        output = core.IBL(training_set, test_set, data, **params)
        if args.show:
            if len(training_set[0]) == 3:
                core.plot(output[0], training_set, header, args.category)
            else:
                print("Cannot show non-2D data.")

    else:
        header, training_set, data, size = core.process_spiral(args.spiral_type, args.grid_size, args.noise)
        test_set = []
        params = {
            "algorithm": args.algorithm,
            "category": 2
        }

        image.save(
            positions=[(x[0], x[1]) for x in training_set],
            colors=[utils.hex_to_tuple(x[2]) for x in training_set],
            width=size,
            height=size,
            path=args.output + "_original.png",
            show=args.show
        )

        output = core.IBL(training_set, test_set, data, **params)
        colors = [utils.hex_to_tuple(x[2]) for x in output[1]]

        if len(training_set[0]) == 3:
            image.save(
                positions=[(x[0], x[1]) for x in output[1]],
                colors=colors,
                width=size,
                height=size,
                path=args.output + ".png",
                show=args.show
            )


