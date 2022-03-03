package crud;
import java.util.List;

import org.apache.curator.framework.CuratorFramework;
import org.apache.curator.framework.CuratorFrameworkFactory;
import org.apache.curator.retry.ExponentialBackoffRetry;
import org.apache.curator.utils.EnsurePath;

public class EnsurePathDemo {

    static String path = "/xxx/c1";
    static CuratorFramework client = CuratorFrameworkFactory.builder()
            .connectString("192.168.197.128:2181")
            .sessionTimeoutMs(5000)
            .retryPolicy(new ExponentialBackoffRetry(1000, 3))
            .build();
	public static void main(String[] args) throws Exception {
		
		client.start();
		
		EnsurePath ensurePath = new EnsurePath(path);
		// ensure方法即使重复调用也不会抛出异常
		ensurePath.ensure(client.getZookeeperClient());
		ensurePath.ensure(client.getZookeeperClient());   
		List<String> children = client.getChildren().forPath("/xxx");
		System.out.println(children);
	}
}