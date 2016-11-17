class Scheduler(object):
    '''The problem is equivalent to fitting rectangles into boxes
    of different widths. Thus, using the corresponding terminology. '''

    def __init__(self):
        # box_id to sorted-list-of-heights
        self.boxes = {}

        # rect_id to width-and-height
        self.rectangles = {}

    def feed_units(self, units):
        id_to_width = {}
        for _id, width in units:
            old_width = id_to_width.get(_id, 0)
            id_to_width[_id] = old_width + width
        for _id, width in id_to_width.iteritems():
            self.boxes[_id] = ([0] * width)

    def feed_tasks(self, tasks):
        for i, task in enumerate(tasks):
            self.rectangles[i] = {
                'width': task[0],
                'height': task[1]
            }

    def get_best_box(self, rect):
        width = rect['width']

        best_id = -1
        best_start_time = -1
        for _id, box in self.boxes.iteritems():
            if len(box) < width:
                continue
            # since box is sorted,
            # the current rectangle will fit right after the <width>th vertical
            start_time = box[width - 1]
            if best_start_time == -1 or start_time < best_start_time:
                best_id = _id
                best_start_time = start_time

        return (best_id, best_start_time)

    # puts the rectangle on top of box & resorts it
    def schedule(self, rect_id, box_id):
        width = self.rectangles[rect_id]['width']
        height = self.rectangles[rect_id]['height']

        box = self.boxes[box_id]
        for i in range(width):
            box[i] = box[width-1] + height
        box.sort()
        self.rectangles.pop(rect_id)

    def get_order(self):
        ''' Returns list of tuples (<task index>, <compute node>) '''
        raise NotImplementedError()


class FCFSScheduler(Scheduler):
    def __str__(self):
        return 'FCFS'

    def get_order(self):
        result = []

        steps = len(self.rectangles)
        for i in range(steps):
            rect = self.rectangles[i]
            best_box = self.get_best_box(rect)

            rect_id = i
            box_id = best_box[0]
            result.append((rect_id, box_id))
            self.schedule(rect_id, box_id)

        return result


class OptimalScheduler(Scheduler):
    def __str__(self):
        return 'Optimal'

    def get_order(self):
        result = []

        steps = len(self.rectangles)
        for _ in range(steps):
            rect_summaries = []
            for _id, rect in self.rectangles.iteritems():
                best_box = self.get_best_box(rect)
                rect_summaries.append({
                    'rect_id': _id,
                    'box_id': best_box[0],
                    'start_time': best_box[1],
                    'width': rect['width'],
                    'height': rect['height']
                })

            # we want the rectangle that:
            # - goes lowest into a box (starts soonest)
            # - out of those: takes widest area (requires most units)
            # - out of those: shortest (takes least time)
            rect_summaries.sort(key = lambda item: (item['start_time'], -item['width'], item['height']))
            next_rect_id = rect_summaries[0]['rect_id']
            next_box_id  = rect_summaries[0]['box_id']

            result.append((next_rect_id, next_box_id))
            self.schedule(next_rect_id, next_box_id)

        return result
