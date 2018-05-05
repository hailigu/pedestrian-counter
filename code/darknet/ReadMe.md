#### darknet training log parser
**注意事项** 
1.  **需要安装 matplotlib** 

**参数说明** 
1. --source-dir  训练日志所在目录 
2. --save-dir 保存Loss曲线图片的目录，保存excel文件的目录
3. --log-file  待解析的darknet训练日志
4. --csv_file loss数据保存到excel的文件名，不指定时和log文件同名

python log_parser.py --source-dir ./person --save-dir ./person --log-file yolo_a7.log


#### darknet mAP && recall tool
**注意事项** 
1.  **需要安装 matplotlib** 

**参数说明** 
1. --base-dir  .data .names .cfg 及生成模型保存文件夹所在根目录，如darknet文件夹下一个子目录 ./gender 
2. --config_prefix 训练时使用的配置文件名，无需后缀 .cfg
3. --data_file  训练用.data文件
4. ----weights_prefix 训练时生成模型的前缀, 如模型名为 tiny-yolo-person_9_400.weights，则传入 tiny-yolo-person_9_
5. --start 要统计模型的开始数字，如开始模型名为 tiny-yolo-person_9_400.weights，则传入 400
6. --end   要统计模型的结束数字，如结束模型名为 tiny-yolo-person_9_1000.weights，则传入 1000
7. --weight_dir 保存模型文件的文件夹名，如果.data配置里 backup = ./person9300/9300_26298/，
则此时应传入 9300_26298，为空时默认为 backup
8. --step 生成模型保存间隔数，如果每100个iter保存一次则传 100，默认为200


python map.py --base_dir ./person9300 --config_prefix tiny-yolo-person_9 --data_file person_9300_26298.data --weights_prefix tiny-yolo-person_9_ --start 85400 --end 89200 --weight_dir 9300_26298 --step 200




  
