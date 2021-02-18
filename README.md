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

### Commands and their outputs
<details><summary>Cities in China</summary>
<p>

```
$ python interface.py @samples/cities_in_china.txt
          geo_city  size  percentage
0                    122    4.704975
172       Shanghai    98    3.779406
62       Guangzhou    86    3.316622
17         Beijing    80    3.085229
69        Hangzhou    62    2.391053
33         Chengdu    57    2.198226
255      Zhengzhou    53    2.043965
190         Suzhou    52    2.005399
206        Wenzhou    51    1.966834
181       Shenzhen    46    1.774007
211          Xi'an    44    1.696876
160        Qingdao    40    1.542615
143        Nanjing    39    1.504049
149         Ningbo    39    1.504049
193        Taizhou    38    1.465484
37       Chongqing    38    1.465484
58          Fuzhou    37    1.426919
112        Kunming    35    1.349788
207          Wuhan    34    1.311223
27        Changsha    33    1.272657
71          Harbin    33    1.272657
195        Tianjin    30    1.156961
212         Xiamen    30    1.156961
51        Dongguan    30    1.156961
201         Urumqi    26    1.002700
24       Changchun    25    0.964134
100          Jinan    24    0.925569
141       Nanchang    24    0.925569
209           Wuxi    22    0.848438
180       Shenyang    21    0.809873
88         Huizhou    21    0.809873
125          Linyi    19    0.732742
55          Foshan    18    0.694177
167       Quanzhou    17    0.655611
73           Hefei    16    0.617046
116        Lanzhou    16    0.617046
236        Yichang    16    0.617046
80          Hohhot    16    0.617046
192        Taiyuan    15    0.578481
29       Changzhou    15    0.578481
221       Xinxiang    15    0.578481
12         Baoding    14    0.539915
147        Nanyang    14    0.539915
76        Hengyang    13    0.501350
144        Nanning    13    0.501350
132        Luoyang    13    0.501350
107       Jiujiang    13    0.501350
103         Jinhua    13    0.501350
259        Zhoukou    13    0.501350
20           Bijie    13    0.501350
194       Tangshan    12    0.462784
146        Nantong    12    0.462784
145        Nanping    12    0.462784
233       Yangzhou    12    0.462784
173       Shangqiu    12    0.462784
257      Zhongshan    11    0.424219
64          Guilin    11    0.424219
189         Suqian    11    0.424219
102       Jingzhou    11    0.424219
227         Xuzhou    11    0.424219
59         Ganzhou    10    0.385654
202        Weifang    10    0.385654
72           Hechi    10    0.385654
178       Shaoxing    10    0.385654
68          Handan    10    0.385654
57          Fuyang    10    0.385654
252      Zhanjiang    10    0.385654
97         Jiaxing    10    0.385654
65         Guiyang     9    0.347088
104         Jining     9    0.347088
150         Ningde     9    0.347088
6           Anshan     9    0.347088
99           Jilin     9    0.347088
93           Ji'an     8    0.308523
264           Zibo     8    0.308523
245       Yuncheng     8    0.308523
115       Langfang     8    0.308523
234         Yantai     8    0.308523
157    Qiandongnan     8    0.308523
158        Qiannan     8    0.308523
86       Huanggang     8    0.308523
191         Tai'an     8    0.308523
266          Zunyi     8    0.308523
81          Honghe     8    0.308523
43          Daqing     8    0.308523
8           Anyang     7    0.269958
208           Wuhu     7    0.269958
235          Yibin     7    0.269958
119    Lianyungang     7    0.269958
162       Qingyuan     7    0.269958
179       Shaoyang     7    0.269958
23        Cangzhou     7    0.269958
251      Zhangzhou     7    0.269958
256      Zhenjiang     7    0.269958
136        Maoming     7    0.269958
96         Jiaozuo     7    0.269958
98         Jieyang     7    0.269958
215      Xiangyang     6    0.231392
18          Bengbu     6    0.231392
83         Huai'an     6    0.231392
49          Dezhou     6    0.231392
237         Yichun     6    0.231392
203         Weihai     6    0.231392
45          Dazhou     6    0.231392
25         Changde     6    0.231392
168         Qujing     6    0.231392
182   Shijiazhuang     6    0.231392
21         Binzhou     6    0.231392
131          Lu'an     6    0.231392
35         Chifeng     6    0.231392
244          Yulin     6    0.231392
92             Ili     6    0.231392
262      Zhumadian     6    0.231392
90      Hulun Buir     6    0.231392
263        Zhuzhou     5    0.192827
41          Dalian     5    0.192827
169         Quzhou     5    0.192827
31        Chaozhou     5    0.192827
222        Xinyang     5    0.192827
153   Pingdingshan     5    0.192827
170         Rizhao     5    0.192827
22          Bozhou     5    0.192827
95        Jiangmen     5    0.192827
78            Heze     5    0.192827
53           Enshi     5    0.192827
139       Mianyang     5    0.192827
253       Zhaoqing     5    0.192827
217       Xianyang     5    0.192827
243        Yueyang     5    0.192827
231       Yancheng     5    0.192827
120      Liaocheng     5    0.192827
60           Garze     5    0.192827
126         Lishui     5    0.192827
197        Tonghua     4    0.154261
151          Ordos     4    0.154261
91          Huzhou     4    0.154261
105       Jinzhong     4    0.154261
196        Tieling     4    0.154261
156         Puyang     4    0.154261
261         Zhuhai     4    0.154261
148       Neijiang     4    0.154261
26         Changji     4    0.154261
30        Chaoyang     4    0.154261
238       Yinchuan     4    0.154261
163    Qinhuangdao     4    0.154261
32         Chengde     4    0.154261
121       Liaoyang     4    0.154261
165        Qiqihar     4    0.154261
61       Guangyuan     4    0.154261
230        Yanbian     4    0.154261
248      Zaozhuang     4    0.154261
54   Fangchenggang     4    0.154261
219        Xingtai     4    0.154261
127     Liupanshui     4    0.154261
176        Shanwei     4    0.154261
183         Shiyan     4    0.154261
225      Xuancheng     4    0.154261
140     Mudanjiang     4    0.154261
174       Shangrao     4    0.154261
39         Chuzhou     4    0.154261
77          Heyuan     4    0.154261
239        Yingkou     3    0.115696
265         Zigong     3    0.115696
184   Shuangyashan     3    0.115696
188        Suizhou     3    0.115696
240        Yingtan     3    0.115696
223        Xinzhou     3    0.115696
34        Chenzhou     3    0.115696
247           Yuxi     3    0.115696
220         Xining     3    0.115696
260       Zhoushan     3    0.115696
229         Yan'an     3    0.115696
242       Yongzhou     3    0.115696
5           Anqing     3    0.115696
228          Ya'an     3    0.115696
210        Wuzhong     3    0.115696
16        Bayingol     3    0.115696
250    Zhangjiakou     3    0.115696
19           Benxi     3    0.115696
175        Shantou     3    0.115696
128        Liuzhou     3    0.115696
94         Jiamusi     3    0.115696
117         Leshan     3    0.115696
47           Deqen     3    0.115696
123         Linfen     3    0.115696
111        Kashgar     3    0.115696
48          Deyang     3    0.115696
66          Haikou     3    0.115696
38        Chongzuo     3    0.115696
138        Meizhou     3    0.115696
129        Longyan     3    0.115696
134        Lvliang     3    0.115696
40            Dali     3    0.115696
84         Huaihua     3    0.115696
85         Huainan     3    0.115696
46          Dehong     3    0.115696
118          Lhasa     2    0.077131
224  Xishuangbanna     2    0.077131
56          Fushun     2    0.077131
130          Loudi     2    0.077131
226        Xuchang     2    0.077131
63         Guigang     2    0.077131
10           Baise     2    0.077131
114          Laiwu     2    0.077131
135      Ma'anshan     2    0.077131
110        Kaifeng     2    0.077131
108        Jiuquan     2    0.077131
106        Jinzhou     2    0.077131
101       Jincheng     2    0.077131
75        Hengshui     2    0.077131
3             Alxa     2    0.077131
89         Huludao     2    0.077131
87       Huangshan     2    0.077131
2            Altay     2    0.077131
216       Xianning     2    0.077131
133         Luzhou     2    0.077131
166          Qoqek     2    0.077131
50          Dingxi     2    0.077131
200        Ulanqab     2    0.077131
164        Qinzhou     2    0.077131
42         Dandong     2    0.077131
155         Putian     2    0.077131
213       Xiangtan     2    0.077131
44          Datong     2    0.077131
198       Tongliao     2    0.077131
199        Tongren     2    0.077131
52        Dongying     2    0.077131
142       Nanchong     2    0.077131
186       Songyuan     2    0.077131
159      Qianxinan     2    0.077131
15       Bayan Nur     2    0.077131
177       Shaoguan     2    0.077131
74           Heihe     1    0.038565
249    Zhangjiajie     1    0.038565
7           Anshun     1    0.038565
70        Hanzhong     1    0.038565
214        Xiangxi     1    0.038565
161       Qingyang     1    0.038565
254       Zhaotong     1    0.038565
4           Ankang     1    0.038565
258       Zhongwei     1    0.038565
171        Sanming     1    0.038565
79          Hezhou     1    0.038565
187         Suihua     1    0.038565
82           Hotan     1    0.038565
185       Shuozhou     1    0.038565
67           Haixi     1    0.038565
241         Yiyang     1    0.038565
246          Yunfu     1    0.038565
204         Weinan     1    0.038565
218        Xiaogan     1    0.038565
1              Aba     1    0.038565
14          Baotou     1    0.038565
137        Meishan     1    0.038565
205        Wenshan     1    0.038565
13           Baoji     1    0.038565
124         Linxia     1    0.038565
122        Lincang     1    0.038565
28        Changzhi     1    0.038565
152         Panjin     1    0.038565
232      Yangjiang     1    0.038565
11         Baishan     1    0.038565
9         Baicheng     1    0.038565
113         Laibin     1    0.038565
154          Pu'er     1    0.038565
109           Jixi     1    0.038565
36         Chizhou     1    0.038565

```
</p>
</details>

<details><summary>Cities in India</summary>
<p>

```


```
</p>
</details>

<details><summary>sku</summary>
<p>

```


```
</p>
</details>

<details><summary>Install Source</summary>
<p>

```


```
</p>
</details>

<details><summary>UA Source</summary>
<p>

```


```
</p>
</details>

<details><summary>Device Category</summary>
<p>

```


```
</p>
</details>

<details><summary>Device Brand Name</summary>
<p>

```


```
</p>
</details>

<details><summary>Device OS</summary>
<p>

```


```
</p>
</details>

<details><summary>Ad Tracking</summary>
<p>

```


```
</p>
</details>

<details><summary>Device Language</summary>
<p>

```


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