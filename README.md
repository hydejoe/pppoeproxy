# pppoeproxy


## 作用

读取一边网卡的pppoe登陆请求，然后在另一站网卡上进行pppoe拨号

## 用法

``` bash
sudo python pppoeproxy.py -L <interface> -S <interface>
```

## Requirment

pypcap,dpkt,pppoe

## 注意事项

在特定的情况下，pppd会将用户名拆开解析，报错"unregconize option xxxxx",解决方法是，编辑`/usr/sbin/pppoe-connect`,大概在217行，有

``` bash
PPP_STD_OPTIONS="$PLUGIN_OPTS noipdefault noauth default-asyncmap $DEFAULTROUTE hide-password nodetach $PEERDNS mtu 1492 mru 1492 noaccomp nodeflate nopcomp novj novjccomp user $USER lcp-echo-interval $LCP_INTERVAL lcp-echo-failure $LCP_FAILURE $PPPD_EXTRA"
```

找到"user $USER",删掉即可。项目代码里已有解决措施（具体在template.py）
