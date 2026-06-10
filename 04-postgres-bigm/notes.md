# Initial Prompt

Write a python script such that does the following:
- It connects to a PostgreSQL instance.
- It creates a table called books with columns isbn and title if it does not exist.
- It imports a CSV file containing multiple columns, which include isbn and title.
- Create a GIN index on title.
- It makes use of the pg_bigm module to search for books with title matching specified string.
- Make postgresql explain the execution plan of the previous search.
- It deletes the table books.

The following are the input.
- The IP address, user account and password of the PostreSQL instance.
- The name of the CSV file.
- The string to perform the search.


# Manual Changes

Manual changes
- make SSL mandatory
- Fine tune or change search function.

# Output Results

```
Extension 'pg_bigm' ensured.
Table 'books' ensured.
GIN index on 'title' ensured.
Data imported from traditional.csv.

--- Execution Plan ---
Seq Scan on books  (cost=0.00..21.00 rows=1 width=68)
  Filter: (title =% '哈利波特'::text)

--- Search Results ---
Searching for titles matching: '哈利波特'...
Score: 0.23529412 - Found: ISBN 439554934 - Title: 哈利波特與魔法石 (哈利波特, #1)
Score: 0.2 - Found: ISBN 618260307 - Title: 哈比人
Score: 0.1904762 - Found: ISBN 043965548X - Title: 哈利波特與阿茲卡班的囚徒 (哈利波特, #3)
Score: 0.2 - Found: ISBN 439358078 - Title: 哈利波特與鳳凰會的密令 (哈利波特, #5)
Score: 0.25 - Found: ISBN 439064864 - Title: 哈利波特與密室 (哈利波特, #2)
Score: 0.23529412 - Found: ISBN 439139600 - Title: 哈利波特與火焰盃 (哈利波特, #4)
Score: 0.21052632 - Found: ISBN 545010225 - Title: 哈利波特與死神的聖物 (哈利波特, #7)
Score: 0.22222222 - Found: ISBN 439785960 - Title: 哈利波特與混血王子 (哈利波特, #6)
Score: 0.09090909 - Found: ISBN 142437174 - Title: 哈克貝利·芬恩的冒險

Table 'books' deleted successfully.
Connection closed.
```

# Bigm similarity calculations

Sensitivity can be fine tuned.

Similarity should be based on
= number of similar bigram / total number of bigrams.

However the number does not match.

Checking the source code of pg_bigm, if the constant DIVUNION is not defined, then the following formula is used:
c / max(len1, len2)

The results matches with the latter case

```
postgres=> select bigm_similarity('哈', '哈利波特');
 bigm_similarity 
-----------------
             0.2
(1 row)

postgres=> select show_bigm('哈');
   show_bigm   
---------------
 {" 哈","哈 "}
(1 row)

postgres=> select show_bigm('哈利波特');
          show_bigm           
------------------------------
 {" 哈",利波,哈利,波特,"特 "}
(1 row)
```


Furthermore
```
postgres=> select bigm_similarity('哈利', '哈利波特');
 bigm_similarity 
-----------------
             0.4
(1 row)


postgres=> select show_bigm('哈利');
     show_bigm      
--------------------
 {" 哈","利 ",哈利}
(1 row)
```

Probably is calculated by:
size ( {" 哈",哈利} ) / size({" 哈",利波,哈利,波特,"特 "}) 



Let us test with 哈比人.
```
postgres=> select bigm_similarity('哈比人', '哈利波特');
 bigm_similarity 
-----------------
             0.2
(1 row)


postgres=> select show_bigm('哈比人');
        show_bigm        
-------------------------
 {" 哈","人 ",哈比,比人}
(1 row)
```

# Limitations

If the title is very long, and you have not input long enough keywords, the similarity may be low.

Short titles may have a high similarity score with your search string.