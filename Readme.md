# Plant-watering RPi

## Local Development

### Setup environment
Run `pipenv install --three`

### Run web ui locally
`cd web_ctl`

`export CONFIG=./config.yml; pipenv run gunicorn --reload src:app`

### Run scheduler locally
`pipenv run python water.py ./web_ctl/config.yml`


## RPi Setup
Run `pi_install_dependencies.sh` once after copying files over

Run `pi_setup.sh`
