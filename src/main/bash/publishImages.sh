#!/bin/bash

SLUG="NonameDev/MathAppData"
BRANCH="beta"
DESTINATION_BRANCH="beta"

#set -e
set -x

if [ "$TRAVIS_REPO_SLUG" != "$SLUG" ]; then
    echo "[SKIPPING] Wrong repository. Expected '$SLUG' but was '$TRAVIS_REPO_SLUG'.\n"
elif [ "$TRAVIS_PULL_REQUEST" != "false" ]; then
    echo "[SKIPPING] Pull request build.\n"
elif [ "$TRAVIS_BRANCH" != "$BRANCH" ]; then
    echo "[SKIPPING] Wrong branch. Expected '$BRANCH' but was '$TRAVIS_BRANCH'.\n"
else
    # Setting up git credentials
    git config credential.helper "store --file=.git/credentials"
    echo "https://${GH_TOKEN}:@github.com" > .git/credentials
    # Set travis as user
    git config --global user.email "travis@travis-ci.org"
    git config --global user.name "travis-ci"
    # Make sure we are using https.
    git remote set-url origin "https://github.com/$SLUG.git"

    if [ -d "./imgs" ]; then
        # Push images to beta branch
        git checkout $BRANCH
        git add -f ./imgs
        git commit -m "Publish images from Travis CI build $TRAVIS_BUILD_NUMBER"
        git push origin $BRANCH
        # Merge images into our destination branch
        git checkout -b $DESTINATION_BRANCH
        git merge $BRANCH
        git push origin $DESTINATION_BRANCH
    else
        echo "[ERROR] imgs folder missing\n"
    fi
fi
