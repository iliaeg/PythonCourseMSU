#!/bin/bash

USAGE="Usage: ./gitconfig.sh [-c|--create] [-r|--remove] [-i|--info] [-h|--help]"

for i in "$@"
do
case $i in
    -c|--create)
    echo "--creating--"
    git config user.name iliaeg
    git config user.email egorovilyak@yandex.ru
    shift # past argument=value
    exit 0
    ;;
    -r|--remove)
    echo "--removing--"
    git config --unset-all user.name
    git config --unset-all user.email
    shift # past argument=value
    exit 0
    ;;
    -i|--info)
    echo "--info--"
    git config --list
    shift # past argument=value
    exit 0
    ;;
    -h|--help)
        echo $USAGE
        exit 0
    ;;
    # *)
    #     echo $USAGE
    #     exit 0
    # ;;
esac
done
 
echo $USAGE