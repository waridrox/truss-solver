#!/bin/sh

# Credits: http://stackoverflow.com/a/750191

git filter-branch -f --env-filter "
    GIT_AUTHOR_NAME='waridrox'
    GIT_AUTHOR_EMAIL='mohdwarid4@gmail.com'
    GIT_COMMITTER_NAME='waridrox'
    GIT_COMMITTER_EMAIL='mohdwarid4@gmail.com'
  " HEAD
