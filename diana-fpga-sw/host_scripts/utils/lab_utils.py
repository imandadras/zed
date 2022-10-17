class InstumentClass():    
    def __init__(self, name, ip_addr_cmd, **res_manager_args):
        self.name = name
        self.IP = ip_addr_cmd
        self.tool = self._open_resource(ip_addr_cmd,**res_manager_args)
        self._init_instrument()

    @staticmethod
    def _open_resource():
        raise NotImplementedError

    def _init_instrument():
        #TO BE implemented/defined by child class
        raise NotImplementedError
    
    def status():
        #TODO define a std version for pyvisa instruments
        raise NotImplementedError

    def close(self):
        if self.tool != None:
            self.tool.close()
