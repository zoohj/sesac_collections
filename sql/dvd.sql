-- Active: 1769143105802@@127.0.0.1@5432@dvdrental@public
select * FROM film
-- 1. 모든 영화의 제목과 대여료를 조회하시오.

SELECT title, rental_rate from film;

-- 2. 대여료가 4달러 이상인 영화의 제목과 대여료를 조회하시오.
SELECT title, rental_rate from film where rental_rate >=4;

-- 3. 등급별 영화 수를 조회하시오.
SELECT rating, count(*) from film GROUP BY rating;

-- 4. 상영 시간을 중복 제거하여 내림차순으로 정렬하고, 상위 10개를 조회하시오.
select distinct length from film ORDER BY length DESC LIMIT 10; 

-- 5. 대여 기간별 영화 수를 대여 기간 내림차순으로 정렬하여 조회하시오.
select rental_duration, count(rental_duration)from film 
GROUP BY rental_duration
ORDER BY rental_duration desc


-- 6. 대여 기간이 5일 이상이고 대여료가 4달러 이상인 영화의 제목, 대여 기간, 대여료를 조회하시오.
select title, rental_duration, rental_rate from film
WHERE rental_duration >= 5 and rental_rate >= 4

-- 7. 등급이 'R'인 영화 중 처음 10개의 제목과 등급을 조회하시오.
select title, rating from film
WHERE rating = 'R'
LIMIT 10

-- 8. 대여료별 영화 수를 영화 수 내림차순으로 정렬하여 조회하시오.
SELECT rental_rate, count(*)
from film GROUP BY rental_rate
ORDER BY count(*) DESC

-- 9. 교체 비용별 영화 수와 평균 대여료를 교체 비용 오름차순으로 정렬하여 조회하시오.
select count(*), avg(rental_rate)
from film
GROUP BY replacement_cost
ORDER BY replacement_cost desc

-- 10. 제목에 'angel'이 포함된 영화의 제목을 조회하시오.
SELECT title from film WHERE title ILIKE '%angel%'


-- 11. 등급별 평균 대여료가 3달러 미만인 등급과 평균 대여료를 조회하시오.
SELECT rating, avg(rental_rate)
from film
GROUP BY rating 
HAVING avg(rental_rate) < 3

-- 12. 상영 시간이 10번째에서 15번째로 긴 영화의 제목과 상영 시간을 조회하시오. (상영 시간이 같을 경우 제목 오름차순으로 정렬)
select title, length from film ORDER BY length desc, title LIMIT 6  OFFSET 9;

-- 13. 등급이 'PG' 또는 'G'이면서 대여 기간이 4일 이하인 영화의 제목, 등급, 대여 기간을 조회하시오.
select title, rating, rental_duration from film where (rating = 'PG' OR rating = 'G') AND rental_duration <= 4

-- 14. 등급별 영화 수와 평균 상영 시간을 조회하시오.
select count(*), avg(length) as avg_length from film GROUP BY rating

-- 15. 상영 시간이 60분 이상 120분 이하인 영화의 제목과 상영 시간을 상영 시간 오름차순으로 조회하시오.
select title, length from film where length >= 60 and length <=120 ORDER BY length 


#join 실습
SELECT * FROM customer

SELECT * FROM address

SELECT * FROM country

--고객의 이름, 이메일 조회
select cu.first_name, cu.last_name, cu.email, ad.address FROM customer cu LEFT JOIN address ad ON cu.address_id=ad.address_id

-- 고객의 이름, 이메일, 주소, 도시 조회
select cu.first_name, cu.last_name, cu.email, ad.address FROM customer cu 
LEFT JOIN address ad ON cu.address_id=ad.address_id
LEFT JOIN city ci ON ad.city_id = ci.city_id

-- London(city)에 사는 고객의 이름, 이메일, 주소, 도시 조회
select cu.first_name, cu.email, ad.address, ci.city FROM customer cu 
LEFT JOIN address ad ON cu.address_id=ad.address_id
LEFT JOIN city ci ON ad.city_id = ci.city_id
WHERE ci.city = 'London'

-- 도시별 고객 수 조회
select ci.city,  count(*)
FROM customer cu 
LEFT JOIN address ad ON cu.address_id=ad.address_id
LEFT JOIN city ci ON ad.city_id = ci.city_id
GROUP BY ci.city 
ORDER BY COUNT(*) DESC

# 배우 - 영화 정보
select * FROM film

SELECT * FROM film_actor

SELECT * FROM actor

-- 배우가 출연한 영화 조회
SELECT ac.first_name, fi.title
FROM actor ac
LEFT JOIN film_actor fa ON fa.actor_id= ac.actor_id
LEFT JOIN film fi ON fi.film_id = fa.film_id

-- 배우별 출연 영화 수
SELECT ac.actor_id, count(*)
FROM actor ac
LEFT JOIN film_actor fa ON fa.actor_id= ac.actor_id
GROUP BY ac.actor_id

-- 영화 별 출연 배우 수
SELECT fi.title, count(fa.actor_id) AS actor_count
FROM film fi
LEFT JOIN film_actor fa ON fa.film_id= fi.film_id
GROUP BY fi.film_id

-- 영화의 카테고리 정보
SELECT * FROM category

SELECT * FROM film_category

-- 영화의 카테고리 정보
SELECT fi.title AS film_title, ca.name AS category
FROM film fi
JOIN film_category fc ON fc.film_id = fi.film_id
JOIN category ca ON fc.category_id=ca.category_id


-- - 카테고리 별 영화 수
SELECT ca.name AS category, COUNT(fi.film_id)
FROM film fi
JOIN film_category fc ON fc.film_id = fi.film_id
JOIN category ca ON fc.category_id=ca.category_id
GROUP BY ca.category_id    

-- - 배우가 출연한 영화를 카테고리를 포함하여 조회
SELECT ac.first_name AS actor_name , fi.title AS movie_title,
ca.name AS category
FROM actor ac
LEFT JOIN film_actor fa ON fa.actor_id= ac.actor_id
LEFT JOIN film fi ON fi.film_id = fa.film_id
JOIN film_category fc ON fc.film_id = fi.film_id
JOIN category ca ON fc.category_id=ca.category_id
ORDER BY ac.actor_id
