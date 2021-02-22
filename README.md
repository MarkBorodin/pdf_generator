# INSTALL_TESTIFY 


### Setup

clone repository:
```
git clone https://github.com/MarkBorodin/pdf_generator.git
```
move to folder "testify":
```
cd pdf_generator
```

to install the required libraries, run on command line:
```
pip install -r requirements.txt
```

you shout make migration:
```
python manage.py migrate
```

### run app


to work you need to create a superuser. Run and follow the prompts:

```
python manage.py createsuperuser
```

to start the server - run:

```
python manage.py runserver
```

and follow the link:

```
http://127.0.0.1:8000/admin
```


### Finish
