import re
MEASUREMENT_PATTERN=re.compile(r"\A[A-Za-z_][A-Za-z0-9_.]*\Z",re.ASCII)
CHARACTERISTIC_PATTERN=re.compile(r"\A(?:[A-Za-z][A-Za-z0-9_.]*|_[A-Za-z0-9_.]+)\Z",re.ASCII)
SYSTEM_CONSTANT_PATTERN=re.compile(r"\A[A-Za-z_][A-Za-z0-9_.]*\Z",re.ASCII)
FUNCTION_REFERENCE_PATTERN=re.compile(r"\A[^\s\"]+\Z",re.ASCII)
class CategoryRegex:
 def measurement_matches(self,x):return MEASUREMENT_PATTERN.fullmatch(x) is not None
 def characteristic_matches(self,x):return CHARACTERISTIC_PATTERN.fullmatch(x) is not None
 def system_constant_matches(self,x):return SYSTEM_CONSTANT_PATTERN.fullmatch(x) is not None
 def function_reference_matches(self,x):return FUNCTION_REFERENCE_PATTERN.fullmatch(x) is not None
