splitlog
========
 
Hadoop Yarn application logs aggregate all container logs of a Yarn application into a single file. This makes it very
difficult to use Unix command line tools to analyze these logs: Grep will search over all containers and context
provided for hits often does not include Yarn container name or host name. `splitlog` splits a combined logfile for all
containers of an application into a file system hierarchy suitable for further analysis:

```
outputfolder
|--. hadoopnode1
|  |--. container_a_b
|  |  |--> stderr.log
|  |  '--> stdout.log
|  |  
|  '--. container_x_y
|     |--> stderr.log
|     '--> stdout.log
|
'--. hadoopnode2
   `--. container_p_q
      |--> stderr.log
      `--> stdout.log
```
 
Installation
------------
Python 3.6+ must be available.

1. Create a a new venv using `python -m venv .venv`
2. Activate venv using `. .venv/bin/activate`
3. Run `python -m pip install -e splitlog`
 
How to use
----------

Read logs from standard input:
```shell script
yarn logs -applicationId application_1582815261257_232080 | python -m splitlog application_1582815261257_232080
```

Read logs from file `application_1582815261257_232080.log`:
```shell script
python -m splitlog -i application_1582815261257_232080.log application_1582815261257_232080 
```
