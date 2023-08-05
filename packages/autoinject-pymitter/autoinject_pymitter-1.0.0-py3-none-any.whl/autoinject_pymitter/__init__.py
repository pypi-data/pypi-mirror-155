""" Simple module that allows using pymitter as an auto-injected dependency """
from pymitter import EventEmitter


def _register_event_emitter(injector):
    """ Entry point for autoinject.registrars that registers the EventEmitter class """
    injector.register_constructor(EventEmitter, EventEmitter, wildcard=True)


__version__ = "1.0.0"
