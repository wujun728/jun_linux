---
layout: post
title: 定时任务发展史(一)
category: java 
tags: [java]
---

定时任务是互联网行业里最常用的服务之一，本文给大家介绍定时任务在我司的发展历程。

linux系统中一般使用crontab命令来实现，在Java世界里，使用最广泛的就是quartz了。我司使用quartz就已经升级了三代，每一代在上一代系统之上有所优化，写这篇文章一方面介绍一下quartz的使用，另一方面可以根据此项目的变迁反应出我司平台架构升级的一个缩影。

定时任务的使用场景很多，以我们平台来讲：计息，派息、对账等等。

## quartz 介绍

Quartz是个开源的作业调度框架，为在Java应用程序中进行作业调度提供了简单却强大的机制。Quartz允许开发人员根据时间间隔（或天）来调度作业。它实现了作业和触发器的多对多关系，还能把多个作业与不同的触发器关联。Quartz可以集成几乎任何的java应用程序—从小的单片机系统到大型的电子商务系统。Quartz可以执行上千上万的任务调度。

Quartz核心的概念：scheduler任务调度、Job任务、JobDetail任务细节、Trigger触发器

- Scheduler：调度器，调度器接受一组JobDetail+Trigger即可安排一个任务，其中一个JobDetail可以关联多个Trigger  
- Job：Job是任务执行的流程，是一个类  
- JobDetail：JobDetail是Job是实例，是一个对象，包含了该实例的执行计划和所需要的数据  
- Trigger：Trigger是定时器，决定任务何时执行

使用Quartz调度系统的思路就是，首先写一个具体的任务（job），配置任务的触发时间（Trigger），Scheduler很根据JobDetail+Trigger安排去执行此任务。

Quartz 定时器的时间设置

时间的配置如下：<value>0 30 16 * * ?</value> 

时间大小由小到大排列，从秒开始，顺序为 秒，分，时，天，月，年 *为任意 ？为无限制。由此上面所配置的内容就是，在每天的16点30分启动buildSendHtml() 方法

具体时间设定可参考 ：

"0/10 * * * * ?" 每10秒触发  
"0 0 12 * * ?" 每天中午12点触发 
"0 * 14 * * ?" 在每天下午2点到下午2:59期间的每1分钟触发   
"0 10,44 14 ? 3 WED" 每年三月的星期三的下午2:10和2:44触发   
"0 15 10 ? * MON-FRI" 周一至周五的上午10:15触发   
"0 0 06,18 * * ?"  在每天上午6点和下午6点触发 


## 第一代定时任务系统

第一代定时任务系统使用的很简单，全部按照当时spring推荐的配置方式来进行，开发于2014年初。

首先在配置线程池

``` xml
<bean id="executor" class="org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor">
 	<property name="corePoolSize" value="50" />
 	<property name="maxPoolSize" value="100" />
 	<property name="queueCapacity" value="500" />
</bean>
```

配置定时任务工厂和任务基类

``` xml
<bean id="timerFactory" class="com.zx.timer.TimerFactory" />

<bean id="baseTask" class="com.zx.timer.core.BaseTask">
	<property name="machineId" value="${machine.id}"/>
	<property name="recordErrorDetail" value="${is.record.errordetail}"/>
</bean>
```

- machineId：机器编码  
- recordErrorDetail：是否记录详细日志


通过timerFactory 来获取具体的任务和触发器

``` java
public class TimerFactory implements BeanFactoryAware {

	private BeanFactory beanFactory;

	public Object getTask(String taskCode) {
		return beanFactory.getBean(taskCode+"Task");
	}
	
	public Object getTrigger(String taskCode) {
		return beanFactory.getBean(taskCode+"Trigger");
	}

	public void setBeanFactory(BeanFactory beanFactory) {
		this.beanFactory = beanFactory;
	}

	public BeanFactory getBeanFactory() {
		return beanFactory;
	}
}
```

baseTask集成了task，在里面做了一些基础的业务，比如定时任务开始执行的时候记录定时任务的开始执行时间，定时任务结束的时候记录执行的结果等。

``` java
public interface Task {
	public void executeTask();
}
```

配置具体的定时任务。以重发短信邮件的定时任务为例

``` xml
<bean id="resendSmsAndEmailTask" class="com.zx.timer.core.tasks.ResendSmsAndEmailTask"
		parent="baseTask">
</bean>

<bean id="resendSmsAndEmailJob" class="org.springframework.scheduling.quartz.MethodInvokingJobDetailFactoryBean">
	<property name="targetObject" ref="resendSmsAndEmailTask" />
	<property name="targetMethod" value="executeTask" />
	<property name="concurrent" value="false" />
</bean>

<bean id="resendSmsAndEmailTrigger" class="org.springframework.scheduling.quartz.CronTriggerBean">
	<property name="jobDetail" ref="resendSmsAndEmailJob" />
	<property name="cronExpression">
		<value>0 0 0 * * ?</value>
	</property>
</bean>
```

- resendSmsAndEmailTask：具体的定时任务类  
- resendSmsAndEmailJob：包装成具体的Job
- resendSmsAndEmailTrigger：设置具体执行的时间，包装成Trigger

具体的task类,删掉了部分业务代码：

