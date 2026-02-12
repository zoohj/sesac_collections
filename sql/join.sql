-- Active: 1769143105802@@127.0.0.1@5432@world@public

SELECT * FROM city

SELECT * FROM country

-- 어느 나라에 속한 도시인지
select co.name AS country_name,
ci.name AS capital_city
from city ci
JOIN country co ON ci.countrycode = co.code

-- 국가와 그 국가의 공식 수도를 매칭
select * from country

select co.name AS country, ci.name AS capital_name from country co JOIN city ci ON co.capital = ci.id 

-- 특정 대륙에 속한 도시들 목록
SELECT co.continent, co.name As country_name, ci.name AS city_name
from country co
join city ci ON co.code = ci.countrycode
WHERE co.continent = 'Asia'
ORDER BY co.name, ci.name;

