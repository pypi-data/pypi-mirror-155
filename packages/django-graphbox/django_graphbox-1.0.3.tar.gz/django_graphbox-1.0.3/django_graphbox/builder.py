# graphene imports
import graphene
from graphene_django.types import DjangoObjectType
# django imports
from django.db.models import Q
from django.core.files import File
from django.core.files.images import ImageFile
from PIL import Image
from django.contrib.auth.hashers import make_password
# helper functions
from .helpers import create_arguments_class, update_arguments_class, delete_arguments_class, get_access_group, evaluate_result
from .helpers import HashManager
# error management
from .exceptions import ErrorManager, ErrorMsgType
# global constants
from .constants import *

class SchemaBuilder:
    """ Class provides the functionality to build a GraphQL schema with basic operations: field_by_id, list_field, create_field, update_field and delete_field."""
    _models_config = {}
    _models_by_op_name = {}

    def __init__(self, session_manager=None):
        """Initialize the schema builder.

        Args:
            session_manager (SessionManager): Session manager to use.
        """
        self._session_manager = session_manager

    def add_model(self, model, exclude_fields=(), pagination_length=0, external_filters=[], internal_filters=[], filters_opeator=Q.AND, access_group=None, access_by_operation={}, validators_by_operation={}, internal_field_resolvers={}, save_as_password=[]):
        """Add a model to the schema.

        Args:
            model (Model): Model to add to the schema.
            exclude_fields (tuple): Fields to exclude from the model type.
            pagination_length (int): Number of items to return in a paginated response. 0 means no pagination.
            external_filters (list): Filters to apply to the model. 
            internal_filters (list): Internal filters to apply to the model. 
            filters_opeator (Q.AND, Q.OR): Operator to use for the filters.
            access_group (str): Access group to use for this model. This will be overriden by the access_by_operation.
            access_by_operation (dict): Dictionary with the operations to use for the access. {'operation': 'access_group', ...}
            validators_by_operation (dict): Dictionary with the validators to use for the access. {'operation': callable(info, model_instance, **kwargs), ...}
            internal_field_resolvers (dict): Dictionary with the internal field value resolvers on create_field and update_field operations
            save_as_password (list): List of fields to save as password.

        This function will add the model to the schema. Here is an example of how to use this function:
        Example::
            from django_graphbox.schema import SchemaBuilder
            from django_graphbox.models import User
            from django_graphbox.session_manager import SessionManager
            from project.settings import ACCESS_GROUPS, MODIFY_PERMISSIONS

            def custom_callable_validator(info, model_instance, **kwargs):
                ''' Custom callable validator example. '''
                return True

            session_manager = SessionManager(User, security_key='SECRET_KEY', groups=ACCESS_GROUPS, modify_permissions=MODIFY_PERMISSIONS)
            schema_builder = SchemaBuilder(session_manager)
            schema_builder.add_model(
                User, 
                exclude_fields=('password',), 
                save_as_password=['password',],
                access_group=GROUP_RESPONSABLE,
                validators_by_operation={
                    'create_field': {
                        'validators':(
                            custom_callable_validator,
                            {
                                'validators': (
                                    session_manager.actual_user_comparer(actual_user_field='parent_field', operator='=', model_field='parent_field'),
                                    session_manager.actual_user_comparer(actual_user_field='parent_field', operator='=', default_value=None),
                                ),
                                'connector': 'OR'
                            }
                        ),
                        'connector': 'AND',
                    },
                    'update_field': {
                        'validators':(
                            custom_callable_validator,
                            {
                                'validators': (
                                    session_manager.actual_user_comparer(actual_user_field='parent_field', operator='=', model_field='parent_field'),
                                    session_manager.actual_user_comparer(actual_user_field='parent_field', operator='=', default_value=None),
                                ),
                                'connector': 'OR'
                            }
                        ),
                        'connector': 'AND',
                    },
                    'delete_field': {
                        'validators':(
                            custom_callable_validator,
                            {
                                'validators': (
                                    session_manager.actual_user_comparer(actual_user_field='parent_field', operator='=', model_field='parent_field'),
                                    session_manager.actual_user_comparer(actual_user_field='parent_field', operator='=', default_value=None),
                                ),
                                'connector': 'OR'
                            }
                        ),
                        'connector': 'AND',
                    },
                },
            ) # after this line the model will be added to the schema and ready to build the schema operations with build_schema_query and build_schema_mutation functions
        """
        #get the model name
        model_name = model.__name__
        #crreate the model type
        model_metaclass = type(f"Meta", (), {'model': model, 'exclude_fields': exclude_fields})
        model_type = type(f"{model_name}Type", (DjangoObjectType,), {'Meta': model_metaclass})
        #make a new model config
        config = {
            'model': model,
            'name': model_name,
            'type': model_type,
            'pagination_length': pagination_length,
            'external_filters': external_filters,
            'internal_filters': internal_filters,
            'filters_operator': filters_opeator,
            'access_group': access_group,
            'access_by_operation': access_by_operation,
            'validators_by_operation': validators_by_operation,
            'internal_field_resolvers': internal_field_resolvers,
            'save_as_password': save_as_password,
        }
        self._models_config[model_name]=config

    def build_schema_query(self):
        """ Build query class for the schema.
        Returns:
            graphene.ObjectType: Query class for the schema.

        This function will build the query class for the schema. Here is an example of the query class:
        Example::
            class Query(graphene.ObjectType):
                user = graphene.Field(UserType, id=graphene.Int())
                all_users = graphene.List(UserType)
        Calling this function will return the query class for the schema:
        Example::
            query_class = schema_builder.build_schema_query()
        After this line the query class will be ready to use on the main schema:
        Example::
            import graphene
            class Query(query_class, graphene.ObjectType):
                pass
            schema = graphene.Schema(query=Query)
        And add the schema on a path on urls.py:
        Example::
            from graphene_django.views import GraphQLView
            path('graphql', GraphQLView.as_view(graphiql=True, schema=schema))
        The query can be called as GraphQL:
        Example::
            query {
                user(id: 1) {
                    id
                    name
                }
                allUsers {
                    id
                    name
                }
            }
        """
        query_class= type("Query", (graphene.ObjectType,), {})
        for key in self._models_config.keys():
            model_config=self._models_config[key]
            def field_resolver_function(parent, info, **kwargs):
                # get model config by this path
                operation_name=info.operation.selection_set.selections[0].name.value.lower()
                config=self._models_by_op_name[operation_name]
                # get access group for validate access
                access_group=get_access_group('field_by_id', config)
                if self._session_manager!=None:
                    valid, actual_user_instance, error=self._session_manager.validate_access(info.context, access_group)
                else:
                    valid=True
                if valid:
                    model=config.get('model')
                    result=model.objects.get(id=kwargs.get('id'))
                    valid_operation=True
                    if 'field_by_id' in config['validators_by_operation']:
                        valid_operation=evaluate_result(config['validators_by_operation']['field_by_id'], info, result, **kwargs)
                    if valid_operation:
                        return result
                return None
            def list_resolver_function(parent, info, **kwargs):
                operation_name=info.operation.selection_set.selections[0].name.value.lower()
                config=self._models_by_op_name[operation_name]
                pagination_length=config.get('pagination_length')
                external_filters=config.get('external_filters')
                filters_operator=config.get('filters_operator')
                query_object=None
                for filter_config in external_filters:
                    param_value=kwargs.get(filter_config.get('param_name'))
                    if param_value is not None:
                        if query_object is None:
                            query_object=Q(**{filter_config.get('field_name'): param_value})
                        else:
                            query_object.add(Q(**{filter_config.get('field_name'): param_value}), filters_operator)
                internal_filters=config.get('internal_filters')
                for filter_config in internal_filters:
                    resolver_filter=filter_config.get('resolver_filter')
                    on_return_none=filter_config.get('on_return_none')
                    value_filter=resolver_filter(info, kwargs)
                    if value_filter==None:
                        if on_return_none=='skip':
                            continue
                        elif on_return_none=='set__isnull':
                            if query_object is None:
                                query_object=Q(**{f"{filter_config.get('field_name')}__isnull": True})
                            else:
                                query_object.add(Q(**{f"{filter_config.get('field_name')}__isnull": True}), filters_operator)
                    else:
                        if query_object is None:
                            query_object=Q(**{filter_config.get('field_name'): value_filter})
                        else:
                            query_object.add(Q(**{filter_config.get('field_name'): value_filter}), filters_operator)
                if query_object is None:
                    query_object=Q()
                # get access group for validate access
                access_group=get_access_group('list_field', config)
                if self._session_manager!=None:
                    valid, actual_user_instance, error=self._session_manager.validate_access(info.context, access_group)
                else:
                    valid=True
                if valid:
                    model=config.get('model')
                    if pagination_length == 0:
                        result=model.objects.filter(query_object)
                    else:
                        pagina=kwargs.get('pagina')
                        inicio=(pagina*pagination_length)-pagination_length
                        fin=inicio+pagination_length
                        result=model.objects.filter(query_object)[inicio:fin]
                    return result
                return None
            object_name=model_config['name'].lower()
            self._models_by_op_name[object_name]=model_config
            setattr(query_class, object_name, graphene.Field(model_config['type'], id=graphene.ID(required=True)))
            setattr(query_class, f'resolve_{object_name}', field_resolver_function)
            self._models_by_op_name['all' + object_name]=model_config
            filters_args={}
            external_filters=model_config.get('external_filters')
            for filter_config in external_filters:
                filters_args[filter_config.get('param_name')]=filter_config.get('param_type')
            if model_config.get('pagination_length') != 0:
                filters_args['pagina']=graphene.Int(required=True)
            setattr(query_class, f"all_{object_name}", graphene.List(model_config['type'], filters_args))
            setattr(query_class, f'resolve_all_{object_name}', list_resolver_function)
        return query_class
    
    def build_schema_mutation(self):
        """Build mutations class for the schema. 
        Returns:
            graphene.ObjectType: Schema mutation.
        This function is used to build the mutation class for the schema. Here is an example of the mutation class:
        Example::
            class CreateUser(graphene.Mutation):
                ... # fields, arguments and resolve function
            class UpdateUser(graphene.Mutation):
                ... # fields, arguments and resolve function
            class DeleteUser(graphene.Mutation):
                ... # fields, arguments and resolve function

            class Mutation(graphene.ObjectType):
                create_user = CreateUser.Field()
                update_user = UpdateUser.Field()
                delete_user = DeleteUser.Field()
        Calling this function will return class:
        Example::
            mutation_class=schema_builder.build_schema_mutation()
        After this line the mutation class is ready to use on the main schema:
        Example::
            import graphene
            class Query(query_class, graphene.ObjectType):
                pass
            class Mutation(mutation_class, graphene.ObjectType):
                pass
            schema = graphene.Schema(query=Query, mutation=Mutation)
        And add the schema on a path on urls.py:
        Example::
            from graphene_django.views import GraphQLView
            path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema))
        """
        mutation_class= type("Mutation", (), {})
        for key in self._models_config.keys():
            model_config=self._models_config[key]
            # create the create mutation
            def mutate_create_function(parent, info, **kwargs):
                operation_name=info.operation.selection_set.selections[0].name.value.lower()
                config=self._models_by_op_name[operation_name]
                # get access group for validate access
                access_group=get_access_group('create_field', config)
                if self._session_manager!=None:
                    valid, actual_user_instance, session_error=self._session_manager.validate_access(info.context, access_group)
                else:
                    valid=True
                model=config.get('model')
                return_object=type(info.return_type.name, (graphene.ObjectType,), {'estado':graphene.Boolean(), model.__name__.lower():graphene.Field(config['type']),'error':graphene.Field(ErrorMsgType)})
                if valid:
                    try:
                        instance=model()
                        # get internal resolvers
                        internal_field_resolvers=model_config.get('internal_field_resolvers')
                        if 'create_field' in internal_field_resolvers.keys():
                            fields_to_resolve=internal_field_resolvers.get('create_field')
                            kwargs.update(fields_to_resolve)
                        for key, value in kwargs.items():
                            field_type=instance._meta.get_field(key).__class__.__name__
                            if callable(value):
                                value=value(info, instance, **kwargs)
                            if field_type=='ForeignKey':
                                foreign_model=instance._meta.get_field(key).related_model
                                value=foreign_model.objects.get(id=value)
                                setattr(instance, key, value)
                            elif field_type=='FileField':
                                file=File(value)
                                extension=file.name.split('.')[-1]
                                sha1_file=HashManager.getSHA1file(file)
                                getattr(instance, key).save(f'{sha1_file}.{extension}', file, save=False)
                            elif field_type=='ImageField':
                                #test if is a valid image
                                Image.open(value)
                                file=ImageFile(value)
                                extension=file.name.split('.')[-1]
                                sha1_file=HashManager.getSHA1file(file)
                                getattr(instance, key).save(f'{sha1_file}.{extension}', file, save=False)
                            elif key in config.get('save_as_password'):
                                value=make_password(value)
                                setattr(instance, key, value)
                            else:
                                if getattr(model, key).field.choices!=None and len(getattr(model, key).field.choices)>0:
                                    choices=getattr(model, key).field.choices
                                    valid_options=[c[0] for c in choices]
                                    if value not in valid_options:
                                        raise Exception(f'{value} no es una opción válida para {key}')
                                setattr(instance, key, value)
                        # evaluate validators
                        valid_operation=True
                        if 'create_field' in config['validators_by_operation']:
                            valid_operation=evaluate_result(config['validators_by_operation']['create_field'], info, instance, **kwargs)
                        if valid_operation:
                            instance.save()
                            return return_object(**{'estado':True, model.__name__.lower():instance, 'error':ErrorManager.get_error_by_code(NO_ERROR)})
                        else:
                            return return_object(**{'estado':False, 'error':ErrorManager.get_error_by_code(INSUFFICIENT_PERMISSIONS)})
                    except Exception as e:
                        return return_object(**{'estado':False, 'error':ErrorManager.get_error_by_code(error_code=UNKNOWN_ERROR, custom_message="Error Inesperado", custom_description=str(e))})
                else:
                    return return_object(**{'estado':False, 'error':session_error})
            fields_resolved_internal=[]
            internal_field_resolvers=model_config.get('internal_field_resolvers')
            if 'create_field' in internal_field_resolvers.keys():
                fields_resolved_internal=internal_field_resolvers.get('create_field').keys()
            arguments_create=create_arguments_class(model_config['model'], fields_resolved_internal)
            create_mutation=type("Create"+model_config['name'], (graphene.Mutation,), {"estado":graphene.Boolean(),model_config['name'].lower(): graphene.Field(model_config['type']), "error":graphene.Field(ErrorMsgType), 'Arguments': arguments_create, 'mutate': mutate_create_function})
            setattr(mutation_class, f"create_{model_config['name'].lower()}", create_mutation.Field())
            self._models_by_op_name['create' + model_config['name'].lower()]=model_config
            # create the update mutation
            def mutate_update_function(parent, info, **kwargs):
                operation_name=info.operation.selection_set.selections[0].name.value.lower()
                config=self._models_by_op_name[operation_name]
                # get access group for validate access
                access_group=get_access_group('update_field', config)
                if self._session_manager!=None:
                    valid, actual_user_instance, session_error=self._session_manager.validate_access(info.context, access_group)
                else:
                    valid=True
                model=config.get('model')
                return_object=type(info.return_type.name, (graphene.ObjectType,), {'estado':graphene.Boolean(), model.__name__.lower():graphene.Field(config['type']),'error':graphene.Field(ErrorMsgType)})
                if valid:
                    try:
                        if model.objects.filter(id=kwargs.get('id')).exists():
                            instance=model.objects.get(id=kwargs.get('id'))
                            valid_operation=True
                            if 'update_field' in config['validators_by_operation']:
                                valid_operation=evaluate_result(config['validators_by_operation']['update_field'], info, instance, **kwargs)
                            if valid_operation:
                                # get internal resolvers
                                internal_field_resolvers=model_config.get('internal_field_resolvers')
                                if 'update_field' in internal_field_resolvers.keys():
                                    fields_to_resolve=internal_field_resolvers.get('update_field')
                                    kwargs.update(fields_to_resolve)
                                for key, value in kwargs.items():
                                    if key!='id':
                                        field_type=instance._meta.get_field(key).__class__.__name__
                                        if callable(value):
                                            value=value(info, instance, **kwargs)
                                        if field_type=='ForeignKey':
                                            foreign_model=instance._meta.get_field(key).related_model
                                            value=foreign_model.objects.get(id=value)
                                            setattr(instance, key, value)
                                        elif field_type=='FileField':
                                            file=File(value)
                                            extension=file.name.split('.')[-1]
                                            sha1_file=HashManager.getSHA1file(file)
                                            getattr(instance, key).save(f'{sha1_file}.{extension}', file, save=False)
                                        elif field_type=='ImageField':
                                            #test if is a valid image
                                            Image.open(value)
                                            file=ImageFile(value)
                                            extension=file.name.split('.')[-1]
                                            sha1_file=HashManager.getSHA1file(file)
                                            getattr(instance, key).save(f'{sha1_file}.{extension}', file, save=False)
                                        elif key in config.get('save_as_password'):
                                            value=make_password(value)
                                            setattr(instance, key, value)
                                        else:
                                            if getattr(model, key).field.choices!=None and len(getattr(model, key).field.choices)>0:
                                                choices=getattr(model, key).field.choices
                                                valid_options=[c[0] for c in choices]
                                                if value not in valid_options:
                                                    raise Exception(f'{value} no es una opción válida para {key}')
                                            setattr(instance, key, value)
                                instance.save()
                                return return_object(**{'estado':True, model.__name__.lower():instance, 'error':ErrorManager.get_error_by_code(NO_ERROR)})
                            else:
                                return return_object(**{'estado':False, 'error':ErrorManager.get_error_by_code(INSUFFICIENT_PERMISSIONS)})
                        else:
                            return return_object(**{'estado':False, 'error':ErrorManager.get_error_by_code(INSTANCE_NOT_FOUND)})
                    except Exception as e:
                        return return_object(**{'estado':False, 'error':ErrorManager.get_error_by_code(error_code=UNKNOWN_ERROR,custom_message="Error Inesperado", custom_description=str(e))})
                else:
                    return return_object(**{'estado':False, 'error':session_error})
            fields_resolved_internal=[]
            internal_field_resolvers=model_config.get('internal_field_resolvers')
            if 'update_field' in internal_field_resolvers.keys():
                fields_resolved_internal=internal_field_resolvers.get('update_field').keys()
            arguments_update=update_arguments_class(model_config['model'], fields_resolved_internal)
            update_mutation=type("Update"+model_config['name'], (graphene.Mutation,), {"estado":graphene.Boolean(),model_config['name'].lower(): graphene.Field(model_config['type']), "error":graphene.Field(ErrorMsgType), 'Arguments': arguments_update, 'mutate': mutate_update_function})
            setattr(mutation_class, f"update_{model_config['name'].lower()}", update_mutation.Field())
            self._models_by_op_name['update' + model_config['name'].lower()]=model_config
            # create the delete mutation
            def mutate_delete_function(parent, info, **kwargs):
                operation_name=info.operation.selection_set.selections[0].name.value.lower()
                config=self._models_by_op_name[operation_name]
                # get access group for validate access
                access_group=get_access_group('delete_field', config)
                if self._session_manager!=None:
                    valid, actual_user_instance, session_error=self._session_manager.validate_access(info.context, access_group)
                else:
                    valid=True
                model=config.get('model')
                return_object=type(info.return_type.name, (graphene.ObjectType,), {'estado':graphene.Boolean(), 'error':graphene.Field(ErrorMsgType)})
                if valid:
                    try:
                        if model.objects.filter(id=kwargs.get('id')).exists():
                            instance=model.objects.get(id=kwargs.get('id'))
                            valid_operation=True
                            if 'delete_field' in config['validators_by_operation']:
                                valid_operation=evaluate_result(config['validators_by_operation']['delete_field'], info, instance, **kwargs)
                            if valid_operation:
                                instance.delete()
                                return return_object(**{'estado':True, 'error':ErrorManager.get_error_by_code(NO_ERROR)})
                            else:
                                return return_object(**{'estado':False, 'error':ErrorManager.get_error_by_code(INSUFFICIENT_PERMISSIONS)})
                        else:
                            return return_object(**{'estado':False, 'error':ErrorManager.get_error_by_code(INSTANCE_NOT_FOUND)})
                    except Exception as e:
                        return return_object(**{'estado':False, 'error':ErrorManager.get_error_by_code(error_code=UNKNOWN_ERROR,custom_message="Error Inesperado", custom_description=str(e))})
                else:
                    return return_object(**{'estado':False, 'error':session_error})
            delete_arguments=delete_arguments_class()
            delete_mutation=type("Delete"+model_config['name'], (graphene.Mutation,), {"estado":graphene.Boolean(), "error":graphene.Field(ErrorMsgType), 'Arguments': delete_arguments, 'mutate': mutate_delete_function})
            setattr(mutation_class, f"delete_{model_config['name'].lower()}", delete_mutation.Field())
            self._models_by_op_name['delete' + model_config['name'].lower()]=model_config
        return mutation_class

    def build_session_schema(self):
        """ Build the session mutations and queries

        Returns:
            tuple: (session_query_class, session_mutation_class)

        The session_query_class is a class with this structure:
        Example::
            class Query(graphene.ObjectType):
                actual_user = graphene.Field(UserType)
        The session_mutation_class is a class with this structure:
        Example::
            class Login(graphene.Mutation):
                estado = graphene.Boolean()
                error = graphene.Field(ErrorMsgType)
                token = graphene.String()
                user = graphene.Field(UserType) # argument name is the same as the session_manager user model

                class Arguments:
                    username = graphene.String(required=True) # the arguments name is the same as the field name of session_manager user model
                    password = graphene.String(required=True)
                    permanent = graphene.Boolean(required=True)
                
                def mutate(self, info, username, password, permanent):
                    ... # do the login
                
            class Mutation(graphene.ObjectType):
                login = Login.Field()
        Calling this function will create the session_query_class and session_mutation_class:
        Example::
            session_query_class, session_mutation_class=session_builder.build_session_schema()
        After this line the session query and mutation class is ready to use on the main schema:
        Example::
            import graphene
            class Query(query_class, session_query_class, graphene.ObjectType):
                pass
            class Mutation(mutation_class, session_mutation_class, graphene.ObjectType):
                pass
            schema = graphene.Schema(query=Query, mutation=Mutation)
        And add the schema on a path on urls.py:
        Example::
            from graphene_django.views import GraphQLView
            path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema))
        """
        if self._session_manager!=None:
            if self._session_manager.user_model.__name__ in self._models_config.keys():
                config_login_model=self._models_config[self._session_manager.user_model.__name__]
            else:
                #get the model name
                model_name = self._session_manager.user_model.__name__
                #crreate the model type
                model_metaclass = type(f"Meta", (), {'model': self._session_manager.user_model, 'excld_fields': (self._session_manager.password_field_name,)})
                model_type = type(f"{model_name}Type", (DjangoObjectType,), {'Meta': model_metaclass})
                config_login_model = {
                    'model': self._session_manager.user_model,
                    'name': model_name,
                    'type': model_type,
                    'pagination_length': 0,
                    'filters': {},
                    'filters_operator': Q.AND,
                    'access_group': None,
                    'access_by_operation': {}
                }
                self._models_config[model_name]=config_login_model
            #build Login Mutation
            mutation_class= type("Mutation", (), {})
            arguments_class= type("Arguments", (), {'permanent':graphene.Boolean(required=True)})
            setattr(arguments_class, self._session_manager.login_id_field_name, graphene.String(required=True))
            setattr(arguments_class, self._session_manager.password_field_name, graphene.String(required=True))
            def login_mutate_function(parent, info, **kwargs):
                config=self._models_by_op_name['login']
                login_id_value=kwargs.get(self._session_manager.login_id_field_name)
                password_value=kwargs.get(self._session_manager.password_field_name)
                permanent=kwargs.get('permanent')
                valid, user_instance, token, error=self._session_manager.start_session(login_id_value, password_value, permanent)
                return_object=type(info.return_type.name, (graphene.ObjectType,), {'estado':graphene.Boolean(),'token':graphene.String(), user_instance.__class__.__name__:graphene.Field(config['type']),'error':graphene.Field(ErrorMsgType)})
                return return_object(**{'estado':valid,'token':token, user_instance.__class__.__name__:user_instance, 'error':error})
            login_mutation=type("Login", (graphene.Mutation,), {'estado': graphene.Boolean(), config_login_model['name'].lower(): graphene.Field(config_login_model['type']), 'token':graphene.String(), 'error': graphene.Field(ErrorMsgType), 'Arguments': arguments_class, 'mutate': login_mutate_function})
            setattr(mutation_class, "login", login_mutation.Field())
            self._models_by_op_name['login']=config_login_model
            # build actual_user query
            query_class= type("Query", (graphene.ObjectType,), {})
            def actual_user_function(parent, info, **kwargs):
                valid, user_instance, error=self._session_manager.validate_access(info.context, 'all')
                return user_instance
            setattr(query_class, "actual_user", graphene.Field(config_login_model['type']))
            setattr(query_class, "resolve_actual_user", actual_user_function)
            self._models_by_op_name['actualuser']=config_login_model
            return query_class, mutation_class
        else:
            assert False, "Session Manager not defined"