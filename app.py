# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import os
from sgtk.platform import Application
from tank import TankError

import MaxPlus


class RunMaxScript(Application):
    """
    The app entry point. This class is responsible for intializing and tearing down
    the application, handle menu registration etc.
    """

    def init_app(self):
        """
        Called as the application is being initialized
        """

        # now register a *command*, which is normally a menu entry of some kind on a Shotgun
        # menu (but it depends on the engine). The engine will manage this command and 
        # whenever the user requests the command, it will call out to the callback.

        for item in self.get_setting("max_scripts"):

            # Only allow configured contexts
            if self.context.entity["type"] not in item["context"]:
                continue

            # define properties
            p = {"script": item["path"],
                 "replacements": item["replacements"]}

            cb = lambda: self.run_maxscript(p)

            # now register the command with the engine
            self.engine.register_command(item["menu_name"], cb)

    def __get_config_path(self):
        path = self.shotgun.find_one("PipelineConfiguration", [["project", "is", self.context.project],
                                              ["code", "is", self.sgtk.configuration_name]], ["windows_path"])
        return path["windows_path"]

    def run_maxscript(self, properties):
        script = properties["script"]

        if not os.path.exists(script):
            raise TankError("Cannot run script: '%s' does not exist." % script)

        script = "".join(open(script, "r").readlines())

        for k, v in properties["replacements"].iteritems():
            if v.startswith("resources/"):
                v = os.path.join(self.__get_config_path(), "config", v).replace("\\", "/")

            script = script.replace(k, v)

        context_params = ["param_project_name", "param_entity_name", "param_task_name"]
        ctx = self.context
        for key in context_params:
            if script.find(key) != -1:
                if key == "param_project_name":
                    script = script.replace(key, ctx.project["name"])
                if key == "param_entity_name":
                    script = script.replace(key, ctx.entity["name"])
                if key == "param_task_name":
                    script = script.replace(key, ctx.task["name"])

        MaxPlus.Core.EvalMAXScript(script)
