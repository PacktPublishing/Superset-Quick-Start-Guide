# ubuntu user with sudo access

# 1. create a superset_config.py file
touch $HOME/.superset/superset_config.py

# 2. set superset_config_path env value in bash_profile to the file path
echo 'export SUPERSET_CONFIG_PATH=$HOME/.superset/superset_config.py' >> ~/.bash_profile

# 3. execute the bash_profile script in current terminal
# new terminals will auto execute this file upon initialization
#  .bash_profile on your machine should contain at least these commands.
# source /usr/local/bin/virtualenvwrapper.sh
# export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.google_cdp_key.json"
# export SUPERSET_CONFIG_PATH=$HOME/.superset/superset_config.py
source ~/.bash_profile


# 4. load virtualenv
# workon supervenv

# 5. install postgres python connector
pip install psycopg2

# 6. install os dependencies as sudo user
sudo apt-get -y install postgresql postgresql-client postgresql-contrib

# 7. switch to postgres user and create superset database
# sudo su postgres
# cd ~
# postgres@superset:~/$ psql
# postgres-# create database superset;
# postgres-# CREATE USER superset WITH PASSWORD 'superset';
# postgres-# GRANT ALL PRIVILEGES ON DATABASE "superset" to superset;
# postges-# \q

# 8. update pg_hba.conf to accept md5 for authentication
# postgres@superset:~$ vim /etc/postgresql/9.6/main/pg_hba.conf
# # --- inside pg_hba.conf ---
# # "local" is for Unix domain socket connections only
# # local          all       postgres     peer
# # replace with 
# local          all       postgres     md5


# 9. switch to ubuntu user with sudo access and restart postgres
sudo service postgresql restart

# 10. install gunicorn and gevent
pip install gunicorn gevent

# 11. install and run nginx
# Install
sudo apt-get update
sudo apt-get install nginx 

# Start and Reload
sudo nginx -s start
sudo nginx -s reload

# Check status
systemctl status nginx

# 12. update superset.conf file for nginx
# # -- inside superset.conf --
# # save in /etc/nginx/sites-enabled/
# server { 
#    listen 80; 
#    server_name 35.233.249.126; 
#    root /var/www/superset;  
#    location / {
#         proxy_buffers 16 4k; 
#         proxy_buffer_size 2k; 
#         proxy_pass http://127.0.0.1:8088; 
#    }
# }

# 13. link superset.conf to nginx/sites-enabled
sudo ln -s /etc/nginx/sites-available/superset.conf /etc/nginx/sites-enabled
# test for syntax errors
sudo nginx -t
# reload
sudo nginx -s reload
