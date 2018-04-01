import apx
import remotefile
import abc
import time

class Tester:
    
    def __init__(self, arg=None):
        
        self.client = apx.Client()
        if arg is not None:
            if isinstance(arg, str):
                self.client.create_node(arg)
            elif isinstance(arg, apx.Node):
                self.client.attach_node(arg)
    def connect_tcp(self, address, port):
        self.client.connect_tcp(address, port)
    
    def end(self):
        self.client.stop()
    
    def sleep(self, t):
        """
        sleeps for t milliseconds
        """
        time.sleep(t*0.001)
    
    def get(self, identifier):
        return self.client.read(identifier)

    def set(self, identifier, value):
        self.client.write(identifier, value)
    
    def ramp(self, identifier, target_value, target_time, step_time):
        """
        Ramps port value from current value to target_value in target_time (milliseconds) in steps of step_time (milliseconds)
        
        Limitations: Only works with simple ports that are of integer type
        
        """
        port = None
        if isinstance(identifier, str):
            port = self.client.find(identifier)            
        else:
            raise NotImplementedError(type(identifier))
        assert(port is not None)
        if not isinstance(port, apx.ProvidePort):
            raise ValueError('Cannot write to require port {0.name}.{1.name}'.format(self.client.node, port))
        
        element = port.dsg.resolve_data_element(self.client.node.dataTypes)
        start_value = self.client.read(port)
        target_steps = float(target_time)/float(step_time)
        if start_value < target_value:
            step_size = (target_value-start_value)/target_steps            
        elif start_value > target_value:
            step_size = (start_value-target_value)/target_steps
        else:
            #start_value and target_value are equal
            return
        next_value = start_value
        target_steps = int(target_steps)
        if target_steps > 0:
            for i in range(int(target_steps)-1):
                self.sleep(step_time)
                next_value+=step_size
                self.set(port, round(next_value))
        self.sleep(step_time)
        self.set(port, target_value)
        
        
        
        
        

    
    



