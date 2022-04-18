"""
This is where the implementation of the plugin code goes.
The CodeGen-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
from webgme_bindings import PluginBase

# Setup a logger
logger = logging.getLogger('CodeGen')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class CodeGen(PluginBase):
    def main(self):
        active_node = self.active_node
        core = self.core
        logger = self.logger
        META = self.META
        nodes = core.load_sub_tree(active_node)
        
        # get main compartments of surface
        for n in nodes:  
            if core.is_instance_of(n, META['Polymer']):
                polymer = n
            if core.is_instance_of(n, META['Initiator']):
                initiator = n
            if core.is_instance_of(n, META['Surface']):
                surface = n
            if core.is_instance_of(n, META['Monomer']):
                monomer = n
            if core.is_instance_of(n, META['EndGroup']):
                endgroup = n
        
        # process monomer
        monomer_bonds = {}
        for n in core.load_sub_tree(monomer):   
            if core.is_instance_of(n, META['Bond']):  #get monomer atom bonds
                monomer_bonds[core.get_pointer_path(n, 'src')] = core.get_pointer_path(n, 'dst')
            #get dummy connections
            if core.is_instance_of(n, META['A2D']):
                if core.is_instance_of(n, META['DummyInitiator']):
                    init_atom = core.get_pointer_path(n, 'src')
                if core.is_instance_of(n, META['DummyEndgroup']):
                    end_atom = core.get_pointer_path(n, 'src')
                if core.is_instance_of(n, META['DummyMonomer']):
                    mono_atom = core.get_pointer_path(n, 'src')
            if core.is_instance_of(n, META['D2A']):
                if core.is_instance_of(n, META['DummyInitiator']):
                    init_atom = core.get_pointer_path(n, 'dst')
                if core.is_instance_of(n, META['DummyEndgroup']):
                    end_atom = core.get_pointer_path(n, 'dst')
                if core.is_instance_of(n, META['DummyMonomer']):
                    mono_atom = core.get_pointer_path(n, 'dst')
        self.add_file('polymer.py', 'helloworld')