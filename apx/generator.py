import apx.base
import apx.context
import cfile as C
import sys
import autosar
import os

def _genCommentHeader(comment):
   lines = []  
   lines.append(C.line('//////////////////////////////////////////////////////////////////////////////'))
   lines.append(C.line('// %s'%comment))
   lines.append(C.line('//////////////////////////////////////////////////////////////////////////////'))
   return lines


class SignalInfo:
   def __init__(self, name,offset, pack_len, func, dsg, operation, init_value=None):
      self.name=name
      self.offset=offset
      self.pack_len=pack_len
      self.init_value=init_value
      self.func=func
      self.dsg=dsg      
      self.init_data = bytearray()
      
      if init_value is not None:         
         self.genInitData(dsg, init_value)
      else:
         self.init_data.extend([0 for x in range(self.pack_len)])
      
      assert(len(self.init_data)==self.pack_len)
      
      if operation == 'pack' or operation == 'unpack':
         self.operation=operation
      else:
         raise ValueError("operation: invalid parameter value '%s', expected 'pack' or 'unpack'"%operation)
   
   def genInitData(self, dsg, init_value):      
      if (init_value['type'] == 'record'):
         if (dsg.data['type'] == 'record'):            
            #not yet implemented
            print("warning: init value for %s not yet implemented, adding zeros"%self.name, file=sys.stderr)
            self.init_data.extend([0 for x in range(self.pack_len)])
         else:
            raise ValueError('expected init_value to have record type')
      else:
         if dsg.data['type']=='C' or dsg.data['type']=='c':
            self.init_data.append(int(init_value['value']) & 0xFF)
         elif dsg.data['type']=='S' or dsg.data['type']=='s':
            #TODO: implement big endian support
            self.init_data.append(int(init_value['value']) & 0xFF)
            self.init_data.append(int(init_value['value'])>>8 & 0xFF)
         elif dsg.data['type']=='L' or dsg.data['type']=='l':
            #TODO: implement big endian support
            self.init_data.append(int(init_value['value']) & 0xFF)
            self.init_data.append(int(init_value['value'])>>8 & 0xFF)
            self.init_data.append(int(init_value['value'])>>16 & 0xFF)
            self.init_data.append(int(init_value['value'])>>24 & 0xFF)
         else:
            #not yet implemented
            print("warning: init value for %s not yet implemented, adding zeros"%self.name, file=sys.stderr)
            self.init_data.extend([0 for x in range(self.pack_len)])


