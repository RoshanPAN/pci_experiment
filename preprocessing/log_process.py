import time, math
import os
import numpy as np

METRICS_ORDERED = ['#blocked_process', '#connections', '#disconnections', '#physical_disk_read',
                     '#physical_disk_write', '#running_process', '#sleeping_process', '#threads',
                     'amount_physical_disk_read', 'amount_physical_disk_write', 'disk_busy_time',
                     'load_avg', 'page-in', 'page-out', 'run_queue_length', 'size_of_incoming_packages',
                     'size_of_outgoing_packages', 'swap-allocated', 'swap-in', 'swap-out', 'system_cpu_usage',
                   'total#incoming_packages', 'total#outgoing_packages', 'total#process', 'unused_physical_memory',
                   'used_physical_memory', 'user_cpu_usage']

class MetricLogRecord(object):
    def __init__(self, record):
        contents = record.split(' ')
        record_time = contents[0] + ' ' + contents[1].split(',')[0]
        self.timestamp = int(time.mktime(time.strptime(record_time, '%Y-%m-%d %H:%M:%S')))
        self.type = contents[2]
        self.value = float(contents[3])
        self.hostname = contents[-1]

    def __str__(self):
        return "%15s   %d   %25s   %.2f" % (self.hostname, self.timestamp, self.type, self.value)

class MetricLogParser(object):
    def __init__(self, log_folder_path):
        self.log_records = []
        # parse each file
        for file_name in os.listdir(log_folder_path):
            file_path = log_folder_path + os.sep + file_name
            self.log_records += MetricLogParser.parse_file(file_path)
        self.log_records.sort(lambda x, y: x.timestamp - y.timestamp)
        self.update_record_map()

    def update_record_map(self):
        self.record_map = {}
        for r in self.log_records:
            self.record_map[r.type] = self.record_map.get(r.type, []) + [r]


    @classmethod
    def parse_file(cls, file_path):
        records = []
        with open(file_path, "r") as fh:
            for line in fh:
                line = line.strip('\n')
                if line in ['']:
                    continue
                records.append( MetricLogRecord(line) )
        return records

    def filter(self, start_ts, end_ts):
        def filter_by_time(r):
            return r.timestamp >= start_ts and r.timestamp <= end_ts
        self.log_records = filter(filter_by_time, self.log_records)
        for metric, records in self.record_map.items():
            self.record_map[metric] = filter(filter_by_time, self.record_map[metric])

    def __str__(self):
        records_str = "\n"
        for record in map(str, self.log_records[:10]):
            records_str += record + "\n"
        type_and_cnt = ""
        for t in self.record_map.keys():
            type_and_cnt += "%20s  %10d\n" % (t, len(self.record_map[t]))
        return "%s \nTotal Record Num: %d\n%s\n" % (records_str, len(self.log_records), type_and_cnt)

    def __len__(self):
        return len(self.log_records)

class YCSBLogRecord(object):
    def __init__(self, record):
        contents = record.split(' ')
        record_time = ' '.join(contents[0:4]) + ' ' + contents[5]
        self.timestamp = int(time.mktime(time.strptime(record_time, "%a %b %d %H:%M:%S %Y")))
        self.value = float(contents[-1])
        self.type = 'throughput'

    def __str__(self):
        return "%d   %12s   %.2f" % (self.timestamp, self.type, self.value)

    def __repr__(self):
        return self.__str__()


class YCSBLogParser(object):
    def __init__(self, log_folder_path):
        # parse each file
        file_name = "YCSB.log"
        file_path = log_folder_path + os.sep + file_name
        self.log_records = YCSBLogParser.parse_file(file_path)
        self.log_records.sort(lambda x, y: x.timestamp - y.timestamp)

    @classmethod
    def parse_file(cls, file_path):
        records = []
        with open(file_path, "r") as fh:
            for line in fh:
                line = line.strip('\n')
                if line in ['']:
                    continue
                r = YCSBLogRecord(line)
                if math.isnan(r.value):
                    continue
                records.append(r)
        return records

    def filter(self, start_ts, end_ts):
        def filter_by_time(r):
            return r.timestamp >= start_ts and r.timestamp <= end_ts
        self.log_records = filter(filter_by_time, self.log_records)

    def __str__(self):
        records_str = "\n"
        for record in map(str, self.log_records[:10]):
            records_str += record + "\n"
        return "%s \nTotal Record Num: %d\n" % (records_str, len(self.log_records))

