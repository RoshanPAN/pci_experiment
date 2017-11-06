import time
import matplotlib.pyplot as plt
import os

class MetricLogData:
    def __init__(self, file, start, interval):
        # read record and put into metric map of list
        self.metric_mp = {}
        with open(file, 'r') as f:
            for line in f:
                metric, (time, value) = self.toMetricMap(line)
                if metric not in self.metric_mp:
                    self.metric_mp[metric] = []
                self.metric_mp[metric].append((time, value))

        # Convert to matrix
        start = self.toTimeStamp(start)
        self.result = self.acumulativeResultAll(start, interval, self.metric_mp)
        print self.result


    # get date formatted to timestamp
    def toTimeStamp(self, date):
        """

        :param String date:
        :return: Int timestamp
        """
        timestamp = time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S'))
        return timestamp


    def toMetricMap(self, line):
        '''

        :param line:
        :return: record metric, (timestamp, value)
        '''
        line = line.strip('\n')
        time = line.split(',')[0]
        detail = line.split(',')[1]
        timestamp = self.toTimeStamp(time)
        detail = detail.split(' ')
        metric = detail[1]
        value = float(detail[2])
        return metric, (timestamp, value)



    def acumulativeResult(self, start, interval, time_value_table):
        time_value_table.sort()
        min_value, max_value, sum_value, count = float('inf'), float('-inf'), 0.0, 0
        for record in time_value_table:
            if record[0] >= start and record[0] <= (start + interval):
                min_value = min(min_value, record[1])
                max_value = max(max_value, record[1])
                sum_value += record[1]
                count += 1
        return [min_value, max_value, sum_value / count]

    def acumulativeResultAll(self, start, interval, metric_mp):
        result = []
        metric_table = ['system_cpu_usage', 'user_cpu_usage', 'load_avg', 'run_queue_length', 'total#process',
                           '#running_process', '#sleeping_process', '#threads', '#blocked_process',
                           'used_physical_memory', 'unused_physical_memory', 'swap-in', 'swap-out', 'page-in',
                           'page-out', 'swap-allocated', '#physical_disk_read', '#physical_disk_write',
                           'amount_physical_disk_read', 'amount_physical_disk_write', 'disk_busy_time',
                           'total#incoming_packages', 'total#outgoing_packages', 'size_of_incoming_packages',
                           'size_of_outgoing_packages', '#connections', '#disconnections']
        for metric in metric_table:
            if metric in metric_mp:
                result += self.acumulativeResult(start, interval, metric_mp[metric])
            else:
                result += [-1, -1, -1]
        return result



class LogDataGrapher:
    def __init__(self, data_map):
        for metric in data_map:
            self.metricGrapher(data_map, metric)





    def metricGrapher(self, data_map, metric):

        x_data = []
        y_data = []
        for tup in data_map[metric]:
            x_data.append(tup[0])
            y_data.append(tup[1])
        fig, ax = plt.subplots(nrows=1, ncols=1)
        plt.plot(x_data, y_data)
        plt.xlabel("time")
        plt.ylabel("value")
        plt.title(metric)
        fig.savefig(os.getcwd() + '/pictures/' + metric + '.png')  # save the figure to file
        plt.close(fig)




metricLogData = MetricLogData('metric.log', '2017-10-25 09:18:21', 500)
data_map = metricLogData.metric_mp
LogDataGrapher(data_map)
