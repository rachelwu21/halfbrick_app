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
$ python interface.py -i INPUT_FILE [-o=OUTPUT_FILE] {--sql | --json | --analyse} [--sql-command-size=NO_OF_BYTES] [--start=EARLIEST_DATE] [--end=LATEST_DATE] [--group-by=COLUMN_NAME] [--filter-os=OS_1,OS2] [--filter-country=COUNTRY_REGION] [--filter-by-name=COLUMN_1,NAME_A,NAME_B;COLUMN_2,NAME_C,NAME_D]
```
All the options after `{--sql | --json | --analyse}` are only used if the `--analyse` option is chosen.

## CSV to JSON

If you 