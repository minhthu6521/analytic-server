
#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/html/analytic-server/")

from Analytics import create_app

app = create_app('../../config.py')
app.run()