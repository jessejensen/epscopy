# ebscopy __init__

import os
import logging 
from ebscopy import edsapi

__all__ = ['edsapi']		#refers to 'edsapi.py' file

log_levels									= {
												'DEBUG':	logging.DEBUG,
												'INFO':		logging.INFO,
												'WARNING':	logging.WARNING,
												'ERROR':	logging.ERROR,
												'CRITICAL':	logging.CRITICAL,
												}

if os.environ.get('EDS_LOG_LEVEL') in log_levels.keys():
    log_level								= log_levels[os.environ.get('EDS_LOG_LEVEL')]
else:
    log_level								= logging.WARNING

log_dir = os.environ.get('EDS_LOG_DIR')
if log_dir != None:
	log_file = '%s/log/ebscopy-%s.log' % (log_dir, os.getpid())
	logging.basicConfig(
		filename= log_file,
		level=log_level,
		format='%(asctime)s %(levelname)s %(module)s.%(funcName)s: %(message)s'
	)

#EOF
