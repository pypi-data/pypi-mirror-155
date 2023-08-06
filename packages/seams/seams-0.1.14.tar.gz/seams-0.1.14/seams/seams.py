#!/usr/bin/env python
from requests import Request, Session
from seams.exceptions import SeamsException, SeamsAPIException

class Seams(object):
    '''
    A Python interface for the Seams API
    '''
    
    def __init__(self, 
                 URL='https://seams-dev-api.rjlglims.com/api'):
        '''
        Create an instance of the Seams API interface
        '''

        self.URL = URL
        self.connected = False


    def connect(self, 
                email, 
                password):
        '''
        Connect to the Seams API 
        :param email:
            The login email for the Seams API  **REQUIRED**
        :param password:
            The login password for the Seams API  **REQUIRED**
        :returns:
            A vertex
        '''

        body = {'email': email, 'password': password}
        session = Session()
        request = Request('POST', '{}/auth/sign-in'.format(self.URL), data=body)
        prepared = session.prepare_request(request)
        response = session.send(prepared)
        if response.text == 'Authentication failed: User or password is incorrect':
            raise SeamsAPIException(response.text)
        else:
            self.bearer = response.text
            self.email = email
            self.connected = True


    def disconnect(self):
        '''
        Disconnect from the Seams API 
        '''
        self.bearer = None
        self.email = None
        self.connected = False


    def me(self):
        '''
        Verifies the user is connected and returns data relating to the graph database

        :returns:
            JSON object representing the graph database
        '''
        
        try:
            response = self.__http_request(self.bearer, 'GET', '{}/auth/me'.format(self.URL))
        except:
            raise SeamsAPIException(response)
        return response.json()


    def whoami(self):
        '''
        Gives info on the connection information of the current Seams object

        :returns:
            The bearer token, URL, email and password
        '''

        try:
            response = {
                'bearer': self.bearer,
                'url': self.URL,
                'email': self.email,
                'connected': self.connected
            }
            return response
        except:
            return {'url': self.URL, 'connected': self.connected}


    def get_vertex_by_id(self, 
                         tenant_id, 
                         vertex_id):
        '''
        Get a vertex by vertex id

        :param tenant_id:
            The id of the tenant the search is on  **REQUIRED**
        :param vertex_id:
            The vertex id of the node the user is getting  **REQUIRED**
        :returns:
            A vertex
        '''

        try:
            response = self.__http_request(self.bearer, 'GET', '{}/tenant/{}/vertex/{}'.format(self.URL, tenant_id, vertex_id))
            return response.json()
        except:
            raise SeamsAPIException(response.text)
    

    def get_vertices_by_label(self, 
                              tenant_id, 
                              vertex_label):
        '''
        Get all vertices with a specific label

        :param tenant_id:
            The id of the tenant the search is on  **REQUIRED**
        :param vertex_label:
            The label of the vertex the user is getting  **REQUIRED**
        :returns:
            JSON formatted list of vertices
        '''

        try:
            response = self.__http_request(self.bearer, 'GET', '{}/tenant/{}/vertices/{}'.format(self.URL, tenant_id, vertex_label))
            return response.json()
        except:
            raise SeamsAPIException(response)


    def update_vertex(self, 
                      tenant_id, 
                      vertex_id, 
                      vertex_label, 
                      attributes):
        '''
        Update a vertex 

        :param tenant_id:
            The id of the tenant the update is on  **REQUIRED**
        :param vertex_id:
            The vertex id of the node the user is getting  **REQUIRED**
        :param vertex_label:
            The label of the vertex the user is getting  **REQUIRED**
        :param attributes:
            A dictionary of key/value pairs that will represent the data fields of the vertex  **REQUIRED**
        :returns:
            JSON formatted vertex with the updates
        '''

        body = self.__properties_formatter(vertex_label, attributes)
        try:
            response = self.__http_request(self.bearer, 'PUT', '{}/tenant/{}/vertex/update/{}'.format(self.URL, tenant_id, vertex_id), content='application/json', data=body)
            return response.json()
        except:
            raise SeamsAPIException(response.text)


    def create_vertex(self, 
                      tenant_id, 
                      vertex_label, 
                      attributes=None):
        '''
        Create a vertex

        :param tenant_id:
            The id of the tenant the creation is on  **REQUIRED**
        :param vertex_label:
            The label of the vertex the user is getting  **REQUIRED**
        :param attributes:
            A dictionary of key/value pairs that will represent the data fields of the vertex  **REQUIRED**
        :returns:
            A JSON formatted object representing the new vertex
        '''
        body = {}
        if attributes:
            body = self.__properties_formatter(vertex_label, attributes)
        try:
            response = self.__http_request(self.bearer, 'POST', '{}/tenant/{}/vertex/create'.format(self.URL, tenant_id), content='application/json', data=body)
            return response.json()
        except:
            raise SeamsAPIException(response.text)


    def delete_vertex(self, 
                      tenant_id, 
                      vertex_id):
        '''
        Delete a vertex

        :param tenant_id:
            The id of the tenant the delete is on  **REQUIRED**
        :param vertex_id:
            The vertex id of the node the user is getting  **REQUIRED**
        :returns:
            A message specifying if the delete was successful or not
        '''

        try:
            response = self.__http_request(self.bearer, 'DELETE', '{}/tenant/{}/vertex/delete/{}'.format(self.URL, tenant_id, vertex_id))
            return response.text
        except:
            raise SeamsAPIException(response.text)
        

    def get_edges_on_vertex(self, 
                            tenant_id, 
                            vertex_id, 
                            edge_label, 
                            direction):
        '''
        Retreive all edges on a vertex based on direction

        :param tenant_id:
            The id of the tenant the search is on  **REQUIRED**
        :param vertex_id:
            The vertex id of the node the user is getting  **REQUIRED**
        :param edge_label:
            The edge label the user is looking for  **REQUIRED**
        :param direction:
            The direction of the edge  **REQUIRED**
        :returns:
            A JSON formatted list of all edges on a vertex
        '''

        try:
            response = self.__http_request(self.bearer, 'GET', '{}/tenant/{}/edgeVertices/{}/{}/{}'.format(self.URL, tenant_id, vertex_id, edge_label, direction))
            return response.json()
        except:
            raise SeamsAPIException(response.text)
        

    def attach_edges(self, 
                    tenant_id, 
                    parent_id, 
                    edge_name, 
                    child_vertices):
        '''
        Attach edge from one vertex to another

        :param tenant_id:
            The id of the tenant the search is on  **REQUIRED**
        :param parent_id:
            The vertex id of the parent vertex  **REQUIRED**
        :param edge_name:
            The name of the new edge  **REQUIRED**
        :param child_vertices:
            A list of vertex id's to attach the edge to  **REQUIRED**
        :returns:
            A success or fail message if the edges were attached
        '''

        body = {
            'parentVertex': parent_id,
            'edgeName': edge_name,
            'edgeVertices': child_vertices
        }
        try:
            response = self.__http_request(self.bearer, 'POST', '{}/tenant/{}/edge/attach'.format(self.URL, tenant_id), data=body)
            return response.text
        except:
            raise SeamsAPIException(response.text)
        

    def attach_label_to_edge(self, 
                             tenant_id, 
                             parent_label, 
                             edge_name, 
                             child_id):
        '''
        Attach label to an edge

        :param tenant_id:
            The id of the tenant the search is on  **REQUIRED**
        :param parent_label:
            The label of the parent vertex  **REQUIRED**
        :param edge_name:
            The name of the edge  **REQUIRED**
        :param child_id:
            A single vertex id of the child  **REQUIRED**
        :returns:
            A success or fail message if the edges were attached
        '''

        body = '{{"parentVertexLabel": "{}", "edgeName": "{}", "childVertex": "{}"}}'.format(parent_label, edge_name, child_id)
        try:
            response = self.__http_request(self.bearer, 'POST', '{}/tenant/{}/edge/attach/label/to'.format(self.URL, tenant_id), data=body)
        except:
            raise SeamsAPIException(response.text)
        return response.text


    def attach_label_from_edge(self, 
                               tenant_id, 
                               parent_vertex, 
                               edge_name, 
                               child_label):
        '''
        Attach label from an edge

        :param tenant_id:
            The id of the tenant the search is on  **REQUIRED**
        :param parent_vertex:
            The parent vertex  **REQUIRED**
        :param edge_name:
            The name of the edge  **REQUIRED**
        :param child_label:
            The label of the child  **REQUIRED**
        :returns:
            A success or fail message if the edges were attached
        '''

        body = '{{"parentVertex": "{}", "edgeName": "{}", "childVertexLabel": "{}"}}'.format(parent_vertex, edge_name, child_label)
        try:
            response = self.__http_request(self.bearer, 'POST', '{}/tenant/{}/edge/attach/label/from'.format(self.URL, tenant_id), data=body)
        except:
            raise SeamsAPIException(response.text)
        return response.text


    def upload_files(self, 
                     tenant_id,
                     caption,
                     *filenames, 
                     file_type='Files'):
        '''
        Bulk upload files

        :param tenant_id:
            The id of the tenant the upload is on  **REQUIRED**
        :param *filenames:
            List of filenames the user would like to upload  **REQUIRED**
        :param file_type:
            Can be 'Files' or 'Images' - defaults to 'Files'
        :returns:
            A list of vertex id's for the uploaded files
        '''

        upload_list = []
        for item in filenames:
            body = {'upload_preset': item, 'fileType': file_type, 'caption': caption}
            files = {'file':(item, open(item, 'rb'))}

            try:
                response = self.__http_request(self.bearer, 'POST', '{}/tenant/{}/upload/file'.format(self.URL, tenant_id), files=files, data=body)
                upload_list.append(response.json())
            except:
                raise SeamsAPIException('Issue uploading file: {}, response: {}'.format(item, response.text))
        return upload_list
    

    def download_files(self, 
                       tenant_id, 
                       *vertex_ids):
        '''
        Bulk download files

        :param tenant_id:
            The id of the tenant the download is on  **REQUIRED**
        :param *files:
            List of vertex id's the user would like to download  **REQUIRED**
        :returns:
            A dictionary where the key is the filename and the value is the file contents
        '''

        download_list = {}
        for vertex_id in vertex_ids:
            try:
                response = self.__http_request(self.bearer, 'GET', '{}/tenant/{}/download/file/{}'.format(self.URL, tenant_id, vertex_id))
                download_list[self.__file_name_formatter(response.headers['filename'])] = response.text
            except:
                raise SeamsAPIException('Issue downloading file: {}, response: {}'.format(vertex_id, response.text))
        return download_list


    def __file_name_formatter(self, 
                              file_name):
        '''
        Private helper function that formats the filename and allows the use of '-' in filenames
        '''

        file_name_list = file_name.split('-')
        del file_name_list[0:5]
        if len(file_name_list) > 1:
            new_file = ''
            for item in file_name_list:
                new_file = new_file + '-' + item
            file_name_list[0] = new_file[1:]
        return file_name_list[0]


    def __properties_formatter(self, 
                               vertex_label, 
                               args):
        '''
        Private helper function that formats a list of key value pairs for properties on a vertex
        '''
        
        properties = []
        for arg in args:
            properties.append('"{}": "{}"'.format(arg, args[arg]))
        finalStr = ','.join(properties)
        return '{{"vertexLabel": "{}","properties": {{{}}}}}'.format(vertex_label, finalStr)


    def __http_request(self, 
                       bearer, 
                       req_type, 
                       url, 
                       data=None, 
                       content=None, 
                       files=None):
        '''
        Private helper function that makes a specific type of HTTP request based on the req_type
        '''
        
        header = {'Authorization': 'Bearer {}'.format(bearer)}
        if content:
            header['Content-Type'] = content
        session = Session()
        request = Request(req_type, url, headers=header, data=data, files=files)
        prepared = session.prepare_request(request)
        response = session.send(prepared)
        return response