class NodeGenerator:
   """
   APX Node generator for c-apx and apx-es
   """
   
   def __init__(self):
      self.includes=None
      self.InPortDataNotifyFunc=None

   def genPackUnpackInteger(self, code, buf, operation, valname, dsg, localvar, offset, indent):   
      dataLen=0
      resolvedDsg = dsg.resolveType()
      if resolvedDsg.data['type']=='c' or resolvedDsg.data['type']=='C':
         dataLen=1
         basetype='sint8' if resolvedDsg.data['type']=='c' else 'uint8'
      elif resolvedDsg.data['type']=='s' or resolvedDsg.data['type']=='S':
         dataLen=2
         basetype='sint16' if resolvedDsg.data['type']=='s' else 'uint16'
      elif resolvedDsg.data['type']=='l' or resolvedDsg.data['type']=='L':
         dataLen=4
         basetype='sint32' if resolvedDsg.data['type']=='l' else 'uint32'
      else:
         raise NotImplementedError(resolvedDsg.data['type'])
      if 'bufptr' in localvar:
         #relative addressing
         if operation == 'pack':
            code.append(C.statement('packLE(%s,(uint32) %s,(uint8) sizeof(%s))'%(localvar['bufptr'].name,valname,basetype),indent=indent))
         else:
            code.append(C.statement('%s = (%s) unpackLE(%s,(uint8) sizeof(%s))'%(valname, basetype, localvar['bufptr'].name, basetype), indent=indent))
         code.append(C.statement('%s+=(uint8) sizeof(%s)'%(localvar['bufptr'].name,basetype),indent=indent))
      else:
         #absolute addressing
         if dataLen==1:
            if operation == 'pack':
               code.append(C.statement("%s[%d]=(uint8) %s"%(buf.name,offset,valname),indent=indent))
            else: #unpack               
               code.append(C.statement("*%s = (%s) %s[%d]"%(valname, basetype, buf.name, offset),indent=indent))
         else:
            if operation == 'pack':
               code.append(C.statement('packLE(&%s[%d],(uint32) %s,(uint8) %du)'%(buf.name,offset,valname,dataLen),indent=indent))
            else: #unpack
               code.append(C.statement('*%s = (%s) unpackLE(&%s[%d],(uint8) %du)'%(valname, basetype, buf.name, offset, dataLen),indent=indent))
      return dataLen
   
   def genPackUnpackItem(self, code, buf, operation, val, dsg, localvar, offset, indent, indentStep):
      packLen=0
      if isinstance(val,C.variable):
         valname=val.name
      elif isinstance(val,str):
         valname=val
      else:
         raise ValueError(val)      
      if (dsg.isComplexType()):
         #raise NotImplemented('complex types not yet fully supported')
         if dsg.data['type'].startswith('a'): #string         
            if 'bufptr' in localvar:
               #use relative addressing using 'p' pointer
               if operation == 'pack':
                  if dsg.data['arrayLen']>1:
                     code.append(C.statement('memcpy(%s,%s,%d)'%(localvar['bufptr'].name,valname,dsg.data['arrayLen']-1),indent=indent))
                  code.append(C.statement("%s[%d]='\\0'"%(localvar['bufptr'].name,dsg.data['arrayLen']),indent=indent))
               else:
                  code.append(C.statement('memcpy(%s,%s,%d)'%(valname,localvar['bufptr'].name,dsg.data['arrayLen']),indent=indent))
               code.append(C.statement('%s+=%d'%(localvar['bufptr'].name,dsg.data['arrayLen']),indent=indent))
            else:               
               #use absolute addressing using buf variable and offset
               if operation == 'pack':
                  if dsg.data['arrayLen']>1:
                     code.append(C.statement('memcpy(&%s[%d],%s,%d)'%(buf.name,offset,valname,dsg.data['arrayLen']-1),indent=indent))
                  code.append(C.statement("%s[%d]='\\0'"%(buf.name,offset+dsg.data['arrayLen']-1),indent=indent))
               else:
                  code.append(C.statement('memcpy(%s,&%s[%d],%d)'%(valname,buf.name,offset,dsg.data['arrayLen']),indent=indent))
            packLen=dsg.data['arrayLen']
         elif dsg.data['type']=='record':
            if 'bufptr' not in localvar:
               localvar['bufptr']=C.variable('p','uint8',pointer=True)      
            for elem in dsg.data['elements']:                     
               if isinstance(val,C.variable):
                  #TODO: replace following lines with call to user hook that instead applies the _RE-rule to record elements
                  if val.pointer:
                     childName="%s->%s_RE"%(valname,elem['name'])
                  else:
                     childName="%s.%s_RE"%(valname,elem['name'])
               elif isinstance(val,str):
                  childName="%s.%s"%(valname,elem['name'])
               assert(elem is not None)
               itemLen=self.genPackUnpackItem(code, buf, operation, childName, apx.DataSignature(elem), localvar, offset, indent, indentStep)
               offset+=itemLen
               packLen+=itemLen
         elif dsg.isArray():      
            if 'loopVar' not in localvar:            
               if dsg.data['arrayLen']<256:
                  typename='uint8'
               elif dsg.data['arrayLen']<65536:
                  typename='uint16'
               else:
                  typename='uint32' 
               localvar['loopVar']=C.variable('i',typename)
            else:
               if localvar['loopVar'].typename=='uint8' and (typename=='uint16' or typename=='uint32'):
                  localvar['loopVar'].typename=typename
               elif localvar['loopVar'].typename=='uint16' and typename=='uint32':
                  localvar['loopVar'].typename=typename
            if 'bufptr' not in localvar:         
               localvar['bufptr']=C.variable('p','uint8',pointer=True)         
            code.append(C.statement('for({0}=0;{0}<{1};{0}++)'.format(localvar['loopVar'].name,dsg.data['arrayLen']),indent=indent))
            block=C.block(indent=indent)
            indent+=indentStep
            itemLen=genPackUnpackItem(block, buf, operation, valname+'[%s]'%localvar['loopVar'].name, childType, localvar, offset)
            indent-=indentStep
            code.append(block)         
      else:
         packLen=self.genPackUnpackInteger(code, buf, operation, valname, dsg, localvar, offset, indent)
      return packLen
   
   def genPackUnpackFunc(self, func, buf, offset, operation, dsg, indent, indentStep):
      indent+=indentStep
      packLen=0
      code=C.block()
      localvar={'buf':'m_outPortdata'}
      val=func.args[0]
            
      codeBlock=C.sequence()
      packLen=self.genPackUnpackItem(codeBlock, buf, operation, val, dsg, localvar, offset, indent, indentStep)
      initializer=C.initializer(None,['(uint16)%du'%offset,'(uint16)%du'%packLen])
      if 'p' in localvar:
         code.append(C.statement(localvar['p'],indent=indent))
      for k,v in localvar.items():
         if k=='p' or k=='buf':
            continue
         else:
            code.append(C.statement(v,indent=indent))
      if operation=='pack':
         code.append(C.statement('apx_nodeData_lockOutPortData(&m_nodeData)', indent=indent))
      else:
         code.append(C.statement('apx_nodeData_lockInPortData(&m_nodeData)', indent=indent))
      if 'bufptr' in localvar:
         code.append(C.statement('%s=&%s[%d]'%(localvar['bufptr'].name,buf.name,offset),indent=indent))      
      code.extend(codeBlock)
      if operation=='pack':      
         code.append(C.statement(C.fcall('outPortData_writeCmd', params=[offset, packLen]),indent=indent))
      else:
         code.append(C.statement('apx_nodeData_unlockInPortData(&m_nodeData)', indent=indent))
      code.append(C.statement('return E_OK',indent=indent))
      indent-=indentStep
      return code,packLen

   def generate(self, output_dir, node, name=None, includes=None):
      """
      generates APX node layer for single APX node
      
      parameters:
      
         node: APX node object
         
         output_dir: directory where to generate header and source files
         
         name: Can be used to override the name of the APX node. Default is 
         
         includes: list of additional include files
      
      """
      signalInfoList=[]
      signalInfoMap={'require':{}, 'provide':{}}
      inPortDataLen=0
      outPortDataLen=0
      offset=0
      if name is None:
         prefixed_name='ApxNode_'+node.name
         name = node.name
      else:
         prefixed_name='ApxNode_'+name
      self.name=name
      self.prefixed_name = prefixed_name
      self.includes=includes
      #require ports (in ports)
      for port in node.requirePorts:
         is_pointer=False        
         func = C.function("ApxNode_Read_%s_%s"%(name,port.name),"Std_ReturnType")
         is_pointer=True
         func.add_arg(C.variable('val',port.dsg.ctypename(node.dataTypes),pointer=is_pointer))         
         packLen=port.dsg.packLen(node.dataTypes)
         port.dsg.typeList=node.dataTypes
         initValue=None
         if port.attr is not None:
            initValue = port.attr.initValue
         tmp = SignalInfo(port.name,offset,packLen,func,port.dsg.resolveType(),'unpack', initValue)
         signalInfoList.append(tmp)
         signalInfoMap['require'][port.name]=tmp
         inPortDataLen+=packLen
         offset+=packLen
      #provide ports (out ports)
      offset=0      
      for port in node.providePorts:
         is_pointer=False        
         func = C.function("ApxNode_Write_%s_%s"%(name,port.name),"Std_ReturnType")
         if port.dsg.isComplexType(node.dataTypes) and not port.dsg.isArray(node.dataTypes):
            is_pointer=True    
         func.add_arg(C.variable('val',port.dsg.ctypename(node.dataTypes),pointer=is_pointer))         
         packLen=port.dsg.packLen(node.dataTypes)
         port.dsg.typeList= node.dataTypes
         initValue=None
         if port.attr is not None:
            initValue = port.attr.initValue
         tmp = SignalInfo(port.name,offset,packLen,func,port.dsg.resolveType(),'pack',initValue)
         signalInfoList.append(tmp)
         signalInfoMap['provide'][port.name]=tmp
         outPortDataLen+=packLen
         offset+=packLen
      self.inPortDataLen=inPortDataLen
      self.outPortDataLen=outPortDataLen
      header_filename = os.path.normpath(os.path.join(output_dir, self.prefixed_name+'.h'))
      source_filename = os.path.normpath(os.path.join(output_dir, self.prefixed_name+'.c'))
      with open(header_filename, "w") as fp:
         (initFunc,nodeDataFunc) = self._writeHeaderFile(fp, signalInfoList, signalInfoMap, prefixed_name.upper()+'_H', node)
      with open(source_filename, "w") as fp:
         self._writeSourceFile(fp,signalInfoMap,initFunc,nodeDataFunc, node, inPortDataLen, outPortDataLen)
   
   
   def _writeHeaderFile(self, fp, signalInfoList, signalInfoMap, guard, node):
      #indent=0
      #indentStep=3
            
      headerFile=C.hfile(None,guard=guard)
      headerFile.code.append(C.blank(1))         
      headerFile.code.append(C.include('apx_nodeData.h'))
      headerFile.code.append(C.include('Std_Types.h'))
      headerFile.code.append(C.include('Rte_Type.h'))
      if self.includes is not None:
         for filename in self.includes:
            headerFile.code.append(C.include(filename))
      
      headerFile.code.append(C.blank(1))
      headerFile.code.extend(_genCommentHeader('CONSTANTS'))
      
