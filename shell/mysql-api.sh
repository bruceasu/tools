#!/bin/bash
user=${1:-用户名}
PASSWD=${2:-密码}
db=${3:-数据库}
host=${3:-地址}
CMD="mysql -h${host} -D${db}  -u${user} -p"

#echo $CMD $PASSWD

#  set timeout 5

LANG=C expect -c "
  spawn $CMD
  expect {
  \"*yes/no\" { send \"yes\r\"; exp_continue }
  \"*password:\" { send \"$PASSWD\r\" }
  }
  interact
  #expect eof
  #interact {
  #   timeout 60 { send \" \"}
  #}
"

