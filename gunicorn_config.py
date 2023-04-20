from multiprocessing import cpu_count

bind = '0.0.0.0:6444'
timeout = 120
workers = cpu_count()