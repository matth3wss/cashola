-- This enables the pgcrypto extension which provides the gen_random_uuid() function
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Create sequences for all BIGINT primary keys
CREATE SEQUENCE business_categories_id_seq START 1;
CREATE SEQUENCE businesses_id_seq START 1;
CREATE SEQUENCE expense_categories_id_seq START 1;
CREATE SEQUENCE income_categories_id_seq START 1;
CREATE SEQUENCE income_id_seq START 1;
CREATE SEQUENCE expenses_id_seq START 1;
CREATE SEQUENCE transactions_id_seq START 1;
CREATE SEQUENCE installments_id_seq START 1;
CREATE SEQUENCE credit_card_bill_history_id_seq START 1;
CREATE SEQUENCE credit_cards_id_seq START 1;
CREATE SEQUENCE bank_accounts_id_seq START 1;
CREATE SEQUENCE users_id_seq START 1;
CREATE SEQUENCE budgets_id_seq START 1;
CREATE SEQUENCE budget_items_id_seq START 1;

-- Create users table first (for foreign key references)
CREATE TABLE "users" (
    "id" BIGINT NOT NULL DEFAULT nextval('users_id_seq'),
    "username" VARCHAR(50) NOT NULL,
    "email" VARCHAR(100) NOT NULL,
    "password_hash" VARCHAR(256) NOT NULL,
    "role" VARCHAR(20) NOT NULL DEFAULT 'user',
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ("id")
);
CREATE UNIQUE INDEX "users_username_unique" ON "users"("username");
CREATE UNIQUE INDEX "users_email_unique" ON "users"("email");

