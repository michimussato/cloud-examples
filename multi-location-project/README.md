# Create venv

```
cd /home/users/michaelmus/git/repos/dagster/cloud-examples
rez env python-3.9
python -m venv venv_test_01
source venv_test_01/bin/activate
python -m pip install --upgrade pip
pip install dagster dagster-webserver
```

## Run Pycharm

```
rez env python-3.9
/scratch/michaelmus/Applications/pycharm-current/bin/pycharm.sh
```

## Activate venv

```
cd /home/users/michaelmus/git/repos/dagster/cloud-examples
rez env python-3.9
source venv_test_01/bin/activate
```

## Running locally

### Build deps

```
cd /home/users/michaelmus/git/repos/dagster/cloud-examples
rez env python-3.9
source venv_test_01/bin/activate

cd /home/users/michaelmus/git/repos/dagster/cloud-examples/multi-location-project/location1-dir
pip install -e .[dev] -r requirements.txt
# force reinstall
# pip install -e .[dev] --force-reinstall -r requirements.txt --no-cache-dir
```



```
cd /home/users/michaelmus/git/repos/dagster/cloud-examples
rez env python-3.9
source venv_test_01/bin/activate
mkdir -p /home/users/michaelmus/git/repos/dagster/cloud-examples/materializations

cd /home/users/michaelmus/git/repos/dagster/cloud-examples/multi-location-project
export DAGSTER_HOME=/home/users/michaelmus/git/repos/dagster/cloud-examples/materializations
dagster dev --workspace workspace.yaml
```