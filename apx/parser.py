#! /bin/python3
#Copyright (c) 2015-2018, Conny Gustafsson

import math
import re
import sys
import apx

START_SECTION=0
NODE_SECTION=1
TYPE_SECTION=2
PROVIDE_SECTION=3
REQUIRE_SECTION=4

_p0=re.compile(r'([\+\-A-Z]+)')
_p1=re.compile(r'([^:]*)')
_p2=re.compile(r'#(.*)')


def strip_comment(apx_text):    
    return re.sub(_p2, '', apx_text)


def apx_split_line(s):
   #remove comment section at end of line
   processed = strip_comment(s).rstrip(' \r\n')   
   if len(processed)==0:
      return None
   r0=_p0.match(processed)   
   if r0 is not None:
      lineType=r0.group(1)
      remain=processed[len(lineType):]
      (name,remain) = apx.parse_str(remain)
      if len(remain)>0:
         r1 = _p1.match(remain)
         if r1 is not None:
            dsg=r1.group(1)
            remain=remain[len(dsg):]
            if len(remain)>0:
               if remain[0]==':':
                  remain=remain[1:]
               return (lineType,name,dsg,remain)
         return (lineType,name,dsg,None)
      else:
         return (lineType,name)
   return None,processed


class Parser:
   @staticmethod
   def _parseHeaderLine(s):
      """returns string with major and minor version of APX header or None if line cannot be parsed"""
      p=re.compile(r'APX/(\d)\.(\d)')
      r = p.match(s)
      if r != None:         
         return "%s.%s"%(r.group(1),r.group(2))
      return None   
   
   def _processLine(self, line):
      parts = apx_split_line(line)
      if parts is None:
         return
      if len(parts)>0:
         if self.cs == START_SECTION:            
            if parts[0]=='N': #Node Line
               self.cs=NODE_SECTION
               apxNode = apx.Node(parts[1])
               self._applyNode(apxNode)
            else:
               raise apx.ParseError('Syntax error on line {:d}. Expected Node definition'.format(self.lineNumber, line))
         elif self.cs == NODE_SECTION:            
            if parts[0]=='T':
               self.cs=TYPE_SECTION
               apxType = apx.DataType(parts[1],parts[2],parts[3])
               self._applyType(apxType)
            elif parts[0]=='P':
               self.cs=PROVIDE_SECTION
               portLine = apx.ProvidePort(parts[1],parts[2],parts[3])
               self._applyPort(portLine)                  
            elif parts[0]=='R':
               self.cs=REQUIRE_SECTION
               portLine = apx.RequirePort(parts[1],parts[2],parts[3])
               self._applyPort(portLine)
            else:
               raise apx.ParseError('Syntax error on line {:d}: {}'.format(self.lineNumber, line))
         elif self.cs == TYPE_SECTION:            
            if parts[0]=='T':               
               typeLine = apx.DataType(parts[1],parts[2],parts[3])
               self._applyType(typeLine)
            elif parts[0]=='P':
               self.cs=PROVIDE_SECTION
               portLine = apx.ProvidePort(parts[1],parts[2],parts[3])
               self._applyPort(portLine)
            elif parts[0]=='R':
               self.cs=REQUIRE_SECTION
               portLine = apx.RequirePort(parts[1],parts[2],parts[3])
               self._applyPort(portLine)
            else:
               raise apx.ParseError('Syntax error on line {:d}: {}'.format(self.lineNumber, line))
         elif self.cs == PROVIDE_SECTION:
            if parts[0]=='P':
               portLine = apx.ProvidePort(parts[1],parts[2],parts[3])
               self._applyPort(portLine)
            elif parts[0]=='R':
               self.cs=REQUIRE_SECTION
               portLine = apx.RequirePort(parts[1],parts[2],parts[3])
               self._applyPort(portLine)
         elif self.cs == REQUIRE_SECTION:
            if parts[0]=='R':               
               portLine = apx.RequirePort(parts[1],parts[2],parts[3])
               self._applyPort(portLine)
            elif parts[0]=='P':
               self.cs=PROVIDE_SECTION
               portLine = apx.ProvidePort(parts[1],parts[2],parts[3])
               self._applyPort(portLine)
            else:
               raise apx.ParseError('Syntax error on line {:d}: {}'.format(self.lineNumber, line))               
         else:
            raise RuntimeError("Internal parser error, line={:d}".format(self.lineNumber))
      else:
         raise apx.ParseError('Syntax error on line {:d}: {}'.format(self.lineNumber, line))
   
   def _parseV12(self,fp,firstLine):
      """parses APX version 1.2 file"""
      while True:
         if firstLine != None:
            line = firstLine #reparse firstLine in case it was given to us as an argument
            firstLine = None
         else:
            line = fp.readline() #read next line from file handle
            if len(line)==0:
               break
            self.lineNumber+=1
            line=line.rstrip('\r\n')
            self._processLine(line)
      self.node.resolve_types()
      return self.node
   
   def __init__(self):      
      self.node = None
      self.lineNumber = None
   
   def load(self,fp):
      self.cs=None
      self.lineNumber=1
      firstLine = fp.readline()
      firstLine=firstLine.rstrip('\r\n')
      parsedVersion=Parser._parseHeaderLine(firstLine)
      if parsedVersion == None:
         version = "1.2"
      else:
         version = parsedVersion      
      if version == "1.2":
         self.cs = START_SECTION
         if parsedVersion==None:
            return self._parseV12(fp,firstLine) #firstLine did not contain APX version line
         else:
            self.lineNumber+=1
            return self._parseV12(fp,None) #firstLine contained APX version line      
      else:
         raise NotImplementedError

   def loads(self, text):
      self.cs=None
      self.lineNumber=1
      lines = text.split('\n')
      skipLine=0
      firstLine = lines[0]
      firstLine=firstLine.rstrip('\r\n')
      parsedVersion=Parser._parseHeaderLine(firstLine)
      if parsedVersion == None:
         version = "1.2"
      else:
         version = parsedVersion      
      if version == "1.2":
         self.cs = START_SECTION
         if parsedVersion is not None:
            skipLine=1         
      else:
         raise NotImplementedError
      for line in lines:
         if skipLine>0:
            self.lineNumber+=1
            skipLine-=1
            continue
         else:         
            self._processLine(line)
            self.lineNumber+=1
      if self.node is None:
         raise RuntimeError('No node was found')
      self.node.text=text
      self.node.resolve_types()
      return self.node
   
   def parse(self, filename):
      """
      Convenience method for parsing file from filename
      """
      with open(filename, "r", encoding='utf-8') as fp:
         return self.load(fp)
   

   def _applyNode(self,apxNode):
      self.node = apxNode
   
   def _applyType(self,apxType):
      self.node.add_type(apxType)
   
   def _applyPort(self,apxPort):
      if isinstance(apxPort,apx.ProvidePort):
         self.node.append(apxPort)
      elif isinstance(apxPort,apx.RequirePort):
         self.node.append(apxPort)
      else:
         raise ValueError
   


   
