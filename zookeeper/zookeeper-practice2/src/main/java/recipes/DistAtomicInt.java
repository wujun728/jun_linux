package recipes;
import org.apache.curator.framework.CuratorFramework;
import org.apache.curator.framework.CuratorFrameworkFactory;
import org.apache.curator.framework.recipes.atomic.AtomicValue;
import org.apache.curator.framework.recipes.atomic.DistributedAtomicInteger;
import org.apache.curator.retry.ExponentialBackoffRetry;
import org.apache.curator.retry.RetryNTimes;

/**
 * 使用Curator实现分布式计数器
 * 把计数结果写入某个节点中，在分布式环境下做原子化的叠加
 * @author shenzhanwang
 *
 */

public class DistAtomicInt {

	static String distatomicint_path = "/curator_recipes_distatomicint_path";
    static CuratorFramework client = CuratorFrameworkFactory.builder()
            .connectString("192.168.197.128:2181")
            .retryPolicy(new ExponentialBackoffRetry(1000, 3)).build();
	public static void main( String[] args ) throws Exception {
		client.start();
		DistributedAtomicInteger atomicInteger = 
		new DistributedAtomicInteger( client, distatomicint_path, 
									new RetryNTimes( 3, 1000 ) );
		AtomicValue<Integer> rc = atomicInteger.add( 8 );
		System.out.println( "Result: " + rc.postValue() );
		System.out.println( "Result: " + rc.preValue() );
	}
}