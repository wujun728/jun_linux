---
layout: post
title: 定时任务发展史(二)
category: java 
tags: [java]
---

第一代定时任务系统上线用了大概半年之后，就被我们厌倦了。于是就规划了第二代定时任务系统。


## 第二代定时任务系统

第二代调度系统主要解决的是，避免每次修改定时任务的执行时间都需要重新启动整个项目。另外也可支持单独重新调度单个定时任务。

我们做了一个请求入口，当更新了库表里面的数据之后，重新请求一下特定的url就会自动重新加载定时任务。

使用scheduler删除定时任务

``` java
public void reScheduler() throws Exception {
	// 取消现有的任务
	String[] jobNames = quartzUtil.getJobNames();
	if (null != jobNames && jobNames.length > 0) {
		for (String jobName : jobNames) {
			logger.info("----开始移除任务:" + jobName);
			quartzUtil.cancelJob(jobName);
			logger.info("----成功移除任务:" + jobName);
		}
	}
	logger.info("现有任务已全部取消");
	this.initScheduler();
}
```

``` java
public void cancelJob(String jobName) throws Exception {
	scheduler.pauseTrigger(jobName, Scheduler.DEFAULT_GROUP);
	scheduler.unscheduleJob(jobName, Scheduler.DEFAULT_GROUP);
	scheduler.deleteJob(jobName, Scheduler.DEFAULT_GROUP);
}
```


使用scheduler重新加载所有的定时任务。

``` java
job.setCronExpression(taskInfo.getSchedulerRule());
String jobName = taskInfo.getTaskNo() + "Job";
job.getJobDataMap().put(QuartzJob.OBJECT_ID,objectMethod);
job.setJobName(jobName);
logger.info("----开始部署任务:" + jobName);
quartzUtil.scheduleCronJob(job);
logger.info("----成功部署任务:" + jobName);
```

``` java
public void scheduleCronJob(QuartzJobEntity jobEntity) throws Exception {
	JobDetailBean jobDetail = createJobDetail(jobEntity);
	scheduler.addJob(jobDetail, true);
	CronTriggerBean trigger = new CronTriggerBean();
	trigger.setCronExpression(jobEntity.getCronExpression());
	trigger.setJobDetail(jobDetail);
	trigger.setName(jobEntity.getJobName());
	trigger.setJobName(jobDetail.getName());
	scheduler.scheduleJob(trigger);
}
```

如果只是重新调度某一个定时任务可以触发单独的调用

``` java
// 初始化某个加载定时任务
public void initScheduler(TaskEntity taskInfo) throws Exception {
	// 设置任务信息到quartz,并调度任务
	QuartzJobEntity job = new QuartzJobEntity();
	String objectName = taskInfo.getTaskNo()+"Task";
	String objectMethod = "executeTask";
	job.getJobDataMap().put(QuartzJob.OBJECT_NAME,objectName);
	job.getJobDataMap().put(QuartzJob.OBJECT_METHOD,objectMethod);
	// 单线程方式执行任务
	job.setJobClass(QuartzJob.class);
	job.setCronExpression(taskInfo.getSchedulerRule());
	String jobName = taskInfo.getTaskNo() + "Job";
	job.getJobDataMap().put(QuartzJob.OBJECT_ID,objectMethod);
	job.setJobName(jobName);
	logger.info("----开始部署任务:" + jobName);
	quartzUtil.scheduleCronJob(job);
	logger.info("----成功部署任务:" + jobName);
}
```


这样我们的第二代定时任务系统就完成了，第二代定时任务是在第一代定时任务的基础上改造的，增加了重新调度所有定时任务和单个定时任务。

> 第二代定时任务系统的缺点是：定时调度和业务代码耦合


## 第三代定时任务系统

第二代定时任务上线没有多久，我们就意识到有很多的子系统也需要定时任务，比如订单系统需要45分钟不支付的订单失效，监控系统需要定时扫描是否有业务报警，统计系统需要定时去统计一些数据，但是如果我们给每一个子系统都做一个定时任务的话，就不太合理，很分散。

