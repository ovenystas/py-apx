import remotefile
import socket
import numheader
import threading
import sys

@remotefile.TransmitHandler.register
class TcpSocketAdapter:
   """
   Remotefile TCP socket adapter
   """
   def __init__(self):
      self.isConnected=False
      self.isAlive=False
      self.receiveHandler=None #a receiveHandler is a class implementing the remotefile.ReceiveHandler interface. One example is remotefile.FileManager
      self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.isGreetingParsed = False
      def worker():
         """
         This is the TCP worker thread, it blocks on socket.recv until either data is received or an exception occurs (sockets shuts down)
         """
         unprocessed=bytes()
         while True:
            try:
               chunk = self.socket.recv(2048)
               if len(chunk)==0:                  
                  break
               else:                  
                  unprocessed+=chunk                  
                  result = self._parseData(unprocessed)
                  #_parse data will return how many bytes was parse or -1 on error
                  #we trim the pendingData buffer from the left using result as the index
                  #if result == 0 it means no data was parsed and it will stay in unprocessed buffer until more data has arrived
                  if result < 0:
                     sys.stderr.write("TcpSocketAdapter._parseData error %d"%result)
                     break
                  elif result > 0:
                     unprocessed=unprocessed[result:]
            except ConnectionAbortedError:               
               break
         print("socket worker shutting down")
                  
      
      self.worker = threading.Thread(target=worker)
   
   def connect(self, address, port):
      if address =='localhost':
         address='127.0.0.1'      
      try:
         self.socket.connect((address, port))
      except ConnectionRefusedError as e:
         print(e)
         return False
      self.isConnected=True
      self.socket.send(bytes('RMFP/1.0\nNumHeader-Format:32\n\n',encoding='ascii'))
      return True
   
   def start(self):
      self.isAlive=True
      self.worker.start()
      
   def stop(self):
      if self.isConnected == True:
         self.socket.shutdown(socket.SHUT_RD)
      if self.isAlive:
         self.socket.close()
         self.worker.join()
   
   def setReceiveHandler(self,handler):
      self.receiveHandler=handler

   def send(self, data : bytes):
      """
      send data bytes on socket
      """
      header=numheader.encode32(len(data))
      self.socket.send(header+data)      
      
   def _parseData(self,buf):
      """
      returns number of bytes parsed or -1 on error. When no messages or data can be parsed it returns 0
      """
      iBegin=0
      iNext=None
      iEnd=len(buf)
      while iBegin<iEnd:
         if self.isGreetingParsed==False:
            iNext = self._parseGreetingData(buf,iBegin, iEnd)
         else:
            iNext = self._parseRemoteFileData(buf,iBegin, iEnd)
         
         if iNext<iBegin:
            sys.stderr.write("remotefile.socket_adapter._parseData failure\n")
            return -1
         elif iNext==iBegin:
            break #wait for more data to arrive before parsing again
         else:
            assert(iNext>iBegin)
            iBegin=iNext
      return iBegin
   
   def _parseGreetingData(self, buf, iBegin, iEnd):
      while(iBegin<iEnd):
         iNext = remotefile.readLine(buf, iBegin, iEnd)
         if iNext<0:
            return iNext
         if iNext==iBegin:
            if buf[iNext]==int(ord('\n')):
               self.isGreetingParsed=True
               print("greeting parsed")
               if self.receiveHandler is not None:
                  self.receiveHandler.onConnected(self)
               return iNext+1
            else:
               return iBegin
         else:
            assert(iNext>iBegin)
            #todo: parse line here
            iBegin=iNext+1
      return iBegin
      
   def _parseRemoteFileData(self, buf, iBegin, iEnd):
      bytesParsed,value=numheader.decode32(buf,iBegin,iEnd)
      if bytesParsed<0:
         return bytesParsed
      elif bytesParsed==0:
         return iBegin
      else:         
         iNext=iBegin+bytesParsed
         #is the entire message data in the buffer? if not return iBegin
         if iNext+value<=iEnd:
            msg=buf[iNext:iNext+value]            
            if self.receiveHandler is not None:
               self.receiveHandler.onMsgReceived(msg)
            return iNext+value
         else:
            return iBegin
      
         
   