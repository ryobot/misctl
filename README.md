********************************************************
misctl --- python cgi (with root ssh commands) ---
for iptables / haproxy / snort / squid ...
********************************************************

#### setup for CentOS6.4 ######

# yum install httpd expect
# vi /etc/httpd/conf/httpd.conf
----
Listen 10080
AddHandler cgi-script .cgi .py
ServerName localhost:10080
<Directory "/var/www/html/webadmin">
    AllowOverride None
    Options ExecCGI
    Order allow,deny 
    Allow from all       ### must be allowed only from the admin client
</Directory>
User webadmin
Group webadmin
----
# groupadd webadmin
# useradd webadmin -g webadmin
# su webadmin
$ cd
$ ssh-keygen
$ exit

*** copy ex_copy_id to /home/webadmin

# chown webadmin:webadmin /home/webadmin/ex_copy_id
# chmod 755 /home/webadmin/ex_copy_id

*** copy other files to /var/www/html/webadmin

# chown -R webadmin:webadmin /var/www/html/webadmin
# cd /var/www/html/webadmin
# chmod 755 *_ctl.py
# chmod 755 webadmin_config.py

Then setup from http://[hostname]:10080/webadmin_config.py
