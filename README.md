# Usage
- Clone the repository by running 
```sh
>>> git clone git@github.com:Cimmanuel/legendary-waddle.git
```
- Navigate into the directory 
```sh
>>> cd legendary-waddle
```
- Create a virtual environment and activate it 
```sh
>>> python -m venv ./waddlenv
>>> source ./waddlenv/bin/activate
```
- Install all dependencies in the requirements file
```sh
>>> pip install -r requirements.txt
```
- Create a .env file from .env.example (see .env.example by running `ls -a`)
```sh
>>> mv .env.example .env
```
- Every other variable in the just created .env file is fine. You just have to fix DATABASE_URL by giving it the absolute path to `db.sqlite3` (the database file which doesn't exist yet). `db.sqlite3` is usually found in the same directory as `manage.py`, so just find the path to `manage.py` and append `db.sqlite3`. In my case, my absolute path is `home/caspian/Documents/work/legendary-waddle/waddle/db.sqlite3`. Therefore, `DATABASE_URL` variable will be `sqlite:////home/caspian/Documents/work/legendary-waddle/waddle/db.sqlite3`
- Navigate into `waddle/`, apply migrations, and run the server
```sh
>>> cd waddle
>>> python manage.py migrate
>>> python manage.py runserver
```
- Open your browser and visit http://127.0.0.1:8000/graphql/ to access the Graphiql interface
- Create a user
```
mutation {
  createUser(
    email: "realuser@mail.com",
    mobile: "+2348100000001",
    name: "Real User",
    password: "helloworld"
	) {
    user {
      id
      name
      email
      mobile
      password
      created
      modified
      isActive
    }
  }
}

# Output should be in this format
{
  "data": {
    "createUser": {
      "user": {
        "id": "1",
        "name": "Real User",
        "email": "realuser@mail.com",
        "mobile": "+2348100000001",
        "password": "pbkdf2_sha256$216000$PtGwTwVV7DgI$1+NsKGOJgrAzMGPgfM7rOPMGTaey7yMyJ5VjDNqq75I=",
        "created": "2021-02-18T01:18:07.994564+00:00",
        "modified": "2021-02-18T01:18:07.994601+00:00",
        "isActive": true
      }
    }
  }
}
```
- Get login token
```
mutation {
  tokenAuth(email: "realuser@mail.com", password: "helloworld") {
    token
    payload
    refreshExpiresIn
  }
}

# Output should be in this format
{
  "data": {
    "tokenAuth": {
      "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InJlYWx1c2VyQG1haWwuY29tIiwiZXhwIjoxNjEzNjExNTYxLCJvcmlnSWF0IjoxNjEzNjExMjYxfQ.bO_qHQwwXUFEj27ecbM6zlyz7AarhQKkGjJLH4cIWJk",
      "payload": {
        "email": "realuser@mail.com",
        "exp": 1613611561,
        "origIat": 1613611261
      },
      "refreshExpiresIn": 1614216061
    }
  }
}
```
- Append JWT to the token above and use it as value of the `Authorization` header and you'll be logged in
- Check user profile
```
query {
  userProfile {
    id
    name
    email
    mobile
    created
    modified
    isActive
  }
}

# Output should be in this format
{
  "data": {
    "userProfile": {
      "id": "1",
      "name": "Real User",
      "email": "realuser@mail.com",
      "mobile": "+2348100000001",
      "created": "2021-02-18T01:18:07.994564+00:00",
      "modified": "2021-02-18T01:18:07.994601+00:00",
      "isActive": true
    }
  }
}
```
