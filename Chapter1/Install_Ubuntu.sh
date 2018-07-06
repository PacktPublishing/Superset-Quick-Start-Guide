# 1) Install os-level dependencies
sudo apt-get install build-essential libssl-dev libffi-dev python-dev python-pip libsasl2-dev libldap2-dev
# 2) Check for Python 2.7
python --version 
# 3) Install pip
wget https://bootstrap.pypa.io/get-pip.py 
sudo python get-pip.py 
# 4) Install virtualenv 
sudo pip install --upgrade virtualenv 
# 5) Install virtualenvironment manager
sudo pip install virtualenvwrapper 
source /usr/local/bin/virtualenvwrapper.sh 
echo 'source /usr/local/bin/virtualenvwrapper.sh' >> ~/.bash_profile
# 6) Make virtual environment
mkvirtualenv supervenv 
# 7) Install superset 
(supervenv) pip install superset
# 8) Install database connector
pip install pybigquery
# 9) Create and open an authentication file for BigQuery
vim ~/.google_cdp_key.json
# 10) Copy and paste the contents of <project_id>.json key file to ~/.google_cdp_key.json
# 11) Load the new authentication file
echo 'export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.google_cdp_key.json"' >> ~/.bash_profile
source ~/.bash_profile
