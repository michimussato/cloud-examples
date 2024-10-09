<!-- TOC -->
* [Reusable Dagster Assets](#reusable-dagster-assets)
  * [Running locally](#running-locally)
<!-- TOC -->

---

# Reusable Dagster Assets

These WIP examples demonstrate different ways
(proof of concept) to create re-usable/shareable
Dagster Assets:

- factories
- ops

## Running locally
To run locally via `dagster dev`, pip install the two projects:

```shell
cd ~/git/repos/cloud-examples/multi-location-project
cd ./location1-dir
pip install -e .[dev] -r requirements.txt
cd ..
DAGSTER_HOME="~/git/repos/cloud-examples/materializations" dagster dev --workspace ~/git/repos/cloud-examples/multi-location-project/workspace.yaml
```

---

Ref: https://github.com/dagster-io/cloud-examples
