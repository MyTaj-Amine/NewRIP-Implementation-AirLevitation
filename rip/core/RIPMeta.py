import ujson


class RIPSerializable(object):

    def __init__(self):
        self.name = 'Object'
        self.data = {}

    def set(self, key, value):
        self.data[key] = value

    def get(self, key, value):
        return self.data[key]

    def __repr__(self):
        return ujson.dumps(self.data, escape_forward_slashes=False)


class RIPMetadata(RIPSerializable):

    def __init__(self, info, readables, writables):
        super(RIPMetadata, self).__init__()
        self.data = {
            'info': info.data,
            'readables': readables.data,
            'writables': writables.data,
        }


class RIPServerInfo(RIPSerializable):

    def __init__(self, name, description, authors='', keywords=''):
        super(RIPServerInfo, self).__init__()
        self.name = 'info'
        self.data = {
            'name': name,
            'description': description,
            'authors': authors,
            'keywords': keywords,
        }


class RIPMethod(RIPSerializable):
    """ Encapsulates metadata of a RIP Method """
    def __init__(self, url, type_, description='Dummy Method', params=[], returns='text/event-stream', example=''):
        super(RIPMethod, self).__init__()
        self.name = 'method'
        try:
            params = [x.data for x in params]
        except:
            pass
        self.data = {
            'url': url,
            # 'name': name,
            'type': type_,
            'description': description,
            'params': params,
            'returns': returns,
            'example': example,
        }


class RIPVariable(RIPSerializable):

    def __init__(self, name, description='Variable', type_='float', min_=0, max_=1, precision=0):
        super(RIPVariable, self).__init__()
        self.name = 'variable'
        self.data = {
            'name': name,
            'description': description,
            'type': type_,
            'min': min_,
            'max': max_,
            'precision': precision,
        }


class RIPVariablesList(RIPSerializable):

    def __init__(self, list_, methods, read_notwrite=False):
        super(RIPVariablesList, self).__init__()
        if read_notwrite:
            self.name = 'readables'
        else:
            self.name = 'writables'

        self.set('list', list_)
        self.set('methods', [x.data for x in methods])


class RIPParam(RIPSerializable):

    def __init__(self, name, required, location, type_=None, subtype=None, value=None, elements=None):
        super(RIPParam, self).__init__()
        self.data = {
            'name': name,
            'required': required,
            'location': location
        }
        if value is not None: self.set('value', value)
        if subtype is not None: self.set('subtype', subtype)
        if type_ is not None: self.set('type', type_)
        if elements is not None: self.set('type', elements)


class RIPExperienceList(RIPSerializable):

    def __init__(self, list_, methods):
        super(RIPExperienceList, self).__init__()
        try:
            m = [x.data for x in methods]
        except:
            m = []
        self.data = {'experiences': {'list': list_, 'methods': m}}
