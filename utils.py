
import time as t

def start():
  return t.perf_counter_ns()

def duration(start, label = "Duration"):
  duration = (t.perf_counter_ns() - start) / 1_000_000
  print(f"{label}: {duration}")
