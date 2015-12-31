#!/bin/bash

BASE="/mnt/sda1"
PROFILE="bws_profile.ini"
APP_BASE="$BASE/html5_test"


MSE_TEST="http:\/\/yt-dash-mse-test\.commondatastorage\.googleapis\.com\/unit-tests\/2015\.html\?test_type=conformance-test\&timestamp=1450244692622\?command=run\&disable_log=true"

usage ()
{
  echo -e '=========================================================================='
  echo -e '    This programe is to edit Youtube conformance tests URL '
  echo -e '=========================================================================='
  echo 'Usage:'
  echo `basename "$0 -m|-mse"`
  echo `basename "$0 -p|-progressive"`
  exit
}

copyAutoScript ()
{
	cp "$BASE/AutoScript.TSS" "$BASE/AutoScript/AutoScript.TSS"
}

modifyBwsProfile ()
{
	local parms="$@"
	while [ "$1" != "" ]; do
		case $parms in
			-m|-mse)
              shift
              sed -i -e "s/NO_THIS_PAGE/$MSE_TEST/g" "$APP_BASE/$PROFILE"
              ;;
            -p|-progressive)
              shift
              ;;
            *)   QUERY=$parms
    esac
    shift
    done
    echo -e '=========================================================================='
    echo -e '    Complete the bws_profile page url modification. Reboot the device now.'
    echo -e '=========================================================================='
}

copyBwsProfile ()
{
	cp "$BASE/$PROFILE" "$APP_BASE/$PROFILE"
}

if [ "$#" -ne 1 ]
then
  usage
fi


# main procedure
copyAutoScript
sed -i -e "s/#CLI/CLI/g" "$BASE/AutoScript/AutoScript.TSS"
copyBwsProfile
modifyBwsProfile "$1"
exit