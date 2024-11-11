DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_database WHERE datname = 'auth-db'
   ) THEN
      PERFORM dblink_exec('dbname=postgres', 'CREATE DATABASE "auth-db"');
   END IF;
END
$do$;



CREATE TABLE IF NOT EXISTS role(
   id UUID PRIMARY KEY,
   name VARCHAR(20)
);


CREATE TABLE IF NOT EXISTS auth_user (
    id UUID PRIMARY KEY,
    name VARCHAR(50),
    last_name VARCHAR(50),
    phone_number VARCHAR(10),
    email VARCHAR(100),
    address VARCHAR(255),
    birthdate TIMESTAMP WITH TIME ZONE,
    password VARCHAR(255),
    role_id UUID,
    salt VARCHAR(255),
    CONSTRAINT fk_role
        FOREIGN KEY (role_id) 
        REFERENCES role (id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS auth_user_customer(
   id UUID PRIMARY KEY,
   auth_user_id UUID,
   customer_id UUID,
   CONSTRAINT fk_user
        FOREIGN KEY (auth_user_id) 
        REFERENCES auth_user (id)
        ON DELETE CASCADE
);
