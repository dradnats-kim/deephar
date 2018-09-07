import numpy as np

class _pa16j():
    """Pose alternated with 16 joints (like Penn Action with three more
    joints on the spine.
    """
    num_joints = 16

    """Horizontal flip mapping"""
    map_hflip = [0, 1, 2, 3, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12, 15, 14]

    """Projections from other layouts to the PA16J standard"""
    map_from_mpii = [6, 7, 8, 9, 12, 13, 11, 14, 10, 15, 2, 3, 1, 4, 0, 5]
    map_from_ntu = [0, 20, 2, 3, 8, 4, 9, 5, 10, 6, 16, 12, 17, 13, 18, 14]

    """Projections of PA16J to other formats"""
    map_to_pa13j = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    map_to_jhmdb = [2, 1, 3, 4, 5, 10, 11, 6, 7, 12, 13, 8, 9, 14, 15]
    map_to_mpii = [14, 12, 10, 11, 13, 15, 0, 1, 2, 3, 8, 6, 4, 5, 7, 9]

    """Color map"""
    color = ['g', 'r', 'b', 'y', 'm']
    cmap = [0, 0, 0, 0, 1, 2, 1, 2, 1, 2, 3, 4, 3, 4, 3, 4]
    links = [[0, 1], [1, 2], [2, 3], [4, 6], [6, 8], [5, 7], [7, 9],
            [10, 12], [12, 14], [11, 13], [13, 15]]

class _pa17j():
    """Pose alternated with 17 joints (like _pa16j, with the middle spine).
    """
    num_joints = 17

    """Horizontal flip mapping"""
    map_hflip = [0, 1, 2, 3, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12, 15, 14, 16]

    """Projections from other layouts to the PA17J standard"""
    map_from_h36m = \
            [0, 12, 13, 15, 25, 17, 26, 18, 27, 19, 1, 6, 2, 7, 3, 8, 11]

    """Projections of PA17J to other formats"""
    map_to_mpii = [14, 12, 10, 11, 13, 15, 0, 1, 2, 3, 8, 6, 4, 5, 7, 9]
    map_to_pa16j = list(range(16))

    """Color map"""
    color = ['g', 'r', 'b', 'y', 'm']
    cmap = [0, 0, 0, 0, 1, 2, 1, 2, 1, 2, 3, 4, 3, 4, 3, 4, 0]
    links = [[0, 16], [16, 1], [1, 2], [2, 3], [4, 6], [6, 8], [5, 7], [7, 9],
            [10, 12], [12, 14], [11, 13], [13, 15]]

class _pa20j():
    """Pose alternated with 20 joints. Similar to _pa16j, but with one more
    joint for hands and feet.
    """
    num_joints = 20

    """Horizontal flip mapping"""
    map_hflip = [0, 1, 2, 3, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12, 15, 14, 17, 16,
            19, 18]

    """Projections from other layouts to the PA20J standard"""
    map_from_h36m = [0, 12, 13, 15, 25, 17, 26, 18, 27, 19, 30, 22, 1, 6, 2,
            7, 3, 8, 4, 9]
    map_from_ntu = [0, 20, 2, 3, 8, 4, 9, 5, 10, 6, 11, 7, 16, 12, 17, 13, 18,
            14, 19, 15]

    """Projections of PA20J to other formats"""
    map_to_mpii = [16, 14, 12, 13, 15, 17, 0, 1, 2, 3, 8, 6, 4, 5, 7, 9]

    """Color map"""
    color = ['g', 'r', 'b', 'y', 'm']
    cmap = [0, 0, 0, 0, 1, 2, 1, 2, 1, 2, 1, 2, 3, 4, 3, 4, 3, 4, 3, 4]
    links = [[0, 1], [1, 2], [2, 3], [4, 6], [6, 8], [8, 10], [5, 7], [7, 9],
            [9, 11], [12, 14], [14, 16], [16, 18], [13, 15], [15, 17], [17, 19]]

class pa16j2d(_pa16j):
    dim = 2

class pa16j3d(_pa16j):
    dim = 3

class pa17j2d(_pa17j):
    dim = 2

class pa17j3d(_pa17j):
    dim = 3

class pa20j3d(_pa20j):
    dim = 3

class ntu25j3d():
    num_joints = 25
    dim = 3


def _func_and(x):
    if x.all():
        return 1
    return 0

def get_visible_joints(x):
    visible = np.apply_along_axis(_func_and, axis=1, arr=(x > 0.))
    visible *= np.apply_along_axis(_func_and, axis=1, arr=(x < 1.))
    return visible

def get_valid_joints(x):
    return np.apply_along_axis(_func_and, axis=1, arr=(x > -1e6))

def convert_pa17j3d_to_pa16j(p, dim=3):
    assert p.shape == (pa17j3d.num_joints, pa17j3d.dim)
    return p[pa17j3d.map_to_pa16j,0:dim].copy()

def convert_sequence_pa17j3d_to_pa16j(seqp, dim=3):
    assert seqp.shape[1:] == (pa17j3d.num_joints, pa17j3d.dim)
    x = np.zeros((len(seqp), _pa16j.num_joints, dim))
    for i in range(len(seqp)):
        x[i,:] = convert_pa17j3d_to_pa16j(seqp[i], dim=dim)
    return x

def write_poselist(filename, poses):
    """ Write a pose list to a text file.
    In the text file, every row corresponds to one pose and the columns are:
    {x1, y1, x2, y2, ...}

        Inputs: 'filename'
                'poses' [nb_samples, nb_joints, 2]
    """
    nb_samples, nb_joints, dim = poses.shape
    x = poses.copy()
    x = np.reshape(x, (nb_samples, nb_joints * dim))
    np.savetxt(filename, x, fmt='%.6f', delimiter=',')

