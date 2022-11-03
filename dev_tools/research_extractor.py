from module.logger import logger  # Change folder automatically
from dev_tools.utils import LuaLoader, FOLDER, temp_render


class Item:
    def __init__(self, data):
        """
        Args:
            data (dict): Such as {0: 2, 1: 20001, 2: 5}
        """
        self.name = ''
        _, self.id, self.amount = data.values()
        if self.id == 1:
            self.id = 59001  # The id of coins is 1 in technology_data_template, but 59001 in item_data_statistics

    def __str__(self):
        return f'{self.name}({self.id}) x {self.amount}'


class Task:
    def __init__(self, data):
        self.name = ''
        self.id = data


class Project:
    def __init__(self, data):
        """
        Args:
            data (dict):
        """
        self.name = data['name']
        self.series = int(data['blueprint_version'])
        self.time = int(data['time'])
        self.input = [Item(item) for item in data['consume'].values()]
        self.output = [Item(item) for item in data['drop_client'].values()]
        self.task = Task(int(data['condition']))

    def encode(self):
        data = {
            'name': self.name,
            'series': self.series,
            'time': self.time,
            'task': self.task.name,
            'input': [{'name': item.name, 'amount': item.amount} for item in self.input],
            'output': [{'name': item.name} for item in self.output],
        }
        return str(data)


# Key: chinese, value: english
DIC_TRANSLATION = {
    '蓝图：安克雷奇': 'Blueprint - Anchorage',
    '蓝图：{namecode:204}': 'Blueprint - Hakuryuu',
    '蓝图：埃吉尔': 'Blueprint - Ägir',
    '蓝图：奥古斯特·冯·帕塞瓦尔': 'Blueprint - August von Parseval',
    '蓝图：马可波罗': 'Blueprint - Marco Polo',
}


def set_translation(cn, en):
    if len(cn) and len(en):
        if cn not in DIC_TRANSLATION:
            DIC_TRANSLATION[cn] = en


class TechnologyTemplate:
    def __init__(self):
        self.projects = self.load_projects(LuaLoader(FOLDER, server='zh-CN'))
        en_projects = self.load_projects(LuaLoader(FOLDER, server='en-US'))

        for key, project in self.projects.items():
            if key not in en_projects:
                continue
            en_project = en_projects[key]
            set_translation(cn=project.task.name, en=en_project.task.name)
            for item, en_item in zip(project.input, en_project.input):
                set_translation(cn=item.name, en=en_item.name)
            for item, en_item in zip(project.output, en_project.output):
                set_translation(cn=item.name, en=en_item.name)

        for project in self.projects.values():
            project.task.name = DIC_TRANSLATION.get(project.task.name, project.task.name)
            for item in project.input:
                # Change Ägir to Agir
                item.name = DIC_TRANSLATION.get(item.name, item.name).replace('Ä', 'A')
            for item in project.output:
                item.name = DIC_TRANSLATION.get(item.name, item.name).replace('Ä', 'A')

    def load_projects(self, loader):
        tech = loader.load('sharecfg/technology_data_template.lua')
        item = loader.load('sharecfgdata/item_data_statistics.lua')
        task = loader.load('sharecfgdata/task_data_template.lua')

        projects = {}
        for key, value in tech.items():
            if key == 'all':
                continue
            project = Project(value)
            if project.task.id:
                project.task.name = task[project.task.id]['desc'].replace('\\n', '')
            for i in project.input:
                i.name = item[i.id]['name'].strip()
            for i in project.output:
                i.name = item[i.id]['name'].strip()

            key = (project.series, project.name)
            if key not in projects:
                projects[key] = project

        return projects

    def encode(self):
        lines = []
        for project in self.projects.values():
            lines.append('    ' + project.encode() + ',')
        return lines

    def write(self, file):
        print(f'writing {file}')
        with open(file, 'w', encoding='utf-8') as f:
            for text in self.encode():
                f.write(text + '\n')

    def write_template(self, file):
        print(f'writing {file}')
        res = temp_render('research', Data=self.encode())
        with open(file, 'w', encoding='utf-8') as f:
            f.write(res)


"""
This an auto-tool to extract research projects used in Alas.

Git clone https://github.com/AzurLaneTools/AzurLaneLuaScripts, to get the decrypted scripts.
Arguments:
    FILE:  Path to AzurLaneData, '<your_folder>/AzurLaneData'
    SAVE:  File to save, 'module/research/project_data.py'
"""
SAVE = 'module/research/project_data.py'

TechnologyTemplate().write_template(SAVE)
