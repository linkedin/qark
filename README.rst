Downloading the v2 branch
#########################
`git clone -b v2 https://github.com/linkedin/qark`

Installation
############

With pip (no security checks on requirements)
#############################################

```
~ pip install qark
~ qark --help
```

With `requirements.txt` (security checks on requirements)
#########################################################

```
~ wget https://raw.githubusercontent.com/linkedin/qark/v2/requirements.txt
~ pip install -r requirements.txt
~ pip install .
~ qark --help
```
