package com.machine.dataset;

import java.util.LinkedList;

import javax.swing.JPanel;

import com.machine.window.Adaboost;

public class Utildata {
	
	public static boolean isset = false;
	
	public static Adaboost adaboost = new Adaboost();
	
	public static JPanel[] classes = {adaboost.jpanel1,adaboost.jpanel2};

	public static String[] type = {"所有","基本","分类","预测","聚类","关联分析"};
	public static String[][] label = {{"平均值","方差","标准差","最小值","最大值","K近邻(KNN)","决策树(tree)","贝叶斯-二分类（bayes)","贝叶斯-多分类(bayes)"
			                   ,"logistic(梯度上升优化)","logistic(随即梯度上升)","logistic(优化随即梯度)","支持向量机(MLIA)","支持向量机(SMO)","自适应Boosting(adaBoosting)"
			                   ,"线性回归(标准回归)","线性回归(局部加权)","线性回归(岭回归)","线性回归(前向逐步)","树回归(回归树)","树回归(模型树)","K-均值(kmans)"
			                   ,"Apriori","FP-树"},{"平均值","方差","标准差","最小值","最大值"},{"K近邻(KNN)","决策树(tree)","贝叶斯-二分类（bayes)","贝叶斯-多分类(bayes)"
			                	   ,"logistic(梯度上升优化)","logistic(随机梯度上升)","logistic(优化随机梯度)","支持向量机(MLIA)","支持向量机(SMO)","自适应Boosting(adaBoosting)"
			                	   },{"线性回归(标准回归)","线性回归(局部加权)","线性回归(岭回归)","线性回归(前向逐步)","树回归(回归树)","树回归(模型树)"}
			                	   ,{"K-均值(kmans)"},{"Apriori","FP-树"}};
	public static String[] label1 = {"平均值","方差","标准差","最小值","最大值","K近邻(KNN)","决策树(tree)","贝叶斯-二分类（bayes)","贝叶斯-多分类(bayes)"
            ,"logistic(梯度上升优化)","logistic(随机梯度上升)","logistic(优化随机梯度)","支持向量机(MLIA)","支持向量机(SMO)","自适应Boosting(adaBoosting)"
            ,"线性回归(标准回归)","线性回归(局部加权)","线性回归(岭回归)","线性回归(前向逐步)","树回归(回归树)","树回归(模型树)","K-均值(kmans)"
            ,"Apriori","FP-树"};
	
	public static int[] type0_1 = {0,1,2,3,4,7,8,14,15,16,17,21,22,18,23};
    public static int[] type0_2 = {5,6,9,10,11,12,13,20,19};
    public static int[] type1_1 = {0,1,2,3,4};
    public static int[] type2_1 = {2,3};
    public static int[] type2_2 = {0,1,4,5,6,7,8,9};
    public static int[] type3_1 = {0,1,2,3};
    public static int[] type3_2 = {4,5};
    public static int[] type4_1 = {0};
    public static int[] type5_1 = {0,1};
    public static LinkedList<Integer> list0_1 = new LinkedList<Integer>();
    public static LinkedList<Integer> list0_2 = new LinkedList<Integer>();
    public static LinkedList<Integer> list1_1 = new LinkedList<Integer>();
    public static LinkedList<Integer> list2_1 = new LinkedList<Integer>();
    public static LinkedList<Integer> list2_2 = new LinkedList<Integer>();
    public static LinkedList<Integer> list3_1 = new LinkedList<Integer>();
    public static LinkedList<Integer> list3_2 = new LinkedList<Integer>();
    public static LinkedList<Integer> list4_1 = new LinkedList<Integer>();
    public static LinkedList<Integer> list5_1 = new LinkedList<Integer>();
    
    static{
         for(int i = 0; i < type0_1.length;i++){
		list0_1.add(type0_1[i]);
	}
         for(int i = 0; i < type0_2.length;i++){
     		list0_2.add(type0_2[i]);
     	}
         for(int i = 0; i < type1_1.length;i++){
     		list1_1.add(type1_1[i]);
     	}
         for(int i = 0; i < type2_1.length;i++){
     		list2_1.add(type2_1[i]);
     	}
         for(int i = 0; i < type2_2.length;i++){
     		list2_2.add(type2_2[i]);
     	}
         for(int i = 0; i < type3_1.length;i++){
     		list3_1.add(type3_1[i]);
     	}
         for(int i = 0; i < type3_2.length;i++){
     		list3_2.add(type3_2[i]);
     	}
         for(int i = 0; i < type4_1.length;i++){
     		list4_1.add(type4_1[i]);
     	}
         for(int i = 0; i < type5_1.length;i++){
     		list5_1.add(type5_1[i]);
     	}
    }
}
