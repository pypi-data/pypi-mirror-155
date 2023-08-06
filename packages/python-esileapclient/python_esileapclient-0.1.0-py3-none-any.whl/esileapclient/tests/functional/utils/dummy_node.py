import os
import json
import tempfile


class DummyNode():
    def __init__(self, node_dir, project_uuid=''):
        if not os.path.exists(node_dir):
            os.mkdir(node_dir)
        elif not os.path.isdir(node_dir):
            raise NotADirectoryError('Invalid value for dummy_node_dir: %s'
                                     % node_dir)

        dummy_node_info = {
            'project_owner_id': project_uuid,
            'server_config': {
                'example_attribute': 'example server config',
                'cpu_type': 'Intel Xeon',
                'cores': 16,
                'ram_gb': 512,
                'storage_type': 'Samsung SSD',
                'storage_size_gb': 1024
            }
        }

        with tempfile.NamedTemporaryFile(prefix='', dir=node_dir,
                                         mode='w+', delete=False) as node:
            json.dump(dummy_node_info, node)
            self.path = node.name
            self.uuid = os.path.basename(node.name)

    def __del__(self):
        os.remove(self.path)
