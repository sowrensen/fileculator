# Fileculator

This scripts calculates the total size of the `storage/app`
directory (user uploaded files) of multiple **Laravel** apps. 
Define the project `root` and `depth` in .env file and run 
the script as a cron job.

Changelog
------
#### Version 1.0
 - Initial release

Usage
------
### Enviroment Variables
Before you can run the script, you've to declare two environment variables 
in `.env` file. I have added an example file for your consistency. Just copy
the `.env.example` file as `.env` and define the values for the following two 
keys.
 - **PROJECT_ROOT**: This will be the directory where all of your Laravel
 projects reside. Note that, if you keep your projects into some place like
 `/var/www/`, you have to run the script as root.
 
 - **PROJECT_DEPTH**: This value defines the searching depths for directories.
 The value should be either 1 or 2. If you have subdirectories in your root 
 directory, you have to put 2, else put 1. For example, suppose this is the file
 structure inside your `PROJECT_ROOT`:
 
   ```
   App-1/
    - App_1_Instance_1/
    - App_1_Instance_2/
   App-2/
    - App_2_Instance_1/
    - App_2_Instance_2/
   ``` 
   In the above case, you have to put depth value 2. If there is only one
   level of application directory, you can put 1.


Output
------
The script calculates the total size (in bytes) of the `/storage/app` directory 
inside each Laravel project and puts the storage information into a json file 
named `storage.json` inside that directory which is Laravel's public directory. 
Thus the generated file is ignored in any version control system. The data inside the 
`storage.json` file looks like:

```
{
    "size": 112, 
    "written_at": "2019-12-17 15:08:42.249758"
}
```

Laravel can use the information for various purposes. Since this is an expensive operation, 
you should run the script as a cron job so that it doesn't interfere with HTTP response.

Cron Example
------------

You can run the file directly from cron job. However, if you face difficulties to run pipenv from cron, better you create a bash script like this.
```
#!/bin/sh

VENV_PYTHON="/path/to/pipenv/python"
FILECULATOR="/path/to/fileculator"
PIPENV="/path/to/pipenv"
SCRIPT="fileculator.py"

cd "${FILECULATOR}" && "${PIPENV}" run "${VENV_PYTHON}" "${SCRIPT}"
```

Now run the bash script as cron job. This following cron job will run on every even hour and write the log into the defined log file.
```
0 */2 * * * /path/to/bash/fileculator.sh > /path/to/fileculator_output.log
```

If you don't want a log file:
```
0 */2 * * * /path/to/bash/fileculator.sh >/dev/null 2>&1
```