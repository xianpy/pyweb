<?php
	header("Content-Type:text/html;charset=utf-8");
	//1、接受客户端的数据
	$vipName   = $_REQUEST['vipName'];
	$goodsId   = $_REQUEST['goodsId'];
	$goodsCount = $_REQUEST['goodsCount'];
	
	//2、数据保存在数据库中
	//1）、建立连接
	$conn = mysql_connect("localhost","root","940923");
	
	//2）、选择数据库
	if(!mysql_select_db("lppz",$conn)){
		die("数据库选择失败".mysql_error());
	}
	
	//3）、传输数据
	$sqlstr = "update shoppingcart set goodsCount='".$goodsCount."' where vipName='".$vipName."' and goodsId='".$goodsId."'";
//	echo($sqlstr);
	
	if(!mysql_query($sqlstr,$conn)){
		die("执行更新SQL语句失败".mysql_error());
		echo "0";
	}
	
	//4）、关闭连接
	mysql_close($conn);
	
	//3、给客户端返回（响应）
	echo 1; //1：表示修改成功,0：表示修改失败
?>