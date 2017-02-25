SCHEMA="public"
DB="projectX"

mkdir -p $2/

declare -a tables=("customers_customer" "customers_skillmatch" "payment_payment" "payment_payout" "payment_transfer" "proj_customerrequest" "proj_skill" "proj_skilltopic" "session_call" "session_session")

$1 -Atc "select tablename from pg_tables where schemaname='$SCHEMA'" $DB |\
    while read TBL; do
	echo $TBL
	if [[ " ${tables[*]} " == *" $TBL "* ]]; then
		$1 -c "COPY $SCHEMA.$TBL TO STDOUT WITH CSV DELIMITER ',' HEADER ENCODING 'UTF-8'" $DB > $2/$TBL.csv
	fi
    done
