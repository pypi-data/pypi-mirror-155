# coding=utf-8

"""
    @header akstatistic.py
    @abstract   
    
    @MyBlog: http://www.kuture.com.cn
    @author  Created by Kuture on 2022/6/15
    @version 1.0.0 2022/6/15 Creation()
    
    @Copyright © 2022年 Mr.Li All rights reserved
"""
import os


class CodeStatistic(object):

    def __init__(self, filter_list: list, source_dir_path=None):

        if source_dir_path is None:
            source_dir_path = os.path.dirname(os.path.abspath('./'))
        if not os.path.exists(source_dir_path):
            raise Exception('{} Is Not Exist!'.format(source_dir_path))
        if len(filter_list) == 0:
            filter_list = ['.py']

        self.source_dir_path = source_dir_path
        self.filter_list = filter_list

    def statistic(self):

        file_count = 0
        line_count = 0
        type_list = []

        for root, dir, files in os.walk(self.source_dir_path):
            for file in files:
                if not file[file.rfind('.'):] in type_list:
                    type_list.append(file[file.rfind('.'):])
                if file[file.rfind('.'):] in self.filter_list:
                    file_ab_path = os.path.join(root, file)
                    try:
                        with open(file_ab_path, 'r') as rf:
                            contents = rf.readlines()
                        file_line = len(contents)
                    except Exception as error:
                        print('File: {} Error: {}'.format(file, error))
                        continue
                    else:
                        file_count += 1
                        line_count += file_line

                        print('{}{}{}'.format(file, '-'*(80-len(file)-len(str(file_count))), file_line))
                        # print('Current File: {} Total Line Count: {} '.format(file, file_line))

        print('\nTotal Files: ', file_count)
        print('Total Lines: ', line_count)
        print('Filter Types: ', self.filter_list)
        print('All Types: ', type_list)


if __name__ == '__main__':

    code_sta = CodeStatistic(['.py'])
    code_sta.statistic()



































