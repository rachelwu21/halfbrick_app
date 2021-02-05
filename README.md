# Table of Contents

1. [Installation](#installation)
2. [Basic Command Line Options](#basic-command-line-options)
3. [CSV to JSON](#csv-to-json)
4. [CSV to SQL commands](#csv-to-sql-commands)
5. [Data Analysis Options](#data-analysis-options)

## Installation

```
$ git clone <>
$ cd <>
```

## Basic Command Line Options

The program has three (mutually exclusive) modes: JSON, SQL, and data analysis. Regardless of the task, this program takes two arguments: input file (CSV) and output file (JSON, SQL).

```
$ python interface.py -i INPUT_FILE [-o=OUTPUT_FILE] {--sql | --json | --analyse} [--sql-command-size=NO_OF_BYTES] [--start=EARLIEST_DATE] [--end=LATEST_DATE] [--group-by=COLUMN_NAME] [--filter-os=OS_1,OS2] [--filter-country=COUNTRY_REGION_CITY] [--filter-by-name=COLUMN_1,NAME_A,NAME_B;COLUMN_2,NAME_C,NAME_D]
```
All the options after `{--sql | --json | --analyse}` are only used if the `--analyse` option is chosen.

## CSV to JSON

If you want to convert a CSV file into JSON, add the `-j` option to activate it. The output file can be specified with the `-o` option. 

## CSV to SQL commands

The CSV file will be turned into SQL commands that insert the data into a table if you use the `--sql` command.

Given that some SQL servers have a maximum command length (measured in memory size), I included an option to set a maximum memory size for each command. The commands will be in the same specified output file, separated by two newline characters. The option to set this is `-z` and `SQL_COMMAND_SIZE` should be specified in bytes.

The name of the table you want to insert the data into also needs to be specified, using the `-t` option. There is a sample SQL script to create an SQL table (named "Sandbox") under `samples/"sql_script_create_table.sql"` . The output script assumes that the field names are the same as the column names.

## Data Analysis Options

The program has several of options for filtering and analysing data. It will do so if you turn on the `--analysis` command. 

There are several example files of how to use the program, which can be tried by running e.g.
`python interface.py @samples/grouup_by.txt`

`--sep` is used to specify the separator between columns used in the CSV. It will default to ',' is left unused.

`--blocksize` is used to break up large CSV files. The size of each block is in bytes.

`--start` and `--end` are for filtering by date. It can handle any date format Pandas' `to_datetime` function can handle. An example of how such a command would work is under `samples/filter_by_time.txt`. 

`--filter-by-name` is used to filter the data based on their values for a number of columns. Each column that should be considered in the filter should be separated by a semicolon. Within each semicolon-separated clause there are comma-separated words. The first such word is the column name, and all subsequent words form a set that each row's field must be in for that row to be included. For example "device_os,android,ios;device_category,tablet" means only rows where the "device_os" is Andoid or iOS (the words are case insensitive) *and* whose"device_category" is "tablet" will be included. An example can be found in `tests/test_name_filter.txt`.

`--filter-by-country` is separate from `--filter-by-name` because `--filter-by-name` always assumes all the conditions must hold true (*and*) while this option assumes any one option will be fine (*or*). The format for `COUNTRY_REGION_CITY` is comma-separated terms of the format `country-region-city`, `country--`, `country-region-`, `-region-city`, `--city`, etc. 

So it can be "the row must be in this country or that region". It also allows for country and region to be considered, so it can be "must be downloaded in the Piura region in Peru, or Cuba" (peru-piura,cuba)

`--group-by` lets you specify a comma-separated list of fields to group the results by. If you do not also choose the `--plot` option, it will output a CSV file with the count of the number of rows in each category. If the `--plot` option is also chosen, there will be several lines on the plot, one for each category. An example of aggregation would be in `samples/grouup_by.txt` where `-g=geo_country,geo_region` means the data is grouped by country and region. 

`--plot` will produce a frequency line plot that will be output to a png, tif, etc. file. An example of a grouped frequency line plot can be found by running `samples/timezones.txt`. An examples of a ungrouped frequency line plot can be found by running `samples/plot.txt`.

`--level` is used with `--plot` to determine the level of the sampling. The options available can be found [here](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases). Examples are in `samples/timezones.txt` and `samples/plot.txt`.