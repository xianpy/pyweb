<?php
	header("content-type:text/html;charset=utf-8");
	
	//1、接收客户端的数据（用户的输入）
	$userName = $_POST['userName'];
	$userPass = $_POST['userPass'];	
	
	//2、处理（判断该用户是否被注册过，如果没有注册过，保存用户输入的信息到数据库中）
	//1)、连接数据库服务器
	$con = mysql_connect("localhost","root","940923");
	if(!$con){
		echo "-1";		
	}else{
		//2)、选择数据库
		mysql_select_db("lppz",$con);
		
		//3)、执行SQL语句（增）
		$sqlStr="select * from user_table where userName='".$userName."' and userPass = '".$userPass."'";
	    //影响的行数
		$result=mysql_query($sqlStr,$con);
		//4)、关闭数据库
		mysql_close($con);

		//3、注册成功返回1		
		$rows=mysql_num_rows($result);
		if($rows>0){ //用户名存在,则可以登录
			echo "1";
		}else{
			echo "0";
		}	
	}
?>