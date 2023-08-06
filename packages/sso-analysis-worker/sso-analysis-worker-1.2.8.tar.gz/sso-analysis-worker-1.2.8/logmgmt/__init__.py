import logging
import sys

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s | %(filename)s', level=logging.WARNING,
                    stream=sys.stdout)
logger = logging.getLogger("ssoworker")
logger.setLevel(logging.INFO)
