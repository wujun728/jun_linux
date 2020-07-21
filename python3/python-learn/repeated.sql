CREATE TABLE tf_user(
ID     NUMBER(14),
NAME   VARCHAR2(255),
email  VARCHAR2(255)
);

Insert into TF_USER
   (ID, NAME, EMAIL)
 Values
   (1, 'chengwei', 'chengwei@tencent.com.cn');
Insert into TF_USER
   (ID, NAME, EMAIL)
 Values
   (2, 'lizm', 'lizm@tencent.com.cn');
Insert into TF_USER
   (ID, NAME, EMAIL)
 Values
   (3, 'changhj', 'changhj@tencent.com.cn');
Insert into TF_USER
   (ID, NAME, EMAIL)
 Values
   (4, 'wujun', 'wujun@tencent.com.cn');
Insert into TF_USER
   (ID, NAME, EMAIL)
 Values
   (5, 'mmtye', 'mmtye@tencent.com.cn');
Insert into TF_USER
   (ID, NAME, EMAIL)
 Values
   (6, 'guona', 'guona@tencent.com.cn');
Insert into TF_USER
   (ID, NAME, EMAIL)
 Values
   (7, 'chengwei', 'chengwei@tencent.com.cn');
Insert into TF_USER
   (ID, NAME, EMAIL)
 Values
   (8, 'guona', 'guona@tencent.com.cn');
Insert into TF_USER
   (ID, NAME, EMAIL)
 Values
   (9, 'mmtye', 'mmtye@tencent.com.cn');
Insert into TF_USER
   (ID, NAME, EMAIL)
 Values
   (10, 'chengwei', 'chengwei@tencent.com.cn');


-- 一条语句删除name重复的记录
DELETE FROM tf_user WHERE ROWID NOT IN(
SELECT b.rod from (
SELECT MIN(ROWID) rod, NAME FROM tf_user a
GROUP BY NAME) b);

SELECT * from tf_user;
