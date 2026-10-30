=============
Query 1: Dados extraídos por consulta SQL já com a remoção de linhas cujo apresentaram células da coluna Department_ID nulo.
#Link do SQL:https://freesql.com/?compressed_code=H4sIAAAAAAAACoWSQW7bMBBF9wJ0h99VNmYKZNnCC0YaxywkMiXpFF4ZtMS2AmzTkGWg7R16ii66yil0sYKxYVnJooBAiI%252BY%252F4d%252FyBgTUpLGJyXkB1h%252BTwU3yAlPJHNuJsgKQdKSAeGR978NmTRJE0MFZTZNAMDdZgtjVyKfjPYzoY1dSV7SmD%252BQzEkPTC2k1cuhvLqgl1qMijNhl5M35I33Ey8uaH37qFW%252Butpncy4lFdfo84JLG5WMKgbKy9jJmFlR0krkaTLTqoSZvxiqkrSBS5MhzHhkeEEG6%252FMVlByiwjT2cf5nLH4z9wsOm%252Bab6%252F%252F2fwKqsIVD59Z%252B41B7iDyu1abxu84fXludMhNkUI3sLuliepXsyfR%252FjnvXPx%252Bi1Zc5aXo1GExx8%252BDbrdv9vGEMRbNtunCE%252F9G1Z7m9ax1qV4dDFDtuT3rwh72v%252BuevTRXShMt8NBC8m%252BIu9qZ917ThiIDK7dwm3v4OtbvWr%252F1JPb5HpXPSuF8OAwI32Ucwptra78IR%252B9Cidp17%252Fz20jjFS2T8PKC2b%252FAIAAA%253D%253D&code_language=PL_SQL&db_version=26&code_format=false
=============

---INNER JOIN: TABELAS DE VENDAS, CLIENTES E PAÍSES

SELECT
    a.CUST_ID,
    a.CUST_FIRST_NAME,
    a.CUST_GENDER,
    a.COUNTRY_ID,
    c.COUNTRY_NAME, 
    a.CUST_CITY,
    a.CUST_CITY_ID,
    a.CUST_VALID,
    b.PROD_ID,
    b.CHANNEL_ID,
    b.QUANTITY_SOLD,
    b.AMOUNT_SOLD,
    b.TIME_ID
FROM SH.CUSTOMERS a
INNER JOIN SH.SALES b 
    ON a.CUST_ID = b.CUST_ID -- -- Faz a ligação com a tabela de ID de clientes
INNER JOIN SH.COUNTRIES c 
    ON a.COUNTRY_ID = c.COUNTRY_ID -- Faz a ligação com a tabela de países
WHERE c.COUNTRY_NAME = 'Germany'-- Limitou extração para dados de um país específico
AND b.CHANNEL_ID != 2 -- Retirou o canal ID 2 da extração de dados

ORDER BY b.TIME_ID ASC; --Ordenou por data/hora 






