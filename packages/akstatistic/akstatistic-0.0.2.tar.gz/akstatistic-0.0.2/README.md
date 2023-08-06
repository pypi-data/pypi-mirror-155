# AKStatistic 项目代码行数统计

* 使用方法：
    * 安装
    ```commandline
    pip install akstatistic
    ```
    * 导入并运行
    ```
    from akstatistic.akstatistic import CodeStatistic

    static_dir = '/home/Kuture/xxx'
    statics = CodeStatistic(filter_list=['.py'],
                          source_dir_path=static_dir)
    statics.statistic()
    ```
  