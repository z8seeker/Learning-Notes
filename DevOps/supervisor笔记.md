# supevisor 使用

## supervisor 配置

supervisor 的配置文件一般在 `/etc/supervisord.conf`，根据指定的配置文件运行 supervisor:

```bash
supervisord -c /etc/supervisord.conf
```


可以把所有配置项都写到 supervisord.conf 文件里，但并不推荐这样做，而应该通过 include 的方式把不同的程序（组）写到不同的配置文件里，像下面这样：

```
[include]
files = supervisord.d/*.ini    ; 可以是 *.conf 或 *.ini
```

可以根据这样的格式编写一份配置文件：

```
[program:klx_subject1]
command=/usr/local/bin/python /opt/sites/klx_subject/enjoystudy.py --port=%(process_num)d --log_file_prefix=/opt/log/subject/klx_subject.log --debug=True
process_name=%(program_name)s-%(process_num)d
directory=/opt/sites/klx_subject/
stopsignal=INT
user=nobody
numprocs=1
numprocs_start=8300
redirect_stderr=true    ; 把 stderr 重定向到 stdout, 默认 false
log_stdout=false
log_stderr=false
```


## 使用 supervisorctl

Supervisorctl 是 supervisord 的一个命令行客户端工具，supervisorctl 这个命令会进入 supervisorctl 的 shell 界面，然后可以执行不同的命令了，同时 supervisorctl 也可以直接在 bash 终端运行:

```
supervisor> help
default commands (type help <topic>):
=====================================
add    clear  fg        open  quit    remove  restart   start   stop  update 
avail  exit   maintail  pid   reload  reread  shutdown  status  tail  version

```

## 将多个进程按组管理

```
[group: thegroupname]
programs=program1, program2    ; each refers to 'x' in [program: x] definitions
```

当添加了上述配置后，progname1 和 progname2 的进程名就会变成 `thegroupname:progname1` 和 `thegroupname:progname2` 以后就要用这个名字来管理进程了，而不是之前的 progname1 。

执行 `supervisorctl stop thegroupname:*` 就能同时结束 progname1 和 progname2，执行 `supervisorctl stop thegroupname:progname1` 就能结束 progname1
