#!/usr/bin/env python3
import sys, os, socket, re, time, json, logging
from urllib.parse import urlparse
import collections
#import threading

#class OVSDBConnection(threading.Thread):
class OVSDBConnection(object):
    """ This is a connects to an ovsdb server that has manager set using
        ovs-vsctl set-manager ptcp:5000
    """
    def __init__(self, server_path, db = None, **kwargs):
        self.id = 0
        self.db_name = db
        self.server_path = server_path
        self.attributes = collections.OrderedDict()
        for k,v in kwargs.items():
            #print("%s: %s" %(k, v))
            self[k] = v

        log_file = "libovsdb_%s.log" %(time.strftime("%Y%m%d%H%M%S", time.localtime()))
        logging.basicConfig(
                #filename = log_file,
                level= kwargs.get("level", logging.INFO),
                format='%(asctime)s%(message)s',
                datefmt='[%Y%m%d %I:%M:%S]',
                filemode = 'w')

        logging.debug("logging start")
        if self["dryrun"]:
            logging.debug("dry-fun, not really connect to: %s."
                    %(server_path))
            return

        #threading.Thread.__init__(self)
        o = urlparse(server_path)
        #print(o)

        if o.scheme == "tcp":
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            addr = o.path.split(":")
            self.socket.connect((addr[0], int(addr[1])))
        elif o.scheme == "unix":
            self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.socket.connect(o.path)

        if not self.db_name:
            ret = self.list_dbs()
            self.db_name = ret["result"][0]
        logging.debug("succeed to connected db: %s/%s" %(server_path, self.db_name))
        #self.start()

    def __getitem__(self, name):
        """
        Get members of the object.
        """
        return self.attributes.get(name, None)

    def __setitem__(self, name, value):
        """
        Set members to the object.
        """
        self.attributes[name] = value

    def send (self, message, callback=None):
        '''
        send request to the ovsdb server
        '''
        if callback:
            self.callbacks[message['id']] = callback
        request = json.dumps(message, separators=(',',':'))

        if self["dryrun"]:
            print("ovsdb-client %s %s '%s'"
                    %(json.dumps(message["method"], separators=(',',':')),
                        self.server_path,
                        json.dumps(message["params"], separators=(',',':'))))
            return
        logging.debug("send message: %s" %(request))
        self.socket.send(request.encode("UTF-8"))

    def recv (self, buffer_len = 4096):
        '''
        recieve response from the ovsdb server. It's in block mode and return
        after receive a complete message or timeout.
        '''
        if self["dryrun"]:
            return
        #response = self.socket.recv(buffer_len).decode("UTF-8")
        #logging.debug("%s" %(response))
        #return json.loads(response)
        chunks = []
        lc = rc = 0
        while True:
            response = self.socket.recv(4096)
            if response:
                response = response.decode('utf8')
                #logging.debug("run() response: %s." %(response))
                message_mark = 0
                for i, c in enumerate(response):
                    #todo fix the curlies in quotes
                    if c == '{':
                        lc += 1
                    elif c == '}':
                        rc += 1

                    if rc > lc:
                        raise Exception("json string not valid")
                    elif lc == rc and lc != 0:
                        chunks.append(response[message_mark:i + 1])
                        message = "".join(chunks)
                        #print("message: %s" %(message))
                        #self._on_remote_message(message)
                        logging.debug("recv message: %s" %(message))
                        json_m = json.loads(message,
                                #object_pairs_hook=collections.OrderedDict,
                                )
                        #if json_m.get("id", -1) == 0:
                        #    return json_m
                        return json_m
                        lc = rc = 0
                        message_mark = i + 1
                        chunks = []
                #if lc != rc:
                #    print("message not complete, continue receiving, lc: %d, rc: %d..." %(lc, rc))
                #    print("response: %s" %(response))
                chunks.append(response[message_mark:])
                #logging.debug("left message: %s." %(response[message_mark:]))

    def list_dbs (self, buffer_len = 4096):
        '''
        list_dbs
        '''
        list_dbs_query = {"method":"list_dbs", "params":[], "id": self.id}
        self.send(list_dbs_query)
        self.id += 1
        return self.recv()

    def transact (self, *args, **kwargs):
        '''
        Generate a transaction for send "TRANSACT" request to the ovsdb
        server. Caller should call commit() to real commit the request
        '''
        return OVSDBTransact(self)
        #list_dbs_query = {"method":"transact",
        #        "params": [self.db_name, *operations],
        #        "id": self.id}
        #self.id += 1
        #self.send(list_dbs_query)
        #return db.recv()

    def insert (self, table, row, **kwargs):
        ''' Insert a row into the given table '''
        tx = self.transact()
        tx.row_insert(table = table, row = row, **kwargs)
        res = tx.commit()
        if not res.get("result", None):
            return None

        item = collections.OrderedDict()
        for r in res["result"]:
            for k,v in r.items():
                if isinstance(v, list):
                    item[k] = v[1]
                else:
                    item[k] = v
        return item

    def delete (self, table, where, **kwargs):
        ''' Delete a row from the given table '''
        tx = self.transact()
        tx.row_delete(table = table, where = where)
        res = tx.commit()
        if not res.get("result", None):
            return None

        item = collections.OrderedDict()
        for r in res["result"]:
            for k,v in r.items():
                if isinstance(v, list):
                    item[k] = v[1]
                else:
                    item[k] = v
        return item

    def update (self, table, row, where, **kwargs):
        ''' update a row in the given table '''
        tx = self.transact()
        tx.row_update(table = table, row = row, where = where)

        res = tx.commit()
        if not res.get("result", None):
            return None

        item = collections.OrderedDict()
        for r in res["result"]:
            for k,v in r.items():
                if isinstance(v, list):
                    item[k] = v[1]
                else:
                    item[k] = v
        return item

    def select (self, table, where, **kwargs):
        ''' select a row in the given table '''
        tx = self.transact()
        tx.row_select(table = table, where = where)
        res = tx.commit()
        if not res.get("result", None):
            return None

        result = []
        for row in res["result"][0]["rows"]:
            item = collections.OrderedDict()
            for k,v in row.items():
                if isinstance(v, list):
                # Remove leading "uuid"
                    item[k] = []
                    for l in v[1]:
                        if isinstance(l, list):
                            # Remove leading "uuid"
                            item[k].append(l[1])
                        else:
                            item[k] = l
                else:
                    item[k] = v
            result.append(item)
        #return res["result"][0]["rows"]
        return result

