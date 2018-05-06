#! /bin/bash

# Get current branch (use in docker build)
git_latest_commit=`git rev-parse HEAD`
git_branch=`git rev-parse --abbrev-ref HEAD`
docker_tag=$git_latest_commit
image_name='traveller_tools_web'
docker_file='Dockerfile'

echo 'Building image '$image_name:$docker_tag' from '$docker_file

/usr/bin/docker build \
    -t $image_name:$docker_tag \
    -f $docker_file \
    .

