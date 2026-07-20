from dataclasses import dataclass,field
from enum import Enum
class ObjectType(str,Enum):MEASUREMENT="Measurement";LOCAL_MEASUREMENT="Local Measurement";CHARACTERISTIC="Characteristic";SYSTEM_CONSTANT="System_Constant"
@dataclass(frozen=True,slots=True)
class Function:name:str;description:str
@dataclass(frozen=True,slots=True)
class Measurement:
 name:str;description:str;unit:str;function_name:str="Not available";function_description:str="Not available";conversion_method:str="";object_type:ObjectType=ObjectType.MEASUREMENT
@dataclass(frozen=True,slots=True)
class Characteristic:
 name:str;description:str;unit:str;function_name:str="Not available";function_description:str="Not available";conversion_method:str="";object_type:ObjectType=ObjectType.CHARACTERISTIC
@dataclass(frozen=True,slots=True)
class SystemConstant:name:str;value:str;object_type:ObjectType=ObjectType.SYSTEM_CONSTANT
@dataclass(slots=True)
class A2LDatabase:
 measurements_by_name:dict[str,Measurement]=field(default_factory=dict);characteristics_by_name:dict[str,Characteristic]=field(default_factory=dict);system_constants_by_name:dict[str,SystemConstant]=field(default_factory=dict);functions_by_name:dict[str,Function]=field(default_factory=dict);measurement_function_by_name:dict[str,Function]=field(default_factory=dict);local_measurement_function_by_name:dict[str,Function]=field(default_factory=dict);characteristic_function_by_name:dict[str,Function]=field(default_factory=dict)
 @property
 def object_count(self):return len(self.measurements_by_name)+len(self.characteristics_by_name)+len(self.system_constants_by_name)
