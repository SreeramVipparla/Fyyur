# Fyyur-Project

# Overview

<img src="https://user-images.githubusercontent.com/86887626/138730751-4eb2feda-ab23-4d5b-95c0-c43796e8e596.jpg" width="700" height="300">

# Introduction

In this project, I have created a website called Fyyur using HTML, CSS, JavaScript, Python and the Python library SQLAlchemy. Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets the user list new artists and venues, discover them, and list shows with artists as a venue owner.

# Dependencies

## 1. Backend Dependencies

1.  **virtualenv** as a tool to create isolated Python environments
2.  **SQLAlchemy ORM** to be our ORM library of choice
3.  **PostgreSQL** as our database of choice
4.  **Python3** and **Flask** as our server language and server framework
5.  **Flask-Migrate** for creating and running schema migrations
    You can download and install the dependencies mentioned above using `pip` as:

```
pip install virtualenv
pip install SQLAlchemy
pip install postgres
pip install Flask
pip install Flask-Migrate
```

## 2. Frontend Dependencies

You must have the **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for the website's frontend. Bootstrap can only be installed by Node Package Manager (NPM). Therefore, if not already, download and install the [Node.js](https://nodejs.org/en/download/). Windows users must run the executable as an Administrator, and restart the computer after installation. After successfully installing the Node, verify the installation as shown below.

```
node -v
npm -v
```

Install [Bootstrap 3](https://getbootstrap.com/docs/3.3/getting-started/) for the website's frontend:

```
npm init -y
npm install bootstrap@3
```

# Instructions to run the Project

1. **Initialize and activate a virtualenv using:**

```
python -m virtualenv env
source env/bin/activate
```

> **Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:

```
source env/Scripts/activate
```

2. **Install the dependencies:**

```
pip install -r requirements.txt
```

3. **Run the development server:**

```
export FLASK_APP=myapp
export FLASK_ENV=development # enables debug mode
python3 app.py
```

4. **Verify on the Browser**<br>
   Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000)
