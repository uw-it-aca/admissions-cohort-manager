#!/bin/sh
set -e
trap 'exit 1' ERR

# travis test script for django app
#
# PRECONDITION: inherited env vars from application's .travis.yml MUST include:
#      DJANGO_APP: django application directory name

# start virtualenv
source bin/activate

# install test tooling
pip install pycodestyle coverage
apt-get install -y nodejs npm
npm install -g npm@latest
hash -r

npm install -g eslint@5.0.0 stylelint@13.3.3 eslint-plugin-vue
npm install

function run_test {
    echo "##########################"
    echo "TEST: $1"
    eval $1
}

run_test "pycodestyle ${DJANGO_APP}/ --exclude='migrations,resources,static'"

node -v

run_test "eslint --ext .js,.vue cohort_manager/static/cohort_manager/js/components/"
run_test "eslint --ext .js,.vue cohort_manager/static/cohort_manager/js/pages/"

run_test "stylelint 'cohort_manager/**/*.vue' 'cohort_manager/**/*.scss' "
run_test "coverage run --source=${DJANGO_APP} '--omit=*/migrations/*' manage.py test ${DJANGO_APP}"

ls -lah
# put generaged coverage result where it will get processed
cp .coverage /coverage

exit 0