#TODO: fix constants generation
      # shortDefines=[]
      # for port in node.requirePorts:
      #    tmp = (['APX',self.name.upper(), 'OFFSET',port.name.upper()])
      #    if self.name.upper().startswith('APX'):
      #       del tmp[0]  
      #    identifier = '_'.join(tmp)
      #    signalInfoElem=signalInfoMap['require'][port.name]
      #    assert(signalInfoElem.operation == 'unpack')
      #    id_len=len(identifier)
      #    headerFile.code.append(C.define(identifier, str(signalInfoElem.offset).rjust(60-id_len)))
      #    shortDefines.append(C.define('APX_OFFSET_'+port.name.upper(),identifier))
      # headerFile.code.append(C.blank(1))      
#      if len(shortDefines)>0:
#         headerFile.code.extend(shortDefines)
      headerFile.code.append(C.blank(1))
      headerFile.code.extend(_genCommentHeader('FUNCTION PROTOTYPES'))      
      initFunc = C.function('ApxNode_Init_%s'%self.name,'void')
      nodeDataFunc = C.function('ApxNode_GetNodeData_%s'%self.name,'apx_nodeData_t',pointer=True) 
      headerFile.code.append(C.statement(initFunc))
      headerFile.code.append(C.statement(nodeDataFunc))
      headerFile.code.append(C.blank(1))
      for elem in signalInfoList:
         headerFile.code.append(C.statement(elem.func))
      
      if self.inPortDataLen>0:
         #void (*inPortDataWritten)(void *arg, struct apx_nodeData_tag *nodeData, uint32_t offset, uint32_t len)
         self.InPortDataNotifyFunc=C.function(self.name+'_inPortDataWritten','void')
         self.InPortDataNotifyFunc.add_arg(C.variable('arg','void',pointer=True))
         self.InPortDataNotifyFunc.add_arg(C.variable('nodeData','apx_nodeData_t',pointer=True))
         self.InPortDataNotifyFunc.add_arg(C.variable('offset','uint32_t'))
         self.InPortDataNotifyFunc.add_arg(C.variable('len','uint32_t'))
      headerFile.code.append(C.statement(self.InPortDataNotifyFunc))
         
      fp.write(str(headerFile))
      return (initFunc,nodeDataFunc)
   
   def _writeSourceFile(self, fp, signalInfoMap, initFunc, nodeDataFunc, node, inPortDataLen, outPortDataLen):
      indent=0
      indentStep=3
      
      ctx = apx.Context()
      ctx.append(node)
      nodeText = ctx.dumps()
      sourceFile=C.cfile(None)
      code = sourceFile.code
      code.append(C.line('//////////////////////////////////////////////////////////////////////////////'))
      code.append(C.line('// INCLUDES'))
      code.append(C.line('//////////////////////////////////////////////////////////////////////////////'))
      code.append(C.sysinclude('string.h'))
      code.append(C.sysinclude('stdio.h')) #TEMPORARY, REMOVE LATER
      code.append(C.include('%s.h'%self.prefixed_name))
      code.append(C.include('pack.h'))
      code.append(C.blank(1))
      code.append(C.line('//////////////////////////////////////////////////////////////////////////////'))
      code.append(C.line('// CONSTANTS AND DATA TYPES'))
      code.append(C.line('//////////////////////////////////////////////////////////////////////////////'))
      code.append(C.define('APX_DEFINITON_LEN', str(len(nodeText)+1)+'u')) #add 1 for empty newline
      code.append(C.define('APX_IN_PORT_DATA_LEN', str(inPortDataLen)+'u'))
      code.append(C.define('APX_OUT_PORT_DATA_LEN', str(outPortDataLen)+'u'))
      
      code.append(C.line('//////////////////////////////////////////////////////////////////////////////'))
      code.append(C.line('// LOCAL FUNCTIONS'))
      code.append(C.line('//////////////////////////////////////////////////////////////////////////////'))
      if outPortDataLen>0:
         code.append(C.statement('static void outPortData_writeCmd(apx_offset_t offset, apx_size_t len )'))

      code.append(C.line('//////////////////////////////////////////////////////////////////////////////'))
      code.append(C.line('// LOCAL VARIABLES'))
      code.append(C.line('//////////////////////////////////////////////////////////////////////////////'))
      
      if (outPortDataLen) > 0:
         outDatabuf=C.variable('m_outPortdata','uint8', static=True, array='APX_OUT_PORT_DATA_LEN')
         outInitData=C.variable('m_outPortInitData','uint8_t', static=True, const=True, array='APX_OUT_PORT_DATA_LEN')
         code.append(str(outInitData)+'= {')         
         initBytes=[]
         for port in node.providePorts:
            signalInfo = signalInfoMap['provide'][port.name]
            initBytes.extend([str(x) for x in signalInfo.init_data])
         assert(len(initBytes) == outPortDataLen)         
         maxItemsPerLine=32
         remain=len(initBytes)
         while(remain>0):            
            if remain>maxItemsPerLine:
               numItems,last=maxItemsPerLine,False
            else:
               numItems,last=remain,True
            if last:
               code.append(' '*indentStep+', '.join(initBytes[0:numItems]))
            else:
               code.append(' '*indentStep+', '.join(initBytes[0:numItems])+',')
            del initBytes[0:numItems]
            remain=len(initBytes)
            
         code.append('};')      
         code.append(C.blank(1))       
         code.append(C.statement(outDatabuf))
         code.append(C.statement(C.variable('m_outPortDirtyFlags','uint8_t', static=True, array='APX_OUT_PORT_DATA_LEN')))
      else:
         outDatabuf,outInitData = None,None         
      
      if (inPortDataLen) > 0:
         inDatabuf=C.variable('m_inPortdata','uint8', static=True, array='APX_IN_PORT_DATA_LEN')
         inInitData=C.variable('m_inPortInitData','uint8_t', static=True, const=True, array='APX_IN_PORT_DATA_LEN')
         code.append(str(inInitData)+'= {')
         initBytes=[]
         for port in node.requirePorts:
            signalInfo = signalInfoMap['require'][port.name]
            initBytes.extend([str(x) for x in signalInfo.init_data])
         assert(len(initBytes) == inPortDataLen)         
         maxItemsPerLine=32
         remain=len(initBytes)
         while(remain>0):            
            if remain>maxItemsPerLine:
               numItems,last=maxItemsPerLine,False
            else:
               numItems,last=remain,True
            if last:
               code.append(' '*indentStep+', '.join(initBytes[0:numItems]))
            else:
               code.append(' '*indentStep+', '.join(initBytes[0:numItems])+',')
            del initBytes[0:numItems]
            remain=len(initBytes)
         code.append('};')      
         code.append(C.blank(1))       
         code.append(C.statement(inDatabuf))
         code.append(C.statement(C.variable('m_inPortDirtyFlags','uint8_t', static=True, array='APX_OUT_PORT_DATA_LEN')))
      else:
         inDatabuf,inInitData = None,None
      
      code.append(C.statement(C.variable('m_nodeData','apx_nodeData_t',static=True)))
      code.append(C.line('static const char *m_apxDefinitionData='))
      for line in nodeText.split('\n'):
         line=line.replace('"','\\"')
         code.append(C.line('"%s\\n"'%line))         
      code.elements[-1].val+=';'
      code.append(C.blank(1))


      
      code.append(C.line('//////////////////////////////////////////////////////////////////////////////'))
      code.append(C.line('// GLOBAL FUNCTIONS'))
      code.append(C.line('//////////////////////////////////////////////////////////////////////////////'))

      sourceFile.code.append(initFunc)
      body=C.block(innerIndent=indentStep)
      if inPortDataLen>0:
         body.append(C.statement('memcpy(&m_inPortdata[0], &m_inPortInitData[0], APX_IN_PORT_DATA_LEN)'))
         body.append(C.statement('memset(&m_inPortDirtyFlags[0], 0, sizeof(m_inPortDirtyFlags))'))
      if outPortDataLen>0:
         body.append(C.statement('memcpy(&m_outPortdata[0], &m_outPortInitData[0], APX_OUT_PORT_DATA_LEN)'))
         body.append(C.statement('memset(&m_outPortDirtyFlags[0], 0, sizeof(m_outPortDirtyFlags))'))
      args = ['&m_nodeData', '"%s"'%(node.name), '(uint8_t*) &m_apxDefinitionData[0]', 'APX_DEFINITON_LEN']
      if inPortDataLen>0:
         args.extend(['&m_inPortdata[0]', '&m_inPortDirtyFlags[0]', 'APX_IN_PORT_DATA_LEN'])
      else:
         args.extend(['0','0','0'])
      if outPortDataLen>0:         
         args.extend(['&m_outPortdata[0]', '&m_outPortDirtyFlags[0]', 'APX_OUT_PORT_DATA_LEN'])
      else:
         args.extend(['0','0','0'])
      body.append(C.statement('apx_nodeData_create(%s)'%(', '.join(args))))
      body.append(C.line('#ifdef APX_POLLED_DATA_MODE', indent=0))
      body.append(C.statement('rbfs_create(&m_outPortDataCmdQueue, &m_outPortDataCmdBuf[0], APX_NUM_OUT_PORTS, APX_DATA_WRITE_CMD_SIZE)'))
      body.append(C.line('#endif', indent=0))
               
      sourceFile.code.append(body)
      sourceFile.code.append(C.blank(1))
    
      sourceFile.code.append(nodeDataFunc)
      body=C.block(innerIndent=indentStep)
      
      body.append(C.statement('return &m_nodeData'))
      sourceFile.code.append(body)
      sourceFile.code.append(C.blank(1))
    
      for port in node.requirePorts:
         signalInfo = signalInfoMap['require'][port.name]
         sourceFile.code.append(signalInfo.func)         
         body,packLen=self.genPackUnpackFunc(signalInfo.func, inDatabuf, signalInfo.offset, signalInfo.operation, signalInfo.dsg, indent, indentStep)
         code.append(body)
         code.append(C.blank())
      for port in node.providePorts:
         signalInfo = signalInfoMap['provide'][port.name]
         sourceFile.code.append(signalInfo.func)         
         body,packLen=self.genPackUnpackFunc(signalInfo.func, outDatabuf, signalInfo.offset, signalInfo.operation, signalInfo.dsg, indent, indentStep)
         code.append(body)
         code.append(C.blank())
      
      if self.InPortDataNotifyFunc is not None:
         code.append(self.InPortDataNotifyFunc)
         indent+=indentStep
         body=C.block(innerIndent=indent)
