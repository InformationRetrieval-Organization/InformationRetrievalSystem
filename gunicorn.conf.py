import multiprocessing

pythonpath = 'src'
bind = '0.0.0.0:3100'
workers = 1
#workers = multiprocessing.cpu_count() * 2 + 1 # maximum workers for the server
worker_class = 'uvicorn.workers.UvicornWorker'
timeout = 600 # 600s startup time for database actions