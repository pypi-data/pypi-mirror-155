## This README file helps to provide instructions on how to make use of the ImpACT tool.

### ImpACT
Imperva API Continuous Testing (ImpACT) tool is designed to uncover the most common security issues such OWASP Top 10 vulnerabilities during early phases of application development. Users provide information on the APIs to be tested in the form of one or more OpenAPI Specification files and ImpACT parse this structured data to construct code that is factored to fuzz the API endpoints with a variety of input. The current version of ImpACT makes use of FuzzDB as the fuzzing pattern database.

ImpACT produces an easy to understand report of summary and detailed information on vulnerabilities found during the execution of tests. This may include findings such as authorization/authentication bypasses, SQL and OS command injections, path traversal issues and other OWASP Top 10 API vulnerabilities. The report also provides links to commands that can easily reproduce the issue.

### Prerequisites
Python>=3.8 and pip on Windows/Mac/Linux based machines.<br>
One or more OpenAPI Specification files (Currently supported v2 only) belonging to an application against which the tests can be run.

### Root Directory of Tests
Create a root test directory where the necessary input OpenAPI spec files and config files can be placed. This is the place where all the output of ImpACT is going to be present. As an example assume the directory is named as "Test". Change to this directory.
```bash
$ cd Test
```
### Create Virtual Environment
Create a new python >=3.8 virtual environment and activate it. Below example uses the name 'venv' for virtual environment name
```bash
$ python -m venv venv
$ source venv/bin/activate
```
Install/Upgrade ImpACT latest version
```bash
(venv) $ pip install -U impactrun
```

### Create/Place the Input Files Under Root Directory
Under the root directory (in our example Test), create a subdirectory called "specs". Place the OpenAPI Spec files under this "specs" folder. Go to the root (Test folder).
Move back to the Root (Test) folder.

### Config
In Root folder (Test) create a file 'cv_config.yaml'. Create the following content in the file. Include all the fuzz attack list or few of them as per requirement.

```
execution_info:
  dhostname: ""  # This is the host target where the application can be accessed. Eg., https://example.com
  dcviast_max_value_to_fuzz: "1"  # Number of fuzz values to try from each attack category
  fuzzattacklist: json,'control-chars','string-expansion','server-side-include'  # This is the fuzz attacklist to choose from different attack categories

# Full Attack List is here
# fuzzattacklist = [
#    'control-chars', 'string-expansion', 'server-side-include', 'xpath', 'unicode', 'html_js_fuzz','disclosure-directory',
#    'xss', 'os-cmd-execution', 'disclosure-source', 'format-strings', 'xml', 'integer-overflow', 'path-traversal',
#    'json', 'mimetypes', 'redirect', 'os-dir-indexing', 'no-sql-injection', 'authentication', 'http-protocol',
#    'business-logic', 'disclosure-localpaths/unix', 'file-upload/malicious-images', 'sql-injection/detect',
#    'sql-injection/exploit', 'sql-injection/payloads-sql-blind']
```

### Authentication Information
ImpACT needs to authenticate to the API endpoint to successfully fuzz the resource. The current version of ImpACT allows users to provide the authentication information in the form of a header that is accepted by the application in a file called "properties.yaml". Create the file "properties.yaml" and add the token/cookie information or any other needed headers as accepted by the application. Format of "properties.yaml" is like below:

```
headers:
  'Content-Type': 'application/json'
  'Authorization': 'Bearer xxxxxxxxxxxxxxxxxxxx'
```

### Generate fuzzing test for all the specs

With a given ImpACT version and a set of specs, you need to only run this once to generate the test code.
```bash
(venv) $ impactrun --generate-tests or impactrun -g
```
Upon successful execution of above command, the test files are generated under the folder(s), <spec_filename_as_in_specs_folder>_tests.

### Running Tests

To start the tests execute below command:
```bash
(venv) $ impactrun --execute-tests or impactrun -e
```
While the test execution is going on, user can check for the execution log by running the below command:
```bash
(venv) $ tail -f cviast_execution_log.txt
```

After the test is complete, the report is saved in a folder "new_report" with the name 'report_summary_<timestamp>.html'. In addition, a file called
`fordev-apis_<timestamp>.csv` is generated. This is a highlevel summary for consumption of a dev team. It highlight just the API endpoints that seem to "fail" the test, ie.
responding positively instead of rejecting the fuzz calls. Please feel free to import such CSV report to a spreadsheet.

The test results are stored in
```
results
results/perapi
results/perattack
```
Test can run for a long time, so one can adjust the spec and the collection of attacks in `cv_config.yaml` to stage each run. Test results of different test will not over-write each other.
