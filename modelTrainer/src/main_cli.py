import argparse
import json

from algorithm import load_algorithm_from_directory


def main(inputfilename, outputfilename):
    algorithm = load_algorithm_from_directory("/app/model")
    with open(inputfilename) as input_file:
        with open(outputfilename, "w") as output_file:
            inputs = json.load(input_file)
            outputs = algorithm.predict(inputs)
            json.dump(outputs, output_file)


parser = argparse.ArgumentParser(
    prog='cli for running ML models in a docker container',
    description='takes an input file, creates an outputfile given the model',
    )

parser.add_argument('inputfilename')
parser.add_argument('outputfilename')

args = parser.parse_args()

main(inputfilename=args.inputfilename, outputfilename=args.outputfilename)
