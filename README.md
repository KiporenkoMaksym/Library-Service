# Library Service API

API service for library management written on DRF

## Installation using GitHub

``` bash
git clone <repository-url>
cd Library-Service

cp .env.sample .env

docker compose up --build
```

## Run with docker
Docker should be installed on your machine.

```bash
docker-compose build
docker-compose up
```

## Getting access
 - create user via /users/

 - get access token via /users/token/

## Features
 - Admin panel /admin/
 - Documentation is located at /doc/swagger/
 - JWT authentication
 - Creating, updating and deleting books can admin only
 - Creating borrowings and returning books can authenticated users and admin 
 - Filtering borrowings by user ID and borrowing activity 
 - Fee for borrowing a book
 - Fine (double rate) for the late return of a book
 - A connected Telegram bot notifies about book borrowings and returns
 - The Telegram bot sends a link for the online payment of book borrowing fees and fines

## Demo / Screenshots
<img width="1894" height="905" alt="Library_Service_1" src="https://github.com/user-attachments/assets/5a11faf1-960f-49b2-a73a-ea1fce725bd3" />
<img width="1908" height="905" alt="Library_Service_2" src="https://github.com/user-attachments/assets/3d16e1fd-4d31-41ce-a7eb-50a776796a66" />
<img width="1908" height="905" alt="Library_Service_3" src="https://github.com/user-attachments/assets/6f5fed0e-193e-41e6-8fe1-710f9e3c6c66" />
<img width="1908" height="905" alt="Library_Service_4" src="https://github.com/user-attachments/assets/16da884f-0280-4798-9404-70819373af5a" />
<img width="1908" height="905" alt="Library_Service_5" src="https://github.com/user-attachments/assets/98011442-7312-46fc-8b5c-7315b81fe332" />
<img width="1908" height="905" alt="Library_Service_6" src="https://github.com/user-attachments/assets/5ab6a889-1224-4679-b6b5-41eb18eacdee" />
<img width="1908" height="905" alt="Library_Service_7" src="https://github.com/user-attachments/assets/30b7fe85-4a69-4490-b187-57084e62b857" />
<img width="1908" height="905" alt="Library_Service_8" src="https://github.com/user-attachments/assets/f43aac62-c59d-4535-b90e-6219a7d75188" />
<img width="1908" height="905" alt="Library_Service_9" src="https://github.com/user-attachments/assets/972dc1d5-7e90-4bb3-9690-90094e74170c" />
<img width="1908" height="905" alt="Library_Service_10" src="https://github.com/user-attachments/assets/6957745a-b243-4f8e-b5c3-3359e4a39445" />
<img width="1908" height="905" alt="Library_Service_11" src="https://github.com/user-attachments/assets/a5fb809c-a198-470a-b418-b75b55c9b5d5" />
<img width="1908" height="905" alt="Library_Service_12" src="https://github.com/user-attachments/assets/6f87f2e9-c407-4c0e-bf95-9a1b13747832" />
