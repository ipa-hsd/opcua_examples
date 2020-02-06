#!/usr/bin/env python
import sys
import time

from opcua import ua, Server

if __name__ == "__main__":

    # setup our server
    server = Server()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

    # setup our own namespace, not really necessary but should as spec
    # namespace URI identifies the naming authority defining the identifiers of NodeIds
    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)

    # get Objects node, this is where we should put our nodes
    objects = server.get_objects_node()

    # populating our address space
    myobj = objects.add_object(idx, "MyObject")
    myvar = myobj.add_variable(idx, "MyVariable", 6.7)
    myvar.set_writable()    # Set MyVariable to be writable by clients

    # starting!
    server.start()

    try:
        count = 0
        myevgen = server.get_event_generator()
        myevgen.event.Severity = 300

        while True:
            time.sleep(1)
            count += 0.1
            myvar.set_value(count)
            if myvar.get_value() > 1.0:
                myevgen.trigger(message="WARNING: Value exceeds 1.0")
                count = 0
    finally:
        #close connection, remove subcsriptions, etc
        server.stop()