class IntervaledSingleMachineFeatureVectors(object):
    def __init__(self, records, start_ts, end_ts, interval=30, is_ycsb_log=False):
        records.sort(lambda x, y: x.timestamp - y.timestamp)
        # Put records into intervaled buckets (list of tuple)
        i = 0
        self.intervaled_records = []
        self.intervals = []
        for ts in xrange(start_ts + interval, end_ts + 1, interval):
            start, end = ts - interval, ts  # right side of this range is open [start, end)
            cur_interval = []
            while True:
                r = records[i]
                if r.timestamp >= end:  # record belong to later interval
                    break
                elif r.timestamp < start_ts:  # go to next record
                    pass
                else:  # belong to this interval
                    cur_interval.append(r)
                i += 1
            self.intervaled_records.append(cur_interval)
            self.intervals.append((start, end))

        self.fvs = []
        # Merge each type of records in each interval into part of a feature vector like [max, avg, min]
        # and concatenate them according to the predefined order: METRICS_ORDER or only a throughput
        if not is_ycsb_log:
            for idx, interval in enumerate(self.intervaled_records):
                feature_vec = []
                type2value_map = {}
                for type in METRICS_ORDERED:
                    type2value_map[type] = []
                for r in interval:
                    type2value_map[r.type].append(r.value)
                for type in METRICS_ORDERED:
                    values = type2value_map[type]
                    if len(values) == 0:
                        features = [-1.0, -1.0, -1.0]  # Value Missing
                    else:
                        features = [max(values), float(sum(values)) / len(values), min(values)]  # max, avg, min
                    feature_vec += features
                self.fvs.append(feature_vec)
        else:
            for idx, interval in enumerate(self.intervaled_records):
                feature_vec = []
                type2value_map = {}
                for type in ['throughput']:
                    type2value_map[type] = []
                for r in interval:
                    type2value_map[r.type].append(r.value)
                for type in ['throughput']:
                    values = type2value_map[type]
                    if len(values) == 0:
                        features = [-1.0, -1.0, -1.0]  # Value Missing
                    else:
                        features = [max(values), float(sum(values)) / len(values), min(values)]  # max, avg, min
                    feature_vec += features
                self.fvs.append(feature_vec)


    def __len__(self):
        return len(self.fvs)


def process_pipeline(log_folder):
    """
    data processing pipeline
    :param log_folder:
    :return:  matrix of [[fv + throughput(max, avg, min)], ... ]
    """
    # Parse record
    m1 = MetricLogParser(log_folder + os.sep + 'log_m01')
    m2 = MetricLogParser(log_folder + os.sep + 'log_m02')
    m3 = MetricLogParser(log_folder + os.sep + 'log_m03')
    ycsb_records = YCSBLogParser(log_folder)

    # filtering by start & end time
    start_time = \
        max(m1.log_records[0].timestamp, m2.log_records[0].timestamp, m3.log_records[0].timestamp) + 1 * 60 * 60
    end_time = \
        min(m1.log_records[-1].timestamp, m2.log_records[-1].timestamp, m3.log_records[-1].timestamp) - 1 * 60 * 60
    print "overlapping internval: %d ~ %d" % (start_time, end_time)

    m_list = [m1, m2, m3]
    for m in m_list:
        l1 = len(m.log_records)
        m.filter(start_time, end_time)
        m.update_record_map()
        print l1, ">>>", len(m.log_records)
    ycsb_records.filter(start_time, end_time)

    # combine into intervals and transform into feature vector
    interval = 30
    fv_m1 = IntervaledSingleMachineFeatureVectors(m1.log_records, start_time, end_time, interval)
    fv_m2 = IntervaledSingleMachineFeatureVectors(m2.log_records, start_time, end_time, interval)
    fv_m3 = IntervaledSingleMachineFeatureVectors(m3.log_records, start_time, end_time, interval)
    throughputs = IntervaledSingleMachineFeatureVectors(
        ycsb_records.log_records,
        start_time,
        end_time,
        interval, is_ycsb_log=True
    )
    avg_throughput = np.array(map(lambda fv: fv[1], throughputs.fvs)).reshape(-1, 1)

    fv_mtx = np.concatenate(
        (np.array(fv_m1.fvs), np.array(fv_m2.fvs), np.array(fv_m3.fvs), avg_throughput),
        axis=1
    )
    return fv_mtx


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='log processing')
    parser.add_argument('--log_folder', type=str, help="path to the folder of log file for a single machine")
    args = parser.parse_args()

    log_folder = args.log_folder
    folder_name = log_folder.split(os.sep)[-2]
    fv_mtx = process_pipeline(log_folder)

    data_file_path = log_folder + os.sep + folder_name + ".numpy"
    with open(data_file_path, "w") as fh:
        np.save(fh, fv_mtx)
        print "Data matrix successfully saved at\n     %s" % data_file_path




