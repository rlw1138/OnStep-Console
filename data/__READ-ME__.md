
# READ ME 
for OnStep-Test-Utility "file.py" module
----------------------------------------

The "file.py" module will (usually) let you use arbitrary datafiles listing 
cosmic objects that you might want to look at with your telescope.

The data file needs to be formatted as a python list (actually a list containing 
multiple "tuples"), specifically:
```
stars = [
   ('name of object', 'optional info', 8.6, '17:34:56', '+15:44:59'), # a row of data (tuple)
   ('object name',    'more info',     7.1,  22.9876,      33.6754 ), # another row (tuple)
] # square brackets indicate a 'list'
```
**Requirement**
we want to be able to use a variety of data files, and not be *too* strict, but 
we will stipulate that **'R/A'** and **'DEC'** are in the last two columns of the table
(ie: the final two entries of each row)

both must be "quoted" or 'quoted' if they are sexagesimal:

> R/A --  HH:MM:SS **or** HH:MM:SS.ms (milliseconds, optional, 4 digits max)

> DEC --  sDD:mm:ss **or** sDD*mm:ss (milliseconds optional for both), sign 
        must be present

either may be floating-point format, eg: 17.8975, -34.7928  ==  "17:53:51", "-34:47:34"
(Messier 7, in Scorpio)



"file.py" will try to make sense of what the other columns contain 
( eg: int vs string vs float vs etc ) but it doesn't try to validate 
so use care when preparing a datafile

I like to know 'magnitude' -- besides 'name' info -- so that's usually 
what I put in a "float" column

formats I've tested include:
```
('name' , "add'l info" , mag , 'r/a' , 'dec' ) // ra & dec are 'strings'
('name' , "add'l info" , mag ,  r/a  ,  dec ) // ra & dec are floating-point
('name' , 'type' , 'r/a' , 'dec' )  # same as the OnStep 'upload' web screen
('name' , mag , 'r/a' , 'dec' )
('name' , "add'l info" , 'r/a' , 'dec' )
('name' , 'r/a' , 'dec' )
```






#[com dot hotmail @ rlw1138] -- 2020-APR-15

See [dillinger](https://dillinger.io/)