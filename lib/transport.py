#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import multiprocessing
import time
import sys
import os
import simplejson
import zmq
import uuid
if(sys.platform.lower().find("linux") >= 0):
  import setproctitle

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))
import lib.debug

class publisher(object):
  def __init__(self,context=None):
    if (not context):
      self._context = zmq.Context()
    else:
      self._context = context
    self._socket = None
    self._start()

  def _start(self,pub_port=5566):
    self._socket = self._context.socket(zmq.PUB)
    self._socket.sndhwm = 100000
    self._socket.bind("tcp://*:{0}".format(pub_port))

  def publish(self,topic="0",message={},publish_id=None):

    self._socket.send_multipart([bytes(unicode(topic)),bytes(unicode(message))])
    if (publish_id != None):
      """
      Update the database tables
      """
      pass
    




class subscriber(object):
  def __init__(self,context=None,topic="0",ip="127.0.0.1",port=5566):
    if (not context):
      self._context = zmq.Context()
    else:
      self._context = context
    self._socket = None
    self._topic = topic
    self._ip = ip
    self._port = port
    self._start()


  def _start(self):
    self._socket = self._context.socket(zmq.SUB)
    self._socket.connect("tcp://{0}:{1}".format(self._ip, self._port))
    if(isinstance(self._topic,list)):
      for topix in self._topic:
        self._socket.setsockopt(zmq.SUBSCRIBE, bytes(unicode(topix)))
    else:
      self._socket.setsockopt(zmq.SUBSCRIBE, bytes(unicode(self._topic)))
    while (True):
      (topic, messagedata) = self._socket.recv_multipart()
      # (topic, messagedata) = string.split("__")
      lib.debug.info ("{0} : {1} ".format(topic,messagedata))
      retmsg = self.process(unicode(messagedata))
      lib.debug.info (retmsg)




  def process(self,msg):
    return (msg)




class server(object):
  def __init__(self,context=None):
    if(not context):
      self._context = zmq.Context()
    else:
      self._context = context


  def process(self, msg):
    return msg


  def _worker(self,worker_url, worker_id=uuid.uuid4()):
    if (sys.platform.lower().find("linux") >= 0):
      setproctitle.setproctitle("server-worker")
    lib.debug.info (worker_url)
    context = zmq.Context()
    # Socket to talk to dispatcher
    socket = context.socket(zmq.REP)
    socket.poll(timeout=1)
    socket.connect(worker_url)


    while True:
      (id ,msg) = socket.recv_multipart()

      lib.debug.info("Received request: [ {0} ] -> [ {1} ]".format(str(worker_id),msg))

      # do some 'work'
      # time.sleep(1)
      reply = self.process(msg)

      # send reply back to client
      socket.send_multipart([bytes(id),bytes(reply)])
      lib.debug.info("Replied to request: [ {0} ] -> [ {1} ]".format(str(worker_id), msg))


  def start(self, worker_port=55999, server_port=55555, pool_size=2):
    if (sys.platform.lower().find("linux") >= 0):
      setproctitle.setproctitle("server-server")
    url_worker = "tcp://127.0.0.1:{0}".format(worker_port)
    url_client = "tcp://*:{0}".format(server_port)

    # Prepare our context and sockets
    # context = zmq.Context()

    # Socket to talk to clients
    clients = self._context.socket(zmq.ROUTER)
    try:
      clients.bind(url_client)
    except:
      lib.debug.info (sys.exc_info())
      self._context.term()
      sys.exit(1)

    # Socket to talk to workers
    workers = self._context.socket(zmq.DEALER)
    try:
      workers.bind(url_worker)
    except:
      lib.debug.info (sys.exc_info())
      self._context.term()
      sys.exit(1)

    # Launch pool of worker process
    p = multiprocessing.Pool(processes=pool_size, initializer=self._worker, initargs=(url_worker,))

    zmq.proxy(clients, workers)

    # We never get here but clean up anyhow
    clients.close()
    workers.close()
    self._context.term()



class client(object):
  def __init__(self,ip='localhost',port=55555):
    self._ip = ip
    self._port = port


  def process(self, message):
    return message


  def send(self,message={},request_id=uuid.uuid4()):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://{0}:{1}".format(self._ip, self._port))
    socket.poll(timeout=1)
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)
    lib.debug.info("Sending request {0} …".format(request_id))
    send_msg = self.process(message)
    timestarted = time.time()

    socket.send_multipart([bytes(unicode(request_id)),bytes(unicode(send_msg))])
    while(True):
      sockets = dict(poller.poll(10000))
      if(sockets):
        for s in sockets.keys():
          if(sockets[s] == zmq.POLLIN):
            try:
              (recv_id, recved_msg) = s.recv_multipart()
              recv_message = self.process(recved_msg)
            except:
              lib.debug.info (sys.exc_info())
            break
        break
      lib.debug.info ("Reciever Timeout error : Check if the server is running")


    lib.debug.info("Received reply %s : %s [ %s ]" % (recv_id,recv_message, time.time() - timestarted))
    socket.close()


if __name__ == "__main__":
  s = server()
  s.start()
