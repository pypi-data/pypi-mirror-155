import logging

c_handler = logging.StreamHandler()
# f_handler = logging.FileHandler('ingestion.log')

c_handler.setLevel('DEBUG')
# f_handler.setLevel('INFO')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(formatter)
# f_handler.setFormatter(formatter)
