# hzdatasdk Package

This is a simple example package. You can use
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.

列举了hzdata相关的一些内容

======================
项目背景
    hzdata提供了一套python的sdk
使用者在集成了sdk之后，可以通过接口直接拉取数据,返回
的数据大都为pandas.dataframe、numpy.array等格式。


======================
服务器架构
1: sdksvr
	sdksvr与回测系统连接, 内部通过rpc协议进行传输。
	用户通过集成sdk，与sdksvr连接，从sdk服务器拉取数据。
	sdksvr可水平扩展。
2：回测系统
	 使用目前已有的回测系统即可。


======================
待调研问题:
	1：python打包(sdk集成)方案。
	2：大数据数据库方案。
	
	


