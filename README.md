# msds
How to run:
- python simulator.py
- output: for the 2 schedulers: list of (task, compute node) pairs chosen by the scheduler

Structure of code
- Simulators (class DCSimulator) are created with a scheduler object
- Before running tests, simulators pass the info about compute nodes and tasks to their schedulers
- While running tests, simulators call their schedulers to get the sequence of task_id and node_id to run next
- All schedulers subclass the Scheduler class (that uses the terminology of boxes and rectangles)

Potential future extensions:
- Inputs: add an Input class that can handle both hardcoded lists, files, (random) generators, etc., so that an instance of Input can be passed to the Simulator constructor
- Handle streams of resources and tasks instead of lists by adding time intervals between tuples, e.g (2,3) t1 (3,1) t2 etc. This would require few modifications (multiple calls to feed_units() and feed_tasks(), and get_order() would need to be called every second)
- Taking width of boxes (pls see schedulers.py for terminology) into consideration in get_order()

Other notes:
- For the current input OptimalScheduler outperforms FCFSScheduler by about 30%; to try different inputs pls modify lines 70 & 71 in simulator.py
