In order to test, you must have virtualenv installed for python 2.7. 

Create a virtual environment in the qark root directory
```
virtualenv .
```

Activate the virtualenv
```
. bin/activate
```

Install mock and pytest in the virtualenv
```
pip install mock pytest
```

Install all QARK requirements in the virtualenv
```
pip install -r requirements.txt
```

go to the test directory and run pytest
```
cd test && export PYTHONPATH=../:$PYTHONPATH && py.test
```