``` java
public class ResendSmsAndEmailTask extends BaseTask{
	private static final String TASK_CODE = "resendSmsAndEmail";
	AtomicInteger ai = new AtomicInteger(0);
	
	public void execute(){
		try {
			ai = new AtomicInteger(0);
			// todo
		}catch (Exception e) {
			String exception = ExceptionUtils.getStackTrace(e);
			logger.error("stat error with exception[{}].", exception);
			this.recordTaskErrorDetail(this.taskRecordId, "ResendSmsAndEmailTask-" + e.getMessage(), exception);
		}finally{
			this.modifyTaskRecord(ai.get(), taskRecordId);
		}
	}
	
	public String getTaskNo() {
		return TASK_CODE;
	}
}
```

最后配置scheduler任务调度

``` xml
<bean id="scheduler" class="org.springframework.scheduling.quartz.SchedulerFactoryBean">
	<property name="triggers">
		<list>
			<ref bean="resendSmsAndEmailTrigger" />
		</list>
	</property>
	<property name="taskExecutor" ref="executor" />
</bean>
<bean class="com.zx.timer.core.scheduler.DynamicJobAssembler" init-method="init" scope="singleton"/>
```

DynamicJobAssembler类代码：


``` java
public class DynamicJobAssembler {

	private static Logger logger = LoggerFactory.getLogger(DynamicJobAssembler.class);

	@Resource
	Scheduler scheduler;

	@Resource
	TimerFactory timerFactory;

	@Resource
	TaskDao taskDao;

	public void init() {
		logger.info("start to assemble task from db.");
		List<TaskEntity> tasks = this.taskDao.getAllTask();
		if (tasks == null || tasks.size() <= 0) {
			return;
		}

		Map<String, String> jobNameMap = this.getAllJobNames();
		for (TaskEntity task : tasks) {
			logger.debug(task.toString());
			CronTriggerBean taskTrigger = (CronTriggerBean) timerFactory.getTrigger(task.getTaskNo());
			if (taskTrigger != null) {
				if (!task.getSchedulerRule().equals(taskTrigger.getCronExpression())) {
					try {
						taskTrigger.setCronExpression(task.getSchedulerRule());
					} catch (ParseException e) {
						logger.error("db task's cronExpression parse error:{}", e.getMessage());
					}
					try {
						logger.info("rescheduleJob jobName:{}",task.getTaskNo());
						scheduler.rescheduleJob(task.getTaskNo() + "Trigger", Scheduler.DEFAULT_GROUP, taskTrigger);
					} catch (SchedulerException e) {
						logger.error("revieved task[{},{}] reschedule error:{}", task.getTaskNo(), task.getSchedulerRule(), e.getMessage());
					}
				}
				jobNameMap.remove(task.getTaskNo() + "Job");
			}
		}

		if (jobNameMap != null) {
			logger.info("=====================================");
			logger.info("Jobs need to be removed:" + Arrays.toString(jobNameMap.keySet().toArray()));
			logger.info("=====================================");
			for (String jobName : jobNameMap.keySet()) {
				try {
					scheduler.deleteJob(jobName, jobNameMap.get(jobName));
				} catch (SchedulerException e) {
					logger.error("Error occured when deleting Job[{}] with Exception:{}", jobName, e.getMessage());
				}
			}
		}
		logger.info("end to assemble task from db.");
	}

	private Map<String, String> getAllJobNames() {
		Map<String, String> jobNameMap = new HashMap<String, String>();
		try {
			String[] groups = scheduler.getJobGroupNames();
			for (String group : groups) {
				String[] jobs = scheduler.getJobNames(group);
				if (jobs != null) {
					for (String job : jobs) {
						jobNameMap.put(job, group);
					}
				}
			}
		} catch (SchedulerException e1) {
			logger.error("Failed in geting all job names with exception:{}", e1.getMessage());
		}
		return jobNameMap;
	}

}
```

定时任务表，执行的时候以表里面的数据为准，方便编辑。

``` sql
SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `zx_task_informations`
-- ----------------------------
DROP TABLE IF EXISTS `zx_task_informations`;
CREATE TABLE `zx_task_informations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `version` int(11) NOT NULL COMMENT '版本号：需要乐观锁控制',
  `taskNo` varchar(64) NOT NULL COMMENT '任务编号',
  `taskName` varchar(64) NOT NULL COMMENT '任务名称',
  `schedulerRule` varchar(64) NOT NULL COMMENT '定时规则表达式',
  `frozenStatus` varchar(16) NOT NULL COMMENT '冻结状态',
  `executorNo` varchar(128) NOT NULL COMMENT '执行方',
  `timeKey` varchar(32) NOT NULL COMMENT '执行时间格式',
  `frozenTime` bigint(13) DEFAULT NULL COMMENT '冻结时间',
  `unfrozenTime` bigint(13) DEFAULT NULL COMMENT '解冻时间',
  `createTime` bigint(13) NOT NULL COMMENT '创建时间',
  `lastModifyTime` bigint(13) DEFAULT NULL COMMENT '最近修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8 COMMENT='定时任务信息表';

-- ----------------------------
-- Records of zx_task_informations
-- ----------------------------
INSERT INTO `zx_task_informations` VALUES ('1', '0', 'resendSmsAndEmail', '重发短信和邮件', '10 */10 * * * ?', 'FROZEN', '0', 'yyyy-MM-dd HH:mm', '0', '0', '0', '1486807296009');
```

这就是我们第一代定时任务系统，达到了定期执行定时任务的效果，但是同样有两个缺点：

- 1、定时调度和业务代码耦合在一起
- 2、每次调整定时任务的时间需要重启服务

