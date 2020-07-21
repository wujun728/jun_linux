package com.machine.dataset;

public class Pythondata {

	public static String trainfile = new String();//训练数据
	public static String testfile = new String();//测试数据
	public static String outfile = new String();//输出数据
	public static String modelfile = new String();//模型
	public static int numiter;//迭代次数
	public static String splittype = new String();//分割符
	public static float minsupport;//最小支持度
	public static float minconf;//最小可信度
	public static int n;//列索引
	public static int k;//聚类中心个数
	public static int knn;//距离预测点最近的个数
	public static float lowspeed;//衰减速度
	public static float C;//常数边界C
	public static float toler;//容错率
	public static float maxIter;//退出前最大循环次数
	public static float k1;//高斯径向基函数用户定义变量
	public static int tols;//容许误差下降值
	public static int toln;//切分的最少样本数
	public static int lamnum;//步长的个数
	public static float eps;//步长
	//public static String[] meancommand = null;
	public static String[] meancommand = {"python","mean.py",trainfile,String.valueOf(n),splittype};
	public static String[] avercommand = {"python","average.py",trainfile,String.valueOf(n),splittype};
	public static String[] stdaommand = {"python","std.py",trainfile,String.valueOf(n),splittype};
	public static String[] maxcommand = {"python","max.py",trainfile,String.valueOf(n),splittype};
	public static String[] mincommand = {"python","min.py",trainfile,String.valueOf(n),splittype};
	public static String[] knncommandtest = {"python","KNN.py",trainfile,String.valueOf(knn),splittype};
	public static String[] knncommandpre = {"python","KNN.py",trainfile,testfile,outfile,String.valueOf(knn),splittype};
	public static String[] treecommandtest = {"python","tree.py",trainfile,modelfile,splittype};
	public static String[] treecommandpre = {"python","tree.py",trainfile,testfile,outfile,modelfile,splittype};
	public static String[] bayetwocommand = {"python","bayes_two.py",trainfile,testfile,outfile};
	public static String[] bayemorecommand = {"python","bayes_more.py",trainfile,testfile,outfile};
	public static String[] loggradcommandtest = {"python","logistic.py","grad",trainfile,String.valueOf(numiter),splittype};
	public static String[] loggradcommandpre = {"python","logistic.py","grad",trainfile,testfile,outfile,String.valueOf(numiter),splittype};
	public static String[] logtoccommandtest = {"python","logistic.py","toc",trainfile,String.valueOf(numiter),splittype};
	public static String[] logtoccommandpre = {"python","logistic.py","toc",trainfile,testfile,outfile,String.valueOf(numiter),splittype};
	public static String[] logstoccommandtest = {"python","logistic.py","stoc",trainfile,splittype};
	public static String[] logstoccommandpre = {"python","logistic.py","stoc",trainfile,testfile,outfile,splittype};
	public static String[] smocommandtest = {"python","SMO.py",trainfile,String.valueOf(C),String.valueOf(toler),String.valueOf(maxIter),splittype};
	public static String[] smocommandpre = {"python","SMO.py",trainfile,testfile,outfile,String.valueOf(C),String.valueOf(toler),String.valueOf(maxIter),splittype};
	public static String[] mliacommandtest = {"python","MLIA.py",trainfile,String.valueOf(C),String.valueOf(toler),String.valueOf(maxIter),String.valueOf(k1),splittype};
	public static String[] mliacommandpre = {"python","MLIA.py",trainfile,testfile,outfile,String.valueOf(C),String.valueOf(toler),String.valueOf(maxIter),String.valueOf(k1),splittype};
	public static String[] adacommandtest = {"python","adaBoost.py",trainfile,String.valueOf(numiter),splittype};
	public static String[] adacommandpre = {"python","adaBoost.py",trainfile,testfile,outfile,String.valueOf(numiter),splittype};
	public static String[] standcommand = {"python","stand.py",trainfile,testfile,outfile,splittype};
	public static String[] lwlrcommand = {"python","lwlr.py",trainfile,testfile,outfile,String.valueOf(lowspeed),splittype};
	public static String[] ridgecommand = {"python","ridge.py",trainfile,testfile,outfile,String.valueOf(numiter),String.valueOf(lamnum),splittype};
	public static String[] stagecommand = {"python","stage.py",trainfile,testfile,outfile,String.valueOf(eps),String.valueOf(numiter),splittype};
	public static String[] regtreecommandtest = {"python","regtree.py",trainfile,String.valueOf(tols),String.valueOf(toln),splittype};
	public static String[] regtreecommandpre = {"python","regtree.py",trainfile,testfile,outfile,String.valueOf(tols),String.valueOf(toln),splittype};
	public static String[] modeltreecommandtest = {"python","modeltree.py",trainfile,String.valueOf(tols),String.valueOf(toln),splittype};
	public static String[] modeltreecommandpre = {"python","modeltree.py",trainfile,testfile,outfile,String.valueOf(tols),String.valueOf(toln),splittype};
	public static String[] aprcommand = {"python","apriori.py",testfile,outfile,String.valueOf(minsupport),String.valueOf(minconf),splittype};
	public static String[] kmeanscommand =  {"python","kmeans.py",testfile,outfile,String.valueOf(k),splittype};
	public static String[] fpcommand =  {"python","FP.py",testfile,outfile,String.valueOf(minsupport),splittype};

	}
	
	
	
