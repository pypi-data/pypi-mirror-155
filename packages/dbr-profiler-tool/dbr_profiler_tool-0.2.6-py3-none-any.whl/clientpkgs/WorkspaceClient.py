import os
import logging
from clientpkgs.ScimClient import ScimClient
from core.logging_utils import LoggingUtils
from core import wmconstants
from core.dbclient import dbclient

class WorkspaceClient(dbclient):
    def get_list_notebooks(self, path):
        """ 
        Returns an array of json objects for notebooks in a path
        """
        # fetch all poolslist
        print(path)
        notebookList = self.get("/workspace/list", json_params={'path': path}, version='2.0').get('objects', [])
        return notebookList


    def get_all_notebooks(self):
        scimClient = ScimClient(self._configs)
        usersLst = scimClient.get_users()
        pathlst = []
        notebooklst = []
        for user in usersLst:
            pathlst.append('/Users/' + user['userName'])
            pathlst.append('/Repos/' + user['userName'])
        for path in pathlst:
            nblist = self.get_list_notebooks(path)
            for entity in nblist:
                if entity['object_type']=='DIRECTORY' or entity['object_type']=='REPO':
                    pathlst.append(entity['path'])
                elif entity['object_type']=='NOTEBOOK' or entity['object_type']=='FILE':
                    notebooklst.append(entity['path'])
        return notebooklst

