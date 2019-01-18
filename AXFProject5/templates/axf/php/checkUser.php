<?php
	header("Content-type","text/html;charset=utf-8");
	//1.接收数据
	$userName=$_GET["userName"];
	//2.在数据库中查询
		//2.1建立连接并选择数据库
		$con = mysql_connect("localhost","root","940923");
		if(!$con){
			echo "-1";
		}
		mysql_select_db("lppz",$con);
		//2.2执行SQL语句
		$sqlStr="select * from user_table where userName='".$userName."'";
		$result=mysql_query($sqlStr,$con);
		//2.3关闭连接
		mysql_close($con);
	//3.响应结果
	$rows=mysql_num_rows($result);
	if($rows>0){ //用户名存在
		echo "0";
	}else{
		echo "1";
	}
?>