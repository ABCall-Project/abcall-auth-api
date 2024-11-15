INSERT INTO role (ID,NAME) VALUES('e4f78f9c-4e24-4588-9315-92dd601c8caa','Agent');
INSERT INTO role (ID,NAME) VALUES('beaa72b1-a7d3-4035-b4b3-bba0cd0c4d5d','User');
INSERT INTO role (ID,NAME) VALUES('9a2a6082-77ff-4056-8305-77c38d839c29','Company Admin');

 

INSERT INTO auth_user (id,name,last_name,phone_number,email,address,birthdate,password,role_id, salt) VALUES ('090b9b2f-c79c-41c1-944b-9d57cca4d582','MIGUEL','TOVAR','55555555','miguel@yopmail.com','Calle luna','1983-05-23','gAAAAABnNpKVXQat4aPCPSGjMTpY0vYYTGFJRDTt-A9-12qLJv_U1rOunGqPtivEBwNSCMjKLCPepJ5DK6EcYHAO8aK91bBX7Q==','beaa72b1-a7d3-4035-b4b3-bba0cd0c4d5d', 'bpc/IFyEaS7UdhPTLI4xmw==');
INSERT INTO auth_user (id,name,last_name,phone_number,email,address,birthdate,password,role_id, salt) VALUES ('e120f5a3-9444-48b6-88b0-26e2a21b1957','DANNA','LOPEZ','55555555','danna@yopmail.com','Calle luna','1983-11-19','gAAAAABnNpd54AkRkKppD0iGskbDo70fJE47HLxMUvkesweoaIXJ7bj0voxoL4vxSXl1A4fAuHgUWxppISk9yX7chTZ_NFhmpA==','e4f78f9c-4e24-4588-9315-92dd601c8caa', '23AYZCU1kJyuujh6mok0BA==');
INSERT INTO auth_user (id,name,last_name,phone_number,email,address,birthdate,password,role_id, salt) VALUES ('5f76c81f-872a-4ea8-8979-f06636264b66','DinoGeek','Company','11111111','abcall@dinogeek.com','Venezuela','2021-05-23','gAAAAABnNpgT8omQpcl0DrSiD14Qv_e5C5SU9z00HKSFq-T2g6AzaLqL4bI6vxR6zJCZtoSUhMkAgD8A0EcElNVtMZPh8YfLHQ==','9a2a6082-77ff-4056-8305-77c38d839c29', '5hiiEEPyBpy0LoMfBgPOWw==');


INSERT INTO auth_user_customer (id,auth_user_id,customer_id) VALUES
	 ('555aac64-c527-4810-bf99-93b539172218'::uuid,'090b9b2f-c79c-41c1-944b-9d57cca4d582'::uuid,'845eb227-5356-4169-9799-95a97ec5ce33'::uuid);
