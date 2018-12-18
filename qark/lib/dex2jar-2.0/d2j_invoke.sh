#!/bin/sh

#
# dex2jar - Tools to work with android .dex and java .class files
# Copyright (c) 2009-2013 Panxiaobo
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#      http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# copy from $Tomcat/bin/startup.sh
# resolve links - $0 may be a softlink
PRG="$0"
while [ -h "$PRG" ] ; do
  ls=`ls -ld "$PRG"`
  link=`expr "$ls" : '.*-> \(.*\)$'`
  if expr "$link" : '/.*' > /dev/null; then
    PRG="$link"
  else
    PRG=`dirname "$PRG"`/"$link"
  fi
done
PRGDIR=`dirname "$PRG"`
#

_classpath="."
if [ `uname -a | grep -i -c cygwin` -ne 0 ]; then # Cygwin, translate the path
    for k in "$PRGDIR"/lib/*.jar
    do
        _classpath="${_classpath};`cygpath -w ${k}`"
    done
else
    for k in "$PRGDIR"/lib/*.jar
    do
        _classpath="${_classpath}:${k}"
    done
fi

java -Xms512m -Xmx1024m -classpath "${_classpath}" "$@"
