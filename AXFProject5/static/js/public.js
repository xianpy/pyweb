// ------------------------------Tools↓-------------------------
//创建Dom元素
function $create(str){
	return document.createElement(str);
}
//显示与隐藏
let makeHideAndShow = function(source,target,timeSpace=200){
	source.mouseenter(function(){
		if(target.css("display")=="none"){
			target.fadeIn(timeSpace);
		}
	});
	source.mouseleave(function(){
		if(target.css("display")=="block"){
			target.fadeOut(timeSpace);
		}	
	});
}
// ------------------------------Tools↑-------------------------

function InitUI(){
	InitTopUI();
	InitLeftUI();
	InitRightUI();
}
function InitTopUI(){
	//我的良品显示隐藏
	makeHideAndShow($(".myInfo_li"),$(".myInfo_hover"),200);
	//关注良品显示隐藏
	makeHideAndShow($(".attention_li"),$(".attention"),200);
	//购物车显示隐藏
	makeHideAndShow($(".main_buy"),$(".buy_show"),200);
}
function InitLeftUI(){
	//左侧边栏显示与隐藏
	setInterval(function(){
		if(	$(window).scrollTop()>=$("#active_target").offset().top){
			$("#aside_left_nav").fadeIn(500);
		}else{	
			$("#aside_left_nav").fadeOut(500);
		}
	},500);
	//左侧边栏按钮点击的滑动效果
	let $left_lis=$(".fn_list").children();
	$left_lis.each(function(){
		$(this).click(function(){
			$('html,body').animate({"scrollTop":$($(this).children().attr("name")).offset().top},500);
		}); 
	});
}
function InitRightUI(){
	//右侧边栏下面二维码的显示与隐藏
	makeHideAndShow($("#qr_cust"),$("#qr_cust_display"));
	//返回顶部按钮
	$(".goback").click(function(){
			$('html,body').animate({"scrollTop":0},500);
	}); 
}

//动态生成菜单
function MenuEvent(){
	let menu_text=[
		["嗑壳坚果","果果仁仁","特惠炒货"],
		["猪肉系列","牛肉系列","鸡鸭系列","海味系列"],
		["缤纷果干","话梅山楂","红枣葡萄"],
		["糕点系列","饼干系列","糖果系列","果冻系列"],
		["美味豆干","笋菌海带","其他山珍"],
		["养生冲调","进口饮料"],
		["进口糕点","进口糖果","休闲零食"],
		["零食礼盒","年货量贩装"]
	];
	let menu_lis=$(".menu_list").children(); //所有菜单item的jq对象
	let menu_show_dom=	$(".menu_show")[0];	 //右侧显示div的dom节点
	for(let i=0;i<menu_lis.length-1;i++){
		$(menu_lis[i]).mouseenter(function(){
			for(let j=0;j<menu_text[i].length;j++){
				let domDiv = $create("div");
				domDiv.className="menu_item";
				let domA = $create("a");
				domA.innerText=menu_text[i][j];
				domDiv.appendChild(domA);
				menu_show_dom.appendChild(domDiv);
			}
			menu_lis[i].appendChild(menu_show_dom);
			menu_show_dom.style.display="block";
		});
		$(menu_lis[i]).mouseleave(function(){
			$(menu_show_dom).empty();//清空
			menu_show_dom.style.display="none";
		});
	}
} 

//顶部登录框根据有无cookie的不同显示状态
function login_cookie(){
	let $no_login_style = $(".toolbar_content_left");
	let $login_style = $(".toolbar_content_left_logined");
	if(getCookie("userName")==null){ //非登录
		$no_login_style.css("display","block");
		$login_style.css("display","none");
	}else{//登录状态
		$no_login_style.css("display","none");
		$login_style.css("display","block");
		$(".toolbar_username").text(getCookie("userName"));
		$(".toolbar_quit").click(function(){
			removeCookie("userName");
			$no_login_style.css("display","block");
			$login_style.css("display","none");
			location.href="login.html";
		});
	}
}

