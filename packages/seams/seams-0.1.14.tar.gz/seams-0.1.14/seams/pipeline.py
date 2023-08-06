#!/usr/bin/env python
from seams import Seams
from abc import ABC, abstractmethod
import os
import tempfile
import json

class Pipeline(object):

    @abstractmethod
    def run(**argsv):
        print("in run")
        pass
    
    def __init__(self, tenant_id, vertex_id, EMAIL, PASSWORD, URL=None):
        self.vertex_id = vertex_id
        self.tenant_id = tenant_id
        if URL:
            self.seams = Seams(URL)
        else:
            self.seams = Seams()
        self.seams.connect(EMAIL, PASSWORD)

    def update_status(self,status):
        vertex = self.seams.update_vertex(self.tenant_id, self.vertex_id, 'status', status)
        print(vertex)

    def run_pipeline(self):
        vertex = self.seams.get_vertex_by_id(self.tenant_id, self.vertex_id)
        return vertex['runParameters']

    def get_test_from_pipeline(self):
        vertex = self.seams.get_vertex_by_id(self.tenant_id, self.vertex_id)
        return vertex

    def update_pipeline_status_in_progress(self):
        status_update = self.seams.update_vertex(self.tenant_id, self.vertex_id, 'PipelineRun', {"status":"IN PROGRESS"})
        print(status_update)
    
    def update_pipeline_status_done(self):
        status_update = self.seams.update_vertex(self.tenant_id, self.vertex_id, 'PipelineRun', {"status":"DONE"})
        print(status_update)

    def update_pipeline_status_error(self):
        status_update = self.seams.update_vertex(self.tenant_id, self.vertex_id, 'PipelineRun', {"status":"ERROR"})
        print(status_update)

    def download_files(self):
        data = json.loads(self.seams.get_vertex_by_id(self.tenant_id, self.vertex_id)['runParameters'])
        files = []
        for item in data['Files']:
            download = self.seams.download_files(self.tenant_id, item['vertexId'])
            for item in download:
                temp_file_full_path = os.path.join(tempfile.gettempdir(), item)
                files.append(temp_file_full_path)
                f = open(temp_file_full_path, 'w', encoding="utf-8")
                f.write(download[item])
                f.close()
        return files
