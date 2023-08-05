# Pymitter Integration

Adds the ability to inject an instance of EventEmitter from [pymitter](https://github.com/riga/pymitter). This instance
will be shared within a context (separate threads have separate emitters). Registration is done via the entry point in
autoinject, so no need to do anything other than install this package.

```python
from autoinject import injector as _injector
import pymitter


class NeedsEvents:

    ee: pymitter.EventEmitter = None

    @_injector.construct
    def __init__(self):
        pass

    def do_stuff(self):
        self.ee.emit("foo.bar", "hello world")


class LikesEvents:

    ee: pymitter.EventEmitter = None

    @_injector.construct
    def __init__(self):
        self.ee.on("foo.bar", self.on_event)

    def on_event(self, arg):
        print("foo bar emitted: {}".format(arg))


emitter = NeedsEvents()
receiver = LikesEvents()

emitter.do_stuff()
# OUTPUT: foo bar emitted: hello world        
```