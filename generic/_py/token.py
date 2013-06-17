'''
 token.py

 @author: Leevi
'''

class FTQuote:
    def __init__(self, text, modifier=''):
        assert type(text) is str, 'FTQuote-"text" is not a string.'
        assert type(modifier) is str, 'FTQuote-"modifier" is not string.'
        assert len(modifier) < 2, 'FTQuote-"modifier" is not a char.'

        self.text = text
        self.modifier = modifier
        pass
    pass

class FTValue:
    def __init(self, vtype, value):
        assert type(vtype) is str, 'FTValue-"vtype" is not a string.'
        # not to check the value.

        self.vtype = vtype
        self.value = value
        pass
    pass

class FTSpecial:
    pass

class FTClause:
    def __init__(self, subject, objects, indent=-1):
        assert (type(subject) is FTQuote or 
                type(subject) is FTValue or
                type(subject) is FTClause or
                type(subject) is FTRef or
                type(subject) is FTDyRef), 'FTClause-"subject" is invalid.'
        assert type(objects) is list, 'FTClause-"objects" is not a list.'
        for obj in objects:
            assert (type(obj) is FTQuote or 
                    type(obj) is FTValue or
                    type(obj) is FTClause or
                    type(obj) is FTRef or
                    type(obj) is FTDyRef or
                    isinstance(subject, FTSpecial)), 'FTClause-"obj" is invalid.'
        assert type(indent) is int, 'FTClause-"indent" is not a integer.'

        self.subject = subject
        self.objects = tuple(objects)
        self.indent = indent
        pass

    def decl(target, entity, indent=-1):
        assert (type(target) is FTQuote or
                type(target) is FTRef or
                type(target) is FTQuoList), 'FTClause-decl-"target" is invalid.'
        assert (type(entity) is FTQuote or
                type(entity) is FTValue or
                type(entity) is FTClause or
                type(entity) is FTRef or
                type(entity) is FTDyRef), 'FTClause-decl-"entity" is invalid.'

        subject = FTQuote('decl')
        objects = [target, entity]
        return FTClause(subject, objects, indent);

    def def_(alias, reality, indent=-1):
        assert type(alias) is FTQuote, 'FTClause-def-"alias" is not a quote.'
        assert (type(reality) is FTQuote or
                type(reality) is FTValue or
                type(reality) is FTClause or
                type(reality) is FTRef or
                type(reality) is FTDyRef), 'FTClause-def-"reality" is invalid.'

        subject = FTQuote('def')
        objects = [alias, reality];
        return FTClause(subject, objects, indent)

    def block(stmts, indent=-1):
        assert type(stmts) is list, 'FTClause-block(*)-"stmts" is not a list.'
        for stmt in stmts:
            assert (type(stmt) is FTQuote or 
                    type(stmt) is FTValue or
                    type(stmt) is FTClause or
                    type(stmt) is FTRef or
                    type(stmt) is FTDyRef), 'FTClause-block(*)-"stmt" is invalid.'
                    
        subject = FTQuote('*')
        return FTClause(subject, stmts, indent)

    def replace(stmt, indent=-1):
        assert (type(stmt) is FTQuote or
                type(stmt) is FTRef), 'FTClause-replace($)-"stmt" is not quote or ref.'

        subject = FTQuote('$')
        objects = [stmt]
        return FTClause(subject, objects, indent)

    def reflect(name, indent=-1):
        assert (type(name) is FTQuote or
                (type(name) is FTValue and name.vtype == 'string' ) or
                type(name) is FTClause or
                type(name) is FTRef or
                type(name) is FTDyRef), 'FTClause-reflect(@)-"name" is invalid.'

        subject = FTQuote('@')
        objects = [name]
        return FTClause(subject, objects, indent)
    
    def prototype(params, indent=-1):
        assert type(params) is list, 'FTClause-prototype(!)-"params" is not a list.'
        for param in params:
            assert type(param) is FTParam, 'FTClause-prototype(!)-"param" is not a param.'

        subject = FRQuote('!')
        return FTClause(subject, params, indent)

    def member(modifier, name, types, value, indent=-1):
        assert type(modifier) is str, 'FTClause-member(:)-"modifier" is not a string.'
        assert len(modifier) < 2, 'FTClause-member(:)-"modifier" is not a char.'
        assert type(name) is str, 'FTClause-member(:)-"name" is not a string.'
        assert type(types) is FTTypeList, 'FTClause-member(:)-"type" is not a type list.'
        assert (type(value) is FTQuote or 
                type(value) is FTValue or
                type(value) is FTClause or
                type(value) is FTRef or
                type(value) is FTDyRef), 'FTClause-member(:)-"value" is invald.'

        subject = FTQuote('!:')
        name = FTQuote(name, modifier)
        objects = [name, types, value]
        return FTClause(subject, objects, indent)
        
    def function(parent, params, result, body, indent=-1):
        assert type(parent) is FTQuote, 'FTClause-function-"super" is not a quote.'
        assert (type(params) is FTClause and 
                params.subject == '!'), 'FTClause-function-"params" is not a prototype.'
        assert ((type(result) is FTTypeList or 
                 type(result) is FTTypeGroup), 
                'FTClause-function-"result" is not a type list/group.')
        assert (type(body) is FTQuote or 
                type(body) is FTValue or
                type(body) is FTClause or
                type(body) is FTRef or
                type(body) is FTDyRef), 'FTClause-function-"body" is invalid.'

        subject = FTQuote('=')
        objects = [parent, params, result, body]
        return FTClause(subject, objects, indent)

    pass

