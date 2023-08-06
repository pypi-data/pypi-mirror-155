import datetime
import time

print(datetime.datetime.now())

start_time = time.time()
print(start_time)

time.sleep(2)

end_time = time.time()
print(end_time)

execution_time = str(end_time - start_time).split('.')[0]
# execution_time = execution_time.split('.')
# execution_time = execution_time[0]
print(f'Execution Time {execution_time} secs')

