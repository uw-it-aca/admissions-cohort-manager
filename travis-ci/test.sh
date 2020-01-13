#!/bin/sh
set -ev
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
echo "pre update"
npm install -g npm@latest
hash -r
npm -v
echo "post update"

npm install -g eslint stylelint
npm install

function run_test {
    echo "##########################"
    echo "TEST: $1"
    eval $1
}

run_test "pycodestyle ${DJANGO_APP}/ --exclude='migrations,resources,static'"


run_test "eslint --ext .js,.vue cohort_manager/static/cohort_manager/js/components/"
run_test "eslint --ext .js,.vue cohort_manager/static/cohort_manager/js/pages/"

run_test "stylelint 'cohort_manager/**/*.vue' 'cohort_manager/**/*.scss' "
run_test "coverage run --source=${DJANGO_APP} '--omit=*/migrations/*' manage.py test ${DJANGO_APP}"

ls -lah
# put generaged coverage result where it will get processed
cp .coverage /coverage

exit 0
