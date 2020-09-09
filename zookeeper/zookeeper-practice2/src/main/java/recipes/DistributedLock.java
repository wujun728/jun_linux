package recipes;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.concurrent.CountDownLatch;

import org.apache.curator.RetryPolicy;
import org.apache.curator.framework.CuratorFramework;
import org.apache.curator.framework.CuratorFrameworkFactory;
import org.apache.curator.framework.recipes.locks.InterProcessMutex;
import org.apache.curator.retry.ExponentialBackoffRetry;

/**
 * curator对分布式锁的实现
 * InterProcessMutex通过在zookeeper的某路径节点下创建临时序列节点来实现分布式锁，
 * 即每个线程（跨进程的线程）获取同一把锁前，都需要在同样的路径下创建一个节点，节点名
 * 字由uuid + 递增序列组成。而通过对比自身的序列数是否在所有子节点的第一位，来判断是
 * 否成功获取到了锁。当获取锁失败时，它会添加watcher来监听前一个节点的变动情况，然后
 * 进行等待状态。直到watcher的事件生效将自己唤醒，或者超时时间异常返回。
 * @author shenzhanwang
 *
 */
public class DistributedLock {
	 private static final String path = "/lock_path";

	    public static void main(String[] args) {

	        CuratorFramework client = getClient();
	        final InterProcessMutex lock = new InterProcessMutex(client, path);
	        // 用于将一组线程放在同一起跑线阻塞，然后同时唤醒竞争锁
	        final CountDownLatch countDownLatch = new CountDownLatch(1);

	        final long startTime = new Date().getTime();
	        for (int i = 0; i < 10; i++) {
	            new Thread(new Runnable() {
	                @Override
	                public void run() {
	                    try {
	                        countDownLatch.await();
	                        lock.acquire();
	                    } catch (Exception e) {
	                        e.printStackTrace();
	                    }

	                    SimpleDateFormat sdf = new SimpleDateFormat("yyyyMMdd HH:mm:ss|SSS");
	                    System.out.println(sdf.format(new Date()));

	                    try {
	                        lock.release();
	                    } catch (Exception e) {
	                        e.printStackTrace();
	                    }
	                    System.out.println("显示此线程大概花费时间（等待+执行）:" + (new Date().getTime() - startTime) + "ms");
	                }
	            }).start();
	        }
	        System.out.println("创建线程花费时间:" + (new Date().getTime() - startTime) + "ms");
	        countDownLatch.countDown();
	    }

	    private static CuratorFramework getClient() {
	        RetryPolicy retryPolicy = new ExponentialBackoffRetry(1000, 3);
	        CuratorFramework client = CuratorFrameworkFactory.builder()
	                .connectString("192.168.197.128:2181")
	                .retryPolicy(retryPolicy)
	                .sessionTimeoutMs(6000)
	                .connectionTimeoutMs(3000)
	                .namespace("demo")
	                .build();
	        client.start();
	        return client;
	    }
}
