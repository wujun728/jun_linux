package com.machine.util;

import com.machine.dataset.Pythondata;



public class Choosepython {

	public static String[] choosepre(int lei,int suanfa){
			if(lei==0&&suanfa==0||lei==1&&suanfa==0){
				String[] meancommand = {"python","mean.py",Pythondata.trainfile,String.valueOf(Pythondata.n),Pythondata.splittype};
				return meancommand;
			}
			else if(lei==0&&suanfa==1||lei==1&&suanfa==1){
				String[] avercommand = {"python","average.py",Pythondata.trainfile,String.valueOf(Pythondata.n),Pythondata.splittype};
				return avercommand;
			}
			else if(lei==0&&suanfa==2||lei==1&&suanfa==2){
				String[] stdaommand = {"python","std.py",Pythondata.trainfile,String.valueOf(Pythondata.n),Pythondata.splittype};
				return stdaommand;
			}
			else if(lei==0&&suanfa==3||lei==1&&suanfa==3){
				String[] mincommand = {"python","min.py",Pythondata.trainfile,String.valueOf(Pythondata.n),Pythondata.splittype};
			    return mincommand;
			}
			else if(lei==0&&suanfa==4||lei==1&&suanfa==4){
				String[] maxcommand = {"python","max.py",Pythondata.trainfile,String.valueOf(Pythondata.n),Pythondata.splittype};
				return maxcommand;
			}
			else if(lei==0&&suanfa==5||lei==2&&suanfa==0){
				String[] knncommandpre = {"python","KNN.py",Pythondata.trainfile,Pythondata.testfile,Pythondata.outfile,String.valueOf(Pythondata.knn),Pythondata.splittype};
				return knncommandpre;
			}
			else if(lei==0&&suanfa==6||lei==2&&suanfa==1){
				String[] treecommandpre = {"python","tree.py",Pythondata.trainfile,Pythondata.testfile,Pythondata.outfile,Pythondata.modelfile,Pythondata.splittype};
                return treecommandpre;
			}
			else if(lei==0&&suanfa==7||lei==2&&suanfa==2){
				String[] bayetwocommand = {"python","bayes_two.py",Pythondata.trainfile,Pythondata.testfile,Pythondata.outfile};
                return bayetwocommand;
			}
			else if(lei==0&&suanfa==8||lei==2&&suanfa==3){
				String[] bayemorecommand = {"python","bayes_more.py",Pythondata.trainfile,Pythondata.testfile,Pythondata.outfile};
                return bayemorecommand;
			}
			else if(lei==0&&suanfa==9||lei==2&&suanfa==4){
				String[] loggradcommandpre = {"python","logistic.py","grad",Pythondata.trainfile,Pythondata.testfile,Pythondata.outfile,String.valueOf(Pythondata.numiter),Pythondata.splittype};
                return loggradcommandpre;
			}
			else if(lei==0&&suanfa==10||lei==2&&suanfa==5){
				String[] logtoccommandpre = {"python","logistic.py","toc",Pythondata.trainfile,Pythondata.testfile,Pythondata.outfile,Pythondata.splittype};
                return logtoccommandpre;
			}
			else if(lei==0&&suanfa==11||lei==2&&suanfa==6){
			 String[] logstoccommandpre = {"python","logistic.py","stoc",Pythondata.trainfile,Pythondata.testfile,Pythondata.outfile,String.valueOf(Pythondata.numiter),Pythondata.splittype};
                  return logstoccommandpre;
			}
			else if(lei==0&&suanfa==12||lei==2&&suanfa==7){
				String[] mliacommandpre = {"python","MLIA.py",Pythondata.trainfile,Pythondata.testfile,Pythondata.outfile,String.valueOf(Pythondata.C),String.valueOf(Pythondata.toler),String.valueOf(Pythondata.maxIter),String.valueOf(Pythondata.k1),Pythondata.splittype};
                return mliacommandpre;
			}
			else if(lei==0&&suanfa==13||lei==2&&suanfa==8){
				String[] smocommandpre = {"python","SMO.py",Pythondata.trainfile,Pythondata.testfile,Pythondata.outfile,String.valueOf(Pythondata.C),String.valueOf(Pythondata.toler),String.valueOf(Pythondata.maxIter),Pythondata.splittype};
                return smocommandpre;
			}
			else if(lei==0&&suanfa==14||lei==2&&suanfa==9){
				String[] adacommandpre = {"python","adaBoost.py",Pythondata.trainfile,Pythondata.testfile,Pythondata.outfile,String.valueOf(Pythondata.numiter),Pythondata.splittype};
                return adacommandpre;
			}
			else if(lei==0&&suanfa==15||lei==3&&suanfa==0){
				String[] standcommand = {"python","stand.py",Pythondata.trainfile,Pythondata.testfile,Pythondata.outfile,Pythondata.splittype};
				return standcommand;
			}
			else if(lei==0&&suanfa==16||lei==3&&suanfa==1){
				String[] lwlrcommand = {"python","lwlr.py",Pythondata.trainfile,Pythondata.testfile,Pythondata.outfile,String.valueOf(Pythondata.lowspeed),Pythondata.splittype};
				return lwlrcommand;
			}
			else if(lei==0&&suanfa==17||lei==3&&suanfa==2){
				String[] ridgecommand = {"python","ridge.py",Pythondata.trainfile,Pythondata.testfile,Pythondata.outfile,String.valueOf(Pythondata.numiter),String.valueOf(Pythondata.lamnum),Pythondata.splittype};
				return ridgecommand;
			}
			else if(lei==0&&suanfa==18||lei==3&&suanfa==3){
				String[] stagecommand = {"python","stage.py",Pythondata.trainfile,Pythondata.testfile,Pythondata.outfile,String.valueOf(Pythondata.eps),String.valueOf(Pythondata.numiter),Pythondata.splittype};
				return stagecommand;
			}
			else if(lei==0&&suanfa==19||lei==3&&suanfa==4){
				String[] regtreecommandpre = {"python","regtree.py",Pythondata.trainfile,Pythondata.testfile,Pythondata.outfile,String.valueOf(Pythondata.tols),String.valueOf(Pythondata.toln),Pythondata.splittype};
				return regtreecommandpre;
			}
			else if(lei==0&&suanfa==20||lei==3&&suanfa==5){
				String[] modeltreecommandpre = {"python","modeltree.py",Pythondata.trainfile,Pythondata.testfile,Pythondata.outfile,String.valueOf(Pythondata.tols),String.valueOf(Pythondata.toln),Pythondata.splittype};
				return modeltreecommandpre;
			}
			else if(lei==0&&suanfa==21||lei==4&&suanfa==0){
				String[] kmeanscommand =  {"python","kmeans.py",Pythondata.testfile,Pythondata.outfile,String.valueOf(Pythondata.k),Pythondata.splittype};
				return kmeanscommand;
			}
			else if(lei==0&&suanfa==22||lei==4&&suanfa==0){
				String[] aprcommand = {"python","apriori.py",Pythondata.testfile,Pythondata.outfile,String.valueOf(Pythondata.minsupport),String.valueOf(Pythondata.minconf),Pythondata.splittype};
				return aprcommand;
			}
			else if(lei==0&&suanfa==23||lei==4&&suanfa==1){
				String[] fpcommand =  {"python","FP.py",Pythondata.testfile,Pythondata.outfile,String.valueOf(Pythondata.minsupport),Pythondata.splittype};
				return fpcommand;
			}
			else
				return null;
	}
	public static String[] choosetest(int lei,int suanfa){
		if(lei==0&&suanfa==5||lei==2&&suanfa==0){
			String[] knncommandtest = {"python","KNN.py",Pythondata.trainfile,String.valueOf(Pythondata.knn),Pythondata.splittype};
			return knncommandtest;
		}
		else if(lei==0&&suanfa==6||lei==2&&suanfa==1){
			String[] treecommandtest = {"python","tree.py",Pythondata.trainfile,Pythondata.modelfile,Pythondata.splittype};
			return treecommandtest;
		}
		else if(lei==0&&suanfa==9||lei==2&&suanfa==4){
			String[] loggradcommandtest = {"python","logistic.py","grad",Pythondata.trainfile,String.valueOf(Pythondata.numiter),Pythondata.splittype};
			return loggradcommandtest;
		}
		else if(lei==0&&suanfa==10||lei==2&&suanfa==5){
			String[] logtoccommandtest = {"python","logistic.py","toc",Pythondata.trainfile,Pythondata.splittype};
			return logtoccommandtest;
		}
		else if(lei==0&&suanfa==11||lei==2&&suanfa==6){
		String[] logstoccommandtest = {"python","logistic.py","stoc",Pythondata.trainfile,String.valueOf(Pythondata.numiter),Pythondata.splittype};
		return logstoccommandtest;
		}
		else if(lei==0&&suanfa==12||lei==2&&suanfa==7){
			String[] mliacommandtest = {"python","MLIA.py",Pythondata.trainfile,String.valueOf(Pythondata.C),String.valueOf(Pythondata.toler),String.valueOf(Pythondata.maxIter),String.valueOf(Pythondata.k1),Pythondata.splittype};
			return mliacommandtest;
		}
		else if(lei==0&&suanfa==13||lei==2&&suanfa==8){
			String[] smocommandtest = {"python","SMO.py",Pythondata.trainfile,String.valueOf(Pythondata.C),String.valueOf(Pythondata.toler),String.valueOf(Pythondata.maxIter),Pythondata.splittype};
			return smocommandtest;
		}
		else if(lei==0&&suanfa==14||lei==2&&suanfa==9){
			String[] adacommandtest = {"python","adaBoost.py",Pythondata.trainfile,String.valueOf(Pythondata.numiter),Pythondata.splittype};
			return adacommandtest;
		}
		else if(lei==0&&suanfa==19||lei==3&&suanfa==4){
			String[] regtreecommandtest = {"python","regtree.py",Pythondata.trainfile,String.valueOf(Pythondata.tols),String.valueOf(Pythondata.toln),Pythondata.splittype};
			return regtreecommandtest;
		}
		else if(lei==0&&suanfa==20||lei==3&&suanfa==5){
			String[] modeltreecommandtest = {"python","modeltree.py",Pythondata.trainfile,String.valueOf(Pythondata.tols),String.valueOf(Pythondata.toln),Pythondata.splittype};
			return modeltreecommandtest;
		}
		else
			return null;
	}
}
