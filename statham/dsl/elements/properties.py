from statham.dsl.constants import NotPassed
from statham.dsl.elements.base import Element, Nothing
from statham.dsl.property import _Property as Property


class Properties:
    def __init__(self, element, props, additional=True):
        self.element = element
        self.props = props or {}
        for name, prop in self.props.items():
            prop.bind_name(name)
            prop.bind_class(self.element)
        if isinstance(additional, bool):
            self.additional = {True: Element(), False: Nothing()}[additional]
        else:
            self.additional = additional

    def property(self, element):
        prop = Property(element)
        prop.bind_class(self.element)
        return prop

    def __repr__(self):
        props = [repr(self.props)]
        if self.additional == Nothing():
            props.append("additionalProperties=False")
        elif self.additional != Element():
            props.append(f"additionalProperties={self.additional}")
        return f"{type(self).__name__}({', '.join(props)})"

    def __getitem__(self, key):
        try:
            return {prop.source: prop for prop in self.props.values()}[key]
        except KeyError:
            pass
        return self.property(self.additional)

    def __contains__(self, key):
        return bool(self[key] != Property(Nothing()))

    def __iter__(self):
        return iter(self.props)

    def __call__(self, value):
        value = {
            **{prop.name: NotPassed() for prop in self.props.values()},
            **value,
        }
        return {
            self[key].name or key: self[key](sub_value)
            for key, sub_value in value.items()
        }