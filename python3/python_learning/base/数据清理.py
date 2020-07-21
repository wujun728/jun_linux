import pandas as pd
data = pd.DataFrame({'food': ['bacon', 'pulled pork', 'bacon','Pastrami', 'corned beef', 'Bacon','pastrami', 'honey ham', 'nova lox'],
                     'ounces': [4, 3, 12, 6, 7.5, 8, 3, 5, 6]})
meat_to_animal = {
  'bacon': 'pig',
  'pulled pork': 'pig',
  'pastrami': 'cow',
  'corned beef': 'cow',
  'honey ham': 'pig',
  'nova lox': 'salmon'
}
lowercased = data['food'].str.lower();
# Series的map方法可以接受一个函数或含有映射关系的字典型对象，但是这里有一个小问题，即有些肉类的首字母大写了，
# 而另一些则没有。因此，我们还需要使用Series的str.lower方法，将各个值转换为小写：
data['animal'] = lowercased.map(meat_to_animal);

print(data);

# 我们也可以传入一个能够完成全部这些工作的函数：
data['food'].map(lambda x: meat_to_animal[x.lower()])

# 使用map是一种实现元素级转换以及其他数据清理工作的便捷方式。