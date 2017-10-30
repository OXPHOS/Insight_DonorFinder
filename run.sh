#!/bin/bash
#
# Script to run find_political_donors.py
#
# Parameters:
# Input, Output(zip), Output(date)
#
# If only one parameter is passed to the script, default output paths will be used.
# If no parameter is passed to the script, default input and output paths will be used.

echo
echo Running find_political_donors.py
echo --------------------------------
echo

function print_path {
    echo Input path: $1
    echo 'Output(zip) path:' $2
    echo 'Output(date) path:' $3
}

function run_script {
     python ./src/find_political_donors.py $1 $2 $3
}

case "$#" in
    0)
        input=./input/itcont.txt
        output_zip=./output/medianvals_by_zip.txt
        output_date=./output/medianvals_by_date.txt
        ;;
    1)
        input=$1
        output_zip=./output/medianvals_by_zip.txt
        output_date=./output/medianvals_by_date.txt
        ;;
    3)
        input=$1
        output_zip=$2
        output_date=$3
        ;;
    *)
        echo ! Incorrect number of arguments. !
        echo Please specify one input file and two output file paths，
        echo or path to input only, or use the default paths.
        echo
        exit 128
esac

print_path $input $output_zip $output_date
echo
echo --------------------------------
run_script $input $output_zip $output_date

echo
