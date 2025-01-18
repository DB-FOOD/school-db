CREATE TABLE "customers" (
    "id" SERIAL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "address" VARCHAR(255) NOT NULL,
    "city" VARCHAR(255) NOT NULL,
    "country" VARCHAR(255) NOT NULL,
    "phone_number" INT
);

CREATE TABLE "suppliers" (
    "id" SERIAL PRIMARY KEY,
    "supplier_name" VARCHAR(255) NOT NULL,
    "country" VARCHAR(255) NOT NULL
);

CREATE TABLE "products" (
    "id" SERIAL PRIMARY KEY,
    "product_name" VARCHAR(255) NOT NULL
);

CREATE TABLE "product_availability" (
    "id" SERIAL PRIMARY KEY,
    "product_id" BIGINT NOT NULL REFERENCES "products" ("id"),
    "supplier_id" BIGINT NOT NULL REFERENCES "suppliers" ("id"),
    "unit_price" DECIMAL NOT NULL,
    "quantity_available" INTEGER NOT NULL CHECK (quantity_available >= 0),
    PRIMARY KEY ("product_id", "supplier_id")
);

CREATE TABLE "orders" (
    "id" SERIAL PRIMARY KEY,
    "order_date" DATE NOT NULL,
    "order_reference" VARCHAR(255),
    "customer_id" BIGINT NOT NULL REFERENCES "customers" ("id")
);

CREATE TABLE "order_items" (
    "id" SERIAL PRIMARY KEY,
    "order_id" BIGINT NOT NULL REFERENCES "orders" ("id"),
    "product_aval_id" BIGINT NOT NULL REFERENCES "product_availability" ("id"),
    "quantity" INTEGER NOT NULL CHECK (quantity >= 0)
);
