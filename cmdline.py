import os


from data.model_types import *
from data_models.domain import *
from data_models.expression_model import *
from data_models.performance_map_model import *
from data_models.plane import *
from utils.utils import *
from utils.settings import *


def print_array(arr: list) -> None:
    for i, el in enumerate(arr, 1):
        print(f'{i}: {el}')


CSE = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'output.cse'
))


if __name__ == "__main__":
    print(CSE)

    plane_map = {
        1: 'YZ Plane', 2: 'ZX Plane', 3: 'XY Plane',
        4: 'Three Points', 5: 'Point and Normal'
    }

    perf_collection = PerformanceMapCollection()
    expr_collection = ExpressionCollectionCache()
    dmn_collection = DomainCollectionCache()

    print('Input folder name with out file: ', end='')
    outfile_dir = os.path.abspath(input())
    files = get_files(ext='out', directory=outfile_dir)
    if files:
        print('Files:')
        print_array([os.path.split(f)[1] for f in files])
    else:
        print(f'There are no out files in the directory {outfile_dir}')
        exit(-1)
    
    print('Select File: ', end='')
    file = files[int(input())-1]

    with open(file, 'r') as f:
        domains = builder(f)

    print('Selet domains to create performance maps (separated by coma):')
    print(domains.show_domains())
    data = domains.data()
    print('Domain:', end=' ')
    dmn_idx = [list(data.keys())[int(i)] for i in input().strip().split(sep=',')]

    print('Load template file (y/n): ', end='')
    if input().lower() == 'y':
        print('Enter template file full name: ', end='')
        tmp_file = input()
        with open(tmp_file, 'r') as fp:
            data = json.load(fp)

    print('Create plane(y/n):', end=' ')
    create_plane = True if input().lower() == 'y' else False
    plane_collection = PlaneCollection()
    idx = 0
    while create_plane:
        settings = {}
        print('Plane name:', end=' ')
        settings['plane'] = input()
        print('Select plane type:')
        for k, v in plane_map.items():
            print(f'{k}: {v}')
        print('Type:', end=' ')
        plane_id = int(input())
        settings['plane_type'] = plane_map[plane_id]
        settings.update(build_plane(plane_type=plane_map[plane_id]))
        plane = PlaneBuilder(plane_type=plane_map[plane_id])
        plane.buildPlane(**settings)
        plane_collection.add(plane.get_builder(), idx)
        idx += 1
        print('Create another plane (y/n):', end=' ')
        create_plane = True if input().lower() == 'y' else False

    with open(CSE, 'w') as cse:
        cse.write(str(plane_collection))
