#installing python

sudo apt-get update
sudo apt-get install python3

#intalling virtual env

pip install --user virtualenv

#creating virtual env

python3 -m virtualenv env_cloudinary_ex

#activating virtual env

source env_cloudinary_ex/bin/activate

#installing dependencies

pip install -r requirements.txt

# running server

export FLASK_APP=app.py
flask run





