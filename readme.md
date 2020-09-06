# Fileculator

This scripts calculates the total size of the `storage/app`
directory (user uploaded files) of multiple **Laravel** apps. 
Define the project `root` and `depth` in .env file and run 
the script as a cron job.

Changelog
------

#### Version 2.0.0

 - Added option to determine whole project size.
 - Improved code structure.
 - Added a `requirement.txt` file to work with usual virtualenv.
 - Removed Pipenv support.

#### Version 1.0.1

 - Fixed bug related to project root.

#### Version 1.0

 - Initial release

Usage
------

### Setup

Run following commands in your terminal to copy this repository and for primary setup.

```
git clone https://github.com/sowrensen/fileculator.git
cd fileculator
python -m venv ./venv
. venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### Environment Variables

Before you can run the script, you've to declare a few environment variables 
in `.env` file. An example `.env` file has been added for your consistency. 
Just copy the `.env.example` file as `.env` and define the values for the 
following two keys.

 - **PROJECT_ROOT**: This will be the directory where all of your Laravel 
  projects reside, e.g.` /home/<user>/project`s, or `/var/www`, or 
  `/usr/share/nginx`. Note that, if you keep your projects into 
  some place which is in root directory, you have to run the 
  script as root. You know how Linux works, right?
 
 - **PROJECT_DEPTH** (1, 2): This key defines the searching depths for directories.
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

 - **STORAGE_ONLY** (0, 1): This key defines the size of the whole Laravel project
 is to be calculate (including `vendor`, `node_modules` etc.) or only the storage
 directory. The expected value should be either 0 or 1. 

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
_Note that, the output file will be replaced during the next run_.

Cron Example
------------

You can run the file directly from cron job. However, if you face difficulties to run 
pipenv from cron, better you create a bash script like this.

```
#!/bin/sh

FILECULATOR="/path/to/fileculator"
PYTHON="${FILECULATOR}/venv/bin/python"
SCRIPT="${FILECULATOR}/fileculator.py"

cd "${FILECULATOR}" && "${PYTHON}" "${SCRIPT}"
```

Make the bash script executable by running:

```shell
chmod +x fileculator.sh
```

Now run the bash script as cron job. This following cron job will run on every even hour and write the log into the defined log file.
```
0 */2 * * * /path/to/bash/fileculator.sh > /path/to/fileculator_output.log
```

If you don't want a log file:
```
0 */2 * * * /path/to/bash/fileculator.sh >/dev/null 2>&1
```
