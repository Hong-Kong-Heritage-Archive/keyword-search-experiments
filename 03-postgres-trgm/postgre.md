# Notes

Make use of this feature to search for books https://www.postgresql.org/docs/current/pgtrgm.html

This assumes you have a running Postgre server

# Calculation of "similarity"

For "apple" and "aple", there are 4 common trigrams and 7 unique trigrams, hence 4/7 = 0.571


```
postgres=# SELECT show_trgm('aple');
SELECT show_trgm('aple');
          show_trgm          
-----------------------------
 {"  a"," ap",apl,"le ",ple}
(1 row)

postgres=# SELECT show_trgm('apple');
SELECT show_trgm('apple');
            show_trgm            
---------------------------------
 {"  a"," ap",app,"le ",ple,ppl}
(1 row)

postgres=# SELECT similarity('apple', 'aple');
SELECT similarity('apple', 'aple');
 similarity 
------------
  0.5714286
(1 row)
```