from setuptools import setup, find_packages

setup(name='seung-test',

      version='0.1.1',

      description='seung wang Test Package',

      author='Seung Wang Kim',

      author_email='seungwangkim@gmail.com',

      license='MIT',

      py_modules=['check_manager', 'compute_manager', 'edge_deploy', 'fw_multi_object', 'general_request', 'import_nsx_info', 'lb_multi_object', 'license', 'log', 'manager_deploy', 'multi_object_create', 'object_search', 'policy', 'profile', 'vcenter_con'],

      python_requires='>=3.9',

      #data_files=['NSX_API.csv', 'nsx_script_log.txt']

      #install_requires=[],

      #packages=['test']

      )