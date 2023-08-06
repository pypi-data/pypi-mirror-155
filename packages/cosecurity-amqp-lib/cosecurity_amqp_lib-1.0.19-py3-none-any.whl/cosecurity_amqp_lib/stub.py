import numpy as np

from typing import Any, Dict
from cosecurity_amqp_lib.producer import Producer


class Stub:
    def __init__(self, destination:str) -> None:
        self._producer = Producer()
        self._destination = destination
    
    def _send(self, primitive:str, content:Dict[str, Any]) -> None:
        self._producer.send_message(
            destination=self._destination, 
            primitive=primitive, 
            content=content
        )

class ExampleStub(Stub):
    def __init__(self):
        super().__init__(
            destination='example'
        )

    def primitive_one(self) -> None:
        self._send(
            primitive='primitive_one',  
            content={
                'hello': 'word'
            }
        )

    def primitive_two(self, message:str) -> None:
        self._send(
            primitive='primitive_two',  
            content={
                'message': message
            }
        )

class ExampleLazyStub(Stub):
    def __init__(self):
        super().__init__(
            destination='example_lazy'
        )

    def primitive_one(self) -> None:
        self._send(
            primitive='primitive_one',  
            content={
                'hello': 'word'
            }
        )

    def primitive_two(self, message:str) -> None:
        self._send(
            primitive='primitive_two',  
            content={
                'message': message
            }
        )

class ObjectDetectionStub(Stub):
    def __init__(self):
        super().__init__(
            destination='object_detection'
        )

    def find(self, camera_id:int, image_id:int, image_key:str) -> None:
        self._send(
            primitive='find',  
            content={
                'camera_id': camera_id,
                'image_id': image_id,
                'image_key': image_key
            }
        )

class FaceDetectionStub(Stub):
    def __init__(self):
        super().__init__(
            destination='face_detection'
        )

    def to_train(self):
        self._send(
            primitive='to_train',  
            content={}
        )

    def to_recognize(self, detected_object_id:int, image_key:str) -> None:
        self._send(
            primitive='to_recognize',  
            content={
                'detected_object_id': detected_object_id,
                'image_key': image_key
            }
        )