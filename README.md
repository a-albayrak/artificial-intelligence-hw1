# CENG461 - HW1

## CENG 461 — Assignment 1:  
### Constraint Satisfaction Problems

Write a Python program that solves logic puzzles with the following properties:

- You are given some clues about 4 subjects.  
- All subjects have 4 attributes.  
- For each attribute, the values are all different for 4 subjects.  
- For each attribute, the 4 possible values are given.  
- The first attribute is always the only numeric one and takes unsigned integers.  
- All attribute names and values are alphanumeric (e.g. no space character).  
- There is a unique solution.  

The scope of the puzzle (attributes and possible values) are given in 4 lines in data-*.txt files, each of which is as follows:

```
attribute,value1,value2,value3,value4
```

Clues are given in clues-*.txt files in any order. The formal language for clues and their semantics:

```
if x=a then y=b
if x=a then not y=b
if x=a then either y=b or z=c
n(x=a) = n(y=b)
n(x=a) = n(y=b) + m
n(x=a) = n(y=b) - m
n(x=a) > n(y=b)
n(x=a) < n(y=b)
one of {x=a,y=b} corresponds to z=c other t=d
{x=a,y=b,z=c} are all different
```

- x, y, z, t: any attribute (including the numeric one)  
- a, b, c, d: attribute values  
- n: the numeric attribute  
- m: an unsigned integer  

---

We provide 3 pairs of text files defining puzzles. All lines end with Unix-style newline characters (`\n`).  
Your script must allow the user to choose a problem, then solve it.  

For example, if the user enters `1`, your script should read `data-1.txt` and `clues-1.txt` and display the solution.  
The solution rows must be **sorted by the numeric values (first column)** in ascending order.  
The column order must follow the order in the data file.

### Example Run

```
The problems available in this directory: 1 2 3  
Choose a problem: 1  

Here is the solution to the problem defined in data-1.txt and clues-1.txt.  

years | owners  | breeds     | dogs  
-------------------------------------  
2006  | Douglas | greatDane  | Shadow  
2007  | Fernando| pekingese  | Harley  
2008  | Anita   | dalmatian  | Molly  
2009  | Barbara | bulldog    | Riley
```

You are free to modify the UI as long as functionality stays the same.  
**Do not use absolute paths**.  
**Use only Python Standard Library** — No third-party modules.  
Your code will be tested on **Linux**.

---

## Appendix

### Example 1

**data-1.txt**
```
years,2006,2007,2008,2009  
owners,Anita,Barbara,Douglas,Fernando  
breeds,bulldog,dalmatian,greatDane,pekingese  
dogs,Harley,Molly,Riley,Shadow
```

**clues-1.txt**
```
if breeds=greatDane then years=2006  
years(owners=Barbara) = years(breeds=pekingese) + 2  
years(dogs=Molly) = years(breeds=pekingese) + 1  
years(dogs=Riley) > years(dogs=Harley)  
if owners=Douglas then not dogs=Harley  
years(owners=Anita) = years(dogs=Shadow) + 2  
if dogs=Riley then either owners=Douglas or breeds=bulldog
```

**Solution**
```
years | owners  | breeds     | dogs  
-------------------------------------  
2006  | Douglas | greatDane  | Shadow  
2007  | Fernando| pekingese  | Harley  
2008  | Anita   | dalmatian  | Molly  
2009  | Barbara | bulldog    | Riley
```

---

### Example 2

**data-2.txt**
```
years,2005,2006,2007,2008  
players,Delbert,Lonnie,Perry,Steven  
teams,Dodgers,Indians,Pirates,Tigers  
hometowns,ChulaVista,Quimby,Ravendale,York
```

**clues-2.txt**
```
years(hometowns=ChulaVista) = years(teams=Indians) - 1  
if teams=Tigers then not players=Steven  
if hometowns=Quimby then not players=Steven  
if teams=Tigers then not hometowns=Quimby  
years(hometowns=York) = years(players=Steven) + 1  
if years=2008 then hometowns=Quimby  
years(hometowns=Ravendale) > years(players=Lonnie)  
if hometowns=Ravendale then either teams=Tigers or players=Delbert  
one of {players=Lonnie,players=Steven} corresponds to years=2006 other teams=Dodgers
```

**Solution**
```
years | players | teams   | hometowns  
--------------------------------------  
2005  | Steven  | Dodgers | ChulaVista  
2006  | Lonnie  | Indians | York  
2007  | Perry   | Tigers  | Ravendale  
2008  | Delbert | Pirates | Quimby
```

---

### Example 3

**data-3.txt**
```
days,270,274,278,282  
sailors,DebraDecker,TaraCarroll,VickyEstes,WendellOrr  
boatTypes,catamaran,pilotCutter,schooner,sloop  
boats,AlphaOne,BayHawk,Confluence,WaveDancer
```

**clues-3.txt**
```
if sailors=WendellOrr then boatTypes=pilotCutter  
days(boats=BayHawk) = days(boatTypes=pilotCutter) - 4  
{boats=AlphaOne,sailors=VickyEstes,sailors=TaraCarroll} are all different  
{days=282,sailors=VickyEstes,boatTypes=pilotCutter} are all different  
days(boatTypes=catamaran) = days(boats=WaveDancer) - 4  
one of {sailors=DebraDecker,days=270} corresponds to boats=BayHawk other boatTypes=schooner  
if boatTypes=sloop then either days=282 or boats=AlphaOne
```

**Solution**
```
days | sailors      | boatTypes   | boats  
---------------------------------------------  
270  | VickyEstes   | catamaran   | BayHawk  
274  | WendellOrr   | pilotCutter | WaveDancer  
278  | DebraDecker  | schooner    | AlphaOne  
282  | TaraCarroll  | sloop       | Confluence
```
