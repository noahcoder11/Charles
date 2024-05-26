import time
import functools

def performance_aware(performance_monitor, ):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            performance_monitor.record_duration(func.__name__, end_time - start_time)
            return result
        return wrapper
    return decorator


class PerformanceMonitor:
    def __init__(self):
        self.durations = {}
    
    def record_duration(self, func_name, duration):
        if func_name not in self.durations:
            self.durations[func_name] = []
        self.durations[func_name].append(duration)

    def get_average_duration(self, func_name):
        if func_name not in self.durations:
            return 0
        return sum(self.durations[func_name]) / len(self.durations[func_name])
    
    def print_perf_analysis(self):
        print('-------------------------')
        print('Performance Analysis:')
        for func_name in self.durations:
            print(f'- {func_name} avg: {self.get_average_duration(func_name)}')
            print('  - Individual Durations: ', self.durations[func_name])
            print('\n')
        print('-------------------------')