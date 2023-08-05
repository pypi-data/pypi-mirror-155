import argparse

from impactrun import fuzzallspecs, runall


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--generate-tests', help='generate fuzz tests', action='store_true')
    parser.add_argument('-e', '--execute-tests', help='execute fuzz tests', action='store_true')
    parser.add_argument('-r', '--regen-report', nargs=2, help='regenerate reports')
    parser.add_argument('-u', '--customer-name', help='customer name (optional)', default='N/A')
    args = parser.parse_args()

    if args.generate_tests:
        fuzzallspecs.fuzzspecs()
    elif args.execute_tests or args.regen_report:
        runall.main(args.regen_report, args.customer_name)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
