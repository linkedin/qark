import abc
import os

LIB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib")
PATH_TO_DECOMPILERS = os.path.join(LIB_PATH, "decompilers")


class ExternalDecompiler(object):
    __meta__ = abc.ABCMeta

    def __init__(self, name, path_to_decompiler, command=None):
        self.name = name.lower()
        self.path_to_decompiler = path_to_decompiler
        self.command = command


class CFR(ExternalDecompiler):
    def __init__(self):
        ExternalDecompiler.__init__(self,
                                    name="cfr",
                                    path_to_decompiler=os.path.join(PATH_TO_DECOMPILERS, "cfr_0_124.jar"),
                                    command="java -jar {path_to_decompiler} {jar} --outputdir {build_directory}/cfr")


class Procyon(ExternalDecompiler):
    def __init__(self):
        ExternalDecompiler.__init__(self,
                                    name="procyon",
                                    path_to_decompiler=os.path.join(PATH_TO_DECOMPILERS,
                                                                    "procyon-decompiler-1.0.jar"),
                                    command="java -jar {path_to_decompiler} {jar} -o {build_directory}/procyon")


class Fernflower(ExternalDecompiler):
    def __init__(self):
        ExternalDecompiler.__init__(self,
                                    name="fernflower",
                                    path_to_decompiler=os.path.join(PATH_TO_DECOMPILERS,
                                                                    "fernflower.jar"),
                                    command="java -jar {path_to_decompiler} -ren=1 {jar} {build_directory}/fernflower")


DECOMPILERS = (CFR(), Procyon(), Fernflower())
