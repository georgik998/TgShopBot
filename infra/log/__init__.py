import logging
from logging import Filter

from tg_bot.infra.log.config import logger_settings

# ================
logger = logging.getLogger(logger_settings.LOGGER_NAME)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")


# ================
# class CountFilter(logging.Filter):
#     def __init__(self):
#         super().__init__()
#         self.count = 0
#
#     def filter(self, record):
#         self.count += 1
#         if self.count >= 1000:
#             self.count = 0
#             max_request = 0
#             window = None
#             with open(logger_settings.LOG_FILE_PATH, 'r') as file:
#                 for log_record in file.readlines():
#                     if 'max Request per' in log_record:
#                         print(int(log_record.split(' ')[-1]))
#                         if int(log_record.split(' ')[-1]) >= max_request:
#                             max_request = int(log_record.split(' ')[-1])
#                             window = int(log_record.split(' ')[11])
#                         break
#             logger.warn(f'Total max Request per {window} seconds = {max_request}')
#         return True


# ================
file_handler = logging.FileHandler(filename=logger_settings.LOG_FILE_PATH, mode="a")
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)
# file_handler.addFilter(CountFilter())

# ================
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# ================
logger.addHandler(file_handler)
logger.addHandler(console_handler)
