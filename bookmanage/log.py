import logging
class Logging :
    def info(self,msg):
        logger = logging.getLogger('bookmanage')
        logger.info(msg)