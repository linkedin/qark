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

Go to the test directory and run pytest
```
cd test && export PYTHONPATH=../:$PYTHONPATH && py.test
```

Install pytest-cov to produce test coverage reports. It supports a centralized testing approach
```
pip install pytest-cov
```

Run pytest-cov. This command will run tests on all the files and folders of the project
```
py.test --cov
```

To check test coverage for a specific folder (modules and plugins in Qark's case)
```
py.test --cov= <absolute path to specific folder>
```

Example syntax to check test coverage for modules and plugins
```
py.test --cov=/../../../qark/qark/modules/
py.test --cov=/../../../qark/qark/plugins/
```

Saving the report in HTML format. This helps in providing a detailed feedback of the code with and without unit tests
```
py.test --cov=<absolute path to specific folder> --cov-report html
```
