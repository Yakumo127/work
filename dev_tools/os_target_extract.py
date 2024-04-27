from dev_tools.utils import LuaLoader

FILE_TO_ZONES = {
    11: [44, 84, 125, 95, 104, 52],
    21: [22, 134, 32, 94, 142, 53],
    31: [83, 122, 135, 143, 63, 54],
    32: [23, 62, 114, 51, 41, 14],
    33: [21, 31, 66, 113, 65, 85],
    41: [43, 112, 34, 133, 61, 71],
    51: [81, 132, 123, 105, 91, 64],
    61: [12, 73, 101, 11, 72, 106],
    71: [102, 124, 144, 121, 153, 155],
    81: [24, 92, 111, 25, 82, 42],
    91: [151, 152, 158, 159, 157, 156],
    101: [93, 131, 141, 33, 103, 13]
}
# (code, i) means file in this zone has number code and needs i previous files to be collectable.
ZONE_TO_FILE = {locations[i]: (code, i) for code, locations in FILE_TO_ZONES.items() for i in range(6)}

SAFE = ['Perform', 'Obtain', 'Collect', 'Conduct', 'Use', 'Encounter']
DANGER = ['Gain', 'Defeat', 'Restore', 'Destroy', 'Repel', 'Activate', 'Retrieve']  
# 'Recover' is target for file.

class OSTarget:
    def __init__(self):
        self.target = {}
        counter = 0
        for index, desc in DATA.items():
            if not isinstance(index, int) or index // 100 == 154:  # skip 154, which is not really used.
                continue
            if index % 100 == 1:
                self.target[index // 100] = []
        
        for index, desc in self.extract_target_desc().items():
            target = self.desc_to_target_type(desc)
            if target is None:
                self.target[index // 100].append(ZONE_TO_FILE[index // 100])
            else:
                self.target[index // 100].append(target)

    def extract_target_desc(self):
        out = {}
        for index, target in DATA.items():
            if not isinstance(index, int) or index // 100 == 154:  # skip 154, which is not really used.
                continue
            name = target['target_desc']
            out[index] = name
        
        return out
        
    def desc_to_target_type(self, str):
        word = str.split()[0]
        if word in SAFE:
            return True
        if word in DANGER:
            return False
        else:  # is File
            return None
            

    def encode(self):
        lines = []
        lines.append('# This file was automatically generated by dev_tools/os_target_extract.py.')
        lines.append("# Don't modify it manually.")
        lines.append('')
        lines.append('DIC_OS_TARGET = {')
        for index, target in self.target.items():
            lines.append(f'    {index}: {str(target)},')
        lines.append('}')
        return lines

    def write(self, file):
        print(f'writing {file}')
        with open(file, 'w', encoding='utf-8') as f:
            for text in self.encode():
                f.write(text + '\n')

"""
This an auto-tool to extract map data for operation siren.

Git clone https://github.com/AzurLaneTools/AzurLaneLuaScripts, to get the decrypted scripts.
Arguments:
    FILE:  Path to repository, such as 'xxx/AzurLaneLuaScripts'
    SAVE:  File to save, 'module/os/map_data.py'
"""
FILE = '../AzurLaneLuaScripts'
SAVE = 'module/os_handler/target_data.py'


LOADER = LuaLoader(FILE, server='EN')
DATA = LOADER.load('./sharecfg/world_target_data.lua')
OSTarget().write(SAVE)