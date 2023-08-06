import enum
import json
import uuid
import random


class Tool(enum.Enum):
    Segmentation = "segmentation"
    Polyline = "polyline"
    Polygon = "polygon"
    Rotated_bounding_box = "rotated-bounding-box"
    Ner = "ner"
    Multi_dropdown = "multi-dropdown"
    Single_dropdown = "single-dropdown"
    Entity = "entity"
    Point = "point"
    Pdf = "pdf"
    Radio = "radio"
    Checkbox = "checkbox"
    Text = "text"
    Instance = "instance"



def random_color():
    return ["#" + ''.join([random.choice('ABCDEF0123456789') for i in range(6)])]


class LabelOption:
    def __init__(self, value, schemaId=uuid.uuid4().hex):
        self.value = value,
        self.schemaId = schemaId

    def toDict(self):
        return self.__dict__


class LabelCategory:
    def __init__(self, tool: Tool, title="", required=False, schemaId=uuid.uuid4().hex,
                 columnField=False, color=random_color(), shortcutKey=None, classifications=[], options=[]):
        self.tool = tool.value
        self.titlr = title
        self.required = required
        self.schemaId = schemaId
        self.columnField = columnField
        self.color = color
        self.shortcutKey = shortcutKey
        self.classifications = classifications
        self.options = options

    def toDict(self):
        d = self.__dict__
        d['classifications'] = list(map(lambda t: t.toDict(), self.classifications))
        d['options'] = list(map(lambda t: t.toDict(), self.options))
