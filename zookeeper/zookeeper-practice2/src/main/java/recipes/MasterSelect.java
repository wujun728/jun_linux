package recipes;

import java.util.ArrayList;
import java.util.List;

import org.apache.curator.RetryPolicy;
import org.apache.curator.framework.CuratorFramework;
import org.apache.curator.framework.CuratorFrameworkFactory;
import org.apache.curator.framework.recipes.leader.LeaderSelector;
import org.apache.curator.framework.recipes.leader.LeaderSelectorListener;
import org.apache.curator.framework.state.ConnectionState;
import org.apache.curator.retry.ExponentialBackoffRetry;
import org.apache.curator.utils.CloseableUtils;


/**
 * master选举，每个客户端同时向zookeeper发起同一节点的创建请求，只有一个客户端可以创建成功，成为master执行任务
 * 功能类似于乐观锁，它是非阻塞的
 * @author shenzhanwang
 *
 */
public class MasterSelect {
	// 选举的根节点
	static String master_path = "/curator_recipes_master_path";
	
    public static void main( String[] args ) throws Exception {

		List<LeaderSelector> selectors = new ArrayList<>();
		List<CuratorFramework> clients = new ArrayList<>();
		try {
			// 创建十个客户端同时进行leader选举
			for (int i = 0; i < 10; i++) {
				CuratorFramework client = getClient();
				clients.add(client);

				final String name = "client#" + i;
				LeaderSelector leaderSelector = new LeaderSelector(client, master_path, new LeaderSelectorListener() {
					@Override
					public void takeLeadership(CuratorFramework client) throws Exception {
						// 获得leader权立即被调用，执行一段业务逻辑，然后马上放弃leader权
						System.out.println(name + ":I am leader.");
						Thread.sleep(2000);
					}

					@Override
					public void stateChanged(CuratorFramework client, ConnectionState newState) {

					}
				});
				// autoRequeue()方法的调用确保此实例在释放领导权后还可能获得领导权。
				leaderSelector.autoRequeue();
				leaderSelector.start();
				selectors.add(leaderSelector);

			}
			Thread.sleep(Integer.MAX_VALUE);
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			for (CuratorFramework client : clients) {
				CloseableUtils.closeQuietly(client);
			}

			for (LeaderSelector selector : selectors) {
				CloseableUtils.closeQuietly(selector);
			}

		}
	}

	private static CuratorFramework getClient() {
		RetryPolicy retryPolicy = new ExponentialBackoffRetry(1000, 3);
		CuratorFramework client = CuratorFrameworkFactory.builder().connectString("192.168.197.128:2181")
				.retryPolicy(retryPolicy).sessionTimeoutMs(6000).connectionTimeoutMs(3000).namespace("wsz").build();
		client.start();
		return client;
	}
}