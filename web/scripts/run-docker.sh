#! /bin/bash

# Args:
#   -p port(s)
#   -e environment var(s)

PORTS="5000:5000"
IMAGE="egor045/traveller_tools_web:latest"
NAME="web_dev"

POSITIONAL=()
while [[ $# -gt 0 ]] ; do
    key="$1"
    case $key in
        -e|--env)
            ENV="$2"
            shift
            shift;;
        -p|--publish)
            PORTS="$2"
            shift
            shift
            ;;
        -n|--name)
            NAME="$2"
            shift
            shift;;
        *)    # unknown option
            POSITIONAL+=("$1") # save it in an array for later
            shift # past argument
            ;;
    esac
done

if [ "$POSITIONAL" != "" ] ; then
    IMAGE="$POSITIONAL"
fi

set -- "${POSITIONAL[@]}"
echo Running docker image $IMAGE with env=$ENV, port=$PORTS

if [ "$ENV" != "" ] ; then
    /usr/bin/docker run --rm --name "$NAME" -p $PORTS -e $ENV $IMAGE
else
    /usr/bin/docker run --rm --name "$NAME" -p $PORTS $IMAGE
fi