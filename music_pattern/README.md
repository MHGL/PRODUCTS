# **如何获取项目**     
- 下载pretrained_models   
百度云链接: https://pan.baidu.com/s/1mjFN-NVKMQuQYHRoL9zDUg  密码: p6w9
- clone仓库      
`git clone http://ai1.gemfield.org/Y/migu5th_cdmusic.git`              
- 切换目录                  
`cd migu5th_cdmusic/`                 

# **如何从Dockerfile创建镜像**      
- 创建镜像                             
`docker build -t gemfield/music-pattern:20.02-python3.7-slim -f ./docker/Dockerfile.music_pattern .`
- 参数含义                    
--tag, -t：镜像名字及标签，通常是name:tag格式                                                
-f：指定要使用的Dockerfile路径，dockerfile文件存放在docker目录下                      

# **如何创建容器并运行服务**                        
- 创建容器                     
`docker run --name music_pattern -p 10080:10080 -it gemfield/music-pattern:20.02-python3.7-slim(或者镜像ID)`                      
- 参数含义                     
--name：容器的名字                 
-p：指定宿主机与容器映射端口，宿主机端口:容器端口，注意10080:10080不能修改            
-it：以终端形式交互式操作，也可以用-d参数指定容器后台运行              
镜像ID：可用docker images命令查看              
如果是以交互式命令创建容器，成功后会提示"2020-02-22 13:26:10,525 - Tornado server starting on port 10080"，终端不再接收输入                    

# **REST API**            
| 地址     | /migu/music_pattern/v1.0                            
-|-
| 作用描述 | 检测音乐节拍类型，检测音乐重拍并返回对应时间戳                
| 请求方式 | POST
| 传入api参数 | 音频文件下载链接或者音频文件本地路径
| 返回数据格式 | Json
| 返回数据意义 | beat_times音乐重拍对应时间戳；vocals_rhythm_times人声起始位置对应时间戳；accompaniment_rhythm_times背景音乐节奏点对应时间戳               
| 返回数据格式样例 | {"beat_times": [0.33, 1.24, 2.04, 2.902.04, 2.90], "vocals_rhythm_times: {"long break: [1.1, 3.2, 11.3], "short break": [2.3, 2.7]"}, "accompaniment_rhythm_times": [3.3, 7.4, 11.7]}                

# **示例**                           
如果是以交互式运行容器，开启另外一个终端，运行：                      
- 进入容器             
`docker exec -it music_pattern bash`                
- 服务本地路径测试命令                
`curl -X POST -F "path=服务本地路径" localhost:10080/migu/music_pattern/v1.0`            
- HTTP下载测试命令                
`curl -X POST -F "url=下载链接" localhost:10080/migu/music_pattern/v1.0`            
- 文件上传测试命令                
`curl -X POST -F "file=@宿主机本地路径" localhost:10080/migu/music_pattern/v1.0`            
- 参数含义                     
-X: 指定method为POST
-F：用于发送POST请求的数据体，以表单形式提交请求                
localhost：或者是容器IP(可用docker inspect 容器ID(容器名字)查看IPADDRESS后面的IP)                          
10080：服务指定端口                           
/migu/music_pattern/v1.0：服务指定url                                             
