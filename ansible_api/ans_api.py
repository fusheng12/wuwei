#!/usr/bin/env python
# -*- coding: utf8 -*-
import os
import json
from collections import namedtuple
from ansible.playbook.play import Play
from tempfile import NamedTemporaryFile
from ansible.vars.manager import VariableManager
from ansible.parsing.dataloader import DataLoader
from ansible.plugins.callback import CallbackBase
from ansible.inventory.manager import InventoryManager
from ansible.executor.task_queue_manager import TaskQueueManager

from cmdb import models



class MyRunner(object):
    """
    This is a General object for parallel execute modules.
    """

    def __init__(self, resource, *args, **kwargs):
        self.resource = resource
        self.inventory = None
        self.variable_manager = None
        self.loader = None
        self.options = None
        self.passwords = None
        self.callback = None
        self.__initializeData()
        self.results_raw = {}

    def __initializeData(self):
        """
        初始化ansible
        """
        # 初始化需要的对象
        Options = namedtuple('Options',
                             ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user',
                              'check', 'diff'])

        # module_path参数指定本地ansible模块包的路径
        self.loader = DataLoader()
        self.options = Options(connection='ssh', module_path='/usr/local/lib/python3.6/site-packages/ansible/modules',
                               forks=100, become=None, become_method=None, become_user=None, check=False, diff=False)
        self.passwords = dict(vault_pass='secret')

        # 创建库存(inventory)并传递给VariableManager
        self.inventory = InventoryManager(loader=self.loader, sources=self.resource)
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)

    def run(self, host_list, module_name, module_args, ):
        """
        run module from andible ad-hoc.
        host_list: 与inventory的resource必须一致
        module_name: ansible module_name
        module_args: ansible module args
        """
        # create play with tasks
        play_source = dict(
            name="Ansible Play",
            hosts=host_list, # 必须和inventory的resource一致 可以是文件或IP用逗号分隔的字符串
            gather_facts='no',
            tasks=[dict(action=dict(module=module_name, args=module_args))]
        )
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)

        # actually run it
        tqm = None
        self.callback = ResultsCollector()
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords,
                stdout_callback='default',
                # stdout_callback=self.callback,
            )
            tqm._stdout_callback = self.callback
            result = tqm.run(play) # 跟执行结果无关


        finally:
            if tqm is not None:
                tqm.cleanup()
            # 操作记录 将数据对象封装到self
            self.record_obj = models.Record.objects.create(hosts=host_list, module=module_name, module_args=module_args)

    # def run_playbook(self, host_list, role_name, role_uuid, temp_param):
    #     """
    #     run ansible palybook
    #     """
    #     try:
    #         self.callback = ResultsCollector()
    #         filenames = [BASE_DIR + '/handlers/ansible/v1_0/sudoers.yml']  # playbook的路径
    #         logger.info('ymal file path:%s' % filenames)
    #         template_file = TEMPLATE_DIR  # 模板文件的路径
    #         if not os.path.exists(template_file):
    #             logger.error('%s 路径不存在 ' % template_file)
    #             sys.exit()
    #
    #         extra_vars = {}  # 额外的参数 sudoers.yml以及模板中的参数，它对应ansible-playbook test.yml --extra-vars "host='aa' name='cc' "
    #         host_list_str = ','.join([item for item in host_list])
    #         extra_vars['host_list'] = host_list_str
    #         extra_vars['username'] = role_name
    #         extra_vars['template_dir'] = template_file
    #         extra_vars['command_list'] = temp_param.get('cmdList')
    #         extra_vars['role_uuid'] = 'role-%s' % role_uuid
    #         self.variable_manager.extra_vars = extra_vars
    #         ##logger.info('playbook 额外参数:%s'%self.variable_manager.extra_vars)
    #         # actually run it
    #         executor = PlaybookExecutor(
    #             playbooks=filenames, inventory=self.inventory, variable_manager=self.variable_manager,
    #             loader=self.loader,
    #             options=self.options, passwords=self.passwords,
    #         )
    #         executor._tqm._stdout_callback = self.callback
    #         executor.run()
    #     except Exception as e:
    #         ##logger.error("run_playbook:%s"%e)
    #         pass

    def get_result(self):
        self.results_raw = {'success': {}, 'failed': {}, 'unreachable': {}}
        for host, result in self.callback.host_ok.items():
            self.results_raw['success'][host] = result._result

        for host, result in self.callback.host_failed.items():
            self.results_raw['failed'][host] = result._result

        for host, result in self.callback.host_unreachable.items():
            self.results_raw['unreachable'][host] = result._result['msg']

        # 更新命令执行结果
        # print('record_obj', self.record_obj.hosts, self.record_obj.time)
        self.record_obj.result = json.dumps(self.results_raw)
        self.record_obj.save()

        # print "Ansible执行结果集:%s"%self.results_raw
        return self.results_raw


class ResultsCollector(CallbackBase):

    def __init__(self, *args, **kwargs):
        super(ResultsCollector, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.host_ok[result._host.get_name()] = result
        host = result._host
        # print(json.dumps({host.name: result._result}, indent=4))

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host_failed[result._host.get_name()] = result

if __name__ == "__main__":
    # 使用列表传入服务器IP
    host_list = ['123.206.210.55']

    # 传入inventory路径 play_source inventory必须一致 传入相同类型参数 可以是文件或IP用逗号分隔的字符串
    ansible = MyRunner(','.join(host_list) + ',')
    # 获取服务器磁盘信息
    # ansible.run('test', 'shell', "ls -l")
    # ansible.run('test', 'shell', "df -h")
    # 拷贝文件存在会覆盖
    # ansible.run('test', 'copy', 'src=/root/python_script/ansible_api/hosts dest=/root/')
    # 结果
    ansible.run(','.join(host_list) + ',', 'ping', '')
    result = ansible.get_result()
    # 成功
    succ = result['success']
    if len(succ) !=0:
        print("执行成功！")
        # print(succ)
        # ansible.run('test', 'shell', "ls -l")
        # a = ansible.get_result()
        # print(a)
    # 失败
    failed = result['failed']
    print(failed)
    # 不可到达
    unreachable = result['unreachable']
    print(unreachable)