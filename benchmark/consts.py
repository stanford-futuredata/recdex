from pathos.helpers import mp
import os

# We want only physical cores, not virtual cores. This means that we'll
# use every _other_ CPU in a given NUM node range
NUM_VIRTUAL_CORES_PER_POOL = 14


# Since we want only physical cores, we grab every other cpu id in the range
# [cpu_id_offset, cpu_id_offset + num_cores)
def get_cpu_assignments(cpu_id_offsets, num_cores):
    return (','.join(
        str(v)
        for v in range(cpu_id_offsets[0], cpu_id_offsets[0] + num_cores, 2)
    ) + ',' + ','.join(
        str(v)
        for v in range(cpu_id_offsets[1], cpu_id_offsets[1] + num_cores, 2)))


# From `lscpu` on raiders6:
#   CPU(s):                112
#   On-line CPU(s) list:   0-111
#   Thread(s) per core:    2
#   Core(s) per socket:    14
#   Socket(s):             4
#   NUMA node(s):          4
#   NUMA node0 CPU(s):     0-13,56-69
#   NUMA node1 CPU(s):     14-27,70-83
#   NUMA node2 CPU(s):     28-41,84-97
#   NUMA node3 CPU(s):     42-55,98-111

NUM_NUMA_NODES = 4

# When assigning cores to a given process, use NUMA_QUEUE
# to fetch in real-time an available NUMA node. This guarantees
# that we won't have any contention.
m = mp.Manager()
NUMA_QUEUE = m.Queue(NUM_NUMA_NODES)
numa_cpu_id_offsets = [(0, 56), (14, 70), (28, 84), (42, 98)]
for cpu_id_offsets in numa_cpu_id_offsets:
    NUMA_QUEUE.put(
        get_cpu_assignments(cpu_id_offsets, NUM_VIRTUAL_CORES_PER_POOL))

MODEL_DIR_BASE = '%s/models-simdex' % os.getenv('HOME')

TO_RUN = [
    ('lemp-paper/Netflix-noav-10', (10, 480189, 17770)),
    ('lemp-paper/Netflix-50', (50, 480189, 17770)),
    ('lemp-paper/Netflix-noav-50', (50, 480189, 17770)),
    ('lemp-paper/Netflix-noav-100', (100, 480189, 17770)),

    ('lemp-paper/KDD-50', (50, 1000990, 624961)),

    ('nomad/KDD-100-gold-standard', (100, 1000990, 624961)),

    ('nomad/R2-10-reg-1', (10, 1823179, 136736)),
    ('nomad/R2-10-reg-0.1', (10, 1823179, 136736)),
    ('nomad/R2-10-reg-0.01', (10, 1823179, 136736)),
    ('nomad/R2-10-reg-0.001', (10, 1823179, 136736)),

    ('nomad/R2-25-reg-1', (25, 1823179, 136736)),
    ('nomad/R2-25-reg-0.1', (25, 1823179, 136736)),
    ('nomad/R2-25-reg-0.01', (25, 1823179, 136736)),
    ('nomad/R2-25-reg-0.001', (25, 1823179, 136736)),

    ('nomad/R2-50-reg-1', (50, 1823179, 136736)),
    ('nomad/R2-50-reg-0.1', (50, 1823179, 136736)),
    ('nomad/R2-50-reg-0.01', (50, 1823179, 136736)),
    ('nomad/R2-50-reg-0.001', (50, 1823179, 136736)),

    ('nomad/R2-100-reg-1', (100, 1823179, 136736)),
    ('nomad/R2-100-reg-0.1', (100, 1823179, 136736)),
    ('nomad/R2-100-reg-0.01', (100, 1823179, 136736)),
    ('nomad/R2-100-reg-0.001', (100, 1823179, 136736)),

    #('pb-new/Netflix-10', (10, 480189, 17770)),
    #('pb-new/Netflix-10-iters-100', (10, 480189, 17770)),
    #('pb-new/Netflix-25', (25, 480189, 17770)),
    #('pb-new/Netflix-50', (50, 480189, 17770)),

    #('sigmod-deadline/Netflix-10', (10, 480189, 17770)),
    #('sigmod-deadline/Netflix-25', (25, 480189, 17770)),
    #('sigmod-deadline/Netflix-50', (50, 480189, 17770)),

    #('pb-new/kdd-10', (10, 1000990, 624961)),
    #('pb-new/kdd-25', (25, 1000990, 624961)),
    #('pb-new/kdd-50', (50, 1000990, 624961)),

    #('sigmod-deadline/kdd-10', (10, 1000990, 624961)),
    #('sigmod-deadline/kdd-25', (25, 1000990, 624961)),
    #('sigmod-deadline/kdd-50', (50, 1000990, 624961)),

    #('ramdisk/r2-10', (10, 1823179, 136736)),
    #('ramdisk/r2-25', (25, 1823179, 136736)),
    #('ramdisk/r2-50', (50, 1823179, 136736)),

    #('lemp-paper/IE-svd-10', (10, 7716114, 1322094)),
    #('lemp-paper/IE-svd-50', (50, 7716114, 1322094)),
    #('lemp-paper/IE-svd-100', (100, 7716114, 1322094)),

    #('lemp-paper/IE-nmf-10', (10, 7716114, 1322094)),
    #('lemp-paper/IE-nmf-50', (50, 7716114, 1322094)),
    #('lemp-paper/IE-nmf-100', (100, 7716114, 1322094)),
]
