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