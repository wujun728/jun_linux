package com.chitry.test;

import org.apache.log4j.Logger;

/**
 * @author chitry@126.com
 * @date   2016年9月28日 上午11:39:07
 * @topic  测试log打印
 * @description TODO
 *
 */
public class TestLog {
	
	private static Logger log = Logger.getLogger(TestLog.class);

	public static void main(String[] args){
		// 记录debug级别的信息  
		log.debug("This is debug message.");  
        // 记录info级别的信息  
		log.info("This is info message.");  
        // 记录error级别的信息  
		log.error("This is error message.");  
	}
}
