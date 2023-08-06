import json
import re
from tkinter.messagebox import NO
import uuid
import requests
import os
from os.path import exists
from daspython.common import response
from daspython.common.api import ApiMethods, Response, Token
from daspython.services.entries.entryservice import EntryService


class FileMetadata():
    description = None
    digitalObjectTypeId = None
    fileName = None
    fileSize = 0
    index = 0
    totalCount = 0
    id = None


class UploadDigitalObjectRequest():
    entryCode = ''
    filePath = ''
    description = ''
    digital_object_type = 'Data file' 

class AttributeDigitalObjectInput():
    attributeId: int
    attributeValueId: str
    digitalObjectId: str
    isDeleted: bool

class UpdateRelationsInput():
    attributeId: int
    attributeValueId: str
    digitalObjects: list[dict]

CHUNK_SIZE = 1000000

class DigitalObjectService(ApiMethods):
    def __init__(self, auth: Token):
        super().__init__(auth)

    # This is our chunk reader. This is what gets the next chunk of data ready to send.
    def _read_in_chunks(self, file_object, CHUNK_SIZE):
        while True:
            data = file_object.read(CHUNK_SIZE)
            if not data:
                break
            yield data        

    def upload(self, request: UploadDigitalObjectRequest):

        if (request is None or request.entryCode is None or request.filePath is None):
            raise Exception('Invalid request. Entry Code and file path are required.')

        if not exists(request.filePath):
            raise FileNotFoundError(f'File not found at: {request.filePath}')

        file_metadata = FileMetadata()
        
        head, tail = os.path.split(request.filePath)
        
        file_metadata.fileName = tail
        file_metadata.fileSize = os.path.getsize(request.filePath)
        file_metadata.description = request.description        
        file_metadata.digitalObjectTypeId = self._get_digital_object_type_id(request.digital_object_type)     
        file_metadata.id = str(uuid.uuid1())
        file_metadata.description = request.description
        file_metadata.totalCount = 1
        file_metadata.index = 0

        binary_file = open(request.filePath, "rb")

        index = 0
        offset = 0        
        headers = {}

        digital_object_id = None

        for chunk in self._read_in_chunks(binary_file, CHUNK_SIZE):

            offset = index + len(chunk)
            headers['Content-Range'] = 'bytes %s-%s/%s' % (index, offset -1, file_metadata.fileSize)
            headers['Authorization'] = f'bearer {self.token.api_token}'
            index = offset
            headers['metadata'] = json.dumps(file_metadata.__dict__)
            try:

                file = {"file": chunk}
                r = requests.post(self.token.api_url_base + "/File/UploadDigitalObject", files=file, headers=headers, verify=self.token.check_https)
                
                response = json.loads(r.content.decode('utf-8'))

                if response.get('result') is None:
                    continue

                digital_object_id = response.get('result')['id']

                # print(r.json())
                # print("r: %s, Content-Range: %s" % (r, headers['Content-Range']))
            except Exception as e:
                print(e) 

        binary_file.close()

        self._set_digital_object_relation(request.entryCode, digital_object_id)

    def _set_digital_object_relation(self, entry_code: str, digital_obj_id :str) -> None:

        entry_service = EntryService(self.token)

        response = entry_service.get_entry_by_code(code=entry_code)

        if response is None or response.entry is None:
            raise Exception(f'Entry not found with the code: {entry_code}')

        input = UpdateRelationsInput()

        input.attributeId = response.attributeId
        input.attributeValueId = response.entry['id']
        attribute_value_digital_object = {
            'attributeId': response.attributeId,
            'attributeValueId': response.entry['id'],
            'digitalObjectId': digital_obj_id,
            'isDeleted': False
        }
        input.digitalObjects = []
        input.digitalObjects.append(attribute_value_digital_object)

        api_url = '/api/services/app/AttributeDigitalObject/UpdateRelations'            
        self.put_data(url=api_url, body=input)
        

    def _get_digital_object_type_id(self, digital_object_type: str) -> str:

        entry_service = EntryService(self.token)
        response = entry_service.get_entry_by_name(name=digital_object_type, attribute_name='Digital Object Type')
        
        if response is None:
            raise Exception('Invalid Digital Object Type {digital_object_type}')

        return response['id']            
        
    def link_existing(self, entry_code, digital_object_code):

        entry_service = EntryService(self.token)

        response_digital_object = entry_service.get_entry_by_code(code=digital_object_code)

        if response_digital_object is None or response_digital_object.entry is None:
            raise Exception(f'Digital Object not found with the code: {digital_object_code}')

        self._set_digital_object_relation(entry_code=entry_code, digital_obj_id=response_digital_object.entry['id'])