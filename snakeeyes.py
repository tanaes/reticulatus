from datetime import datetime
import sys
import os

FLAG_PATH = sys.argv[1]
for line in open(os.path.join(FLAG_PATH, "q.txt")):
    fields = line.strip().split()
    sample = fields[0]
    depth = fields[1]
    status = fields[2]
    if status == '-':
        continue
    jobid = fields[3]
    rule = fields[4]

    start_p = os.path.join(FLAG_PATH, '%s.start' % jobid)
    finish_p = os.path.join(FLAG_PATH, '%s.finish' % jobid)

    times = ['-', '-']
    if os.path.exists(start_p):
        times[0] = datetime.fromtimestamp(os.path.getmtime(start_p)).strftime('%Y-%m-%d_%H:%M:%S')

    if os.path.exists(finish_p):
        times[1] = datetime.fromtimestamp(os.path.getmtime(finish_p)).strftime('%Y-%m-%d_%H:%M:%S')

    fields.extend(times)
    print("\t".join(fields))
