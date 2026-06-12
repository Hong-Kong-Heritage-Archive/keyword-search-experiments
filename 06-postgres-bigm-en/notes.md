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
Data imported from books.csv.

--- Set Similarity Limit ---

--- Execution Plan ---
Seq Scan on books  (cost=0.00..21.00 rows=1 width=68)
  Filter: (title =% 'Harry Potter'::text)

--- Search Results ---
Searching for titles matching: 'Harry Potter'...
Score: 0.30952382 - Found: ISBN 439554934 - Title: Harry Potter and the Sorcerer's Stone (Harry Potter, #1)
Score: 0.2 - Found: ISBN 1594480001 - Title: The Kite Runner
Score: 0.2888889 - Found: ISBN 043965548X - Title: Harry Potter and the Prisoner of Azkaban (Harry Potter, #3)
Score: 0.30232558 - Found: ISBN 439358078 - Title: Harry Potter and the Order of the Phoenix (Harry Potter, #5)
Score: 0.2826087 - Found: ISBN 439064864 - Title: Harry Potter and the Chamber of Secrets (Harry Potter, #2)
Score: 0.30232558 - Found: ISBN 439139600 - Title: Harry Potter and the Goblet of Fire (Harry Potter, #4)
Score: 0.31707317 - Found: ISBN 545010225 - Title: Harry Potter and the Deathly Hallows (Harry Potter, #7)
Score: 0.30952382 - Found: ISBN 439785960 - Title: Harry Potter and the Half-Blood Prince (Harry Potter, #6)
Score: 0.25 - Found: ISBN 64410935 - Title: Charlotte's Web
Score: 0.22222222 - Found: ISBN 743454537 - Title: My Sister's Keeper
Score: 0.23076923 - Found: ISBN 014241493X - Title: Paper Towns

--- Execution Plan with LIKE ---
Seq Scan on books  (cost=0.00..21.00 rows=1 width=68)
  Filter: (title ~~ '%Harry Potter%'::text)

--- Search Results with LIKE ---
Searching for titles matching: 'Harry Potter'...
Score: 0.30952382 - Found: ISBN 439554934 - Title: Harry Potter and the Sorcerer's Stone (Harry Potter, #1)
Score: 0.2888889 - Found: ISBN 043965548X - Title: Harry Potter and the Prisoner of Azkaban (Harry Potter, #3)
Score: 0.30232558 - Found: ISBN 439358078 - Title: Harry Potter and the Order of the Phoenix (Harry Potter, #5)
Score: 0.2826087 - Found: ISBN 439064864 - Title: Harry Potter and the Chamber of Secrets (Harry Potter, #2)
Score: 0.30232558 - Found: ISBN 439139600 - Title: Harry Potter and the Goblet of Fire (Harry Potter, #4)
Score: 0.31707317 - Found: ISBN 545010225 - Title: Harry Potter and the Deathly Hallows (Harry Potter, #7)
Score: 0.30952382 - Found: ISBN 439785960 - Title: Harry Potter and the Half-Blood Prince (Harry Potter, #6)

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