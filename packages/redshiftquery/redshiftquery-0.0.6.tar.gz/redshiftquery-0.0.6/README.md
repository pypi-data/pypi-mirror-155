# Amazon Connect Tools

These tools are intended to be used to connect and query **one** redshift instance and **one** database.  

## Requirements:

This package is dependant upon [keyring](https://pypi.org/project/keyring/) for keeping credentials secure for connecting to your desired Redshift instance. 

## Instructions:

1. Installation:

```
pip install redshiftquery
```

2. Setup:

Next you will need to setup the [keyring](https://pypi.org/project/keyring/) Login information unique to your redshift database.

You will need to store a 'Host', 'Database', 'Username', and 'Password' by running the following in python once:

```py
import keyring
keyring.set_password('Redshift', 'Host', '[Your Host Server]')
keyring.set_password('Redshift', 'Database', '[Your Database]')
keyring.set_password('Redshift', 'Username', '[Your Username]')
keyring.set_password('Redshift', 'Password', '[Your Password]')
```

*note that the strings used here are case sensitive*

Copy this exactly but replace [Your Host Server], [Your Database], [Your Username], and [Your Password] with your actual login credentials. This will be stored in your OS. 

You can check that it was set up properly by executing keyring's get_password function, for example to check your Username was set up correctly:

```py
keyring.get_password('RedShift', 'Username')
```

## Usage:

### Quick and Dirty Querying 

The main usage of this tool is to quickly get a dataframe from a query writtin in a SQL file. However sometimes queries are short and files may be overkill in these cases the use of ``` exquery() ``` is an easy way to see and get results. I typically use this when checking something from terminal.

Start by importing:

```py```

 
### Query Module

For querying redshift from SQL files in order to retrieve data frames there are a few functions that can be used.

In this example you can see df will be a dataframe holding the contents of mysqlscript.sql which is a file stored in the same working directory of where you are executing your code by using the ``` queryredshift() function ```
 
```py
from redshiftquery import query
df = query.queryredshift('mysqlscript.sql')
```

Additional functionality allows for SQl to be written dynamically and for us to use python to execute the same sql files but by specifying differen values for wildcards coded into a sql file.

Wildcards are expected to be inclused in brackets {}

Suppose now we have the following in our mysqlscript:

```sql
Select * from table1 where col1 = {foo1} and col2 = {foo2}
```

We can execute this from python by specifying a value for ``` foo1 ``` and ```foo2``` by creating a dictionary with the variables we want replaced and the values we want them replaced by. 


```py
from redshiftquery import query

mydict = {'foo1': 4, 'foo2': 'USA'}
df = query.querywithwhere('mysqlscript.sql', mydict)
```

This will replace the bracketed values in mysqlscript.sql and ultimately will execute:

```sql
Select * from table1 where col1 = 4 and col2 = 'USA'
```

You can use dates. I recommend using the datetime module and passing a string.

```py
import datetime
from redshiftquery import query
mydate = dateime.date(2021, 10, 1).strftime('%m/%d/%Y')
mydict = {'foo1':4, 'foo2': mydate}
df = query.querywithwhere('mysqlscript.sql', mydict)
```

## Example

The real power of this tool is the ability to paramaterize and run mulitple queries. 