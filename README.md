python version == 2.7.18

Clone dev-ops
```bash
cd /opt/dev-ops
source bootstrap.sh 
```


INSTALL SERVER:
```bash
python2 /opt/dev-ops/install.py --master --groups server
```
INSTALL CLIENT:
```
python2 /opt/dev-ops/install.py --slave --groups archlinux
```
