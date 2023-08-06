# -*- coding: utf-8 -*-
def pyy(list33):
	for l in list33:
	  #这也是注释信息
		if isinstance(l,list):
			pyy(l)
		else:
			print(l)
