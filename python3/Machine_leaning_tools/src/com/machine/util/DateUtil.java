package com.machine.util;


	import java.text.ParseException;
	import java.text.SimpleDateFormat;
	import java.util.Calendar;
	import java.util.Date;
	import java.util.Locale;

	public class DateUtil {

		public static String getAfterDay(String date, int num) {
			SimpleDateFormat parser = new SimpleDateFormat("yyyy-MM-dd");
			Date dt = null;
			try {
				dt = parser.parse(date);
			} catch (ParseException e) {
				e.printStackTrace();
			}

			Calendar calendar = Calendar.getInstance();
			calendar.setTime(dt);
			calendar.add(Calendar.DATE, num);
			SimpleDateFormat simpledateformat = new SimpleDateFormat("yyyy-MM-dd",
					Locale.ENGLISH);
			return simpledateformat.format(calendar.getTime());
		}

		public static String getBeforeDate(int num) {
			Calendar calendar = Calendar.getInstance();
			calendar.setTime(new Date());
			calendar.add(Calendar.DATE, -num);
			SimpleDateFormat simpledateformat = new SimpleDateFormat("yyyy-MM-dd",
					Locale.ENGLISH);
			return simpledateformat.format(calendar.getTime());
		}

		public static String getDate() {
			Date dt = new Date();
			long tmLong = dt.getTime();
			return (new java.sql.Date(tmLong)).toString();
		}

		public static String getDateTime() {
			Date dt = new Date();
			Long tmLong = dt.getTime();
			return (new java.sql.Date(tmLong) + " " + (new java.sql.Time(tmLong)))
					.toString();

		}
		
		public static String getTime() {
			Date dt = new Date();
			Long tmLong = dt.getTime();
			return (new java.sql.Time(tmLong))
					.toString();

		}

		public static java.sql.Date getStringToDate(String day) {
			SimpleDateFormat parser = new SimpleDateFormat("yyyy-MM-dd");
			Date dt = new Date();
			try {
				dt = parser.parse(day);
			} catch (ParseException e) {
				e.printStackTrace();
			}
			return (new java.sql.Date(dt.getTime()));
		}
}
