# PyUserRole
PureConnect ICWS script to generate a .csv of users with their actual and inherited roles.  Python 3.5+

Script is very basic and has a few requirements:
* you need to have an ICWS SDK license for your PureConnect environment
* this uses IC authentication
* this script is set up to use ICWS over https.  You can change it to http if you want, but you will need to adjust the URL (and port within).


Currently, you put your IC credentials into the constants at the top of the script along with the name of your currently active primary server (this is not set up to be switchover intelligent)

Once you add that into the script, running this will result in the following process:

1.  An ICWS connection is established
2.  All roles in the environment are pulled back to create headers in the resulting CSV
3.  All users in the environment are pulled back
4.  Effective roles are retrieved for each user
5.  These values are all written to a .csv file in the execution directory.

The format of the csv is that it will list the username in the left most column, and then have a "Yes" under a role if the user has (or has inherited) that role.

There is no warranty provided on this.  It makes multiple calls to ICWS.  I always recommend testing things in a development environment first and running exports like these outside of peak hours.

Enjoy,

Aaron Lael
* this work is my own and in no way is any form of it attributed to any current or former employer *