#         body.append(C.line('uint32_t endOffset=offset+len;',indent=indent))
#         body.append(C.statement('(void) arg'))         
#         body.append(C.blank())
         # body.append(C.line('while(offset < endOffset)',indent=indent))
         # body.append(C.line('{',indent=indent))
         # indent+=indentStep
         # 
         # body.append(C.line('switch(offset)',indent=indent))
         # body.append(C.line('{',indent=indent))
         # for port in node.requirePorts:
         #    signal = signalInfoMap['require'][port.name]
         #    tmp = (['APX',self.name.upper(), 'OFFSET',port.name.upper()])
         #    if self.name.upper().startswith('APX'):
         #       del tmp[0]  
         #    identifier = '_'.join(tmp)
         #    body.append(C.line('case %s:'%identifier,indent=indent))            
         #    indent+=indentStep
         #    body.append(C.line('///TODO: if a callback function has been registered, call it here',indent=indent))
         #    body.append(C.statement(C.fcall('printf',['"%s\\n"'%port.name]), indent=indent))
         #    body.append(C.statement('offset+=%du'%signal.pack_len,indent=indent))
         #    indent-=indentStep
         #    body.append(C.statement('break',indent=indent))
         # body.append(C.line('default:',indent=indent))         
         # body.append(C.statement('offset=endOffset; //breaks out of while-loop',indent=indent+indentStep))
         # body.append(C.line('}',indent=indent))
         # indent-=indentStep
         # body.append(C.line('}',indent=indent)) 

   
   
         code.append(body)
         indent-=indentStep
                  
      code.append(C.line('//////////////////////////////////////////////////////////////////////////////'))
      code.append(C.line('// LOCAL FUNCTIONS'))
      code.append(C.line('//////////////////////////////////////////////////////////////////////////////'))
      if outPortDataLen>0:
         code.append('''static void outPortData_writeCmd(apx_offset_t offset, apx_size_t len )
{
   if ( (m_outPortDirtyFlags[offset] == 0) && (true == apx_nodeData_isOutPortDataOpen(&m_nodeData) ) )
   {      
      m_outPortDirtyFlags[offset] = (uint8_t) 1u;
      apx_nodeData_unlockOutPortData(&m_nodeData);
      apx_nodeData_outPortDataNotify(&m_nodeData, (uint32_t) offset, (uint32_t) len);
      return;
   }
   apx_nodeData_unlockOutPortData(&m_nodeData);
}


''')      
      fp.write(str(sourceFile))
    

