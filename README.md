# Table of Contents

1. [Installation](#installation)
2. [Basic Command Line Options](#basic-command-line-options)
3. [CSV to JSON](#csv-to-json)
4. [CSV to SQL commands](#csv-to-sql-commands)
5. [Data Analysis Options](#data-analysis-options)
6. [Examples and Insights from the Given Dataset](#examples-and-insights-from-the-given-dataset)
7. [Unit tests](#unit-tests)
8. [Pip install](#pip-install)
9. [Docker install](#docker-install)

## Installation

```
$ git clone <>
$ cd <>
```

## Basic Command Line Options

The program has three (mutually exclusive) modes: JSON, SQL, and data analysis. Regardless of the task, this program an input file (CSV).

All modes require a CSV input file, and all but the "aggregate" option for data analysis require an output file (the results of the aggregation may be printed). The SQL option can take an .sql or .txt file, the JSON option takes a .json file, the data analysis option takes a .csv output for aggregation, and prints the output to terminal if one is not specified. The `--plot` option for analysis takes eps, jpeg, jpg, pdf, pgf, png, ps, raw, rgba, svg, svgz, tif, tiffeps, jpeg, jpg, pdf, pgf, png, ps, raw, rgba, svg, svgz, tif and tiff files as output.

```
$ python interface.py -i INPUT_FILE [-o=OUTPUT_FILE] {--sql | --json --table TABLE_NAME| --analyse} [--sql-command-size=NO_OF_BYTES] [--start=EARLIEST_DATE] [--end=LATEST_DATE] [--group-by=COLUMN_NAME] [--filter-os=OS_1,OS2] [--filter-country=COUNTRY_REGION_CITY] [--filter-by-name=COLUMN_1,NAME_A,NAME_B;COLUMN_2,NAME_C,NAME_D] [--blocksize BLOCKSIZE] [--sep SEPERATOR]
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
`python interface.py @samples/group_by.txt`

`--sep` is used to specify the separator between columns used in the CSV. It will default to ',' is left unused.

`--blocksize` is used to break up large CSV files and manage memory, by default Dask should prevent overflow. The size of the blocks is in bytes.

`--start` and `--end` are for filtering by date. It can handle any date format Pandas' `to_datetime` function can handle. An example of how such a command would work is under `samples/filter_by_time.txt`. 

`--filter-by-name` is used to filter the data based on their values for a number of columns. Each column that should be considered in the filter should be separated by a semicolon. Within each semicolon-separated clause there are comma-separated words. The first such word is the column name, and all subsequent words form a set that each row's field must be in for that row to be included. For example "device_os,android,ios;device_category,tablet" means only rows where the "device_os" is Andoid or iOS (the words are case insensitive) *and* whose"device_category" is "tablet" will be included. An example can be found in `tests/test_name_filter.txt`.

`--filter-by-country` is separate from `--filter-by-name` because `--filter-by-name` always assumes all the conditions must hold true (*and*) while this option assumes any one option will be fine (*or*). The format for `COUNTRY_REGION_CITY` is comma-separated terms of the format `country-region-city`, `country--`, `country-region-`, `-region-city`, `--city`, etc. 

So it can be "the row must be in this country or that region". It also allows for country and region to be considered, so it can be "must be downloaded in the Piura region in Peru, or Cuba" (peru-piura,cuba)

`--group-by` lets you specify a comma-separated list of fields to group the results by. If you do not also choose the `--plot` option, it will output a CSV file with the count of the number of rows in each category. If the `--plot` option is also chosen, there will be several lines on the plot, one for each category. An example of aggregation would be in `samples/grouup_by.txt` where `-g=geo_country,geo_region` means the data is grouped by country and region. 

`--plot` will produce a frequency line plot that will be output to a png, tif, etc. file. An example of a grouped frequency line plot can be found by running `samples/timezones.txt`. An examples of a ungrouped frequency line plot can be found by running `samples/plot.txt`.

`--level` is used with `--plot` to determine the level of the sampling. The options available can be found [here](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases). Examples are in `samples/timezones.txt` and `samples/plot.txt`.

## Examples and Insights from the Given Dataset

By running the right commands, it is possible to extract informative aggregations from the data.

By running:

```
python interface.py @samples/countries.txt
```

We learn the number of downloads in the last 24 hours (the data given only covers 24 hours) in each nation. The top ten nations with the most downloads are, in order: India, China, Brazil, Italy, Spain, Egypt, Chile, Peru, Iraq, Iran. By comparison, the ten most populous nations in the world are: China, India, United States, Indonesia, Pakistan, Brazil, Nigeria, Bangladesh, Russia, Mexico.

It may be useful to look at the cities with the most downloads in the two top nations:

``` 
python interface.py @samples/cities_in_china.txt
python interface.py @samples/cities_in_india.txt
```

We learn that the most downloads in China are not recorded as any specific city, and the city with the most downloads is Shanghai, with 98 out of the total 2593 (3.8%) downloads in China. This makes sense, since Shanghai was the most populous city in China as of the 2010 census, with 1.5% of the nation's total population. This means the city is vastly over-represented in terms of number of downloads. This makes sense, as people living in cities are more likely to be able to afford higher-end smartphones for games.

The city with the most downloads in India is Hyderabad, which is only the fourth most populous city in India, with 0.9% of the nation's total population as of 2019. In comparison, it made up 11.7% of the number of downloads from India in the 24 hours given.

A quick look as all the other possible aggregations will also be useful:

```
python interface.py @samples/sku.txt
python interface.py @samples/install_source.txt
python interface.py @samples/ua_source.txt
python interface.py @samples/device_category.txt
python interface.py @samples/device_brand_name.txt
python interface.py @samples/device_os.txt
python interface.py @samples/is_limited_ad_tracking.txt
python interface.py @samples/device_language.txt
```


<details><summary>Commands and their outputs</summary>
<p>
```
$ python interface.py @samples/cities_in_china.txt

$ python interface.py @samples/cities_in_india.txt

$ python interface.py @samples/sku.txt

$ python interface.py @samples/install_source.txt

$ python interface.py @samples/ua_source.txt

$ python interface.py @samples/device_category.txt

$ python interface.py @samples/device_brand_name.txt

$ python interface.py @samples/device_os.txt

$ python interface.py @samples/is_limited_ad_tracking.txt

$ python interface.py @samples/device_language.txt

```
</p>
</details>

You can also run example plots.

```
python interface.py @samples/
```

## Unit tests

The unit tests can be run like so:

```
cd tests
python tests.py
```

## Pip install

Install with

````
pip install ....
````

The name of the package is `happ` , and can be run with:

```
happ [OPTIONS]
```

For example:

```
happ @samples/device_os
```



## Docker install

Install with

```
docker build -t halfbrick_app .
```

Try running it for a print output:

```
docker run --rm halfbrick_app @samples/device_category.txt
```
If you want to make your own file with command-line arguments in the host machine and pass it to the docker container, run:

```
docker run --name h_app -v $(pwd):$(pwd) halfbrick_app @YOUR/PATH/HERE
```

If you want to copy the output file to the host:

```
sudo docker cp h_app:EXAMPLE_FILE $(pwd)
```

For example:

```
docker run --name h_app -v $(pwd):$(pwd) halfbrick_app @samples/plot_total.txt
sudo docker cp h_app:plot_total.png $(pwd)
```

Will copy the output image to your current directory.