# Copyright 2007 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Validation tools for generic object structures.

This library is used for defining classes with constrained attributes.
Attributes are defined on the class which contains them using validators.
Although validators can be defined by any client of this library, a number
of standard validators are provided here.

Validators can be any callable that takes a single parameter which checks
the new value before it is assigned to the attribute.  Validators are
permitted to modify a received value so that it is appropriate for the
attribute definition.  For example, using int as a validator will cast
a correctly formatted string to a number, or raise an exception if it
can not.  This is not recommended, however.  the correct way to use a
validator that ensure the correct type is to use the Type validator.

This validation library is mainly intended for use with the YAML object
builder.  See yaml_object.py.
"""

# WARNING: This file is externally viewable by our users.  All comments from
# this file will be stripped.  The docstrings will NOT.  Do not put sensitive
# information in docstrings.  If you must communicate internal information in
# this source file, please place them in comments only.

from __future__ import absolute_import
import re
from googlecloudsdk.appengine._internal import six_subset
from ruamel import yaml


class SortedDict(dict):
  """Represents a dict with a particular key order for yaml representing."""

  def __init__(self, keys, data):
    super(SortedDict, self).__init__()
    self.keys = keys
    self.update(data)

  def ordered_items(self):  # pylint: disable=invalid-name
    result = []
    for key in self.keys:
      if self.get(key) is not None:
        result.append((key, self.get(key)))
    return result


class ItemDumper(yaml.SafeDumper):
  """For dumping validation.Items. Respects SortedDict key ordering."""

  def represent_mapping(self, tag, mapping, flow_style=None):
    if hasattr(mapping, 'ordered_items'):
      return super(ItemDumper, self).represent_mapping(
          tag, mapping.ordered_items(), flow_style=flow_style)
    return super(ItemDumper, self).represent_mapping(
        tag, mapping, flow_style=flow_style)


ItemDumper.add_representer(
    SortedDict, ItemDumper.represent_dict)


class Error(Exception):
  """Base class for all package errors."""


class AttributeDefinitionError(Error):
  """An error occurred in the definition of class attributes."""


class ValidationError(Error):
  """Base class for raising exceptions during validation."""

  def __init__(self, message, cause=None):
    """Initialize exception."""
    if hasattr(cause, 'args') and cause.args:
      Error.__init__(self, message, *cause.args)
    else:
      # If exception has no args, create message by turning cause
      # in to a string.
      Error.__init__(self, message)
    self.message = message
    self.cause = cause

  def __str__(self):
    return str(self.message)


class MissingAttribute(ValidationError):
  """Raised when a required attribute is missing from object."""

  def __init__(self, key):
    msg = 'Missing required value [{}].'.format(key)
    super(MissingAttribute, self).__init__(msg)


def AsValidator(validator):
  """Wrap various types as instances of a validator.

  Used to allow shorthand for common validator types.  It
  converts the following types to the following Validators.

    strings -> Regex
    type -> Type
    collection -> Options
    Validator -> Its self!

  Args:
    validator: Object to wrap in a validator.

  Returns:
    Validator instance that wraps the given value.

  Raises:
    AttributeDefinitionError: if validator is not one of the above described
      types.
  """
  if (six_subset.is_basestring(validator)
      or validator == six_subset.string_types):
    return StringValidator()
  if isinstance(validator, (str, six_subset.text_type)):
    return Regex(validator, type(validator))
  if isinstance(validator, type):
    return Type(validator)
  if isinstance(validator, (list, tuple, set)):
    return Options(*tuple(validator))
  if isinstance(validator, Validator):
    return validator
  else:
    raise AttributeDefinitionError('%s is not a valid validator' %
                                   str(validator))


def _SimplifiedValue(validator, value):
  """Convert any value to simplified collections and basic types.

  Args:
    validator: An instance of Validator that corresponds with 'value'.
      May also be 'str' or 'int' if those were used instead of a full
      Validator.
    value: Value to convert to simplified collections.

  Returns:
    The value as a dictionary if it is a ValidatedBase object.  A list of
    items converted to simplified collections if value is a list
    or a tuple. Otherwise, just the value.
  """
  if isinstance(value, ValidatedBase):
    # Convert validated object to dictionary.
    return value.ToDict()
  elif isinstance(value, (list, tuple)):
    # Convert all elements in the list.
    return [_SimplifiedValue(validator, item) for item in value]
  elif isinstance(validator, Validator):
    return validator.ToValue(value)
  return value


class ValidatedBase(object):
  """Base class for all validated objects."""

  @classmethod
  def GetValidator(cls, key):
    """Safely get the Validator corresponding to the given key.

    This function should be overridden by subclasses

    Args:
      key: The attribute or item to get a validator for.

    Returns:
      Validator associated with key or attribute.

    Raises:
      ValidationError: if the requested key is illegal.
    """
    raise NotImplementedError('Subclasses of ValidatedBase must '
                              'override GetValidator.')

  def SetMultiple(self, attributes):
    """Set multiple values on Validated instance.

    All attributes will be validated before being set.

    Args:
      attributes: A dict of attributes/items to set.

    Raises:
      ValidationError: when no validated attribute exists on class.
    """
    for key, value in attributes.items():
      self.Set(key, value)

  def Set(self, key, value):
    """Set a single value on Validated instance.

    This method should be overridded by sub-classes.

    This method can only be used to assign validated attributes/items.

    Args:
      key: The name of the attributes
      value: The value to set

    Raises:
      ValidationError: when no validated attribute exists on class.
    """
    raise NotImplementedError('Subclasses of ValidatedBase must override Set.')

  def CheckInitialized(self):
    """Checks for missing or conflicting attributes.

    Subclasses should override this function and raise an exception for
    any errors. Always run this method when all assignments are complete.

    Raises:
      ValidationError: when there are missing or conflicting attributes.
    """

  def ToDict(self):
    """Convert ValidatedBase object to a dictionary.

    Recursively traverses all of its elements and converts everything to
    simplified collections.

    Subclasses should override this method.

    Returns:
      A dictionary mapping all attributes to simple values or collections.
    """
    raise NotImplementedError('Subclasses of ValidatedBase must '
                              'override ToDict.')

  def ToYAML(self):
    """Print validated object as simplified YAML.

    Returns:
      Object as a simplified YAML string compatible with parsing using the
      SafeLoader.
    """
    return yaml.dump(self.ToDict(),
                     default_flow_style=False,
                     Dumper=ItemDumper)

  def GetWarnings(self):
    """Return all the warnings we've got, along with their associated fields.

    Returns:
      A list of tuples of (dotted_field, warning), both strings.
    """
    raise NotImplementedError('Subclasses of ValidatedBase must '
                              'override GetWarnings')


class Validated(ValidatedBase):
  """Base class for classes that require validation.

  A class which intends to use validated fields should sub-class itself from
  this class.  Each class should define an 'ATTRIBUTES' class variable which
  should be a map from attribute name to its validator.  For example:

    class Story(Validated):
      ATTRIBUTES = {'title': Type(str),
                    'authors': Repeated(Type(str)),
                    'isbn': Optional(Type(str)),
                    'pages': Type(int),
                    }

  Attributes that are not listed under ATTRIBUTES work like normal and are
  not validated upon assignment.
  """

  # Override this variable in derived classes to defined validated fields.
  ATTRIBUTES = None

  def __init__(self, **attributes):
    """Constructor for Validated classes.

    This constructor can optionally assign values to the class via its
    keyword arguments.

    Raises:
      AttributeDefinitionError: when class instance is missing ATTRIBUTE
        definition or when ATTRIBUTE is of the wrong type.
    """
    super(Validated, self).__init__()
    if not isinstance(self.ATTRIBUTES, dict):
      raise AttributeDefinitionError(
          'The class %s does not define an ATTRIBUTE variable.'
          % self.__class__)

    # Clear all attributes
    for key in self.ATTRIBUTES.keys():
      object.__setattr__(self, key, self.GetValidator(key).default)

    self.SetMultiple(attributes)

  @classmethod
  def GetValidator(cls, key):
    """Safely get the underlying attribute definition as a Validator.

    Args:
      key: Name of attribute to get.

    Returns:
      Validator associated with key or attribute value wrapped in a
      validator.
    Raises:
      ValidationError: if no such attribute exists.
    """
    if key not in cls.ATTRIBUTES:  # pylint: disable=unsupported-membership-test
      raise ValidationError(
          'Unexpected attribute \'%s\' for object of type %s.' %
          (key, cls.__name__))

    return AsValidator(cls.ATTRIBUTES[key])

  def GetWarnings(self):
    ret = []
    for key in self.ATTRIBUTES.keys():
      ret.extend(self.GetValidator(key).GetWarnings(
          self.GetUnnormalized(key), key, self))
    return ret

  def Set(self, key, value):
    """Set a single value on Validated instance.

    This method can only be used to assign validated attributes.

    Args:
      key: The name of the attributes
      value: The value to set

    Raises:
      ValidationError when no validated attribute exists on class.
    """
    setattr(self, key, value)

  def GetUnnormalized(self, key):
    """Get a single value on the Validated instance, without normalizing."""
    validator = self.GetValidator(key)  # verify that we have the field at all.
    try:
      return super(Validated, self).__getattribute__(key)
    except AttributeError:
      return validator.default

  def Get(self, key):
    """Get a single value on Validated instance.

    This method can only be used to retrieve validated attributes.

    Args:
      key: The name of the attributes

    Raises:
      ValidationError when no validated attribute exists on class.
    """
    self.GetValidator(key)
    return getattr(self, key)

  def __getattribute__(self, key):
    # __getattribute__ allows us to normalize even attributes we have on the
    # class, which is what we want. (__getattr__ only overrides for absent
    # attributes)
    ret = super(Validated, self).__getattribute__(key)
    if key in ['ATTRIBUTES', 'GetValidator', '__name__', '__class__']:
      return ret
    try:
      validator = self.GetValidator(key)
    except ValidationError:
      return ret
    if isinstance(validator, Normalized):
      return validator.Get(ret, key, self)
    return ret

  def CheckInitialized(self):
    for key in self.ATTRIBUTES.keys():
      value = self.GetUnnormalized(key)
      self.GetValidator(key).CheckFieldInitialized(value, key, self)

  def __setattr__(self, key, value):
    """Set attribute.

    Setting a value on an object of this type will only work for attributes
    defined in ATTRIBUTES.  To make other assignments possible it is necessary
    to override this method in subclasses.

    It is important that assignment is restricted in this way because
    this validation is used as validation for parsing.  Absent this restriction
    it would be possible for method names to be overwritten.

    Args:
      key: Name of attribute to set.
      value: The attribute's new value or None to unset.

    Raises:
      ValidationError: when trying to assign to an attribute
        that does not exist.
    """
    if value is not None:
      value = self.GetValidator(key)(value, key)
    object.__setattr__(self, key, value)

  def __str__(self):
    """Formatted view of validated object and nested values."""
    return repr(self)

  def __repr__(self):
    """Formatted view of validated object and nested values."""
    values = [(attr, getattr(self, attr)) for attr in self.ATTRIBUTES.keys()]
    dent = '    '
    value_list = []
    for attr, value in values:
      value_list.append('\n%s%s=%s' % (dent, attr, value))

    return "<%s %s\n%s>" % (self.__class__.__name__, ' '.join(value_list), dent)

  def __eq__(self, other):
    """Equality operator.

    Comparison is done by comparing all attribute values to those in the other
    instance.  Objects which are not of the same type are not equal.

    Args:
      other: Other object to compare against.

    Returns:
      True if validated objects are equal, else False.
    """
    if type(self) != type(other):
      return False
    for key in self.ATTRIBUTES.keys():
      if getattr(self, key) != getattr(other, key):
        return False
    return True

  def __ne__(self, other):
    """Inequality operator."""
    return not self.__eq__(other)

  def __hash__(self):
    """Hash function for using Validated objects in sets and maps.

    Hash is done by hashing all keys and values and xor'ing them together.

    Returns:
      Hash of validated object.
    """
    result = 0
    for key in self.ATTRIBUTES.keys():
      value = getattr(self, key)
      if isinstance(value, list):
        value = tuple(value)
      result = result ^ hash(key) ^ hash(value)
    return result

  def ToDict(self):
    """Convert Validated object to a dictionary.

    Recursively traverses all of its elements and converts everything to
    simplified collections.

    Returns:
      A dict of all attributes defined in this classes ATTRIBUTES mapped
      to its value.  This structure is recursive in that Validated objects
      that are referenced by this object and in lists are also converted to
      dicts.
    """
    result = {}
    for name, validator in self.ATTRIBUTES.items():
      value = self.GetUnnormalized(name)
      # Skips values that are the same as the default value.
      if not(isinstance(validator, Validator) and value == validator.default):
        result[name] = _SimplifiedValue(validator, value)
    return result


class ValidatedDict(ValidatedBase, dict):
  """Base class for validated dictionaries.

  You can control the keys and values that are allowed in the dictionary
  by setting KEY_VALIDATOR and VALUE_VALIDATOR to subclasses of Validator (or
  things that can be interpreted as validators, see AsValidator).

  For example if you wanted only capitalized keys that map to integers
  you could do:

    class CapitalizedIntegerDict(ValidatedDict):
      KEY_VALIDATOR = Regex('[A-Z].*')
      VALUE_VALIDATOR = int  # this gets interpreted to Type(int)

  The following code would result in an error:

    my_dict = CapitalizedIntegerDict()
    my_dict['lowercase'] = 5  # Throws a validation exception

  You can freely nest Validated and ValidatedDict inside each other so:

    class MasterObject(Validated):
      ATTRIBUTES = {'paramdict': CapitalizedIntegerDict}

  Could be used to parse the following yaml:
    paramdict:
      ArbitraryKey: 323
      AnotherArbitraryKey: 9931
  """
  KEY_VALIDATOR = None
  VALUE_VALIDATOR = None

  def __init__(self, **kwds):
    """Construct a validated dict by interpreting the key and value validators.

    Args:
      **kwds: keyword arguments will be validated and put into the dict.
    """
    super(ValidatedDict, self).__init__()
    self.update(kwds)

  @classmethod
  def GetValidator(cls, key):
    """Check the key for validity and return a corresponding value validator.

    Args:
      key: The key that will correspond to the validator we are returning.
    """
    key = AsValidator(cls.KEY_VALIDATOR)(key, 'key in %s' % cls.__name__)
    return AsValidator(cls.VALUE_VALIDATOR)

  def __setitem__(self, key, value):
    """Set an item.

    Only attributes accepted by GetValidator and values that validate
    with the validator returned from GetValidator are allowed to be set
    in this dictionary.

    Args:
      key: Name of item to set.
      value: Items new value.

    Raises:
      ValidationError: when trying to assign to a value that does not exist.
    """
    dict.__setitem__(self, key, self.GetValidator(key)(value, key))

  def setdefault(self, key, value=None):
    """Trap setdefaultss to ensure all key/value pairs are valid.

    See the documentation for setdefault on dict for usage details.

    Raises:
      ValidationError: if the specified key is illegal or the
      value invalid.
    """
    return dict.setdefault(self, key, self.GetValidator(key)(value, key))

  def update(self, other, **kwds):
    """Trap updates to ensure all key/value pairs are valid.

    See the documentation for update on dict for usage details.

    Raises:
      ValidationError: if any of the specified keys are illegal or
        values invalid.
    """
    if hasattr(other, 'keys') and callable(getattr(other, 'keys')):
      newother = {}
      for k in other:
        newother[k] = self.GetValidator(k)(other[k], k)
    else:
      newother = [(k, self.GetValidator(k)(v, k)) for (k, v) in other]

    newkwds = {}
    for k in kwds:
      newkwds[k] = self.GetValidator(k)(kwds[k], k)

    dict.update(self, newother, **newkwds)

  def Set(self, key, value):
    """Set a single value on Validated instance.

    This method checks that a given key and value are valid and if so
    puts the item into this dictionary.

    Args:
      key: The name of the attributes
      value: The value to set

    Raises:
      ValidationError: when no validated attribute exists on class.
    """
    self[key] = value

  def GetWarnings(self):
    ret = []
    for name, value in self.items():
      ret.extend(self.GetValidator(name).GetWarnings(value, name, self))
    return ret

  def ToDict(self):
    """Convert ValidatedBase object to a dictionary.

    Recursively traverses all of its elements and converts everything to
    simplified collections.

    Subclasses should override this method.

    Returns:
      A dictionary mapping all attributes to simple values or collections.
    """
    result = {}
    for name, value in self.items():
      validator = self.GetValidator(name)
      result[name] = _SimplifiedValue(validator, value)
    return result


################################################################################
# Validators


class Validator(object):
  """Validator base class.

  Though any callable can be used as a validator, this class encapsulates the
  case when a specific validator needs to hold a particular state or
  configuration.

  To implement Validator sub-class, override the validate method.

  This class is permitted to change the ultimate value that is set to the
  attribute if there is a reasonable way to perform the conversion.
  """

  expected_type = object

  def __init__(self, default=None):
    """Constructor.

    Args:
      default: Default assignment is made during initialization and will
        not pass through validation.
    """
    self.default = default

  def __call__(self, value, key='???'):
    """Main interface to validator is call mechanism."""
    return self.Validate(value, key)

  def Validate(self, value, key='???'):
    """Validate this field. Override to customize subclass behavior.

    Args:
      value: Value to validate.
      key: Name of the field being validated.

    Returns:
      Value if value is valid, or a valid representation of value.
    """
    return value

  def CheckFieldInitialized(self, value, key, obj):  # pylint: disable=unused-argument
    """Check for missing fields or conflicts between fields.

    Default behavior performs a simple None-check, but this can be overridden.
    If the intent is to allow optional fields, then use the Optional validator
    instead.

    Args:
      value: Value to validate.
      key: Name of the field being validated.
      obj: The object to validate against.

    Raises:
      ValidationError: when there are missing or conflicting fields.
    """
    if value is None:
      raise MissingAttribute(key)

  def ToValue(self, value):
    """Convert 'value' to a simplified collection or basic type.

    Subclasses of Validator should override this method when the dumped
    representation of 'value' is not simply <type>(value) (e.g. a regex).

    Args:
      value: An object of the same type that was returned from Validate().

    Returns:
      An instance of a builtin type (e.g. int, str, dict, etc).  By default
      it returns 'value' unmodified.
    """
    return value

  def GetWarnings(self, value, key, obj):
    """Return any warnings on this attribute.

    Validates the value with an eye towards things that aren't fatal problems.

    Args:
      value: Value to validate.
      key: Name of the field being validated.
      obj: The object to validate against.

    Returns:
      A list of tuples (context, warning) where
        - context is the field (or dotted field path, if a sub-field)
        - warning is the string warning text
    """
    del value, key, obj
    return []


class StringValidator(Validator):
  """Verifies property is a valid text string.

  In python 2: inherits from basestring
  In python 3: inherits from str
  """

  def Validate(self, value, key='???'):
    if not isinstance(value, six_subset.string_types):
      raise ValidationError(
          'Value %r for %s is not a valid text string.' % (
              value, key))
    return value


class Type(Validator):
  """Verifies property is of expected type.

  Can optionally convert value if it is not of the expected type.

  It is possible to specify a required field of a specific type in shorthand
  by merely providing the type.  This method is slightly less efficient than
  providing an explicit type but is not significant unless parsing a large
  amount of information:

    class Person(Validated):
      ATTRIBUTES = {'name': unicode,
                    'age': int,
                    }

  However, in most instances it is best to use the type constants:

    class Person(Validated):
      ATTRIBUTES = {'name': TypeUnicode,
                    'age': TypeInt,
                    }
  """

  def __init__(self, expected_type, convert=True, default=None):
    """Initialize Type validator.

    Args:
      expected_type: Type that attribute should validate against.
      convert: Cause conversion if value is not the right type.
        Conversion is done by calling the constructor of the type
        with the value as its first parameter.
      default: Default assignment is made during initialization and will
        not pass through validation.
    """
    super(Type, self).__init__(default)
    self.expected_type = expected_type
    self.convert = convert

  def Validate(self, value, key):
    """Validate that value has the correct type.

    Args:
      value: Value to validate.
      key: Name of the field being validated.

    Returns:
      value if value is of the correct type. value is coverted to the correct
      type if the Validator is configured to do so.

    Raises:
      ValidationError: if value is not of the right type and the validator
        is either configured not to convert or cannot convert.
    """
    if not isinstance(value, self.expected_type):

      if self.convert:
        try:
          return self.expected_type(value)
        except ValueError as e:
          raise ValidationError(
              'Value %r for %s could not be converted to type %s.' % (
                  value, key, self.expected_type.__name__), e)
        except TypeError as e:
          raise ValidationError(
              'Value %r for %s is not of the expected type %s' % (
                  value, key, self.expected_type.__name__), e)
      else:
        raise ValidationError(
              'Value %r for %s is not of the expected type %s' % (
                  value, key, self.expected_type.__name__))
    else:
      return value

  def GetWarnings(self, value, key, obj):
    del obj
    if issubclass(self.expected_type, ValidatedBase):
      return [('%s.%s' % (key, subkey), warning)
              for subkey, warning in value.GetWarnings()]
    return []


TYPE_BOOL = Type(bool)
TYPE_INT = Type(int)
# long is going away in Python 3. Luckily, in Python 2, the int constructor
# happily returns a long if you pass it something that should be a long,
# and the validator happens to work ok when this happens, because `convert`
# is true. In python 3 TYPE_INT and TYPE_LONG are literally the same.
TYPE_LONG = Type(int)
TYPE_STR = Type(str)
TYPE_UNICODE = Type(six_subset.text_type)
TYPE_FLOAT = Type(float)


class Exec(Type):
  """Coerces the value to accommodate Docker CMD/ENTRYPOINT requirements.

  Validates the value is a string, then tries to modify the string (if
  necessary) so that the command represented will become PID 1 inside the
  Docker container. See Docker documentation on "docker kill" for more info:
  https://docs.docker.com/engine/reference/commandline/kill/

  If the command already starts with `exec` or appears to be in "exec form"
  (starts with `[`), no further action is needed. Otherwise, prepend the
  command with `exec` so that it will become PID 1 on execution.
  """

  def __init__(self, default=None):
    """Initialize parent, a converting type validator for `str`."""
    super(Exec, self).__init__(str, convert=True, default=default)

  def Validate(self, value, key):
    """Validate according to parent behavior and coerce to start with `exec`."""

    # Validate/convert to string using parent behavior.
    value = super(Exec, self).Validate(value, key)

    if value.startswith('[') or value.startswith('exec'):
      # The command does not appear to need any changes.
      return value
    else:
      # Prepend the command with `exec`.
      return 'exec ' + value


class Options(Validator):
  """Limit field based on pre-determined values.

  Options are used to make sure an enumerated set of values are the only
  one permitted for assignment.  It is possible to define aliases which
  map multiple string values to a single original.  An example of usage:

    class ZooAnimal(validated.Class):
      ATTRIBUTES = {
        'name': str,
        'kind': Options('platypus',                   # No aliases
                        ('rhinoceros', ['rhino']),    # One alias
                        ('canine', ('dog', 'puppy')), # Two aliases
                        )
  """

  def __init__(self, *options, **kw):
    """Initialize options.

    Args:
      options: List of allowed values.
    """
    if 'default' in kw:
      default = kw['default']
    else:
      default = None

    alias_map = {}
    def AddAlias(alias, original):
      """Set new alias on alias_map.

      Raises:
        AttributeDefinitionError: when option already exists or if alias is
          not of type str.
      """
      if not isinstance(alias, str):
        raise AttributeDefinitionError(
            'All option values must be of type str.')
      elif alias in alias_map:
        raise AttributeDefinitionError(
            "Option '%s' already defined for options property." % alias)
      alias_map[alias] = original

    # Build the alias map.
    for option in options:
      if isinstance(option, str):
        AddAlias(option, option)

      elif isinstance(option, (list, tuple)):
        # Doing this test is better than generating a ValueError.
        if len(option) != 2:
          raise AttributeDefinitionError("Alias is defined as a list or tuple "
                                         "with two items.  The first is the "
                                         "original option, while the second "
                                         "is a list or tuple of str aliases.\n"
                                         "\n  Example:\n"
                                         "      ('original', ('alias1', "
                                         "'alias2'")
        original, aliases = option
        AddAlias(original, original)
        if not isinstance(aliases, (list, tuple)):
          raise AttributeDefinitionError('Alias lists must be a list or tuple')

        for alias in aliases:
          AddAlias(alias, original)

      else:
        raise AttributeDefinitionError("All options must be of type str "
                                       "or of the form (str, [str...]).")
    super(Options, self).__init__(default)
    self.options = alias_map

  def Validate(self, value, key):
    """Validate options.

    Returns:
      Original value for provided alias.

    Raises:
      ValidationError: when value is not one of predefined values.
    """
    value = str(value)
    if value not in self.options:
      raise ValidationError('Value \'%s\' for %s not in %s.'
                            % (value, key, self.options))
    return self.options[value]


class Optional(Validator):
  """Definition of optional attributes.

  Optional values are attributes which can be set to None or left
  unset.  All values in a basic Validated class are set to None
  at initialization.  Failure to assign to non-optional values
  will result in a validation error when calling CheckInitialized.
  """

  def __init__(self, validator, default=None):
    """Initializer.

    This constructor will make a few guesses about the value passed in
    as the validator:

      - If the validator argument is a type, it automatically creates a Type
        validator around it.

      - If the validator argument is a list or tuple, it automatically
        creates an Options validator around it.

    Args:
      validator: Optional validation condition.

    Raises:
      AttributeDefinitionError: if validator is not callable.
    """
    self.validator = AsValidator(validator)
    self.expected_type = self.validator.expected_type
    self.default = default

  def Validate(self, value, key):
    """Optionally require a value.

    Normal validators do not accept None.  This will accept none on
    behalf of the contained validator.

    Args:
      value: Value to be validated as optional.
      key: Name of the field being validated.

    Returns:
      None if value is None, else results of contained validation.
    """
    return self.validator(value, key)

  def CheckFieldInitialized(self, value, key, obj):
    if value is None:
      return
    self.validator.CheckFieldInitialized(value, key, obj)

  def ToValue(self, value):
    """Convert 'value' to a simplified collection or basic type."""
    if value is None:
      return None
    return self.validator.ToValue(value)


class Regex(Validator):
  """Regular expression validator.

  Regular expression validator always converts value to string.  Note that
  matches must be exact.  Partial matches will not validate.  For example:

    class ClassDescr(Validated):
      ATTRIBUTES = { 'name': Regex(r'[a-zA-Z_][a-zA-Z_0-9]*'),
                     'parent': Type(type),
                     }

  Alternatively, any attribute that is defined as a string is automatically
  interpreted to be of type Regex.  It is possible to specify unicode regex
  strings as well.  This approach is slightly less efficient, but usually
  is not significant unless parsing large amounts of data:

    class ClassDescr(Validated):
      ATTRIBUTES = { 'name': r'[a-zA-Z_][a-zA-Z_0-9]*',
                     'parent': Type(type),
                     }

    # This will raise a ValidationError exception.
    my_class(name='AName with space', parent=AnotherClass)
  """

  def __init__(self, regex, string_type=six_subset.text_type, default=None):
    """Initialized regex validator.

    Args:
      regex: Regular expression string to use for comparison.
      string_type: Type to be considered a string.
      default: Default value.

    Raises:
      AttributeDefinitionError: if string_type is not a kind of string.
    """
    super(Regex, self).__init__(default)
    if (not issubclass(string_type, six_subset.string_types) or
        six_subset.is_basestring(string_type)):
      raise AttributeDefinitionError(
          'Regex fields must be a string type not %s.' % str(string_type))
    if isinstance(regex, six_subset.string_types):
      self.re = re.compile('^(?:%s)$' % regex)
    else:
      raise AttributeDefinitionError(
          'Regular expression must be string.  Found %s.' % str(regex))

    self.expected_type = string_type

  def Validate(self, value, key):
    """Does validation of a string against a regular expression.

    Args:
      value: String to match against regular expression.
      key: Name of the field being validated.

    Raises:
      ValidationError: when value does not match regular expression or
        when value does not match provided string type.
    """
    if issubclass(self.expected_type, str):
      cast_value = TYPE_STR(value)
    else:
      cast_value = TYPE_UNICODE(value)

    if self.re.match(cast_value) is None:
      raise ValidationError('Value \'%s\' for %s does not match expression '
                            '\'%s\'' % (value, key, self.re.pattern))
    return cast_value


class _RegexStrValue(object):
  """Simulates the regex object to support recompilation when necessary.

  Used by the RegexStr class to dynamically build and recompile regular
  expression attributes of a validated object.  This object replaces the normal
  object returned from re.compile which is immutable.

  When the value of this object is a string, that string is simply used as the
  regular expression when recompilation is needed.  If the state of this object
  is a list of strings, the strings are joined in to a single 'or' expression.
  """

  def __init__(self, attribute, value, key):
    """Initialize recompilable regex value.

    Args:
      attribute: Attribute validator associated with this regex value.
      value: Initial underlying python value for regex string.  Either a single
        regex string or a list of regex strings.
      key: Name of the field.
    """
    self.__attribute = attribute
    self.__value = value
    self.__regex = None
    self.__key = key

  def __AsString(self, value):
    """Convert a value to appropriate string.

    Returns:
      String version of value with all carriage returns and line feeds removed.
    """
    if issubclass(self.__attribute.expected_type, str):
      cast_value = TYPE_STR(value)
    else:
      cast_value = TYPE_UNICODE(value)

    cast_value = cast_value.replace('\n', '')
    cast_value = cast_value.replace('\r', '')
    return cast_value

  def __BuildRegex(self):
    """Build regex string from state.

    Returns:
      String version of regular expression.  Sequence objects are constructed
      as larger regular expression where each regex in the list is joined with
      all the others as single 'or' expression.
    """
    if isinstance(self.__value, list):
      value_list = self.__value
      sequence = True
    else:
      value_list = [self.__value]
      sequence = False

    regex_list = []
    for item in value_list:
      regex_list.append(self.__AsString(item))

    if sequence:
      return '|'.join('%s' % item for item in regex_list)
    else:
      return regex_list[0]

  def __Compile(self):
    """Build regular expression object from state.

    Returns:
      Compiled regular expression based on internal value.
    """
    regex = self.__BuildRegex()
    try:
      return re.compile(regex)
    except re.error as e:
      raise ValidationError('Value \'%s\' for %s does not compile: %s' %
                            (regex, self.__key, e), e)

  @property
  def regex(self):
    """Compiled regular expression as described by underlying value."""
    return self.__Compile()

  def match(self, value):  # pylint: disable=invalid-name
    """Match against internal regular expression.

    Args:
      value: String to match against regular expression.

    Returns:
      Regular expression object built from underlying value.
    """
    return re.match(self.__BuildRegex(), value)

  def Validate(self):
    """Ensure that regex string compiles."""
    self.__Compile()

  def __str__(self):
    """Regular expression string as described by underlying value."""
    return self.__BuildRegex()

  def __eq__(self, other):
    """Comparison against other regular expression string values."""
    if isinstance(other, _RegexStrValue):
      return self.__BuildRegex() == other.__BuildRegex()
    return str(self) == other

  def __ne__(self, other):
    """Inequality operator for regular expression string value."""
    return not self.__eq__(other)


class RegexStr(Validator):
  """Validates that a string can compile as a regex without errors.

  Use this validator when the value of a field should be a regex.  That
  means that the value must be a string that can be compiled by re.compile().
  The attribute will then be a compiled re object.
  """

  def __init__(self, string_type=six_subset.text_type, default=None):
    """Initialized regex validator.

    Args:
      string_type: Type to be considered a string.
      default: Default value.

    Raises:
      AttributeDefinitionError: if string_type is not a kind of string.
    """
    if default is not None:
      default = _RegexStrValue(self, default, None)
      re.compile(str(default))
    super(RegexStr, self).__init__(default)
    # The first part of this condition is a normal 2*3 subclass check.
    # The second part tests for python2 basestring itself, without hitting
    # python3 str.
    if (not issubclass(string_type, six_subset.string_types) or
        six_subset.is_basestring(string_type)):
      raise AttributeDefinitionError(
          'RegexStr fields must be a string type not %s.' % str(string_type))

    self.expected_type = string_type

  def Validate(self, value, key):
    """Validates that the string compiles as a regular expression.

    Because the regular expression might have been expressed as a multiline
    string, this function also strips newlines out of value.

    Args:
      value: String to compile as a regular expression.
      key: Name of the field being validated.

    Raises:
      ValueError when value does not compile as a regular expression.  TypeError
      when value does not match provided string type.
    """
    if isinstance(value, _RegexStrValue):
      return value
    value = _RegexStrValue(self, value, key)
    value.Validate()
    return value

  def ToValue(self, value):
    """Returns the RE pattern for this validator."""
    return str(value)


class Range(Validator):
  """Validates that numbers fall within the correct range.

  In theory this class can be emulated using Options, however error
  messages generated from that class will not be very intelligible.
  This class essentially does the same thing, but knows the intended
  integer range.

  Also, this range class supports floats and other types that implement
  ordinality.

  The range is inclusive, meaning 3 is considered in the range
  in Range(1,3).
  """

  def __init__(self, minimum, maximum, range_type=int, default=None):
    """Initializer for range.

    At least one of minimum and maximum must be supplied.

    Args:
      minimum: Minimum for attribute.
      maximum: Maximum for attribute.
      range_type: Type of field.  Defaults to int.

    Raises:
      AttributeDefinitionError: if the specified parameters are incorrect.
    """
    super(Range, self).__init__(default)
    min_max_type = range_type
    if range_type in six_subset.integer_types:
      min_max_type = six_subset.integer_types
    if minimum is None and maximum is None:
      raise AttributeDefinitionError('Must specify minimum or maximum.')
    if minimum is not None and not isinstance(minimum, min_max_type):
      raise AttributeDefinitionError(
          'Minimum value must be of type %s, instead it is %s (%s).' %
          (str(range_type), str(type(minimum)), str(minimum)))
    if maximum is not None and not isinstance(maximum, min_max_type):
      raise AttributeDefinitionError(
          'Maximum value must be of type %s, instead it is %s (%s).' %
          (str(range_type), str(type(maximum)), str(maximum)))

    self.minimum = minimum
    self.maximum = maximum
    self.expected_type = range_type
    self._type_validator = Type(range_type)

  def Validate(self, value, key):
    """Validate that value is within range.

    Validates against range-type then checks the range.

    Args:
      value: Value to validate.
      key: Name of the field being validated.

    Raises:
      ValidationError: when value is out of range.  ValidationError when value
      is not of the same range type.
    """
    cast_value = self._type_validator.Validate(value, key)
    if self.maximum is None and cast_value < self.minimum:
      raise ValidationError('Value \'%s\' for %s less than %s'
                            % (value, key, self.minimum))
    elif self.minimum is None and cast_value > self.maximum:
      raise ValidationError('Value \'%s\' for %s greater than %s'
                            % (value, key, self.maximum))

    elif ((self.minimum is not None and cast_value < self.minimum) or
          (self.maximum is not None and cast_value > self.maximum)):
      raise ValidationError('Value \'%s\' for %s is out of range %s - %s'
                            % (value, key, self.minimum, self.maximum))
    return cast_value


class Repeated(Validator):
  """Repeated field validator.

  Indicates that attribute is expected to be a repeated value, ie,
  a sequence.  This adds additional validation over just Type(list)
  in that it retains information about what can be stored in the list by
  use of its constructor field.
  """

  def __init__(self, constructor, default=None):
    """Initializer for repeated field.

    Args:
      constructor: Type used for verifying elements of sequence attribute.
    """
    super(Repeated, self).__init__(default)
    self.constructor = constructor
    self.expected_type = list

  def Validate(self, value, key):
    """Do validation of sequence.

    Value must be a list and all elements must be of type 'constructor'.

    Args:
      value: Value to validate.
      key: Name of the field being validated.

    Raises:
      ValidationError: if value is None, not a list or one of its elements is
        the wrong type.
    """
    if not isinstance(value, list):
      raise ValidationError('Value \'%s\' for %s should be a sequence but '
                            'is not.' % (value, key))

    for idx, item in enumerate(value):
      if isinstance(self.constructor, Validator):
        value[idx] = self.constructor.Validate(item, key)
      elif not isinstance(item, self.constructor):
        raise ValidationError('Value element \'%s\' for %s must be type %s.' % (
            str(item), key, self.constructor.__name__))

    return value

  def CheckFieldInitialized(self, value, key, obj):
    if value is None:
      raise MissingAttribute(key)
    for idx, item in enumerate(value):
      if isinstance(self.constructor, Validator):
        self.constructor.CheckFieldInitialized(item, key, self)
        # TODO(b/117299409):
        # validators should be called incrementally for each element
        value[idx] = self.constructor.Validate(item, key)
      elif not isinstance(item, self.constructor):
        raise ValidationError('Value element \'%s\' for %s must be type %s.' % (
            str(item), key, self.constructor.__name__))


class TimeValue(Validator):
  """Validates time values with units, such as 1h or 3.5d."""

  _EXPECTED_SYNTAX = ('must be a non-negative number followed by a time unit, '
                      'such as 1h or 3.5d')

  def __init__(self):
    super(TimeValue, self).__init__()
    self.expected_type = str

  def Validate(self, value, key):
    """Validate a time value.

    Args:
      value: Value to validate.
      key: Name of the field being validated.

    Raises:
      ValidationError: if value is not a time value with the expected format.
    """
    if not isinstance(value, six_subset.string_types):
      raise ValidationError("Value '%s' for %s is not a string (%s)"
                            % (value, key, TimeValue._EXPECTED_SYNTAX))
    if not value:
      raise ValidationError("Value for %s is empty (%s)"
                            % (key, TimeValue._EXPECTED_SYNTAX))
    if value[-1] not in "smhd":
      raise ValidationError("Value '%s' for %s must end with a time unit, "
                            "one of s (seconds), m (minutes), h (hours), "
                            "or d (days)" % (value, key))
    try:
      t = float(value[:-1])
    except ValueError:
      raise ValidationError("Value '%s' for %s is not a valid time value (%s)"
                            % (value, key, TimeValue._EXPECTED_SYNTAX))
    if t < 0:
      raise ValidationError("Value '%s' for %s is negative (%s)"
                            % (value, key, TimeValue._EXPECTED_SYNTAX))
    return value


class Normalized(Validator):
  """Normalizes a field on lookup, but serializes with the original value.

  Only works with fields on Validated.
  """

  def Validate(self, value, key):
    return self.validator(value, key)

  def Get(self, value, key, obj):  # pylint: disable=unused-argument
    """Returns the normalized value. Subclasses must override."""
    raise NotImplementedError('Subclasses must override `Get`!')


class Preferred(Normalized):
  """A non-deprecated field when there's a deprecated one.

  For use with Deprecated. Only works as a field on Validated.

  Both fields will work for value access. It's an error to set both the
  deprecated and the corresponding preferred field.
  """

  def __init__(self, deprecated, validator, default=None):
    """Initializer for Preferred.

    Args:
      deprecated: The name of the corresponding deprecated field
      validator: The validator for the actual value of this field.
      default: The default value for this field.
    """
    super(Preferred, self).__init__(default=None)
    self.validator = AsValidator(validator)
    self.deprecated = deprecated
    # To make serializing work right, we need to use a different field name
    # here, leaving `None` as the `default`
    self.synthetic_default = default

  def CheckFieldInitialized(self, value, key, obj):
    deprecated_value = obj.GetUnnormalized(self.deprecated)
    if value is not None and deprecated_value is not None:
      raise ValidationError('Only one of the two fields [{}] (preferred)'
                            ' and [{}] (deprecated) may be set.'.format(
                                key, self.deprecated))
    if deprecated_value is not None:
      return
    if not self.synthetic_default:
      self.validator.CheckFieldInitialized(value, key, obj)

  def Get(self, value, key, obj):
    if value is not None:
      return value
    deprecated_value = obj.GetUnnormalized(self.deprecated)
    if deprecated_value is not None:
      return deprecated_value
    return self.synthetic_default


class Deprecated(Normalized):
  """A deprecated field.

  For use with Preferred. Only works as a field on Validated.

  Both fields will work for value access. It's an error to set both the
  deprecated and the corresponding preferred field.
  """

  def __init__(self, preferred, validator, default=None):
    """Initializer for Deprecated.

    Args:
      preferred: The name of the preferred field.
      validator: The validator for the actual value of this field.
      default: The default value for this field.
    """
    super(Deprecated, self).__init__(default=None)
    self.validator = Optional(validator)
    self.preferred = preferred
    self.synthetic_default = default

  def GetWarnings(self, value, key, obj):
    del obj
    if value is not None:
      return [(
          key,
          'Field %s is deprecated; use %s instead.' % (key, self.preferred))]
    return []

  def Get(self, value, key, obj):
    preferred_value = obj.GetUnnormalized(self.preferred)
    if preferred_value is not None:
      return preferred_value
    elif value is not None:
      return value
    else:
      return self.synthetic_default

  def CheckFieldInitialized(self, value, key, obj):
    pass  # This is done on the preferred