class ComSendReceiveFunction:
   def __init__(self, portName, dataType, upperLayerFunc, lowerLayerFunc):
      self.portName = portName
      self.dataType = dataType
      self.func = upperLayerFunc
      self.innerFunc = lowerLayerFunc
      self.innerIndent = 3
      self.var = C.variable('m_'+portName, dataType.name, static=True)
   

class ComSendFunction(ComSendReceiveFunction):
   def __init__(self, portName, dataType, upperLayerFunc, lowerLayerFunc):
      super().__init__(portName, dataType, upperLayerFunc, lowerLayerFunc)
      self._generateBody()
   
   def _generateBody(self):
      self.body = C.block(innerIndent = self.innerIndent)
      self.body.append(C.line('if (%s != %s)'%(self.func.args[0].name, self.var.name)))
      block = C.block(innerIndent = self.innerIndent)
      block.append(C.statement('%s = %s'%(self.var.name, self.func.args[0].name)))
      block.append(C.statement(C.fcall(self.innerFunc.name, [self.func.args[0].name])))
      self.body.append(block)
      self.body.append(C.statement('return E_OK'));


class ComReceiveFunction(ComSendReceiveFunction):
   def __init__(self, portName, dataType, upperLayerFunc, lowerLayerFunc):
      super().__init__(portName, dataType, upperLayerFunc, lowerLayerFunc)
      self._generateBody()
   
   def _generateBody(self):
      self.body = C.block(innerIndent = self.innerIndent)
      self.body.append(C.statement(C.fcall(self.innerFunc.name, [self.func.args[0].name])))      
      self.body.append(C.statement('return E_OK'));