于是计划开发一个统一的定时任务调度中心，负责整个平台中所有的定时任务的调度，另外规划了监控系统，来监控和分析每次定时任务的执行结果和执行时间等信息。为了更好的管理定时任务开发了简单的管理界面。如下：

 
![](http://www.itmind.net/assets/images/2017/quartz-01.png)

根据上图可以看出，通过这个管理界面我们可以非常方便的去修改、启动、暂停定时任务。别的系统如果需要定时任务，可以随时在页面去添加，全部界面化操作，不需要重新启动项目等。

点击详情可以清晰的查看定时任务的上次执行情况

 
![](http://www.itmind.net/assets/images/2017/quartz-02.png)


定时任务的支持的调度方式分有两种：http和mq，我们一般建议使用mq。

- http :使用http一般适用于用时特别少的定时任务。或者接收请求之后立刻返回结果，重新启动另外一个线程去执行具体的业务，业务执行完成之后在通过http回调返回执行结果。

- mq :使用mq的话，调度系统和业务系统的交互就完全异步来执行，调度系统定时触发后，发送MQ消息给业务系统，业务系统接收到消息开始执行业务，执行完毕之后，再发送MQ系统通知调度系统的执行结果。


**主要核心代码**

初始化加载

``` java
public void initScheduler(){
	List<TaskInformationsEntity> taskList = taskInformationsDao.getTaskList();
	Scheduler scheduler = schedulerBean.getScheduler();
	for(TaskInformationsEntity task : taskList){
		try {
			this.scheduler(task, scheduler);
		} catch (Exception e) {
			logger.error("定时：" + task.getTaskNo() + "启动失败");
		}
	}
}
```

遍历调度

``` java
public void scheduler(TaskInformationsEntity task,Scheduler scheduler){
	TriggerKey triggerKey = TriggerKey.triggerKey(task.getTaskNo(), Scheduler.DEFAULT_GROUP);
	JobDetail jobDetail = JobBuilder.newJob(QuartzJobFactory.class).withDescription(task.getTaskName()).withIdentity(task.getTaskNo(), Scheduler.DEFAULT_GROUP).build();
	jobDetail.getJobDataMap().put("targetObjectId", task.getTaskNo());
	jobDetail.getJobDataMap().put("executorNo", task.getExecutorNo());
	jobDetail.getJobDataMap().put("sendType", task.getSendType());
	jobDetail.getJobDataMap().put("url", task.getUrl());
	jobDetail.getJobDataMap().put("executeParamter", task.getExecuteParamter());
	CronScheduleBuilder scheduleBuilder = CronScheduleBuilder.cronSchedule(task.getSchedulerRule());
	CronTrigger trigger = TriggerBuilder.newTrigger().withIdentity(triggerKey).withSchedule(scheduleBuilder).build();
	try {
		scheduler.scheduleJob(jobDetail, trigger);
		logger.info("task "+task.getTaskNo()+" schedulerRule :"+task.getSchedulerRule()+" reload succeed");
	} catch (Exception e) {
		logger.error("scheduler--异常：",e);
		throw new RuntimeException();
	}
}
```

添加定时任务

``` java
public String addScheduler(String key){
	TaskInformationsEntity entity = taskInformationsDao.getTaskByTaskNo(key);
	if(null != entity){
		Scheduler scheduler = schedulerBean.getScheduler();
		try {
			scheduler.deleteJob(new JobKey(key));
			this.scheduler(entity, scheduler);
			entity.setFrozenStatus(TaskStatusEnum.UNFROZEN);
			entity.setUnfrozenTime(DateUtil.getLastModifyTime());
			entity.setLastModifyTime(DateUtil.getLastModifyTime());
			taskInformationsDao.updateById(entity);
			return "任务启动成功";
		} catch (Exception e) {
			logger.info("异常：",e);
			return "任务启动失败";
		}
	}else{
		return "该任务编号不存在";
	}
}
```


删除定时任务

``` java
public String delScheduler(String key){
	TaskInformationsEntity entity = taskInformationsDao.getTaskByTaskNo(key);
	if(null != entity && TaskStatusEnum.UNFROZEN == entity.getFrozenStatus()){
		Scheduler scheduler = schedulerBean.getScheduler();
		try {
			scheduler.deleteJob(new JobKey(key));
			entity.setFrozenStatus(TaskStatusEnum.FROZEN);
			entity.setFrozenTime(DateUtil.getLastModifyTime());
			entity.setLastModifyTime(DateUtil.getLastModifyTime());
			taskInformationsDao.updateById(entity);
			return "暂停任务成功";
		} catch (Exception e) {
			logger.error("异常：",e);
			return "暂停任务异常";
		}
	}else{
		return "该任务编号不存在";
	}
}
```



重新加载定时任务

``` java
public String resumeScheduler(String key){
	TaskInformationsEntity entity = taskInformationsDao.getTaskByTaskNo(key);
	if(null != entity){
		Scheduler scheduler = schedulerBean.getScheduler();
		try {
			scheduler.deleteJob(new JobKey(key));
			this.scheduler(entity, scheduler);
			return "重启成功";
		} catch (SchedulerException e) {
			logger.info("异常：",e);
			return "重启异常";
		}
	}else{
		return "该任务编号不存在";
	}
}
```

项目已经开源,详细的代码请在github上面查看。

[zx-quartz](https://github.com/justdojava/zx-quartz)


其实最后这版定时调度系统，还是有很多的缺陷，http模式没有进行完善，开源的代码中有部分内部依赖的jar还没有去掉。开放出来仅仅做为交流使用，后期有时间的话再去慢慢完善。也欢迎各网友多提提建议，一起加入完善。