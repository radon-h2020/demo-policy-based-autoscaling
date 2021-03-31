import sys
import os
import subprocess
path = os.getcwd()
os.system('python dynamic.py steIgeneral__testLbNginx.tosca NginxHtmlSite_0')
os.system('echo "Y" | opera deploy _definitions/steIgeneral__testLbNginx.tosca -r')

