import argparse
from critparse import CriterionParser, CriterionMovieParse


def main():
    args = process_args()
    if args.url:
        parser = CriterionParser.CriterionParser(args.url)
        if args.api:
            parser.collect_information_for_api()
        else:
            parser.print_info()


def process_args():
    usage_desc = "This is how you use this thing"
    parser = argparse.ArgumentParser(description=usage_desc)
    parser.add_argument("url", help="URL to parse")
    parser.add_argument("-a", "--api", help="Add movie via REST api", action='store_true')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
