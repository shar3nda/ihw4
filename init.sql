CREATE DATABASE restaurant_users;
ALTER DATABASE restaurant_users OWNER TO db_user;

CREATE DATABASE restaurant_orders;
ALTER DATABASE restaurant_orders OWNER TO db_user;

\c restaurant_orders;

CREATE TABLE dish
(
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100)   NOT NULL,
    description TEXT,
    price       NUMERIC(10, 2) NOT NULL,
    quantity    INTEGER        NOT NULL,
    created_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at  TIMESTAMP WITH TIME ZONE
);

CREATE TABLE "order"
(
    id               SERIAL PRIMARY KEY,
    status           VARCHAR(50) NOT NULL,
    special_requests TEXT,
    created_at       TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at       TIMESTAMP WITH TIME ZONE
);

CREATE TABLE order_dish
(
    id       SERIAL PRIMARY KEY,
    order_id INTEGER        NOT NULL REFERENCES "order" (id),
    dish_id  INTEGER        NOT NULL REFERENCES dish (id),
    quantity INTEGER        NOT NULL,
    price    NUMERIC(10, 2) NOT NULL
);

INSERT INTO dish (name, description, price, quantity)
VALUES ('Dish 1', 'This is dish 1', 10.00, 100),
       ('Dish 2', 'This is dish 2', 15.00, 200),
       ('Dish 3', 'This is dish 3', 20.00, 300);

INSERT INTO "order" (status, special_requests)
VALUES ('new', 'No onions'),
       ('completed', 'Extra cheese'),
       ('cancelled', 'Change of plans');

INSERT INTO order_dish (order_id, dish_id, quantity, price)
VALUES (1, 1, 2, 20.00),
       (2, 2, 1, 15.00),
       (3, 3, 3, 60.00);

\c restaurant_users;

CREATE TABLE session
(
    id            SERIAL PRIMARY KEY,
    user_id       INTEGER                     NOT NULL,
    session_token VARCHAR(255)                NOT NULL,
    expires_at    TIMESTAMP WITHOUT TIME ZONE NOT NULL
);

-- Create user table
CREATE TABLE "user"
(
    id            SERIAL PRIMARY KEY,
    username      VARCHAR(50)  NOT NULL,
    email         VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role          VARCHAR(10)  NOT NULL,
    created_at    TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at    TIMESTAMP WITHOUT TIME ZONE
);

-- Insert mock data into user table
INSERT INTO "user" (username, email, password_hash, role)
VALUES ('User1', 'user1@example.com', 'hash1', 'manager'),
       ('User2', 'user2@example.com', 'hash2', 'customer'),
       ('User3', 'user3@example.com', 'hash3', 'chef');
