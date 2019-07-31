import threading

PYTHON_INTERNALS = ["__module__", "__dict__", "__weakref__"]

class KlassThreadWrapper:
    def __init__(self, user_defined_klass):
        self.user_defined_klass = user_defined_klass

    def __call__(self, *args, **kwargs):
        self._raise_if_user_defined_class_does_not_exist()
        self._inst_klass = self.user_defined_klass(*args, **kwargs)
        self._allow_full_transparency_to_user_defined_methods()
        return self._inst_klass

    def _raise_if_user_defined_class_does_not_exist(self):
        if self.user_defined_klass is not None:
            return

        raise NotImplementedError(
            f"self.klass does not exist!, call #__init__() first!"
        )

    def _allow_full_transparency_to_user_defined_methods(self):
        for name, method in self._inst_klass.__class__.__dict__.items():
            # basically, we want this object to interact
            # exactly as if the user was interacting with their own
            # custom made object.
            #
            # We implement this in two stages:
            #
            # 1. We begin by checking if the current method exists
            # in this class. If it does, we rename the methods in this class
            # by appending another underscore to it. Hopefully that will be enough.
            # I don't think a third underscore is actually necessary.
            # This will probably be an expensive operation, so only done once.
            #
            # 2. We copy the method over to this class, and wrap the method
            # such that calls to it are re-directed over to _inst_klass.

            # if self._name_conflict(name):
            #     self._rename_our_internal_method(name)
            #
            # self._redirect_method_to_inst_klass(name, method)
            pass

    def _name_conflict(self, name):
        return name in self.__class__.__name__

    def _rename_our_internal_method(self, name):
        method = getattr(self, name)
        delattr(self, name)
        setattr(self, f"_{name}", method)

    def _redirect_method_to_inst_klass(self, name, user_defined_method):
        if name in PYTHON_INTERNALS:
            return

        setattr(self, name, user_defined_method)

    def run(self):
        # the user _must_ have already defined this method!
        pass
