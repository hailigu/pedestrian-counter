#### darknet training log parser
**注意事项** 
1.  **需要安装 matplotlib** 

**参数说明** 
1. --source-dir  训练日志所在目录 
2. --save-dir 保存Loss曲线图片的目录，保存excel文件的目录
3. --log-file  待解析的darknet训练日志
4. --csv_file loss数据保存到excel的文件名，不指定时和log文件同名

python log_parser.py --source-dir ./person --save-dir ./person --log-file yolo_a7.log





  
