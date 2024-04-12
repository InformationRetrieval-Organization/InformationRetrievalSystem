/*
 - This script performs a search through the title and content of posts with the given queries. 
 - It only uses the posts that came through the preprocessing, so are inserted in processed_post. 
 - The output is the search term (query) and the count of posts that matched all words in the query.

 NOTE: its not a replacement for a manually search
 */
-- Define search queries as an array variable and split the query into individual words
WITH search_terms AS (
    SELECT
        UNNEST(
            ARRAY ['election', 'korea election', 'parties', 'president parties']
        ) AS query
),
word_list AS (
    SELECT
        query,
        unnest(string_to_array(query, ' ')) AS word
    FROM
        search_terms
),
posts AS (
    SELECT
        p.id,
        p.title || ' ' || p.content as text
    FROM
        public."Post" p
        INNER JOIN public."Processed_Post" pp ON p.id = pp.id
) -- Execute search query and return matching document IDs
SELECT
    DISTINCT wl.query AS query,
    p.id AS document_id
FROM
    posts p,
    word_list wl
WHERE
    wl.query IN (
        SELECT
            query
        FROM
            word_list wl2
        WHERE
            p.text ILIKE '%' || wl2.word || '%'
        GROUP BY
            query
        HAVING
            COUNT(*) = (
                SELECT
                    COUNT(*)
                FROM
                    word_list
                WHERE
                    query = wl.query
            )
    )
ORDER BY
    wl.query,
    p.id;