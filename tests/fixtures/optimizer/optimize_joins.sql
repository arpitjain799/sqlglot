SELECT * FROM x JOIN y ON y.a = 1 JOIN z ON x.a = z.a AND y.a = z.a;
SELECT * FROM x JOIN z ON x.a = z.a AND TRUE JOIN y ON y.a = 1 AND y.a = z.a;

SELECT * FROM x JOIN y ON y.a = 1 JOIN z ON x.a = z.a;
SELECT * FROM x JOIN y ON y.a = 1 JOIN z ON x.a = z.a;

SELECT * FROM x CROSS JOIN y JOIN z ON x.a = z.a AND y.a = z.a;
SELECT * FROM x JOIN z ON x.a = z.a AND TRUE JOIN y ON y.a = z.a;

SELECT * FROM x LEFT JOIN y ON y.a = 1 JOIN z ON x.a = z.a AND y.a = z.a;
SELECT * FROM x JOIN z ON x.a = z.a AND TRUE LEFT JOIN y ON y.a = 1 AND y.a = z.a;

SELECT * FROM x INNER JOIN z;
SELECT * FROM x JOIN z;

SELECT * FROM x LEFT OUTER JOIN z;
SELECT * FROM x LEFT JOIN z;

SELECT * FROM x CROSS JOIN z;
SELECT * FROM x CROSS JOIN z;
