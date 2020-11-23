package watcher;

import java.util.List;

import org.apache.curator.framework.CuratorFramework;
import org.apache.curator.framework.CuratorFrameworkFactory;
import org.apache.curator.framework.recipes.cache.NodeCache;
import org.apache.curator.framework.recipes.cache.NodeCacheListener;
import org.apache.curator.retry.ExponentialBackoffRetry;
import org.apache.zookeeper.CreateMode;

/**
 * cache是curator对事件监听的包装，对事件的监听看做本地缓存与服务器的对比
 * @author Wujun
 * NodeCache用于监听指定节点的变化（被修改）
 */
public class NodeCacheDemo {
	static String path = "/zk/nodecache";
    static CuratorFramework client = CuratorFrameworkFactory.builder()
            .connectString("192.168.197.128:2181")
            .sessionTimeoutMs(5000)
            .retryPolicy(new ExponentialBackoffRetry(1000, 3))
            .build();
	
	public static void main(String[] args) throws Exception {
		client.start();
		client.create()
		      .creatingParentsIfNeeded()
		      .withMode(CreateMode.EPHEMERAL)
		      .forPath(path, "init".getBytes());
	    final NodeCache cache = new NodeCache(client,path,false);
	    // 开启对/zk/nodecache节点的监听
		cache.start(true);
		// 添加监听的回调方法
		cache.getListenable().addListener(new NodeCacheListener() {
			@Override
			public void nodeChanged() throws Exception {
				System.out.println("Node data update, new data: " + 
			    new String(cache.getCurrentData().getData()));
			}
		});
		// 改变数据触发监听的方法
		client.setData().forPath( path, "u".getBytes() );
		// 删除不会触发节点的监听
		client.delete().deletingChildrenIfNeeded().forPath( path );
		cache.close();
	}
}
