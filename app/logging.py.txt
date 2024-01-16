# import logging
# import json

#============================================================
# # Define a standard formatter
# class StandardFormatter(logging.Formatter):
#     def __init__(self, fmt=None, datefmt=None):
#         super().__init__(fmt, datefmt)

# # Setup logging
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)

# # Use a more human-readable format for the logs
# standard_format = '%(asctime)s - %(levelname)s - %(message)s'
# date_format = '%Y-%m-%d %H:%M:%S'
# formatter = StandardFormatter(standard_format, date_format)

# log_handler = logging.StreamHandler()
# log_handler.setFormatter(formatter)
# logger.addHandler(log_handler)
#=======================================================================
# class JsonFormatter(logging.Formatter):
#     def format(self, record):
#         log_record = {
#             "time": self.formatTime(record, self.datefmt),
#             "level": record.levelname,
#             "message": record.getMessage()
#         }
#         if record.exc_info:
#             log_record["exc_info"] = self.formatException(record.exc_info)
#         return json.dumps(log_record)

# # Setup logging
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)
# log_handler = logging.StreamHandler()
# log_handler.setFormatter(JsonFormatter())
# logger.addHandler(log_handler)