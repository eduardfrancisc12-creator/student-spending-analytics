-- Schema for the student spending analytics database.
DROP TABLE IF EXISTS spending;

CREATE TABLE spending (
    student_id           INTEGER PRIMARY KEY,
    age                  INTEGER NOT NULL,
    gender               TEXT NOT NULL,
    year_in_school        INTEGER NOT NULL,
    major                TEXT NOT NULL,
    monthly_income       REAL NOT NULL,
    financial_aid        REAL NOT NULL,
    tuition              REAL NOT NULL,
    housing              REAL NOT NULL,
    food                 REAL NOT NULL,
    transportation       REAL NOT NULL,
    books_supplies       REAL NOT NULL,
    entertainment        REAL NOT NULL,
    personal_care        REAL NOT NULL,
    technology           REAL NOT NULL,
    health_wellness      REAL NOT NULL,
    miscellaneous        REAL NOT NULL,
    preferred_payment_method TEXT NOT NULL
);

CREATE INDEX idx_spending_major ON spending(major);
CREATE INDEX idx_spending_year ON spending(year_in_school);
