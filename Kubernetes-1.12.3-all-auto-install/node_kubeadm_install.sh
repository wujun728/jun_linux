# 安装k8s-dashboard扩展
kubectl apply -f ~/kubernetes-dashboard.yaml
kubectl apply -f ~/kubernetes-dashboard-admin.rbac.yaml
# 完成后等待pod:dashboard创建启动
# 查看pod状态
kubectl get pods -n kube-system
# 查看service状态
kubectl get service -n kube-system

#打开浏览器：访问 ：https://localhost:30001，使用token登录，token查看方法如下
#kubectl -n kube-system get secret
#kubectl -n kube-system describe secret kubernetes-dashboard-admin-token-skhfh #{上条命令输出的结果中复制的类似kubernetes-dashboard-admin-token-skhfh的key字符串到这里替换}
#复制tokdn数据到登录框内登录即可登录