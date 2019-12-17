# Fileculator

Calculates the total size of a user defined directory and stores the data
in a json file. It created to calculate total size of user uploaded files
in CGIT digital ocean server. It targets all **Laravel** projects and puts
the calculated file size as a json file in `storage/app` directory. You
should run the file as a cron job.

Changelog
------
#### Version 1.0
 - Initial release

Usage
------
### Enviroment Variables
Before you can run the script, you've to declare two environment variables 
in `.env` file. We have added an example file for your consistency. Just copy
the `.env.example` file as `.env` and define the values for the following two 
keys.
 - **PROJECT_ROOT**: This will be the directory where all of your Laravel
 projects reside. Note that if you keep your projects into some place like
 `/var/www/`, you have to run the script as root.
 
 - **PROJECT_DEPTH**: This value defines the searching depths for directories.
 The value should be either 1 or 2. If you have subdirectories in your root 
 directory, you have to put 2, else 1. For example, suppose this is the file
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
named `storage.json` inside that directory. The data inside the `storage.json` 
file looks like:

```
{
    "size": 112, 
    "written_on": "2019-12-17 15:08:42.249758"
}
```

Laravel can use the information in various purpose. Since this is an expensive
operation, you should run the script as a cron job so that it doesn't interferes
with http response.