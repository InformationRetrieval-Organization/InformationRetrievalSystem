--first third
SELECT * 
FROM public."Post" as p
INNER JOIN public."Processed_Post" as pp ON pp.id = p.id
ORDER BY p.id ASC 
LIMIT (
    SELECT COUNT(*) / 3 
    FROM public."Processed_Post"
);


--second third
SELECT * 
FROM public."Post" as p
INNER JOIN public."Processed_Post" as pp ON pp.id = p.id
ORDER BY p.id ASC 
OFFSET (
    SELECT COUNT(*) / 3 
    FROM public."Processed_Post"
)
LIMIT (
    SELECT COUNT(*) / 3 
    FROM public."Processed_Post"
);

--third third
SELECT * 
FROM public."Post" as p
INNER JOIN public."Processed_Post" as pp ON pp.id = p.id
ORDER BY p.id ASC 
OFFSET (
    SELECT COUNT(*) / 3 * 2
    FROM public."Processed_Post"
);