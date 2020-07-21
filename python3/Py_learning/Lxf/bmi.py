#!/usr/bin/python3
ming_h=float(input('请输入身高:'))
ming_k=float(input('请输入体重：'))

bmi=ming_k/(ming_h*ming_h)

if bmi<18.5:
	print('过轻')
elif bmi<25:
	print('正常')
elif bmi<28:
	print('肥胖')
else:
	print('严重肥胖!')