class ComGenerator:
   def __init__(self, com_config, apx_context):
      self.config = com_config
      self.apx_context = apx_context
      self.upperLayerAPI = {'receive':[], 'send':[]}
      self.localVars = []
      self.innerIndent=3
      self.includes = []
      self.createAPI()
      
      
   def createAPI(self):
      for name in sorted(self.config.send.keys()):
         signal = self.config.send[name]
         self.createSendFunction(signal.name, signal.dataType)
      for name in sorted(self.config.receive.keys()):
         signal = self.config.receive[name]
         self.createReceiveFunction(signal.name, signal.dataType)
   
   def createSendFunction(self, signal_name, dataType):      
      upperLayerFunc = C.function('ApxCom_Send_'+signal_name, 'Std_ReturnType')
      isPointer = True if dataType.isComplexType else False      
      upperLayerFunc.add_arg(C.variable('value', dataType.name, pointer=isPointer))      
      lowerLayerFunc = None
      for node in self.apx_context.nodes:
         for apx_port in node.requirePorts + node.providePorts:
            if apx_port.name == signal_name:
               name = 'ApxNode_Write_%s_%s'%(node.name,apx_port.name)
               lowerLayerFunc = C.function(name, 'Std_ReturnType')
               lowerLayerFunc.add_arg(C.variable('val', dataType.name, pointer=isPointer))
               include_file = 'ApxNode_%s.h'%node.name
               if include_file not in self.includes:
                  self.includes.append(include_file)
               break
      if lowerLayerFunc is None:
         raise ValueError('unable to find apx node with port '+signal_name)
      info = ComSendFunction(signal_name, dataType, upperLayerFunc, lowerLayerFunc)
      self.upperLayerAPI['send'].append(info)
      self.localVars.append(info.var)

   def createReceiveFunction(self, signal_name, dataType):      
      upperLayerFunc = C.function('ApxCom_Receive_'+signal_name, 'Std_ReturnType')
      isPointer = True
      upperLayerFunc.add_arg(C.variable('value', dataType.name, pointer=isPointer))      
      lowerLayerFunc = None
      for node in self.apx_context.nodes:
         for apx_port in node.requirePorts + node.providePorts:
            if apx_port.name == signal_name:
               name = 'ApxNode_Read_%s_%s'%(node.name,apx_port.name)
               lowerLayerFunc = C.function(name, 'Std_ReturnType')
               lowerLayerFunc.add_arg(C.variable('val', dataType.name, pointer=isPointer))
               include_file = 'ApxNode_%s.h'%node.name
               if include_file not in self.includes:
                  self.includes.append(include_file)
               break
      if lowerLayerFunc is None:
         raise ValueError('unable to find apx node with port '+signal_name)
      info = ComReceiveFunction(signal_name, dataType, upperLayerFunc, lowerLayerFunc)
      self.upperLayerAPI['receive'].append(info)
      self.localVars.append(info.var)
      
      
   def generateHeader(self, path):
      hfile = C.hfile(path)
      code = hfile.code
      code.extend(_genCommentHeader('INCLUDES'))
      code.append(C.include("Rte_Type.h"))
      code.append(C.blank(1))
      code.extend(_genCommentHeader('CONSTANTS AND DATA TYPES'))
      code.append(C.blank(1))
      code.extend(_genCommentHeader('GLOBAL FUNCTIONS'))
      code.extend(self._genUpperLayerPrototypes())
      with open(path, "w") as fp:
         fp.write(str(hfile))
      
   
   def _genUpperLayerPrototypes(self):
      code = C.sequence()
      for info in self.upperLayerAPI['send'] + self.upperLayerAPI['receive']:
         code.append(C.statement(info.func))
      return code
   
   def generateSource(self, path):
      file = C.cfile(path)
      code = file.code
      code.extend(self._writeIncludes())
      code.append(C.blank(1))
      code.extend(_genCommentHeader('CONSTANTS AND DATA TYPES'))
      code.append(C.blank(1))
      code.extend(_genCommentHeader('LOCAL FUNCTION PROTOTYPES'))      
      code.extend(self._writeLocalVars())      
      code.extend(self._generateGlobalFunctionsSource())      
      with open(path, "w") as fp:
         fp.write(str(file))
   
   def _writeIncludes(self):
      code = C.sequence()
      code.extend(_genCommentHeader('INCLUDES'))
      code.append(C.include("Rte_Type.h"))
      for file_name in self.includes:
         code.append(C.include(file_name))
      return code

   def _writeLocalVars(self):
      code = C.sequence()
      code.append(C.blank(1))
      code.extend(_genCommentHeader('LOCAL VARIABLES'))
      for var in self.localVars:
         code.append(C.statement(var))
      return code
   
   def _generateGlobalFunctionsSource(self):
      code = C.sequence()
      code.append(C.blank(1))
      code.extend(_genCommentHeader('GLOBAL FUNCTIONS'))
      for info in self.upperLayerAPI['send'] + self.upperLayerAPI['receive']:
         code.append(info.func)
         code.append(info.body)
      return code