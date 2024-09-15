import inspect

class Form:
    def params(self, form, validators):
        def factory(fn):
            names = inspect.getfullargspec(fn).args
            def decorator(*args, **kwargs):
                form_data = form()
                for name in names:
                    if name in validators:
                        form_data_value = form_data[name].strip()
                        validators[name](form_data_value)
                    kwargs[name] = form_data[name].strip()
                return fn(*args, **kwargs)
            return decorator
        return factory

form = Form()
