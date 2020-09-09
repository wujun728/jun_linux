package crud;


import java.util.List;

import org.apache.curator.RetryPolicy;
import org.apache.curator.framework.CuratorFramework;
import org.apache.curator.framework.CuratorFrameworkFactory;
import org.apache.curator.retry.ExponentialBackoffRetry;
import org.apache.zookeeper.CreateMode;
import org.apache.zookeeper.data.Stat;

/**
 * 使用curator做节点增删改查
 * @author shenzhanwang
 *
 */
public class CrudZookeeper {
	public static void main(String[] args) throws Exception {
		// 创建一个客户端
		RetryPolicy retryPolicy = new ExponentialBackoffRetry(1000, 3);
        CuratorFramework client = CuratorFrameworkFactory.builder()
                             .connectString("192.168.197.128:2181")
                             .sessionTimeoutMs(5000)
                             .retryPolicy(retryPolicy)
//                             .namespace("wsz")
                             .build();
        client.start();
        client.create()
        	.creatingParentsIfNeeded()
        	// 创建一个临时节点
        	.withMode(CreateMode.EPHEMERAL)
        	.forPath("/www/a","test".getBytes());
        	// 读取节点的数据并把状态信息写入stat
        Stat stat = new Stat();
        System.out.println(new String(client.getData().storingStatIn(stat).forPath("/www/a")));
        System.out.println(stat.getVersion());
        	// 写入数据到节点，带版本号
        client.setData().withVersion(stat.getVersion()).forPath("/www/a","shenzhanwang".getBytes());
        System.out.println(new String(client.getData().forPath("/www/a")));
        	// 版本号不一致则写入错误
        try{
//        	client.setData().withVersion(stat.getVersion()).forPath("/www/a","shenzhanwang".getBytes());
        } catch (Exception e) {
        	e.printStackTrace();
        }
        	// 删除一个节点
        client.delete().guaranteed().deletingChildrenIfNeeded().forPath("/www/a");
        	// 显示所有根节点的子节点列表
        List<String> children = client.getChildren().forPath("/");
		System.out.println(children);
	}
}