class FTRef:
    def __init__(self, subject, members):
        assert type(subject) is FTQuote, 'FTRef-"subject" is not a quote.'
        assert type(members) is list, 'FTRef -"members" is not a list.'
        for mem in members:
            assert (type(mem) is FTQuote or
                    (type(mem) is FTClause and 
                     type(mem.subject) is FTQuote and
                     mem.subject.text == '@')), 'FTRef-"mem" is invalid.'

        self.subject = subject
        self.memebers = tuple(members)
        pass
    pass

class FTDyRef:
    def __init__(self, subject, members):
        assert type(subject) is FTClause, 'FTDyRef-"subject" is not a clause.'
        assert type(members) is list, 'FTDyRef-"members" is not a list.'
        for mem in members:
            assert (type(mem) is FTQuote or 
                    (type(mem) is FTClause and 
                     type(mem.subject) is FTQuote and
                     mem.subject.text == '@')), 'FTDyRef-"mem" is invalid.'

        self.subject = subject
        self.memebers = tuple(members)
        pass
    pass

class FTQuoList(FTSpecial):
    def __init__(self, quotes):
        assert type(quotes) is list, 'FTQuoList-"quotes" is not a list.'
        for quote in quotes:
            assert type(quote) is FTQuote, 'FTQuoList-"quote" is not a FTQuote.'

        self.quotes = tuple(quotes)
        pass
    pass

class FTTypeList(FTSpecial):
    def __init__(self, types):
        assert type(types) is list, 'FTTypeList-"types" is not a list.'
        for t in types:
            assert type(t) is FTQuote, 'FTTypeList-"type" is not a quote.'

        self.types = tuple(types);
        pass
    pass

class FTTypeGroup(FTSpecial):
    def __init__(self, slots):
        assert type(slots) is list, 'FTTypeGroup-"slots" is not a list.'
        for tl in slots:
            assert type(tl) is FTTypeList, 'FTTypeGroup-"tl" is not a type list.'

        self.slots= tuple(slots);
        pass
    pass

class FTParam(FTSpecial):
    def __init__(self, modifier, name, types, defaulue):
        assert type(modifier) is str, 'FTParam-"modifier" is not a string.'
        assert len(modifier) < 2, 'FTParam-"modifier" is not a char.'
        assert type(name) is str, 'FTParam-"name" is not a string.'
        assert type(types) is FTTypeList, 'FTParam-"type" is not a type list.'
        assert (type(defaulue) is FTValue or 
                type(defaulue) is FTQuote), 'FTParam-"defaulue" is not value or quote.'

        self.name = FTQuote(name, modifier)
        self.types = types
        self.defaulue = defaulue
        pass
    pass

