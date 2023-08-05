# xtesting-db-populate

Script to populate xtesting-db with project, tests cases and pods.

This application read local xtesting files and variables to populate
test databases.

## Install

``` pip install xtesting-db-populate```

## Requirements

To create projects and populate tests cases, `testcases.yaml` file
is **Mandatory**

To get the testapi url, the **Mandatory** variable `TEST_DB_URL` must
be set with the value of the test api url
(`https://testapi.test/api/v1/`)

If you want to set pods, **One of** the two may be set:

- an environment variable `NODE_NAME` must be set to the pod value
(`pod1`)
- a file `pods.yaml` that should be like:
  ```yaml
  ---
  pods:
    - pod1
    - pod2
  ```

## Usage

```bash
 !  ~/D/v/a/v/xtesting_project   testing-db-populate
🎯 get testapi url [success]
📤 read pods.yaml [success]
🤖 populate pod "pod1" [skipped]
🤖 populate pod "pod2" [skipped]
📤 read testcases.yaml [success]
📦 populate project "project1" [skipped]
📋 populate case "test 1" [skipped]
📋 populate case "test 2" [skipped]
📋 populate case "test 3" [skipped]
📋 populate case "test 4" [skipped]
```

To specify the folder where is store testcases.yaml et pods.yaml add
the folder path as argument. As an example if they are on `tests`
folder:

```bash
 !  ~/D/v/a/v/xtesting_project   testing-db-populate tests
🎯 get testapi url [success]
📤 read pods.yaml [success]
🤖 populate pod "pod1" [skipped]
🤖 populate pod "pod2" [skipped]
📤 read testcases.yaml [success]
📦 populate project "project1" [skipped]
📋 populate case "test 1" [skipped]
📋 populate case "test 2" [skipped]
📋 populate case "test 3" [skipped]
📋 populate case "test 4" [skipped]
```
