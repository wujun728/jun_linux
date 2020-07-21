# 员工离职预测

数据主要包括影响员工离职的各种因素（工资、出差、工作环境满意度、工作投入度、是否加班、是否升职、工资提升比例等）以及员工是否已经离职的对应记录。
数据分为训练数据和测试数据，分别保存在pfm_train.csv和pfm_test.csv两个文件中。
其中训练数据主要包括1100条记录，31个字段，主要字段说明如下：
（1）Age：员工年龄
（2）Attrition：员工是否已经离职，1表示已经离职，2表示未离职，这是目标预测值；
（3）BusinessTravel：商务差旅频率，Non-Travel表示不出差，Travel_Rarely表示不经常出差，Travel_Frequently表示经常出差；
（4）Department：员工所在部门，Sales表示销售部，Research & Development表示研发部，Human Resources表示人力资源部；
（5）DistanceFromHome：公司跟家庭住址的距离，从1到29，1表示最近，29表示最远；
（6）Education：员工的教育程度，从1到5，5表示教育程度最高；
（7）EducationField：员工所学习的专业领域，Life Sciences表示生命科学，Medical表示医疗，Marketing表示市场营销，Technical Degree表示技术学位，Human Resources表示人力资源，Other表示其他；
（8）EmployeeNumber：员工号码；
（9）EnvironmentSatisfaction：员工对于工作环境的满意程度，从1到4，1的满意程度最低，4的满意程度最高；
（10）Gender：员工性别，Male表示男性，Female表示女性；
（11）JobInvolvement：员工工作投入度，从1到4，1为投入度最低，4为投入度最高；
（12）JobLevel：职业级别，从1到5，1为最低级别，5为最高级别；
（13）JobRole：工作角色：Sales Executive是销售主管，Research Scientist是科学研究员，Laboratory Technician实验室技术员，Manufacturing Director是制造总监，Healthcare Representative是医疗代表，Manager是经理，Sales Representative是销售代表，Research Director是研究总监，Human Resources是人力资源；
（14）JobSatisfaction：工作满意度，从1到4，1代表满意程度最低，4代表满意程度最高；
（15）MaritalStatus：员工婚姻状况，Single代表单身，Married代表已婚，Divorced代表离婚；
（16）MonthlyIncome：员工月收入，范围在1009到19999之间；
（17）NumCompaniesWorked：员工曾经工作过的公司数；
（18）Over18：年龄是否超过18岁；
（19）OverTime：是否加班，Yes表示加班，No表示不加班；
（20）PercentSalaryHike：工资提高的百分比；
（21）PerformanceRating：绩效评估；
（22）RelationshipSatisfaction：关系满意度，从1到4，1表示满意度最低，4表示满意度最高；
（23）StandardHours：标准工时；
（24）StockOptionLevel：股票期权水平；
（25）TotalWorkingYears：总工龄；
（26）TrainingTimesLastYear：上一年的培训时长，从0到6，0表示没有培训，6表示培训时间最长；
（27）WorkLifeBalance：工作与生活平衡程度，从1到4，1表示平衡程度最低，4表示平衡程度最高；
（28）YearsAtCompany：在目前公司工作年数；
（29）YearsInCurrentRole：在目前工作职责的工作年数
（30）YearsSinceLastPromotion：距离上次升职时长
（31）YearsWithCurrManager：跟目前的管理者共事年数；
测试数据主要包括350条记录，30个字段，跟训练数据的不同是测试数据并不包括员工是否已经离职的记录，学员需要通过由训练数据所建立的模型以及所给的测试数据，得出测试数据相应的员工是否已经离职的预测。

