package watcher;

import org.apache.curator.framework.CuratorFramework;
import org.apache.curator.framework.CuratorFrameworkFactory;
import org.apache.curator.framework.recipes.cache.PathChildrenCache;
import org.apache.curator.framework.recipes.cache.PathChildrenCacheEvent;
import org.apache.curator.framework.recipes.cache.PathChildrenCacheListener;
import org.apache.curator.framework.recipes.cache.PathChildrenCache.StartMode;
import org.apache.curator.retry.ExponentialBackoffRetry;
import org.apache.zookeeper.CreateMode;

/**
 * PathChildrenCache用于监听指定节点的子节点的变化，包括子节点的新增、修改和删除
 * 这种监听只适用于直接下属节点，对于间接下属无法监听
 * @author shenzhanwang
 *
 */
public class NodeChildrenCacheDemo {
	 static String path = "/zk-listen";
	    static CuratorFramework client = CuratorFrameworkFactory.builder()
	            .connectString("192.168.197.128:2181")
	            .retryPolicy(new ExponentialBackoffRetry(1000, 3))
	            .sessionTimeoutMs(5000)
	            .build();
		public static void main(String[] args) throws Exception {
			client.start();
			// 配置为true表示接到节点变更时能够去除变更数据
			PathChildrenCache cache = new PathChildrenCache(client, path, true);
			cache.start(StartMode.POST_INITIALIZED_EVENT);
			cache.getListenable().addListener(new PathChildrenCacheListener() {
				public void childEvent(CuratorFramework client, 
						               PathChildrenCacheEvent event) throws Exception {
					switch (event.getType()) {
					case CHILD_ADDED:
						System.out.println("CHILD_ADDED," + event.getData().getPath());
						break;
					case CHILD_UPDATED:
						System.out.println("CHILD_UPDATED," + event.getData().getPath());
						break;
					case CHILD_REMOVED:
						System.out.println("CHILD_REMOVED," + event.getData().getPath());
						break;
					default:
						break;
					}
				}
			});
			client.create().withMode(CreateMode.PERSISTENT).forPath(path);
			Thread.sleep( 1000 );
			// 新增子节点，触发监听
			client.create().withMode(CreateMode.PERSISTENT).forPath(path+"/c1");
			Thread.sleep( 1000 );
			// 删除子节点，触发监听
			client.delete().forPath(path+"/c1");
			Thread.sleep( 1000 );
			client.delete().forPath(path);
		}
}
