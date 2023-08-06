#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 4.0.1-9346c8cc45 (http://hl7.org/fhir/StructureDefinition/OperationOutcome) on 2022-06-21.
#  2022, SMART Health IT.


from . import domainresource

class OperationOutcome(domainresource.DomainResource):
    """ Information about the success/failure of an action.
    
    A collection of error, warning, or information messages that result from a
    system action.
    """
    
    resource_type = "OperationOutcome"

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['issue'] = """A single issue associated with the action."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""

    @classmethod
    def attribute_enums(cls):
        """Get dict of attributes with enums, Code or CodeableConcept."""
        return cls._attribute_enums

    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.issue = None
        """ A single issue associated with the action.
        List of `OperationOutcomeIssue` items (represented as `dict` in JSON). """
        
        super(OperationOutcome, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(OperationOutcome, self).elementProperties()
        js.extend([
            ("issue", "issue", OperationOutcomeIssue, True, None, True),
        ])
        return js


from . import backboneelement

class OperationOutcomeIssue(backboneelement.BackboneElement):
    """ A single issue associated with the action.
    
    An error, warning, or information message that results from a system
    action.
    """

    _attribute_docstrings = {}
    """ Dictionary of attribute documentation."""
    _attribute_docstrings['severity'] = """Indicates whether the issue indicates a variation from successful processing."""
    _attribute_docstrings['code'] = """Describes the type of the issue. The system that creates an OperationOutcome SHALL choose the most applicable code from the IssueType value set, and may additional provide its own code for the error in the details element."""
    _attribute_docstrings['details'] = """Additional details about the error. This may be a text description of the error or a system code that identifies the error."""
    _attribute_docstrings['diagnostics'] = """Additional diagnostic information about the issue."""
    _attribute_docstrings['location'] = """Deprecated: Path of element(s) related to issue."""
    _attribute_docstrings['expression'] = """FHIRPath of element(s) related to issue."""

    @classmethod
    def attribute_docstrings(cls):
        """Get dict of attributes docstrings."""
        return cls._attribute_docstrings

    _attribute_enums = {}
    """ Dictionary of enum configuration."""
    _attribute_enums['severity'] = {
        'url': 'http://hl7.org/fhir/issue-severity',
        'restricted_to': ['fatal', 'error', 'warning', 'information'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['code'] = {
        'url': 'http://hl7.org/fhir/issue-type',
        'restricted_to': ['invalid', 'structure', 'required', 'value', 'invariant', 'security', 'login', 'unknown', 'expired', 'forbidden', 'suppressed', 'processing', 'not-supported', 'duplicate', 'multiple-matches', 'not-found', 'deleted', 'too-long', 'code-invalid', 'extension', 'too-costly', 'business-rule', 'conflict', 'transient', 'lock-error', 'no-store', 'exception', 'timeout', 'incomplete', 'throttled', 'informational'],
        'binding_strength': 'required',
        'class_name': 'str'
    }
    _attribute_enums['details'] = {
        'url': 'http://terminology.hl7.org/CodeSystem/operation-outcome',
        'restricted_to': ['DELETE_MULTIPLE_MATCHES', 'MSG_AUTH_REQUIRED', 'MSG_BAD_FORMAT', 'MSG_BAD_SYNTAX', 'MSG_CANT_PARSE_CONTENT', 'MSG_CANT_PARSE_ROOT', 'MSG_CREATED', 'MSG_DATE_FORMAT', 'MSG_DELETED', 'MSG_DELETED_DONE', 'MSG_DELETED_ID', 'MSG_DUPLICATE_ID', 'MSG_ERROR_PARSING', 'MSG_ID_INVALID', 'MSG_ID_TOO_LONG', 'MSG_INVALID_ID', 'MSG_JSON_OBJECT', 'MSG_LOCAL_FAIL', 'MSG_NO_EXIST', 'MSG_NO_MATCH', 'MSG_NO_MODULE', 'MSG_NO_SUMMARY', 'MSG_OP_NOT_ALLOWED', 'MSG_PARAM_CHAINED', 'MSG_PARAM_INVALID', 'MSG_PARAM_MODIFIER_INVALID', 'MSG_PARAM_NO_REPEAT', 'MSG_PARAM_UNKNOWN', 'MSG_RESOURCE_EXAMPLE_PROTECTED', 'MSG_RESOURCE_ID_FAIL', 'MSG_RESOURCE_ID_MISMATCH', 'MSG_RESOURCE_ID_MISSING', 'MSG_RESOURCE_NOT_ALLOWED', 'MSG_RESOURCE_REQUIRED', 'MSG_RESOURCE_TYPE_MISMATCH', 'MSG_SORT_UNKNOWN', 'MSG_TRANSACTION_DUPLICATE_ID', 'MSG_TRANSACTION_MISSING_ID', 'MSG_UNHANDLED_NODE_TYPE', 'MSG_UNKNOWN_CONTENT', 'MSG_UNKNOWN_OPERATION', 'MSG_UNKNOWN_TYPE', 'MSG_UPDATED', 'MSG_VERSION_AWARE', 'MSG_VERSION_AWARE_CONFLICT', 'MSG_VERSION_AWARE_URL', 'MSG_WRONG_NS', 'SEARCH_MULTIPLE', 'SEARCH_NONE', 'UPDATE_MULTIPLE_MATCHES'],
        'binding_strength': 'example',
        'class_name': 'CodeableConcept'
    }

    @classmethod
    def attribute_enums(cls):
        """Get dict of attributes with enums, Code or CodeableConcept."""
        return cls._attribute_enums

    def __init__(self, jsondict=None, strict=True):
        """ Initialize all valid properties.
        
        :raises: FHIRValidationError on validation errors, unless strict is False
        :param dict jsondict: A JSON dictionary to use for initialization
        :param bool strict: If True (the default), invalid variables will raise a TypeError
        """
        
        self.severity = None
        """ Indicates whether the issue indicates a variation from successful
        processing.
        Type `str`. """
        
        self.code = None
        """ Describes the type of the issue. The system that creates an
        OperationOutcome SHALL choose the most applicable code from the
        IssueType value set, and may additional provide its own code for
        the error in the details element.
        Type `str`. """
        
        self.details = None
        """ Additional details about the error. This may be a text description
        of the error or a system code that identifies the error.
        Type `CodeableConcept` (represented as `dict` in JSON). """
        
        self.diagnostics = None
        """ Additional diagnostic information about the issue.
        Type `str`. """
        
        self.location = None
        """ Deprecated: Path of element(s) related to issue.
        List of `str` items. """
        
        self.expression = None
        """ FHIRPath of element(s) related to issue.
        List of `str` items. """
        
        super(OperationOutcomeIssue, self).__init__(jsondict=jsondict, strict=strict)
    
    def elementProperties(self):
        js = super(OperationOutcomeIssue, self).elementProperties()
        js.extend([
            ("severity", "severity", str, False, None, True),
            ("code", "code", str, False, None, True),
            ("details", "details", codeableconcept.CodeableConcept, False, None, False),
            ("diagnostics", "diagnostics", str, False, None, False),
            ("location", "location", str, True, None, False),
            ("expression", "expression", str, True, None, False),
        ])
        return js


import sys
try:
    from . import codeableconcept
except ImportError:
    codeableconcept = sys.modules[__package__ + '.codeableconcept']
