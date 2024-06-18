python version == 2.7.18

Clone dev-ops and setup virtualenv
```bash
cd /opt; git clone https://github.com/aumanimationstudios/dev-ops.git;
cd /opt/dev-ops; git checkout archlinux-py2
source bootstrap.sh
```

INSTALL SERVER:
```bash
python2 /opt/dev-ops/install.py --master --groups server
```
INSTALL CLIENT:
```bash
python2 /opt/dev-ops/install.py --slave --groups archlinux
```

Exit venv
```bash
deactivate
```

Start supervisor
```bash
systemctl enable supervisord
systemctl start supervisord
```