CREATE TABLE "business_categories"(
    "id" BIGINT NOT NULL DEFAULT nextval('business_categories_id_seq'),
    "name" TEXT NOT NULL UNIQUE,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NULL DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE
    "business_categories" ADD PRIMARY KEY("id");

CREATE TABLE "businesses"(
    "id" BIGINT NOT NULL DEFAULT nextval('businesses_id_seq'),
    "business_tax_id" TEXT NOT NULL,
    "business_name" TEXT NOT NULL,
    "zip_code" TEXT NULL,
    "street_address" TEXT NULL,
    "street_number" TEXT NULL,
    "city" TEXT NULL,
    "state" CHAR(2) NULL,
    "business_category_id" BIGINT NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE
    "businesses" ADD PRIMARY KEY("id");
-- Add unique constraint on business_tax_id
ALTER TABLE
    "businesses" ADD CONSTRAINT "businesses_business_tax_id_unique" UNIQUE("business_tax_id");
CREATE INDEX "businesses_business_name_index" ON
    "businesses"("business_name");

CREATE TABLE "expense_categories"(
    "id" BIGINT NOT NULL DEFAULT nextval('expense_categories_id_seq'),
    "name" TEXT NOT NULL UNIQUE,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NULL DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE
    "expense_categories" ADD PRIMARY KEY("id");

CREATE TABLE "purchased_items"(
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "expense_id" BIGINT NULL,
    "name" TEXT NOT NULL,
    "code" TEXT NOT NULL,
    "quantity" DECIMAL(10, 3) NOT NULL,
    "unit_type" TEXT NOT NULL,
    "unit_price" DECIMAL(10, 2) NOT NULL,
    "total_price" DECIMAL(10, 2) NOT NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "main_category_id" BIGINT NULL
);
ALTER TABLE
    "purchased_items" ADD PRIMARY KEY("id");
CREATE INDEX "purchased_items_expense_id_index" ON
    "purchased_items"("expense_id");
CREATE INDEX "purchased_items_name_index" ON
    "purchased_items"("name");
CREATE INDEX "purchased_items_code_index" ON
    "purchased_items"("code");
CREATE INDEX "purchased_items_main_category_id_index" ON
    "purchased_items"("main_category_id");

-- Fixed purchased_item_subcategories with correct composite primary key
CREATE TABLE "purchased_item_subcategories"(
    "purchased_item_id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "subcategory_id" BIGINT NOT NULL
);
ALTER TABLE
    "purchased_item_subcategories" ADD PRIMARY KEY("purchased_item_id", "subcategory_id");

CREATE TABLE "income_categories"(
    "id" BIGINT NOT NULL DEFAULT nextval('income_categories_id_seq'),
    "name" TEXT NOT NULL UNIQUE,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);
ALTER TABLE
    "income_categories" ADD PRIMARY KEY("id");

-- Fixed income.income_category_id type to match income_categories.id
CREATE TABLE "income"(
    "id" BIGINT NOT NULL DEFAULT nextval('income_id_seq'),
    "user_id" BIGINT NULL,
    "name" TEXT NOT NULL,
    "total" DECIMAL(10, 2) NOT NULL,
    "income_category_id" BIGINT NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE
    "income" ADD PRIMARY KEY("id");

-- Recreated expenses table with qrcode_scanned field in a different position
-- Added purchase_timestamp field to track the actual date and time of purchase
CREATE TABLE "expenses"(
    "id" BIGINT NOT NULL DEFAULT nextval('expenses_id_seq'),
    "user_id" BIGINT NULL,
    "bank_account_id" INTEGER NULL,
    "business_id" BIGINT NULL,
    "total" DECIMAL(10, 2) NULL,
    "total_due" DECIMAL(10, 2) NOT NULL,
    "cashback" DECIMAL(10, 2) NOT NULL DEFAULT 0,
    "qrcode_scanned" BOOLEAN NOT NULL DEFAULT FALSE,
    "discounts" DECIMAL(10, 2) NULL DEFAULT 0,
    "taxes" DECIMAL(10, 2) NULL DEFAULT 0,
    "payment_method" TEXT NOT NULL,
    "installments" INTEGER NULL,
    "additional_info" TEXT NULL,
    "items_count" INTEGER NOT NULL DEFAULT 0,
    "nfce_bpe_link" TEXT NULL UNIQUE,
    "currency" CHAR(3) NULL DEFAULT 'BRL',
    "purchase_timestamp" TIMESTAMP(0) WITHOUT TIME ZONE NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(0) WITHOUT TIME ZONE NULL DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE
    "expenses" ADD PRIMARY KEY("id");
CREATE INDEX "expenses_bank_account_id_index" ON
    "expenses"("bank_account_id");
CREATE INDEX "expenses_payment_method_index" ON
    "expenses"("payment_method");
CREATE INDEX "expenses_purchase_timestamp_index" ON
    "expenses"("purchase_timestamp");

CREATE TABLE "transactions"(
    "id" BIGINT NOT NULL DEFAULT nextval('transactions_id_seq'),
    "name" TEXT NOT NULL,
    "amount" DECIMAL(10, 2) NOT NULL,
    "transaction_id" BIGINT NULL,
    "type" SMALLINT NOT NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE
    "transactions" ADD PRIMARY KEY("id");
COMMENT
ON COLUMN
    "transactions"."type" IS 'Type of transaction debit or credit';

-- Improved installments table with better structure
CREATE TABLE "installments"(
    "id" BIGINT NOT NULL DEFAULT nextval('installments_id_seq'),
    "expense_id" BIGINT NOT NULL,
    "installment_number" INTEGER NOT NULL,
    "value" DECIMAL(10, 2) NOT NULL,
    "due_date" DATE NULL,
    "paid" BOOLEAN DEFAULT FALSE,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE
    "installments" ADD PRIMARY KEY("id");
CREATE INDEX "installments_expense_id_index" ON
    "installments"("expense_id");

-- Improved credit_card_bill_history with clearer relationships
CREATE TABLE "credit_card_bill_history"(
    "id" BIGINT NOT NULL DEFAULT nextval('credit_card_bill_history_id_seq'),
    "credit_card_id" BIGINT NOT NULL,
    "expense_id" BIGINT NOT NULL,
    "installment_id" BIGINT NULL,
    "total_installments" INTEGER NOT NULL,
    "bill_date" DATE NOT NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);
ALTER TABLE
    "credit_card_bill_history" ADD PRIMARY KEY("id");
CREATE INDEX "credit_card_bill_history_credit_card_id_index" ON
    "credit_card_bill_history"("credit_card_id");
CREATE INDEX "credit_card_bill_history_expense_id_index" ON
    "credit_card_bill_history"("expense_id");

CREATE TABLE "credit_cards"(
    "id" BIGINT NOT NULL DEFAULT nextval('credit_cards_id_seq'),
    "card_name" TEXT NOT NULL DEFAULT 'defaults to bank_name',
    "bank_account_id" BIGINT NOT NULL,
    "credit_amount" BIGINT NOT NULL,
    "billing_period_end_date" DATE NOT NULL,
    "payment_due_date" DATE NOT NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "updated_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);
ALTER TABLE
    "credit_cards" ADD PRIMARY KEY("id");

CREATE TABLE "bank_accounts"(
    "id" BIGINT NOT NULL DEFAULT nextval('bank_accounts_id_seq'),
    "user_id" BIGINT NULL,
    "bank_name" TEXT NOT NULL,
    "account_name" TEXT NOT NULL DEFAULT 'bank_name',
    "account_number" TEXT NOT NULL,
    "account_type" TEXT NOT NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NULL DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE
    "bank_accounts" ADD PRIMARY KEY("id");
-- Add unique constraint on account_number
ALTER TABLE
    "bank_accounts" ADD CONSTRAINT "bank_accounts_account_number_unique" UNIQUE("account_number");
CREATE INDEX "bank_accounts_bank_name_index" ON
    "bank_accounts"("bank_name");
COMMENT
ON COLUMN
    "bank_accounts"."account_name" IS 'Defaults to bank_name';

-- Budget management tables
CREATE TABLE "budgets" (
    "id" BIGINT NOT NULL DEFAULT nextval('budgets_id_seq'),
    "user_id" BIGINT NOT NULL,
    "name" VARCHAR(100) NOT NULL,
    "description" TEXT NULL,
    "start_date" DATE NOT NULL,
    "end_date" DATE NOT NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ("id")
);

CREATE TABLE "budget_items" (
    "id" BIGINT NOT NULL DEFAULT nextval('budget_items_id_seq'),
    "budget_id" BIGINT NOT NULL,
    "expense_category_id" BIGINT NOT NULL,
    "planned_amount" DECIMAL(10, 2) NOT NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ("id")
);

-- Foreign key constraints with CASCADE options
ALTER TABLE
    "transactions" ADD CONSTRAINT "transactions_expense_foreign" FOREIGN KEY("transaction_id") REFERENCES "expenses"("id") ON DELETE CASCADE;
ALTER TABLE
    "transactions" ADD CONSTRAINT "transactions_income_foreign" FOREIGN KEY("transaction_id") REFERENCES "income"("id") ON DELETE CASCADE;
ALTER TABLE
    "purchased_item_subcategories" ADD CONSTRAINT "purchased_item_subcategories_purchased_item_id_foreign" FOREIGN KEY("purchased_item_id") REFERENCES "purchased_items"("id") ON DELETE CASCADE;
ALTER TABLE
    "purchased_item_subcategories" ADD CONSTRAINT "purchased_item_subcategories_subcategory_id_foreign" FOREIGN KEY("subcategory_id") REFERENCES "expense_categories"("id") ON DELETE RESTRICT;
ALTER TABLE
    "purchased_items" ADD CONSTRAINT "purchased_items_main_category_id_foreign" FOREIGN KEY("main_category_id") REFERENCES "expense_categories"("id") ON DELETE SET NULL;
ALTER TABLE
    "expenses" ADD CONSTRAINT "expenses_bank_account_id_foreign" FOREIGN KEY("bank_account_id") REFERENCES "bank_accounts"("id") ON DELETE SET NULL;
ALTER TABLE
    "businesses" ADD CONSTRAINT "businesses_business_category_id_foreign" FOREIGN KEY("business_category_id") REFERENCES "business_categories"("id") ON DELETE SET NULL;
ALTER TABLE
    "purchased_items" ADD CONSTRAINT "purchased_items_expense_id_foreign" FOREIGN KEY("expense_id") REFERENCES "expenses"("id") ON DELETE CASCADE;
ALTER TABLE
    "income" ADD CONSTRAINT "income_income_category_id_foreign" FOREIGN KEY("income_category_id") REFERENCES "income_categories"("id") ON DELETE SET NULL;
ALTER TABLE
    "credit_cards" ADD CONSTRAINT "credit_cards_bank_account_id_foreign" FOREIGN KEY("bank_account_id") REFERENCES "bank_accounts"("id") ON DELETE CASCADE;
ALTER TABLE
    "credit_card_bill_history" ADD CONSTRAINT "credit_card_bill_history_credit_card_id_foreign" FOREIGN KEY("credit_card_id") REFERENCES "credit_cards"("id") ON DELETE CASCADE;
ALTER TABLE
    "expenses" ADD CONSTRAINT "expenses_business_id_foreign" FOREIGN KEY("business_id") REFERENCES "businesses"("id") ON DELETE SET NULL;
ALTER TABLE
    "installments" ADD CONSTRAINT "installments_expense_id_foreign" FOREIGN KEY("expense_id") REFERENCES "expenses"("id") ON DELETE CASCADE;
ALTER TABLE
    "credit_card_bill_history" ADD CONSTRAINT "credit_card_bill_history_expense_id_foreign" FOREIGN KEY("expense_id") REFERENCES "expenses"("id") ON DELETE CASCADE;
ALTER TABLE
    "credit_card_bill_history" ADD CONSTRAINT "credit_card_bill_history_installment_id_foreign" FOREIGN KEY("installment_id") REFERENCES "installments"("id") ON DELETE SET NULL;

-- Add foreign key constraints for user relationships
ALTER TABLE "bank_accounts" 
    ADD CONSTRAINT "bank_accounts_user_id_foreign" 
    FOREIGN KEY("user_id") REFERENCES "users"("id") ON DELETE SET NULL;
    
ALTER TABLE "expenses" 
    ADD CONSTRAINT "expenses_user_id_foreign" 
    FOREIGN KEY("user_id") REFERENCES "users"("id") ON DELETE SET NULL;
    
ALTER TABLE "income" 
    ADD CONSTRAINT "income_user_id_foreign" 
    FOREIGN KEY("user_id") REFERENCES "users"("id") ON DELETE SET NULL;

-- Add foreign key constraints for budget tables
ALTER TABLE "budgets" 
    ADD CONSTRAINT "budgets_user_id_foreign" 
    FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE CASCADE;

ALTER TABLE "budget_items" 
    ADD CONSTRAINT "budget_items_budget_id_foreign" 
    FOREIGN KEY ("budget_id") REFERENCES "budgets"("id") ON DELETE CASCADE;
    
ALTER TABLE "budget_items" 
    ADD CONSTRAINT "budget_items_expense_category_id_foreign" 
    FOREIGN KEY ("expense_category_id") REFERENCES "expense_categories"("id") ON DELETE RESTRICT;

-- View to track budget vs actual spending (updated to use purchase_timestamp when available)
CREATE VIEW budget_vs_actual AS
SELECT 
    b.id AS budget_id,
    b.name AS budget_name,
    bi.expense_category_id,
    ec.name AS category_name,
    bi.planned_amount,
    COALESCE(SUM(pi.total_price), 0) AS actual_amount,
    (bi.planned_amount - COALESCE(SUM(pi.total_price), 0)) AS remaining_amount,
    (COALESCE(SUM(pi.total_price), 0) / NULLIF(bi.planned_amount, 0) * 100) AS percentage_used
FROM 
    budgets b
JOIN 
    budget_items bi ON b.id = bi.budget_id
JOIN 
    expense_categories ec ON bi.expense_category_id = ec.id
LEFT JOIN 
    expenses e ON e.user_id = b.user_id AND COALESCE(e.purchase_timestamp::date, e.created_at::date) BETWEEN b.start_date AND b.end_date
LEFT JOIN 
    purchased_items pi ON pi.expense_id = e.id AND pi.main_category_id = bi.expense_category_id
GROUP BY 
    b.id, b.name, bi.expense_category_id, ec.name, bi.planned_amount;

-- View for monthly expense summary (updated to use purchase_timestamp when available)
CREATE VIEW monthly_expenses_summary AS
SELECT 
    u.id AS user_id,
    u.username,
    TO_CHAR(COALESCE(e.purchase_timestamp, e.created_at), 'YYYY-MM') AS month,
    ec.id AS category_id,
    ec.name AS category_name,
    SUM(pi.total_price) AS total_amount,
    COUNT(DISTINCT e.id) AS transaction_count
FROM 
    users u
JOIN 
    expenses e ON u.id = e.user_id
JOIN 
    purchased_items pi ON e.id = pi.expense_id
JOIN 
    expense_categories ec ON pi.main_category_id = ec.id
GROUP BY 
    u.id, u.username, TO_CHAR(COALESCE(e.purchase_timestamp, e.created_at), 'YYYY-MM'), ec.id, ec.name
ORDER BY 
    month DESC, total_amount DESC;