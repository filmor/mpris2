import dbus


class DbusObject():
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
        return "<{}(bus_name='{}')>".format(self.__class__.__qualname__, self._objects.popitem()[1].requested_bus_name)

    __repr__ = __str__

    def _get_dbus_attr(self, item):
        for interface in self._objects.keys():
            if item in self._properties.GetAll(interface):
                return self._properties.Get(interface, item)

        def hack(*args, **kwargs):
            for proxy in self._objects.values():
                try:
                    return getattr(proxy, item)(*args, **kwargs)
                except dbus.exceptions.DBusException:
                    continue
            raise NameError("This is not a method. Or something. TODO introspection")

        return hack

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
