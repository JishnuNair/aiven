#!/bin/bash

# Run the extract.py script, then write_stage and write_final
# scripts to generate the final output files
# Print logs for each step

extract_only=0
stage_only=0
final_only=0

while (( "$#" )); do
    case "$1" in
        --yellow-data)
            yellow_file_path=$2
            shift 2
            ;;
        --green-data)
            green_file_path=$2
            shift 2
            ;;
        --db-name)
            database=$2
            shift 2
            ;;
        --db-user)
            dbuser=$2
            shift 2
            ;;
        --db-pass)
            dbpass=$2
            shift 2
            ;;
        --db-host)
            dbhost=$2
            shift 2
            ;;
        --db-port)
            dbport=$2
            shift 2
            ;;
        --extract-only)
            extract_only=1
            shift
            ;;
        --stage-only)
            stage_only=1
            shift
            ;;
        --final-only)
            final_only=1
            shift
            ;;
        --) # end argument parsing
            shift
            break
            ;;
        -*|--*=) # unsupported flags
            echo "Error: Unsupported flag $1" >&2
            exit 1
            ;;
        *) # preserve positional arguments
            PARAMS="$PARAMS $1"
            shift
            ;;
    esac
done
# set positional arguments in their proper place
eval set -- "$PARAMS"

if [[ $extract_only -eq 1 || ($extract_only -eq 0 && $stage_only -eq 0 && $final_only -eq 0) ]]; then
    echo "Running extract.py"
    python src/extract.py
fi

if [[ $stage_only -eq 1 || ($extract_only -eq 0 && $stage_only -eq 0 && $final_only -eq 0) ]]; then
    echo "Running write_stage"
    python src/write_stage.py --yellow_file_path $yellow_file_path --green_file_path $green_file_path --db_name $database --db_user $dbuser --db_pass $dbpass --db_host $dbhost --db_port $dbport
fi

if [[ $final_only -eq 1 || ($extract_only -eq 0 && $stage_only -eq 0 && $final_only -eq 0) ]]; then
    echo "Running write_final"
    python src/write_final.py --db_name $database --db_user $dbuser --db_pass $dbpass --db_host $dbhost --db_port $dbport
fi