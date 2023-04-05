class WrappedList(list):
    """Creates a list that calls a callback function on edit"""

    def __init__(self, callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.callback = callback
        
    def append(self, *args, **kwargs):
        result = super().append(*args, **kwargs)
        self.callback()
        return result

    def extend(self, *args, **kwargs):
        result = super().extend(*args, **kwargs)
        self.callback()
        return result

    def insert(self, *args, **kwargs):
        result = super().insert(*args, **kwargs)
        self.callback()
        return result

    def remove(self, *args, **kwargs):
        result = super().remove(*args, **kwargs)
        self.callback()
        return result

    def pop(self, *args, **kwargs):
        result = super().pop(*args, **kwargs)
        self.callback()
        return result

    def clear(self, *args, **kwargs):
        result = super().clear(*args, **kwargs)
        self.callback()
        return result

    def sort(self, *args, **kwargs):
        result = super().sort(*args, **kwargs)
        self.callback()
        return result

    def reverse(self, *args, **kwargs):
        result = super().reverse(*args, **kwargs)
        self.callback()
        return result

    def __setitem__(self, *args, **kwargs):
        result = super().__setitem__(*args, **kwargs)
        self.callback()
        return result

    def __delitem__(self, *args, **kwargs):
        result = super().__delitem__(*args, **kwargs)
        self.callback()
        return result

    def __iadd__(self, *args, **kwargs):
        result = super().__iadd__(*args, **kwargs)
        self.callback()
        return result

    def __imul__(self, *args, **kwargs):
        result = super().__imul__(*args, **kwargs)
        self.callback()
        return result

    def __get__(self, obj, type=None):
        print('__get__', self, obj, type)

    def __set__(self, obj, val):
        print('__set__', self, obj, val)

    def __delete__(self, obj):
        print('__delete__', self, obj)


class WrappedListDescriptor:
    """Creates a list property that calls a callback function on edit"""

    def __init__(self, callback_name):
        self.callback_name = callback_name

    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, instance, owner):
        cur_lst = getattr(instance, self.private_name, None)
        if cur_lst is None:
            callback = getattr(instance, self.callback_name, lambda: None)
            new_lst = WrappedList(callback, [])
            setattr(instance, self.private_name, new_lst)
            return new_lst
        return cur_lst

    def __set__(self, instance, new_lst):
        cur_lst = getattr(instance, self.private_name, None)
        callback = getattr(instance, self.callback_name, lambda: None)
        if new_lst is not cur_lst:
            setattr(instance, self.private_name, WrappedList(callback, new_lst))
        callback()

    def __delete__(self, instance):
        raise AttributeError

