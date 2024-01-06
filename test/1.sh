#!/bin/bash

#----------------------------------------------
#!/bin/bash

#----------------------------------------------
#Author: 
#Description:
#   
#Date: 
#----------------------------------------------

#global variables
script_dir=$(realpath "$(dirname "${BASH_SOURCE[0]}")")

print_help(){
    #EOF makes that cat will print  until next EOF
    cat<<EOF
     [-h] [-p <path>]
    
    options:
        -h              print help
        -p  <path>      path to directory       
EOF
    exit 0
}

validate_input(){
    parInput="$1"
    regExp="$2"
    echo $parInput | awk -v rE=$regExp '{if ($1 ~ /^[a-zA-Z0-9/]+$/) print}'
}

#parsing parameters
#here getopts approach is used, because it is built in
parse_param(){
    while getopts ":hp:" options; do
        case $options in
            h)
                print_help
                ;;
            p)
                pathFromArgs=$OPTARG
                #echo "$pathFromArgs" >&2
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
    #echo "Path $pathFromArgs"
    validate_input $pathFromArgs
}

#invoke main function
main "$@"
