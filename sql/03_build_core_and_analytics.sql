-- Customers
DROP TABLE IF EXISTS core.customers;
CREATE TABLE core.customers AS
SELECT
    customer_id,
    gender,
    senior_citizen,
    partner,
    dependents,
    tenure
FROM staging.telco_raw;

ALTER TABLE core.customers ADD PRIMARY KEY (customer_id);

-- Services
DROP TABLE IF EXISTS core.services;
CREATE TABLE core.services AS
SELECT
    customer_id,
    phone_service,
    multiple_lines,
    internet_service,
    online_security,
    online_backup,
    device_protection,
    tech_support,
    streaming_tv,
    streaming_movies
FROM staging.telco_raw;

ALTER TABLE core.services ADD PRIMARY KEY (customer_id);

-- Billing
DROP TABLE IF EXISTS core.billing;
CREATE TABLE core.billing AS 
SELECT
    customer_id,
    contract,
    paperless_billing,
    payment_method,
    monthly_charges,
    NULLIF(BTRIM(total_charges), '')::numeric AS total_charges
FROM staging.telco_raw;

ALTER TABLE core.billing ADD PRIMARY KEY (customer_id);

-- Labels
DROP TABLE IF EXISTS core.churn_labels;
CREATE TABLE core.churn_labels AS
SELECT
    customer_id,
    CASE WHEN churn ILIKE 'Yes' THEN 1 ELSE 0 END AS churn
FROM staging.telco_raw;

ALTER TABLE core.churn_labels ADD PRIMARY KEY (customer_id);

-- Feature view
CREATE OR REPLACE VIEW analytics.churn_features_v1 AS
SELECT
    c.customer_id,
    c.gender, c.senior_citizen, c.partner, c.dependents, c.tenure,
    s.phone_service, s.multiple_lines, s.internet_service, s.online_security,
    s.online_backup, s.device_protection, s.tech_support, s.streaming_tv, s.streaming_movies,
    b.contract, b.paperless_billing, b.payment_method, b.monthly_charges, b.total_charges,
    y.churn
FROM core.customers c
JOIN core.services s USING (customer_id)
JOIN core.billing b USING (customer_id)
JOIN core.churn_labels y USING (customer_id);