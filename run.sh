
#!/bin/bash

#history -d `history | tail -n 2 | xargs | awk '{print $1}'`
history -d $(history | tail -n 1 | xargs | awk '{print $1}')

if [ -z $1 ] ; then
  echo "Usage : . ./run.sh <Your-Bot-Token>"
  echo "ex) . ./run.sh abcd.1234.abcd_1-1234"
else
  cp Dockerfile save_Dockerfile
  sed -i 's/<TOKEN>/'$1'/g' ./Dockerfile

  docker build -t isdpt-bot .
  docker run -it -d -p 10000:10000 --name isdpt-bot isdpt-bot
  rm Dockerfile
  mv save_Dockerfile Dockerfile
fi