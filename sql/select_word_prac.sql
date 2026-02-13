-- Active: 1769143105802@@127.0.0.1@5432@world@public

SELECT * FROM city;
SELECT * FROM country WHERE continent='Asia';
SELECT * FROM countrylanguage;



-- - 인구가 800만 이상인 도시의 name, population을 조회하시오
SELECT name, population FROM country WHERE population >= 8000000;

-- - 한국(KOR)에 있는 도시의 name, countrycode를 조회하시오
SELECT name, countrycode FROM city WHERE countrycode = 'KOR';

-- - 유럽 대륙에 속한 나라들의 name과 region을 조회하시오.
select name, region from country WHERE continent ='Europe';
-- - 이름이 'San'으로 시작하는 도시의 name을 조회하시오
SELECT name FROM country WHERE name LIKE 'San%' 

-- - 독립 연도(IndepYear)가 1900년 이후인 나라의 name, indepyear를 조회하시오.
select name, indepyear from country where indepyear >= 1900;

-- - 인구가 100만에서 200만 사이인 한국 도시의 name을 조회하시오
SELECT name, population from city where countrycode='KOR' AND (population >= 1000000 OR population <= 2000000);
-- - 인구가 500만 이상인 한국, 일본, 중국의 도시의 name, countrycode, population 을 조회하시오
SELECT name, countrycode, population from city 
where (countrycode='KOR' OR countrycode='JPN' OR countrycode='CHN') AND population >=5000000;
-- - 도시 이름이 'A'로 시작하고 'a'로 끝나는 도시의 name을 조회하시오.
select name from city where name ILIKE 'A%a'; 

-- - 동남아시아(Southeast Asia) 지역(Region)에 속하지 않는 아시아(Asia) 대륙 나라들의 name, region을 조회하시오.

SELECT name, region from country where (region != 'Southeast Asia' AND region ILIKE '%asia');

-- - 오세아니아 대륙에서 예상 수명의 데이터가 없는 나라의 name, lifeexpectancy, continent를 조회하시오.
SELECT name, lifeexpectancy, continent FROM country WHERE LifeExpectancy IS NULL;



SELECT * FROM country

-- group by
-- - 대륙별 총 인구수를 구하시오.
-- SELECT * FROM country
select continent, sum(population) as continent_population
FROM country GROUP BY continent

-- - 대륙별 평균 GNP와 평균 인구를 구하시오.
select continent, avg(gnp) as gnp_avg, avg(population) as pop_avg
FROM country GROUP BY continent


-- - 인구가 50만에서 100만 사이인 도시들에 대해, District별 도시 수를 구하시오.
SELECT * FROM city

SELECT district, count(*)
FROM city
WHERE population >= 500000 and population <= 1000000
GROUP BY district

-- - 아시아 대륙 국가들의 Region별 총 GNP를 구하세요.
SELECT region, sum(gnp) as region_gnp
FROM country
WHERE continent LIKE 'Asia'
GROUP BY region

-- - GNP가 가장 높은 Region를 찾으시오.(GNP : 국민 총 생산)
SELECT region, max(gnp) as high_gnp
FROM country
GROUP BY region
ORDER BY high_gnp DESC
LIMIT 1;


SELECT * FROM city

SELECT * FROM country
-- - 각 국가별 도시가 10개 이상인 국가의 CountryCode, 도시 수를 조회하시오.

select countrycode, count(*)
FROM city
GROUP BY countrycode
HAVING count(*) >= 10;


-- - District별 평균 인구가 100만 이상이면서 도시 수가 3개 이상인 District,  도시 수, 총 인구를 구하시오
select district, count(*), sum(population)
from city
GROUP BY district
HAVING count(*)>=3 and (sum(population)/count(*))>=1000000

-- - 아시아 대륙의 국가들 중에서, Region별 평균 GNP가 1000 이상인 Region,  평균 GNP를 조회하시오
select region, avg(gnp) as gnp_avg
from country
WHERE continent LIKE 'Asia'
GROUP BY region
HAVING avg(gnp)>=1000

-- - 독립년도가 1900년 이후인 국가들 중에서, 대륙별 평균 기대수명이 70세 이상인 Continent, 평균 기대수명을 조회하시오.
select continent, avg(lifeexpectancy)
from country
where indepyear >= 1900
GROUP BY continent 
HAVING avg(lifeexpectancy)>-70


-- - 도시 평균 인구가 100만 이상이고, 도시 최소 인구가 50만 이상인 국가의 countrycode, 총 도시수, 총 인구수를 조회하시오.
SELECT countrycode, count(*), sum(population)
from city
GROUP BY countrycode
HAVING avg(population)>=1000000 and min(population) >= 500000

-- - 인구가 50만 이상인 city들의 평균 인구가 100만 이상 인 국가의 CountryCode, 총 도시수, 총 인구수를 조회하시오.
SELECT countrycode, count(*), sum(population)
from city
WHERE population >= 500000
GROUP BY countrycode
HAVING avg(population)>=1000000
