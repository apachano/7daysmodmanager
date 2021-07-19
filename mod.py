import os
import shutil
import xml.etree.ElementTree as ET

dir_active = os.path.expanduser('~/.steam/debian-installation/steamapps/common/7 Days To Die/Mods')
dir_library = os.path.expanduser('~/.steam/debian-installation/steamapps/common/7 Days To Die/ModLibrary')


def get_mods():
    library = {}
    mods = os.listdir(dir_library)
    mods.sort()

    for mod in mods:
        library[mod] = (Mod(mod))

    return library


class Mod:
    __active = []
    library = {}

    def __init__(self, directory: os.path):
        self.directory = directory
        self.name = ""
        self.version = ""
        self.authors = []
        self.website = ""

        mod_info_path = f'{self.get_library_path()}/ModInfo.xml'
        if os.path.exists(mod_info_path):
            data = ET.parse(mod_info_path).getroot()
            for element in data[0]:
                if element.tag == 'Name':
                    self.name = element.attrib["value"]
                elif element.tag == 'Description':
                    self.description = element.attrib["value"]
                elif element.tag == 'Author':
                    self.authors.append(element.attrib["value"])
                elif element.tag == 'Version':
                    self.version = element.attrib["value"]
                elif element.tag == 'Website':
                    self.website = element.attrib["value"]

        for mod in os.listdir(dir_active):
            if mod[4:] == directory:
                self.__active.append(self)
                if int(mod[:3]) != self.get_index():
                    shutil.move(f'{dir_active}/{mod}', self.get_active_path())

        self.library[self.directory] = self

    def __repr__(self):
        return self.name or self.directory

    def sort(self):
        for active in os.listdir(dir_active):
            mod = self.library[active[4:]]
            if int(active[:3]) != mod.get_index():
                shutil.move(f'{dir_active}/{active}', mod.get_active_path())

    def get_library_path(self):
        return f'{dir_library}/{self.directory}'

    def get_active_path(self):
        return f'{dir_active}/{self.get_index():03}-{self.directory}'

    def get_index(self):
        return self.__active.index(self)

    @staticmethod
    def get_active_mods():
        return Mod.__active.copy()

    def activate(self):
        self.__active.append(self)
        shutil.copytree(self.get_library_path(), self.get_active_path())

    def deactivate(self):
        shutil.rmtree(self.get_active_path())
        self.__active.remove(self)
        self.sort()

    def inc_priority(self):
        i = self.get_index()
        self.__active.insert(i - 1, self.__active.pop(i))
        self.sort()

    def dec_priority(self):
        self.__active.insert(self.get_index() + 1, self.__active.pop(self.get_index()))
        self.sort()

    def is_active(self):
        return self in self.__active
