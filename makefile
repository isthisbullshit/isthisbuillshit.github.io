download-data:
    ssh root@64.226.88.99  -t 'tar czf data.tar.gz /root/isthisbuillshit.github.io/backend/data'
    scp root@64.226.88.99:/root/data.tar.gz .\backend\data.tar.gz
    tar xf  .\data.tar.gz