class OVSDBTransact(object):
    """transact
    """
    def __init__(self, ovsdb_connection):
        self.start_time = time.time()
        self.ovsdb_connection = ovsdb_connection
        self.counter = 0
        self.operations = []

    def __del__(self):
        '''
        Recycle resource when the object is destroied.
        '''
        logging.debug("transact %d, finish in %.2f seconds\n"
                %(self.ovsdb_connection.id, time.time() - self.start_time))

    def insert (self, table, row, op = "insert", **kwargs):
        '''
        Insert a row into the given table, you should compute the op
        parameters as the RFC7047:

            "op": "insert"          required
            "table": <table>        required
            "row": <row>            required
            "uuid-name": <id>       optional

        If there is reTable, you should open an mutate op, you should call
        commit() to send the transaction to the server, for example:

            name = tx.insert(table = "Logical_Switch_Port",
                            row = {"name":"ls1-lsp0"})
            tx.mutate(table = "Logical_Switch",
                      where = [["name", "==", "ls1"]],
                      mutations = [tx.make_mutations("ports", "insert", {"named-uuid": name})])
        '''
        self.counter += 1
        uuid_name = "row%d"%(self.counter)
        #operation = kwargs
        #operation["op"] = "insert"
        #operation["uuid-name"] = operation.get("uuid-name", uuid_name)
        operation = {"op": op,
                "row": row,
                "table": table}
        operation["uuid-name"] = operation.get("uuid-name", uuid_name)
        self.operations.append(operation)
        return uuid_name

    def mutate (self, table, where, mutations, op = "mutate", **kwargs):
        '''
        Mutate a column in the given table, you should compute the op
        parameters as the RFC7047:

            "op":  "mutate"               required
            "table": <table>              required
            "where": [<condition>*]       required
            "mutations": [<mutation>*]    required

        Normally mutate is used along with insert/delete, you should call
        commit() to send the transaction to the server, for example:

            name = tx.insert(table = "Logical_Switch_Port",
                            row = {"name":"ls1-lsp0"})
            tx.mutate(table = "Logical_Switch",
                      where = [["name", "==", "ls1"]],
                      mutations = [tx.make_mutations("ports", "insert", {"named-uuid": name})])
        '''
        #operation = kwargs
        #operation["op"] = "mutate"
        #self.operations.append(operation)
        #if args:
        #    operation["mutations"] = operation.get("mutations", []) 
        #    operation["mutations"].extend(args)
        #print("mutations: %s" %(mutations))
        operation = {"op": op,
                "where": where,
                "table": table,
                "mutations": mutations}
        self.operations.append(operation)

    def update (self, table, where, row, op = "update", **kwargs):
        '''
        Update a row in the given table, you should compute the op
        parameters as the RFC7047:

            "op": "update"                required
            "table": <table>              required
            "where": [<condition>*]       required
            "row": <row>                  required

        you should call commit() to send the transaction to the server, for
        example:

            tx.update(table = "Logical_Switch_Port",
                    row = {"addresses": "00:00:00:00:00:05"},
                    where = [["name", "==", "ls1-lsp0"]])
            tx.commit()
        '''
        #operation = kwargs
        #operation["op"] = "update"
        #operation["where"] = operation.get("where", [[]])
        operation = {"op": op,
                "where": where,
                "table": table,
                "row": row}
        self.operations.append(operation)

    def delete (self, table, where, op = "delete", **kwargs):
        '''
        Delete a row from the given table, you should compute the op
        parameters as the RFC7047:

            "op":  "delete"               required
            "table": <table>              required
            "where": [<condition>*]       required

        you should call commit() to send the transaction to the server, for
        example:

            # Get the uuid in other way, since it's needed in mutate op.
            uuid = 03934fdf-6087-48e7-b5ce-54d4d76e4368
            tx.delete(table = "Logical_Switch_Port",
                    where = [["uuid", "==", uuid]])
            tx.commit()
        '''
        #operation = kwargs
        #operation["op"] = "delete"
        #operation["where"] = operation.get("where", [[]])
        #self.operations.append(operation)
        operation = {"op": op,
                "where": where,
                "table": table}
        self.operations.append(operation)

    def select (self, table, where, op = "select", columns = None, **kwargs):
        '''
        select rows from the given table, you should compute the op
        parameters as the RFC7047:

            "op": "select"                required
            "table": <table>              required
            "where": [<condition>*]       required
            "columns": [<column>*]        optional

        you should call commit() to send the transaction to the server, for
        example:

            # Get the uuid in other way, since it's needed in mutate op.
            uuid = 03934fdf-6087-48e7-b5ce-54d4d76e4368
            tx.delete(table = "Logical_Switch_Port",
                    where = [["uuid", "==", uuid]])
            tx.commit()
        '''
        #operation = kwargs
        #operation["op"] = "select"
        #operation["where"] = operation.get("where", [])
        #operation["columns"] = operation.get("columns", [])
        #self.operations.append(operation)
        operation = {"op": op,
                "where": where,
                "table": table}
        if columns:
            operation["columns"] = columns
        self.operations.append(operation)

    def make_mutations (self, item, mutator, *args):
        '''
        自动生成operations 返回给调用者，以便作为参数传给transact. uuid_name
        为uuid-name, 如果该insert操作需要mutate 操作则必须传入mutate 里相同的
        参数，否则不需要传。
        {"mutations":[["ports","insert",["set",[["named-uuid","row3"]]]]],
        "op":"mutate","table":"Logical_Switch","where":[["name","==","ls1"]]}
        '''
        mutatesets = []
        # It seems that json don't support dump python set, so conver it to
        # list, in other words, conver {"key": "value"} to ["key": "value"]
        for a in args:
            #print("aaaaaaaaa: %s, type: %s" %(a, type(a)))
            if isinstance(a, dict):
                mutateset = []
                #{"named-uuid": name}
                for k,v in a.items():
                    mutateset.append(k)
                    mutateset.append(v)
            else:
                #['uuid', '433fb2e1-fd87-4a40-b3ef-991dcd7b8014']
                mutateset = a
            mutatesets.append(mutateset)
            #print("mutatesets: %s" %(mutatesets))
        mutations = [item, mutator, ["set", mutatesets]]
        return mutations

    def commit (self):
        '''
        接收来自ovsdb server的字典，并转成字符发给ovsdb server, 接收到回答后
        转成字典返回给调用者。
        注意：本函数可能阻塞
        '''
        list_dbs_query = {"method":"transact",
                "params": [self.ovsdb_connection.db_name, *self.operations],
                "id": self.ovsdb_connection.id}
        self.ovsdb_connection.send(list_dbs_query)
        self.ovsdb_connection.id += 1
        self.operations = [] # Clear the operations list for next commit.
        response = self.ovsdb_connection.recv()
        #print("transact %d, finish in %.2f seconds\n"
        #        %(self.ovsdb_connection.id, time.time() - self.start_time))
        #self.start_time = time.time() # reset the timer
        return response

    def row_insert (self, table, row, refer = None):
        '''
        Insert a row, if there is refTable by others, mutate it. It's a
        wrapper for self.insert() to let caller insert a row in one line. an
        example:
            tx.row_insert(table = "Logical_Switch_Port", row = {"name":"ls1-lsp0"},
                    refer = ["Logical_Switch", "ports", ["name", "==", "ls1"]])
        '''
        uuid_names = []
        rows = isinstance(row, list) and row or [row]
        for r in rows:
            name = self.insert(table = table, row = r)
            if refer: #It's a refTable
                uuid_names.append({"named-uuid": name})
        #print(uuid_names)
        if refer: #It's a refTable
            mutations = self.make_mutations(refer[1], "insert", *uuid_names)
            self.mutate(table = refer[0],
                    where = [refer[2]],
                    mutations = [mutations])

    def row_delete (self, table, where = None, refer = None):
        '''
        Delete a row, if there is refTable by others, mutate it. It's a
        wrapper for self.delete() to let caller delete a row in one line. for
        example:
            tx.row_delete(table = "Logical_Switch_Port",
                    where = [["name", "==", "ls1-lsp0"]],
                    refer = ["Logical_Switch", "ls1", "ports"])
        '''

        if not refer: #It's a refTable
            #print("not refer")
            self.delete(table = table, where = where) #delete op is not needed???
        else: #It's a refTable
            # select the uuid at frist since it's needed in mutations.
            select_op = {"op": "select",
                    "table": table,
                    "columns": ["_uuid"]}
            select_op["where"] = where and where or []
            list_dbs_query = {"method":"transact",
                    "params": [self.ovsdb_connection.db_name, select_op],
                    "id": self.ovsdb_connection.id}
            self.ovsdb_connection.send(list_dbs_query)
            self.ovsdb_connection.id += 1
            response = self.ovsdb_connection.recv()
            uuid = []
            for row in response["result"][0]["rows"]:
                uuid.append(row["_uuid"])
                #print(uuid)
            self.mutate(table = refer[0], where = [refer[2]],
                    mutations = [self.make_mutations(refer[1],
                                                    "delete",
                                                    *uuid)])

    def row_update (self, table, row, where = None):
        '''
        Update a row, it's wrapper for self.update() an example:
            tx.row_update(table = "Logical_Switch_Port",
                    row = {"addresses": "00:00:00:00:00:05"},
                    where = [["name", "==", "ls1-lsp0"]])
        '''
        self.update(table = table, row = row, where = where)
    def row_select (self, **kwargs):
        '''
        select a row, it's wrapper for self.update() an example:
            response = tx.row_select(table = "Logical_Switch",
                    columns = ["_uuid", "name"],
                    where = [["name", "==", "ls1"]])
        '''
        self.select(**kwargs)

if __name__ == '__main__':
    ovsdb_server = 'unix:/usr/local/var/run/ovn/ovnnb_db.sock'
    db = OVSDBConnection(ovsdb_server, "OVN_Northbound", False)
    tx = db.transact()

    if options.insert:
        #tx.row_insert(table = "Logical_Switch", row = {"name":"ls1"})
        tx.row_insert(table = "Logical_Switch_Port",
                row = {"name":"ls1-lsp0"},
                refer = ["Logical_Switch", "ports", ["name", "==", "ls1"]])

    if options.update:
        tx.row_update(table = "Logical_Switch_Port",
                row = {"addresses": "00:00:00:00:00:05"},
                where = [["name", "==", "ls1-lsp0"]])

    if options.select:
        tx.row_select(table = "Logical_Switch",
                columns = ["_uuid", "name"],
                where = [["name", "==", "ls1"]])

    if options.delete:
        tx.row_delete(table = "Logical_Switch_Port",
                where = [["name", "==", "ls1-lsp0"]],
                referby = ["Logical_Switch", "ls1", "ports"])

    response = tx.commit()
    print("%s" %(response["result"]))
