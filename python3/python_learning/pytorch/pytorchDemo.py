import torch
from torch.autograd import Variable

tensor = torch.FloatTensor([[1,2],[3,4]])
print(tensor)

# require_grad:  表示要不要把Variable涉及到反向传播上去
variable = Variable(tensor, requires_grad=True)

t_out = torch.mean(tensor*tensor)
print(t_out)

# 应用了反向传播
v_out = torch.mean(variable*variable);
print(v_out);

# 设置方向传递
v_out.backward();
# v_out = 1/4 * sum(var*var)
# d(v_out) / d(var) = 1/4 * 2 * variable = variable /2

# 打印梯度值
print(variable);
print(variable.grad);
print(variable.data);
