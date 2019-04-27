# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from jirapointsweb import app

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8085)