//从数据库中获取购物车信息
function updateCartCount(){
	if(getCookie("userName")!=null){
		let p =new Promise(function(resolve,reject){
			$.ajax({
				type:"get",
				url:"php/getShoppingCart.php",
				async:true,
				data:{
					"vipName":getCookie("userName") 
				},
				success:function(msg){
					let data=eval(msg);
					resolve(data);
				}
			});
		});
		return p;
	}else{
		return null;
	}
}
//通过传入的购物车数据来更新购物车数量显示，并调用计算总价
function setTopCartCount(data){
	let count=0;
	for(let i=0; i<data.length; i++){
		count+=parseInt(data[i].beiyong1);
	}
	$(".buy_num b").text(count);
	$(".cart_shop_count").text(count);
	if($(".gw .sum").length!=0){
		$(".gw .sum").text(count);
	}
	//购物车总价
	setCartAllMoney();
	let p = new Promise(function(reslove,reject){
		reslove();
	});
	return p;
}

//通过已加载的商品条目来计算购物车总价
function setCartAllMoney(){
	let all_money=0;
	let prices=$(".buy_show tbody .small_cart_price");
	let nums=$(".buy_show tbody .small_cart_sum");
	for(let i=0;i<prices.length;i++){
		let item_price=parseFloat(prices[i].innerText.substring(1))*parseInt(nums[i].innerText);
		all_money+=item_price;
	}
	$(".cart_shop_money").text(all_money.toFixed(2));
}


//模拟生成GUID
function newGuid()
{
    var guid = "";
    for (var i = 1; i <= 32; i++){
      var n = Math.floor(Math.random()*16.0).toString(16);
      guid +=   n;
      if((i==8)||(i==12)||(i==16)||(i==20))
        guid += "-";
    }
    return guid;   
}



//动态创建购物车产品
function setCartList(data){
	let goods_list_arr=data;
	//动态创建商品
	for(let i=0; i<goods_list_arr.length; i++){
		$tr_goods_tr=$("<tr></tr>");
		$tr_goods_tr.attr("goodsid",goods_list_arr[i].goodsId);
		 //图片
		$li_goods_img=$('<td class="tr_shop_img" width=60><a href="javascript:;"><img/></a></td>');
		$li_goods_img.children().children().prop("src",goods_list_arr[i].goodsImg); //图片
		//名称
		$li_goods_name=$("<td><a></a></td>");
		$li_goods_name.children("a").text(goods_list_arr[i].goodsName);//名称
		$li_goods_name.children("a").prop({
			"title":goods_list_arr[i].goodsName,
			"target":"_blank"
		});
		$li_goods_delete=$('<td><span><b class="small_cart_price">¥'+goods_list_arr[i].goodsPrice+'</b> x <i class="small_cart_sum">'+goods_list_arr[i].beiyong1+'</i></span><br/><a href="javascript:;" class="cart_delete_btn">删除</a></td>');
		$tr_goods_tr.append($li_goods_img,$li_goods_name,$li_goods_delete);
		$(".buy_show tbody").append($tr_goods_tr);
	}
	var p = new Promise(function(resolve,reject){
		resolve(goods_list_arr);
	});
	return p;
}
	
//商品删除按钮事件注册
function delete_event(){
	$(".cart_delete_btn").click(function(){
		let goodsid=$(this).parents("tr").attr("goodsid");
		if(!confirm("真的真的真的不想要了？")){
				return;
		}
		$.ajax({
			type:"get",
			url:"php/deleteGoods.php",
			async:true,
			data:{
				"vipName":getCookie("userName"),
				"goodsId":$(this).parents("tr").attr("goodsid")
			},
			success:function(msg){
				if(msg==1){
					$(".buy_show tbody tr").remove("tr[goodsid="+goodsid+"]");
					//更新购物车数量和总价
					updateCartCount().then(setTopCartCount);
					console.log("删除成功");
				}else{
					console.log("删除失败");
				}
			}
		});
	});
}