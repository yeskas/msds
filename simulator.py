from schedulers import FCFSScheduler, OptimalScheduler


class Node(object):
    '''Compute Node Simulator'''
    def __init__(self, unit_count):
        # self.times is how much time is left for a unit to run
        self.times = []
        for _ in range(unit_count):
            self.times.append(0)

    def can_assign(self, units_needed):
        zeros = 0
        for _time in self.times:
            if _time == 0:
                zeros += 1
        return zeros >= units_needed

    def assign(self, units_needed, time_needed):
        assert self.can_assign(units_needed)
        for i, _time in enumerate(self.times):
            if _time == 0:
                self.times[i] = time_needed
                units_needed -= 1
                if units_needed == 0:
                    break

    def second_passed(self):
        for i, _time in enumerate(self.times):
            if _time > 0:
                self.times[i] -= 1

    def complete(self):
        time_left = max(self.times)
        for i in range(len(self.times)):
            self.times[i] = 0
        return time_left


class DCSimulator(object):
    def __init__(self, sched):
        self.sched = sched
        self.nodes = {}
        self.total_time = 0

    def init_nodes(self, units):
        node_to_count = {}
        for node_id, count in units:
            old_count = node_to_count.get(node_id, 0)
            node_to_count[node_id] = old_count + count
        for node_id, count in node_to_count.iteritems():
            self.nodes[node_id] = Node(count)

    def second_passed(self):
        for node in self.nodes.values():
            node.second_passed()
        self.total_time += 1

    def complete_tasks(self):
        time_left = 0
        for node in self.nodes.values():
            node_time_left = node.complete()
            time_left = max(time_left, node_time_left)
        self.total_time += time_left

    def run(self):
        print '%s scheduler\'s performance:' % self.sched

        # hardcoded input for now
        units = [(2,3), (7,3), (1,3)]
        tasks = [(2,11), (2,12), (2,13), (3,1), (1,7), (1,8), (1,9)]
        self.init_nodes(units)

        # scheduler algorithm
        self.sched.feed_units(units)
        self.sched.feed_tasks(tasks)
        order = self.sched.get_order()
        assert len(order) == len(tasks)

        # run based on scheduler's order
        for task_idx, node_id in order:
            task = tasks[task_idx]
            node = self.nodes[node_id]
            print 'next: task #%d (%s) on node #%d' % (task_idx, task, node_id)

            units_needed, time_needed = task
            while not node.can_assign(units_needed):
                print 'node\'s times left:', node.times
                self.second_passed()
            node.assign(units_needed, time_needed)

        self.complete_tasks()
        print 'Overall time for %s: %d seconds\n' % (self.sched, self.total_time)


if __name__ == '__main__':
    sched1 = FCFSScheduler()
    sim1 = DCSimulator(sched1)
    sim1.run()

    sched2 = OptimalScheduler()
    sim2 = DCSimulator(sched2)
    sim2.run()
