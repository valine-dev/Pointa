import getopt
from sys import argv

from . import Serve, init_app
from .configs.Config import UserConfig

production = False

opts,args = getopt.getopt(argv[1:],'-p',['production'])
for opt_name,opt_value in opts:
    if opt_name in ('-p', '--production'):
        production = True

if production:
    Serve(5000)
else:
    init_app(UserConfig).run(port=5000)
