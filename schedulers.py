class Scheduler(object):
    def feed_units(self, units):
        raise NotImplementedError()

    def feed_tasks(self, tasks):
        raise NotImplementedError()

    def get_order(self):
        ''' Returns list of tuples (<task index>, <compute node>) '''
        raise NotImplementedError()


class FCFSScheduler(Scheduler):
    def __init__(self):
        self.units = []
        self.tasks = []

    def feed_units(self, units):
        self.units = units

    def feed_tasks(self, tasks):
        self.tasks = tasks

    def get_order(self):
        res = []
        for i in range(len(self.tasks)):
            res.append((i, 2))
        return res

    def __str__(self):
        return 'FCFS'


class OptimalScheduler(FCFSScheduler):
    def __str__(self):
        return 'Optimal'
