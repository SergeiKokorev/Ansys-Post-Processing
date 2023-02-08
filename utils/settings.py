def build_plane(plane_type: str) -> dict:

    plane_offset = {
        'yz plane': 'x', 'zx plane': 'y', 'xy plane': 'z'
    }

    settings = {}
    if plane_type.lower() == 'three points':
        settings['points'] = []
        print('Enter point coordinates x, y, z separated with coma')
        for i in range(1, 4):
            print(f'Enter point {i}:', end=' ')
            settings['points'].append([float(p.strip()) for p in input().split(',')])
    elif plane_type.lower() == 'point and normal':
        print('Input point coordinates separated with coma:', end=' ')
        settings['point'] = [float(p.strip()) for p in input().split(',')]
        print('Input normal x, y and z direction separated with coma', end=' ')
        settings['normal'] = [float(p.strip()) for p in input().split(',')]
    elif plane_type.lower() in ['yz plane', 'zx plane', 'xy plane']:
        print(f'Enter offset {plane_offset[plane_type.lower()]}:', end=' ')
        settings['offset'] = float(input())
        settings['plane_type'] = plane_type
    else:
        return {}
    
    return settings

