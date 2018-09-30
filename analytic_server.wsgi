
#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/html/analytic-server/")

from Analytics import create_app

appplication = create_app('../../config.py')
application.run()