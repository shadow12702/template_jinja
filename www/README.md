
# www-orapy

## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://github.com/osas-vn/www.git
git branch -M <branch>
git push -uf origin <branch>
```

## Setting debug on VSCode

```
[_launch.json_]
 {
 "version": "0.2.0",
 "configurations": [
      {
         "name": "Python: Flask",
         "type": "debugpy",
         "request": "launch",
         "module": "flask",
         "env": {
           "FLASK_APP": "app.py",
           "FLASK_ENV": "development"
       },
       "jinja": true,
       "justMyCode": true,
       "args": ["run", "--no-debugger", "--no-reload"]
      }
  ]
 }
```

**Explaination**:

- name: A descriptive name for the debug configuration (e.g., "FastAPI Debug").
- type: Set to "python" for Python debugging.
- request: Set to "launch" to start the application.
- module: Use flask to run the Flask application.
- env: Optional environment variables.
  - FLASK_APP : Python file has Flask instance, example: app.py
  - FLASK_ENV : Environment for Flask application
- jinja: Set to true if you're using Jinja2 templates.
- justMyCode: Set to true to exclude library code from debugging.
- args: Arguments passed to Flask application:
  - "run": run Flask application
  - "--no-debugger":
  - "--no-reload": Enables auto-reloading when code changes (optional but useful during development).

---

## Start Project

use command below to start Flask Application

```
py app.py --host 0.0.0.0 --port 5001
```

**Explaination**:

- app.py : name of Python file that has Flask instance
- host : IP or hostname of www server
- port : Port open to use for www
