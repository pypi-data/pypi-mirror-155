# coding: utf-8

"""
    FINBOURNE Access Management API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.0.2064
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from finbourne_access.configuration import Configuration


class PolicyCreationRequest(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'code': 'str',
        'description': 'str',
        'applications': 'list[str]',
        'grant': 'Grant',
        'selectors': 'list[SelectorDefinition]',
        '_for': 'list[ForSpec]',
        '_if': 'list[IfExpression]',
        'when': 'WhenSpec',
        'how': 'HowSpec'
    }

    attribute_map = {
        'code': 'code',
        'description': 'description',
        'applications': 'applications',
        'grant': 'grant',
        'selectors': 'selectors',
        '_for': 'for',
        '_if': 'if',
        'when': 'when',
        'how': 'how'
    }

    required_map = {
        'code': 'required',
        'description': 'optional',
        'applications': 'optional',
        'grant': 'required',
        'selectors': 'required',
        '_for': 'optional',
        '_if': 'optional',
        'when': 'required',
        'how': 'optional'
    }

    def __init__(self, code=None, description=None, applications=None, grant=None, selectors=None, _for=None, _if=None, when=None, how=None, local_vars_configuration=None):  # noqa: E501
        """PolicyCreationRequest - a model defined in OpenAPI"
        
        :param code:  Code of the policy being created (required)
        :type code: str
        :param description:  Description of what the policy will be used for
        :type description: str
        :param applications:  Applications this policy is used with
        :type applications: list[str]
        :param grant:  (required)
        :type grant: finbourne_access.Grant
        :param selectors:  Selectors that identify what resources this policy qualifies for (required)
        :type selectors: list[finbourne_access.SelectorDefinition]
        :param _for:  \"For Specification\" for when the policy is to be applied
        :type _for: list[finbourne_access.ForSpec]
        :param _if:  \"If Specification\" for when the policy is to be applied
        :type _if: list[finbourne_access.IfExpression]
        :param when:  (required)
        :type when: finbourne_access.WhenSpec
        :param how: 
        :type how: finbourne_access.HowSpec

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._code = None
        self._description = None
        self._applications = None
        self._grant = None
        self._selectors = None
        self.__for = None
        self.__if = None
        self._when = None
        self._how = None
        self.discriminator = None

        self.code = code
        self.description = description
        self.applications = applications
        self.grant = grant
        self.selectors = selectors
        self._for = _for
        self._if = _if
        self.when = when
        if how is not None:
            self.how = how

    @property
    def code(self):
        """Gets the code of this PolicyCreationRequest.  # noqa: E501

        Code of the policy being created  # noqa: E501

        :return: The code of this PolicyCreationRequest.  # noqa: E501
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this PolicyCreationRequest.

        Code of the policy being created  # noqa: E501

        :param code: The code of this PolicyCreationRequest.  # noqa: E501
        :type code: str
        """
        if self.local_vars_configuration.client_side_validation and code is None:  # noqa: E501
            raise ValueError("Invalid value for `code`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                code is not None and len(code) > 100):
            raise ValueError("Invalid value for `code`, length must be less than or equal to `100`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                code is not None and len(code) < 3):
            raise ValueError("Invalid value for `code`, length must be greater than or equal to `3`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                code is not None and not re.search(r'^(?=.*[a-zA-Z])[\w][\w +-]{2,100}$', code)):  # noqa: E501
            raise ValueError(r"Invalid value for `code`, must be a follow pattern or equal to `/^(?=.*[a-zA-Z])[\w][\w +-]{2,100}$/`")  # noqa: E501

        self._code = code

    @property
    def description(self):
        """Gets the description of this PolicyCreationRequest.  # noqa: E501

        Description of what the policy will be used for  # noqa: E501

        :return: The description of this PolicyCreationRequest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this PolicyCreationRequest.

        Description of what the policy will be used for  # noqa: E501

        :param description: The description of this PolicyCreationRequest.  # noqa: E501
        :type description: str
        """
        if (self.local_vars_configuration.client_side_validation and
                description is not None and len(description) > 1024):
            raise ValueError("Invalid value for `description`, length must be less than or equal to `1024`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                description is not None and len(description) < 0):
            raise ValueError("Invalid value for `description`, length must be greater than or equal to `0`")  # noqa: E501

        self._description = description

    @property
    def applications(self):
        """Gets the applications of this PolicyCreationRequest.  # noqa: E501

        Applications this policy is used with  # noqa: E501

        :return: The applications of this PolicyCreationRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._applications

    @applications.setter
    def applications(self, applications):
        """Sets the applications of this PolicyCreationRequest.

        Applications this policy is used with  # noqa: E501

        :param applications: The applications of this PolicyCreationRequest.  # noqa: E501
        :type applications: list[str]
        """

        self._applications = applications

    @property
    def grant(self):
        """Gets the grant of this PolicyCreationRequest.  # noqa: E501


        :return: The grant of this PolicyCreationRequest.  # noqa: E501
        :rtype: finbourne_access.Grant
        """
        return self._grant

    @grant.setter
    def grant(self, grant):
        """Sets the grant of this PolicyCreationRequest.


        :param grant: The grant of this PolicyCreationRequest.  # noqa: E501
        :type grant: finbourne_access.Grant
        """
        if self.local_vars_configuration.client_side_validation and grant is None:  # noqa: E501
            raise ValueError("Invalid value for `grant`, must not be `None`")  # noqa: E501

        self._grant = grant

    @property
    def selectors(self):
        """Gets the selectors of this PolicyCreationRequest.  # noqa: E501

        Selectors that identify what resources this policy qualifies for  # noqa: E501

        :return: The selectors of this PolicyCreationRequest.  # noqa: E501
        :rtype: list[finbourne_access.SelectorDefinition]
        """
        return self._selectors

    @selectors.setter
    def selectors(self, selectors):
        """Sets the selectors of this PolicyCreationRequest.

        Selectors that identify what resources this policy qualifies for  # noqa: E501

        :param selectors: The selectors of this PolicyCreationRequest.  # noqa: E501
        :type selectors: list[finbourne_access.SelectorDefinition]
        """
        if self.local_vars_configuration.client_side_validation and selectors is None:  # noqa: E501
            raise ValueError("Invalid value for `selectors`, must not be `None`")  # noqa: E501

        self._selectors = selectors

    @property
    def _for(self):
        """Gets the _for of this PolicyCreationRequest.  # noqa: E501

        \"For Specification\" for when the policy is to be applied  # noqa: E501

        :return: The _for of this PolicyCreationRequest.  # noqa: E501
        :rtype: list[finbourne_access.ForSpec]
        """
        return self.__for

    @_for.setter
    def _for(self, _for):
        """Sets the _for of this PolicyCreationRequest.

        \"For Specification\" for when the policy is to be applied  # noqa: E501

        :param _for: The _for of this PolicyCreationRequest.  # noqa: E501
        :type _for: list[finbourne_access.ForSpec]
        """

        self.__for = _for

    @property
    def _if(self):
        """Gets the _if of this PolicyCreationRequest.  # noqa: E501

        \"If Specification\" for when the policy is to be applied  # noqa: E501

        :return: The _if of this PolicyCreationRequest.  # noqa: E501
        :rtype: list[finbourne_access.IfExpression]
        """
        return self.__if

    @_if.setter
    def _if(self, _if):
        """Sets the _if of this PolicyCreationRequest.

        \"If Specification\" for when the policy is to be applied  # noqa: E501

        :param _if: The _if of this PolicyCreationRequest.  # noqa: E501
        :type _if: list[finbourne_access.IfExpression]
        """

        self.__if = _if

    @property
    def when(self):
        """Gets the when of this PolicyCreationRequest.  # noqa: E501


        :return: The when of this PolicyCreationRequest.  # noqa: E501
        :rtype: finbourne_access.WhenSpec
        """
        return self._when

    @when.setter
    def when(self, when):
        """Sets the when of this PolicyCreationRequest.


        :param when: The when of this PolicyCreationRequest.  # noqa: E501
        :type when: finbourne_access.WhenSpec
        """
        if self.local_vars_configuration.client_side_validation and when is None:  # noqa: E501
            raise ValueError("Invalid value for `when`, must not be `None`")  # noqa: E501

        self._when = when

    @property
    def how(self):
        """Gets the how of this PolicyCreationRequest.  # noqa: E501


        :return: The how of this PolicyCreationRequest.  # noqa: E501
        :rtype: finbourne_access.HowSpec
        """
        return self._how

    @how.setter
    def how(self, how):
        """Sets the how of this PolicyCreationRequest.


        :param how: The how of this PolicyCreationRequest.  # noqa: E501
        :type how: finbourne_access.HowSpec
        """

        self._how = how

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, PolicyCreationRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PolicyCreationRequest):
            return True

        return self.to_dict() != other.to_dict()
