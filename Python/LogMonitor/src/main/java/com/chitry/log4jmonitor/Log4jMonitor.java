package com.chitry.log4jmonitor;

import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.AsyncContext;
import javax.servlet.AsyncEvent;
import javax.servlet.AsyncListener;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.log4j.Logger;

import com.chitry.log4jmonitor.core.Log4jAsyncWriter;

/**
 * @author chitry@126.com
 * @date   2016年9月28日 上午11:36:34
 * @topic  异步获取log日志信息
 * @description TODO
 *
 */
@SuppressWarnings("serial")
@WebServlet(urlPatterns = { "/log4jmonitor" }, asyncSupported = true)
public class Log4jMonitor extends HttpServlet {

	private static Logger log = Logger.getLogger(Log4jMonitor.class);
	
	/**
	 * 注册 监听Logger的消息队列
	 */
	@Override
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		response.setContentType("text/html;charset=UTF-8");
		response.setHeader("Cache-Control", "private");
		response.setHeader("Pragma", "no-cache");
		response.setCharacterEncoding("UTF-8");
		PrintWriter writer = response.getWriter();
		writer.println("<!-- author by chitry@126.com -->\n");
		writer.flush();

		final AsyncContext ac = request.startAsync();
		ac.setTimeout(1 * 60 * 60 * 1000);//1小时
		ac.addListener(new AsyncListener() {
			public void onComplete(AsyncEvent event) throws IOException {
				ac.getResponse().getWriter().close();
				Log4jAsyncWriter.deleteAc(ac);
				log.info("AsyncListener onComplete");
			}

			public void onTimeout(AsyncEvent event) throws IOException {
				ac.getResponse().getWriter().close();
				Log4jAsyncWriter.deleteAc(ac);
				log.info("AsyncListener onTimeout");
			}

			public void onError(AsyncEvent event) throws IOException {
				ac.getResponse().getWriter().close();
				Log4jAsyncWriter.deleteAc(ac);
				log.info("AsyncListener onError");
			}

			public void onStartAsync(AsyncEvent event) throws IOException {
				log.info("AsyncListener onStartAsync");
			}
		});
		Log4jAsyncWriter.addAc(ac);
	}
	
	@Override
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		this.doGet(request, response);
	}
}
