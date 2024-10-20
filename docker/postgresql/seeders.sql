INSERT INTO role (ID,NAME) VALUES('e4f78f9c-4e24-4588-9315-92dd601c8caa','Agent');
INSERT INTO role (ID,NAME) VALUES('beaa72b1-a7d3-4035-b4b3-bba0cd0c4d5d','User');

 

INSERT INTO auth_user (id,name,last_name,phone_number,email,address,birthdate,password,role_id) VALUES ('090b9b2f-c79c-41c1-944b-9d57cca4d582','MIGUEL','TOVAR','55555555','miguel@yopmail.com','Calle luna','1983-05-23','abc123','beaa72b1-a7d3-4035-b4b3-bba0cd0c4d5d');
INSERT INTO auth_user (id,name,last_name,phone_number,email,address,birthdate,password,role_id) VALUES ('e120f5a3-9444-48b6-88b0-26e2a21b1957','DANNA','LOPEZ','55555555','danna@yopmail.com','Calle luna','1983-11-19','abc123','e4f78f9c-4e24-4588-9315-92dd601c8caa');


INSERT INTO auth_user_customer (id,auth_user_id,customer_id) VALUES
	 ('555aac64-c527-4810-bf99-93b539172218'::uuid,'090b9b2f-c79c-41c1-944b-9d57cca4d582'::uuid,'845eb227-5356-4169-9799-95a97ec5ce33'::uuid);
