import dbus
from sys import version_info

class MaybeDbusMethod():
    def __init__(self, proxies, method_name):
        self.proxies = proxies
        self.method_name = method_name

    def __str__(self):
        return "<MaybeDbusMethod(bus_name='{}', method_name='{}')>".format(self.proxies.popitem()[1].requested_bus_name, self.method_name)

    __repr__ = __str__

    def __call__(self, *args, **kwargs):
        for proxy in self.proxies.values():
            try:
                return getattr(proxy, self.method_name)(*args, **kwargs)
            except dbus.exceptions.DBusException:
                continue
        raise NameError("This is not a method. Or something. TODO introspection")

class DbusObject(object):
    _objects = {}
    _properties = None

    def __init__(self, bus_name, object_path, interfaces, bus=dbus.SessionBus()):

        proxy = bus.get_object(bus_name, object_path)

        self._properties = dbus.Interface(proxy, 'org.freedesktop.DBus.Properties')

        for interface in interfaces:
            self._objects[interface] = dbus.Interface(proxy, interface)
            try:
                self._properties.GetAll(interface)
            except dbus.exceptions.DBusException as ex:
                if ex._dbus_error_name == "org.freedesktop.DBus.Error.UnknownInterface":
                    del self._objects[interface]

    def __str__(self):
        ver = version_info.major
        if ver < 3:
            return "<%s(bus_name='%s')>" % (self.__class__.__name__, self._objects.popitem()[1].requested_bus_name)
        return "<{}(bus_name='{}')>".format(self.__class__.__qualname__, self._objects.popitem()[1].requested_bus_name)
#        try:
#            return "<{}(bus_name='{}')>".format(self.__class__.__qualname__, self._objects.popitem()[1].requested_bus_name)
#        except AttributeError:
#            return "<{}(bus_name='{}')>".format(self.__class__.__name__, self._objects.popitem()[1].requested_bus_name)

    __repr__ = __str__
 
    def _get_dbus_attr(self, item):
        for interface in self._objects.keys():
        # try/except for valid interface
            if item in self._properties.GetAll(interface):
                return self._properties.Get(interface, item)

        return MaybeDbusMethod(self._objects, item)

    def __getattr__(self, item):
        if item in self.__dict__.keys():
            return self.__dict__[item]
        else:
            return self._get_dbus_attr(item)

    def __setattr__(self, key, value):
        if key.startswith('_') or key in self.__dict__.keys():
            self.__dict__[key] = value
            return

        for interface in self._objects.keys():
            if key in self._properties.GetAll(interface):
                return self._properties.Set(interface, key, value)

    def connect_to_signal(self, signal_name, handler):
        for proxy in self._objects.values():
            proxy.connect_to_signal(signal_name, handler)
