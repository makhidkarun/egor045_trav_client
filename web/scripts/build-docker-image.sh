#! /bin/bash

# Get current branch (use in docker build)

docker_tag=`git rev-parse --abbrev-ref HEAD`
image_name='egor045/traveller_tools_web'
docker_file='Dockerfile'

echo 'Building image '$image_name:$docker_tag' from '$docker_file

/usr/bin/docker build \
    -t $image_name:$docker_tag \
    -f $docker_file \
    .

