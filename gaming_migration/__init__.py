import logging
from datetime import datetime

'''Setup logging'''
time_now = datetime.now().strftime("%m-%d-%y_%H%M%S")
logging.basicConfig(
    level=logging.DEBUG,
    filename=f'gaming_migration_{time_now}.log',
    filemode='w',
    format='%(asctime)s %(levelname)s: %(message)s'
)

