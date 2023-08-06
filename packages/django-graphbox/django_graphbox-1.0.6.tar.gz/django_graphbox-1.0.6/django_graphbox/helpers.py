""" Helper functions for building schema """
from .constants import MODEL_FIELD_TO_GRAPHENE_TYPE
import graphene

def create_arguments_class(model, fields_resolved_internal=[]):
    """Create graphene arguments class for create_field operation

    Args:
        model (object): Django model class to create arguments class for.
        fields_resolved_internal (list): list of fields resolved internally that don't need to be on arguments class.
    Returns:
        class: Arguments class

    The returned class has this structure:
    Example::
        class Arguments:
            model_field_name_str = graphene.String(required=True) # required=True if field is not null
            model_field_name_2_bool = graphene.Boolean(required=True) # model_field will be converted to equivalent graphene type
    """
    class Arguments:
        pass
    exclude_fields = ['id', 'created_at', 'updated_at'] + fields_resolved_internal
    for field in model._meta.fields:
        if field.name not in exclude_fields:
            field_type=field.get_internal_type()
            if field_type!='ManyToManyField':
                argument_type=MODEL_FIELD_TO_GRAPHENE_TYPE[field_type]
                required=True
                if field.null:
                    required=False
                setattr(Arguments, field.name.lower(), argument_type(required=required))
    return Arguments

def update_arguments_class(model, fields_resolved_internal=[]):
    """ Create graphene arguments class for update_field operation 
    
    Args:
        model (object): Django model class to create arguments class for.
        fields_resolved_internal (list): list of fields resolved internally that don't need to be on arguments class.
    Returns:
        class: Arguments class

    The returned class has this structure:
    Example::
        class Arguments:
            id = graphene.ID(required=True)
            model_field_name_str = graphene.String(required=True) # required=True if field is not null
            model_field_name_2_bool = graphene.Boolean(required=True) # model_field will be converted to equivalent graphene type
    """
    class Arguments:
        pass
    exclude_fields = ['created_at', 'updated_at'] + fields_resolved_internal
    for field in model._meta.fields:
        if field.name not in exclude_fields:
            field_type=field.get_internal_type()
            if field_type!='ManyToManyField':
                argument_type=MODEL_FIELD_TO_GRAPHENE_TYPE[field_type]
                required=True
                if field.null:
                    required=False
                setattr(Arguments, field.name.lower(), argument_type(required=required))
    return Arguments

def delete_arguments_class():
    """ Create graphene arguments class for delete_field operation 
    
    Returns:
        class: Arguments class
    The returned class has this structure:
    Example::
        class Arguments:
            id = graphene.ID(required=True)
    """
    class Arguments:
        id=graphene.ID(required=True)
    return Arguments

def get_access_group(operation, model_config):
    """ Get access group for operation based on model config 
    
    Args:
        operation (str): operation name
        model_config (dict): model config

    Returns:
        str: access group finaly selected for operation
    """
    if operation in model_config['access_by_operation']:
        return model_config['access_by_operation'][operation]
    return model_config['access_group']

import hashlib

class HashManager:
    """ Hash manager class """
    @classmethod
    def getSHA1file(cls, file):
        """ Get SHA1 hash of file 
        
        Args:
            file (File): File to hash

        Returns:
            str: SHA1 hash of file
        """
        BLOCKSIZE = 65536
        hasher = hashlib.sha1()
        buf = file.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = file.read(BLOCKSIZE)
        return (hasher.hexdigest())

def evaluate_result(operation, info, model_instance, **kwargs):
    """Evaluate result of operation validators and return a boolean result

    Args:
        operation (dict): operation validators config.
        info (dict): graphql.execution.base.ResolveInfo object.
        model_instance (object): model instance of operation.
        **kwargs (dict): kwargs input from graphql.
    Returns:
        bool: Result of evaluation of validators of operation config.

    The argguments needs to be passed in the following structure:
    Example::
        result = evaluate_result(
            operation={
                'validators': (callable_1(info, model_instance, **kwargs), callable_2(info, model_instance, **kwargs), ...),
                'connector': 'AND' or 'OR'
            }, 
            info=info, 
            model_instance=model_instance, 
            **kwargs
            )
        result = evaluate_result(
            operation={
                'validators': [
                    {
                        'validators':(callable_1(info, model_instance, **kwargs), callable_2(info, model_instance, **kwargs), ...),
                        'connector': 'AND' (default) or 'OR'
                        }, 
                    ...
                    ],
                'connector': 'AND' or 'OR'
                }, 
            info=info, 
            model_instance=model_instance, 
            **kwargs
            )
    """
    if 'validators' in operation:
        validators = operation['validators']
        if 'connector' in operation:
            connector = operation['connector']
        else:
            connector = 'AND'
        if connector == 'AND':
            result = True
            for validator in validators:
                if callable(validator):
                    result = result and validator(info, model_instance, **kwargs)
                else:
                    if validator==None:
                        raise Exception('Validator must be a callable or dict with validators and connector')
                    else:
                        result = result and evaluate_result(validator, info, model_instance, **kwargs)
            return result
        else:
            result = False
            for validator in validators:
                if callable(validator):
                    result = result or validator(info, model_instance, **kwargs)
                else:
                    if validator==None:
                        raise Exception('Validator must be a callable or dict with validators and connector')
                    else:
                        result = result or evaluate_result(validator, info, model_instance, **kwargs)
            return result
    else:
        return True
