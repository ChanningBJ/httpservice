import shutil
import os
import datetime
import subprocess
import tabulate as tabulate


class DocGenerator:
    def __init__(self, input_path, output_path, name="API", author="unknown"):
        self.__input_path = input_path
        self.__output_path = output_path
        self.__api_name = name
        self.__author = author
        self.__service_list = dict()
        self.__root = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '../'
        )
        pass

    def __copy_files(self):
        shutil.copy(os.path.join(self.__root,'resources/styles.css'), self.__output_path)

        copyright_file = os.path.join(self.__input_path, '_copyright')
        if os.path.isfile(copyright_file):
            shutil.copy(copyright_file, self.__output_path)
        else:
            with open(copyright_file,'w') as fp:
                fp.write('default copyright')
            shutil.copy(copyright_file, self.__output_path)

    def __generate_toc_conf(self):
        with open(os.path.join(self.__output_path, 'toc.conf'), 'w') as fp:
            for service_name in self.__service_list:
                fp.write(service_name+'.md\n')

    def __generate_index(self):
        index_file = os.path.join(self.__input_path, 'index.md')
        if os.path.isfile(index_file):
            shutil.copy(index_file, self.__output_path)
        else:
            with open(index_file,'w') as fp:
                fp.write('% '+self.__api_name+"\n")
                fp.write('% '+self.__author+"\n")
                fp.write('% '+datetime.datetime.now().strftime("%Y/%m/%d")+"\n")
                fp.write('\n')
                fp.write(self.__api_name+'\n')
                fp.write('='*len(self.__api_name)*2+'\n')
                fp.write('This is the API document\n')
            shutil.copy(index_file, self.__output_path)

    def __generate_service_page(self):
        for service_name in self.__service_list:
            input_md_file_part1 = os.path.join(self.__input_path,service_name+'_part1.md')
            if not os.path.isfile(input_md_file_part1):
                with open(input_md_file_part1, 'w', encoding='utf8') as fp:
                    fp.write('API Description\n')
                    fp.write('=======\n')
                    fp.write('TODO: add contents here\n')
            input_md_file_part2 = os.path.join(self.__input_path,service_name+'_part2.md')
            if not os.path.isfile(input_md_file_part2):
                with open(input_md_file_part2, 'w', encoding='utf8') as fp:
                    fp.write('Details\n')
                    fp.write('=======\n')
                    fp.write('TODO: add contents here\n')
            output_md_file = os.path.join(self.__output_path,service_name+'.md')
            with open(output_md_file, 'w', encoding='utf8') as fp:
                fp.write('% '+service_name+"\n")
                fp.write('% '+self.__author+"\n")
                fp.write('% '+datetime.datetime.now().strftime("%Y/%m/%d")+"\n")
                fp.write('\n')
                with open(input_md_file_part1, encoding='utf8') as input_fp:
                    for line in input_fp:
                        fp.write(line)
                fp.write('\n')
                fp.write('Parameters\n')
                fp.write('==========\n')
                fp.write('\n')
                fp.write('\n')
                fp.write(self.__generate_parameters(self.__service_list[service_name]))
                fp.write('\n')
                fp.write('\n')
                with open(input_md_file_part2, encoding='utf8') as input_fp:
                    for line in input_fp:
                        fp.write(line)

    def __generate_parameters(self,parameters):
        headers = ['name', 'type', 'default', 'is optional', 'allowed values', 'comments']
        content = []
        for param in parameters:
            content.append([
                param.name,
                param.get_type(),
                str(param.get_default_value()) if param.get_default_value() is not None else 'N/A',
                str(param.is_optional()),
                ','.join(param.get_allowed_values()),
                param.get_comments()
            ])
        return tabulate.tabulate(content, headers, tablefmt="simple")

    def add_service(self, service):
        self.__service_list[service.__name__] = service.get_parameters()

    def generate_doc(self):
        self.__copy_files()
        self.__generate_toc_conf()
        self.__generate_index()
        self.__generate_service_page()
        subprocess.Popen(['java', '-jar', os.path.join(self.__root, 'bin', 'rippledoc-0.1.1-standalone.jar'), '"$@"'],
                         cwd=self.__output_path).wait()
