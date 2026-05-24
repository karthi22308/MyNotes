-- ROW_NUMBER()

--👉 Assign unique sequence numbers.

SELECT Name, Salary,
       ROW_NUMBER() OVER (order by Salary ) AS RowNum
FROM Employee 


SELECT Name, DeptId, Salary,
       ROW_NUMBER() OVER (PARTITION BY DeptId ORDER BY Salary DESC) AS DeptRow
FROM Employee;


-------------------------------------------------------

--RANK()

--👉 Ties get the same rank, skips numbers.


SELECT Name, Salary,
       RANK() OVER (ORDER BY Salary DESC) AS SalaryRank
FROM Employee;


SELECT Name, DeptId, Salary,
       RANK() OVER (PARTITION BY DeptId ORDER BY Salary DESC) AS DeptRank
FROM Employee;
----------------------------------------------------
--DENSE_RANK()

--👉 Ties get same rank, no skips.----
SELECT  Salary,
       DENSE_RANK() OVER (ORDER BY Salary DESC) AS DenseRank
FROM Employee;


WITH Ranked AS (
    SELECT Name, DeptId, Salary,
           DENSE_RANK() OVER (ORDER BY Salary DESC) AS rnk
    FROM Employee
)
SELECT * FROM Ranked WHERE rnk = 2;




------------------


SELECT EmpId, SaleMonth, Amount,
       FIRST_VALUE(Amount) OVER (ORDER BY SaleMonth) AS FirstSale
FROM Sales;



SELECT 
    (
        SELECT DISTINCT Salary
        FROM Employee 
        ORDER BY Salary DESC
        OFFSET 1 ROW FETCH NEXT 1 ROW ONLY
    ) AS SecondHighestSalary;

	---------------------------------------------------
	SELECT DeptId, SUM(Salary) AS TotalSalary
FROM Employee
GROUP BY DeptId;

