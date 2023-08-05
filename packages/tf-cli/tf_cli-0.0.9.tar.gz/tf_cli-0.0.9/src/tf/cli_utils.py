#!/bin/python3
import os
import sys

from dataclasses import dataclass
from enum import Enum

from .api_methods import logger

# Path Info 
class PATH_UTILS(Enum):
    SCRIPT_DIR = "scripts/"
    SCRIPT_BUID = "build.sh"
    SCRIPT_COMMIT = "commit.sh"
    SCRIPT_PUSH = "push.sh"
    SCRIPT_CLEAN = "clean.sh"

@dataclass
class CLI_Utils():
    path:str = os.path.dirname(os.path.realpath(__file__))
    script_path:str = os.path.realpath( os.path.join(path, PATH_UTILS.SCRIPT_DIR.value) )

    def build(self) -> None:
        logger.info("Build is running...")
        self.__exe__(script_name=PATH_UTILS.SCRIPT_BUID.value)
                         
    def commit(self) -> None:
        logger.info("Commit is running...")
        self.__exe__(script_name=PATH_UTILS.SCRIPT_COMMIT.value)

    def push(self) -> None:
        logger.info("Push is running...")
        self.__exe__(script_name=PATH_UTILS.SCRIPT_PUSH.value)

    def clean(self) -> None:
        logger.info("Clean is running...")
        self.__exe__(script_name=PATH_UTILS.SCRIPT_CLEAN.value)

    def __exe__(self, script_name) -> None:
        tmp_path = os.path.realpath( os.path.join(self.script_path, script_name) )

        if os.path.exists(tmp_path):
            os.system(tmp_path)
        else:
            logger.error("Internal Error: Path does not exist")

