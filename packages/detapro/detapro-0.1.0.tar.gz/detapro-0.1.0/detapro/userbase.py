from __future__ import annotations
from typing import Optional, Any, Union
from .errors import DisconnectedError

from deta import Deta

__all__ = (
    'User', 
    'UserBase',
)

def fetch_all(base,query):
    objects = []
    last = None
    while True:
        results = base.fetch(query=query,last=last)
        objects.extend(results.items)
        last = results.last
        if last is None:
            return objects

class User:
    '''Represents a Detapro `User` object
    By manually intialising a `User` object, you need to have created a `UserBase` object

    Methods
    -------
    update(self)->None
        Updates user in the database
    '''
    def __init__(self,parent:UserBase,**kwargs)->None:
        self._parent = parent
        if 'key' not in kwargs:
            raise KeyError("'key' is a required argument")
        self.__dict__.update(**kwargs)
        self._parent.add_child(self)
    
    # Decorator to make sure parent is connected before calling method
    def _check_parent(func):
        def _wrapper(self,*args,**kwargs):
            if self._parent is None:
                raise DisconnectedError("Parent UserBase is not connected")
            return func(self,*args,**kwargs)
        _wrapper.__name__ = func.__name__

    # Decorator to check if key is in headers
    def _check_key(func):
        def _wrapper(self,key,value):
            if key not in self._parent.headers:
                raise KeyError(f"'{key}' is not a valid key/header defined in parent headers'")
            elif key == "key":
                raise KeyError("'key' is a reserved value and cannot be changed")
            return func(self,key,value)
        _wrapper.__name__ = func.__name__
    
    @_check_key
    def __setitem__(self,key,value):
        self.__dict__[key] = value
    
    @_check_key
    def __setattr__(self,key,value):
        self.__dict__[key] = value

    def __getitem__(self,key)->Any:
        return self.__dict__[key]
    
    def __getattr__(self,key)->Any: # Essentially Useless, for completeness sake
        return self.__dict__[key]

    def __dict__(self)->dict[str,Any]:
        '''Returns a dictionary of the user's attributes
        Only to be called by the parent class
        '''
        return {k:v for k,v in self.__dict__.items() if not k.startswith('_')}

    @_check_parent
    def update(self)->None:
        '''Updates the user in the database
        '''
        self._parent.update_user(self)

    @_check_parent
    def delete(self)->None:
        '''Deletes the user from the database
        '''
        self._parent.delete_user(self)
        self._parent = None # Disconnects from Parent

    @_check_parent
    def sync(self)->None:
        '''Syncs the user with the database
        Local data will be overwritten

        Warning
        -------
        If key is changed in the database, the local key will have no way of updating
        current object would be made useless
        Solution: Do not change key on other clients
        '''
        self._parent.sync_user(self) 

class UserBase:
    def __init__(self,project_key:str, base_name:str, headers: Optional[dict[str,Any]]=None)->None:
        '''Initialises UserBase object for User management

        Parameters
        ----------
        project_key: str
            The project key of the project to which the deta base belongs (should be kept secret)
        base_name: str
            The name of the deta base to use within the project
        headers: Optional[dict[str,Any]], default=None
            Keys of this dictionary define properties that can be accessed,
            this is to standardise the properties of each user.
            Values of this dictionary define the default values for each property, used when:
            creating a new user or when ambuiguity is present and a value needs to be decided.
            Headers default to the properties of the first user in the base and `None` for each key
            Keys should strictly not start with an underscore as they will be ignored
            The key 'key' is reserved and is automatically added as a header

        Raises
        ------
        RuntimeError
            If headers not provided and no users in base
        '''
        self.base = Deta(project_key).Base(base_name)
        if headers is None:
            results = self.base.fetch(limit=1).items
            if len(results) > 0:
                raise RuntimeError('Cannot set headers. No headers provided and no users in base')
            self.headers = {key:None for key in results[0].keys()}
        else:
            self.headers = headers
        self.headers |= {'key':None}
        self.children = {}

    # New User
    def new_user(self, **kwargs:dict[str, Any])->User:
        '''Creates a new user in the userbase
    
        Parameters:
        -----------
        **kwargs: dict[str, Any]
            A dictionary of key-value pairs to use for the new user
            If key not in headers (defined on initialisation), it will be ignored

        Returns:
        --------
        dict[str, Any]
            A dictionary of actual key-value pairs pushed to the deta base for the new user
        '''
        for prop in kwargs:
            if prop not in self.headers:
                del kwargs[prop]
        assert 'key' in kwargs
        # Deta Documentation: 'key' can be included in kwargs instead of explicitly being passed
        return User(self,self.base.put(kwargs))
    
    # Read User
    def get_user(self,query:Union[str,dict[str,Any]])->User:
        '''Gets a user from the userbase

        Parameters
        ----------
        query: Union[str,dict[str,Any],list[dict]]
            If type `str` is provided, it is assumed to be the key of the user to be read,
            if type `dict[str,Any]` is provided, 
            it is assumed to be a dictionary of postgres query statements
            Accepts `list[dict]`, but a single `dict` is preferred
            See Accepted Syntax Here: https://docs.deta.sh/docs/base/queries/

        Returns
        -------
        User
            Returns User object, creates new aware `User` object if user not found in local cache
        '''
        if isinstance(query,str):
            user_dicts = [self.base.get(query)]
        elif isinstance(query,(dict,list)):
            if isinstance(query,list):
                query = dict((k,v) for k,v in [item for subtup in query for item in subtup])
            user_dicts = fetch_all(self.base,query)
        else:
            raise TypeError("Query must be of type str or dict[str,Any]")

        if user_dicts is None or len(user_dicts) == 0:
            raise KeyError("Query returned nothing")

        results = []
        for user in user_dicts:
            if user['key'] in self.children:
                self.children[user['key']].__dict__.update(**user)
                results.append(self.children[user['key']])
            results.append(User(self,**user))
        return results

    # Update User
    def update_user(self, user:User)->None:
        '''Updates a user in the userbase
        Should not be called directly, instead called from `User.update()`

        Parameters
        ----------
        user: User
            The user object to be updated in the userbase
        '''
        self.base.put(user.__dict__, user.key)
        if user.key not in self.children:
            self.children[user.key] = user

    # Update All Children
    def update_children(self)->None:
        '''Updates all children in the local cache
        Under the hood, it runs `update_children` on each child
        '''
        for child in self.children:
            child.update()

    # Delete User
    def delete_user(self, user:User)->None:
        '''Deletes a user from the userbase
        Should not be called directly, instead called from `User.delete()`

        Parameters
        ----------
        user: User
            The user object to be deleted from the userbase
        '''
        if user.key in self.children:
            del self.children[user.key]
        self.base.delete(user.key)

    # Sync User
    def sync_user(self, user:User)->None:
        '''Sync local user with database values
        Should not be called directly, instead called from `User.sync()`

        Warning
        -------
        Local values will be overwritten without question
        '''
        new_data = self.base.get(user.__dict__, user.key)
        user.__dict__.update(**new_data)

    # Sync All Children
    def sync_children(self)->None:
        '''Sync children users with database values
        Under the hood, it runs `User.sync()` on each child

        Warning
        -------
        Local values will be overwritten without question
        '''
        for child in self.children:
            child.sync()

    # Internal Method
    def add_child(self,child:User)->int:
        '''Adds a child to local UserBase Cache
        Not to be invoked dierectly, instead called from `User.__init__`

        Parameters
        ----------
        child: User
            The child to add to the local cache
        
        Returns
        -------
        int
            The number of children in the local cache
        '''
        self.children[child.key] = child
        return len(self.children.keys())
