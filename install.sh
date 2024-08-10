#!/bin/bash

#----------------------------------------------
#Author: github.com/matauto
#Description:
#   install templates in your system
#Date: 29 July 2024
#----------------------------------------------

#global variables
script_dir=$(realpath "$(dirname "${BASH_SOURCE[0]}")")

print_help(){
    #EOF makes that cat will print  until next EOF
    cat<<EOF
    install.sh [-h]
    install templates.py in your system
    options:
        -h              print help
EOF
    exit 0
}


#parsing parameters
#here getopts approach is used, because it is built in
parse_param(){
    while getopts ":hp:" options; do
        case $options in
            h)
                print_help
                ;;
            \?)
                echo "Invalid option: -$OPTARG" >&2
                exit 1
                ;;
            :)
                echo "Option -$OPTARG need argument." >&2
                exit 1
                ;;
        esac
    done
}

main(){
    parse_param "$@"

    echo "Add alias to .bash_aliases in your home directory"
    echo "alias templates='$script_dir/templates.py'"
    echo "alias templates='$script_dir/templates.py'" >> .bash_aliases

    echo "Done."
}

#invoke main function
main "$@"
