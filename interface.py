import argparse
from src.stats import *
from src.utils import *
import csv
import sys

def parse_args(args):
    parser = argparse.ArgumentParser(description="Placeholder",fromfile_prefix_chars='@')

    parser.add_argument('-i','--input',type=str,action='store',
    help="""The path of the input CSV file.""", required=True, nargs=1)

    parser.add_argument('-o','--output',type=str,action='store',
    help="""The path of the output SQL/json/summary file.""", required=False, nargs=1)

    parser.add_argument('-t','--table',type=str,action='store',
    help="""The name of the SQL table to be used.""", required=False, nargs=1)

    parser.add_argument('-d','--sql', action="store_true", default=False)

    parser.add_argument('-j','--json', action="store_true", default=False)

    parser.add_argument('-a','--analyse', action="store_true", default=False)

    parser.add_argument('-z','--sql-command-size', action="store", 
    required=False, nargs=1, type=int)

    parser.add_argument('-p','--parse-dates', action="store", 
    required=False, nargs=1, type=str)

    parser.add_argument('-sep','--sep', action="store", 
    required=False, nargs=1, type=str)

    parser.add_argument('-b','--blocksize', action="store", 
    required=False, nargs=1, type=int)

    parser.add_argument('-g','--group-by', type=str, action='store',
    help="""specify which variables you want the results grouped by: 
    e.g. country, region, country-and-region, device-type, brand, model, 
         OS, install-source, sku, language""", required=False, nargs=1)

    parser.add_argument('-s','--start', type=str, action='store',
    help="""specify the earliest date and time (UTC) you want included in the results. 
    Format YYYY-MM-DD HH:MM:SS.MMM""", required=False, nargs=1)

    parser.add_argument('-e','--end', type=str, action='store',
    help="""specify the latest date and time (UTC) you want included in the results. 
    Format YYYY-MM-DD HH:MM:SS.MMM""", required=False, nargs=1)

#    parser.add_argument('-fos','--filter-os', type=str, action='store',
#    help="""comma seperated OSes to include: android-max-4.0,ios-min-5.0.1-max-6.0""", 
#    required=False, nargs=1)

    parser.add_argument('-fc','--filter-country', type=str, action='store',
    help="""comma seperated countries/regions to include: country,
    country-region,-region""", 
    required=False, nargs=1)

    parser.add_argument('-fn','--filter-by-name', type=str, action='store',
    help="""spec""", 
    required=False, nargs=1)

    return parser.parse_args(args)

def main():
    args = parse_args(sys.argv[1:])
    #args = parse_args(['@../halfbrick_app/samples/arguments.txt'])

    csvFilePath = args.input[0]
    outputFilePath = args.output[0]

    if args.json:
        csv_to_json(csvFilePath, outputFilePath)
    elif args.sql:
        tableName = args.table[0]
        if args.sql_command_size:
            sql_input_statement(csvFilePath, tableName, outputFilePath, one_statement=False, max_sql_size=args.sql_command_size[0])
        else:
            sql_input_statement(csvFilePath, tableName, outputFilePath)
    elif args.analyse:
        stats = Stats(args)
        #print(stats.dfd[['user_pseudo_id','timestamp_raw']].head())
        stats.filter()
        #stats.aggregate()
        stats.dfd.compute()
        #print('\n\n',stats.dfd[['user_pseudo_id','timestamp_raw']].head())


if __name__ == '__main__':
    main()
