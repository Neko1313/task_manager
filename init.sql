CREATE TABLE AccessDates (
    id SERIAL PRIMARY KEY,
    chart BYTEA NOT NULL,
    access_date TIMESTAMP NOT NULL
);