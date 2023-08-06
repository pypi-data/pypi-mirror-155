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
        #try/catch to do this work
        #set pipeline status
        #download files
        pass
    
    def __init__(self, tenant_id, vertex_id, EMAIL, PASSWORD, URL=None):
        self.vertex_id = vertex_id
        self.tenant_id = tenant_id
        self.files = []
        if URL:
            self.seams = Seams(URL)
        else:
            self.seams = Seams()
        self.seams.connect(EMAIL, PASSWORD)

    def run_pipeline(self):
        return self.seams.get_vertex_by_id(self.tenant_id, self.vertex_id)['runParameters']

    def get_test_from_pipeline(self):
        return self.seams.get_vertex_by_id(self.tenant_id, self.vertex_id)

    def update_pipeline_status_in_progress(self):
        return self.seams.update_vertex(self.tenant_id, self.vertex_id, 'PipelineRun', {"status":"IN PROGRESS"})
    
    def update_pipeline_status_done(self):
        return self.seams.update_vertex(self.tenant_id, self.vertex_id, 'PipelineRun', {"status":"DONE", "runResults": self.files})

    def update_pipeline_status_error(self):
        return self.seams.update_vertex(self.tenant_id, self.vertex_id, 'PipelineRun', {"status":"ERROR"})

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
    
    def upload_files(self, caption, files):
        return self.seams.upload_files(self.tenant_id, caption, files)

    def get_uploaded_files(self):
        return self.files

    def add_new_file(self, file_vertex_id, label, name):
        new_file = {
            "vertexId": file_vertex_id,
            "label": label, 
            "name": name
        }
        self.files.append(new_file)

