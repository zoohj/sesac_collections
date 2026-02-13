-- 1. 배우가 출연한 영화의 제목을 조회
SELECT ac.first_name, fi.title
FROM actor ac
LEFT JOIN film_actor fa ON fa.actor_id= ac.actor_id
LEFT JOIN film fi ON fi.film_id = fa.film_id

SELECT * FROM actor
    
-- 2. first_name이 `PENELOPE` 인 배우가 출연한 영화의 제목을 조회
SELECT ac.first_name, fi.title
FROM actor ac
LEFT JOIN film_actor fa ON fa.actor_id= ac.actor_id
LEFT JOIN film fi ON fi.film_id = fa.film_id
WHERE ac.first_name ILIKE 'PENELOPE'
    
-- 3. 영화 별 출연 배우의 수를 조회
SELECT fi.title, count(fa.actor_id) AS actor_count
FROM film fi
LEFT JOIN film_actor fa ON fa.film_id= fi.film_id
GROUP BY fi.film_id
    
    
-- 4. 영화 별 출연 배우의 수가 5가 넘는 데이터를 배우의 수가 큰순으로 조회
SELECT fi.title, count(fa.actor_id) AS actor_count
FROM film fi
LEFT JOIN film_actor fa ON fa.film_id= fi.film_id
GROUP BY fi.film_id
HAVING count(fa.actor_id) > 5
ORDER BY actor_count DESC

-- 5. 고객의 대여 정보 조회
SELECT * FROM rental
SELECT * FROM inventory

SELECT cu.last_name AS customer_name, re.rental_id, fi.title AS rental_film
FROM customer cu 
LEFT JOIN rental re ON re.customer_id = cu.customer_id
LEFT JOIN inventory inv ON inv.inventory_id = re.inventory_id
LEFT JOIN film fi ON inv.film_id = fi.film_id


-- 6. 고객이 대여한 영화 정보 조회(위에)

-- 7. `YENTL IDAHO` 영화를 대여한 고객 정보 조회

SELECT cu.last_name AS customer_name, fi.title AS rental_film
FROM customer cu 
LEFT JOIN rental re ON re.customer_id = cu.customer_id
LEFT JOIN inventory inv ON inv.inventory_id = re.inventory_id
LEFT JOIN film fi ON inv.film_id = fi.film_id
WHERE fi.title ILIKE 'YENTL IDAHO'

-- 8. 배우별로 출연한 영화의 등급(rating)을 조회
SELECT ac.first_name, fi.title, fi.rating
FROM actor ac
LEFT JOIN film_actor fa ON fa.actor_id= ac.actor_id
LEFT JOIN film fi ON fi.film_id = fa.film_id
ORDER BY ac.actor_id

-- 9. 1번 고객이 자주 대여한 영화의 카테고리를 찾으시오
select cu.customer_id, count(ca.category_id) AS category_count, ca.name AS category_name
FROM customer cu 
JOIN rental re ON re.customer_id = cu.customer_id
JOIN inventory inv ON inv.inventory_id = re.inventory_id
JOIN film fi ON fi.film_id = inv.film_id
JOIN film_category fc ON fc.film_id = fi.film_id
JOIN category ca ON fc.category_id = ca.category_id
WHERE cu.customer_id = 1
GROUP BY cu.customer_id, ca.category_id, ca.name
ORDER BY category_count DESC
LIMIT 1

-- 10. 각 직원이 일하는 매장의 주소와 도시를 조회
SELECT * FROM address

SELECT st.first_name, ad.address, ci.city
FROM staff st
LEFT JOIN store ON st.store_id = store.store_id
LEFT JOIN address ad ON store.address_id = ad.address_id
JOIN city ci ON ad.city_id = ci.city_id

-- 11. 고객별로 대여한 영화 제목과 지불한 금액, 날짜를 조회
SELECT cu.customer_id, fi.title AS film_title, pa.amount, pa.payment_date
FROM customer cu 
JOIN rental re ON re.customer_id = cu.customer_id
JOIN inventory inv ON inv.inventory_id = re.inventory_id
JOIN film fi ON fi.film_id = inv.film_id -- 영화제목 가져오기위해서
JOIN payment pa ON re.rental_id=pa.rental_id -- pa.amount로 지불 금액, pa.payment_date로 날짜
ORDER BY customer_id

-- 12. 국가별 고객 수를 조회
SELECT co.country, count(cu.customer_id)
FROM customer cu 
JOIN address ad ON cu.address_id = ad.address_id
JOIN city ci ON ci.city_id = ad.city_id
JOIN country co ON ci.country_id = co.country_id
GROUP BY co.country_id

-- 13. `Action` 카테고리에 출연한 배우 조회
SELECT ac.first_name AS actor_name , fi.title AS movie_title,
ca.name AS category
FROM actor ac
JOIN film_actor fa ON fa.actor_id= ac.actor_id
JOIN film fi ON fi.film_id = fa.film_id
JOIN film_category fc ON fc.film_id = fi.film_id
JOIN category ca ON fc.category_id=ca.category_id
WHERE ca.name ILIKE 'action'
ORDER BY ac.actor_id


-- 14. 재고(inventory)가 없는 영화 찾기
select fi.title, inventory_id
from film fi 
left join inventory inv ON fi.film_id = inv.film_id
WHERE inventory_id is NULL

-- 15. 카테고리별 평균 대여료
SELECT ca.name AS category_name, avg(pa.amount)
FROM rental re
JOIN inventory inv ON inv.inventory_id = re.inventory_id
JOIN film fi ON fi.film_id = inv.film_id -- 영화제목 가져오기위해서
JOIN film_category fc ON fc.film_id = fi.film_id
JOIN category ca ON fc.category_id = ca.category_id
JOIN payment pa ON re.rental_id=pa.rental_id -- pa.amount로 지불 금액, pa.payment_date로 날짜
GROUP BY ca.category_id