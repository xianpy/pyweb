$(function(){

    $("button.addShopping").click(function(){
        var goods_id = $(this).attr("ga");   // 获取点击按钮所在行的商品id
        $.getJSON("/addshop/",{"goods_id":goods_id},function(data){
            $("span#totalPrice").html(data["totalPrice"]);  // 设置总价
            if(data["status"]=="200"){
                document.getElementById(goods_id).innerHTML=data["cart_num"];
            }
        });
    });

    $("button.subShopping").click(function(){
        var goods_id = $(this).attr("ga");
        var $current_subbtn = $(this);
        $.getJSON("/subcart/",{"goods_id":goods_id},function(data){
            $("span#totalPrice").html(data["totalPrice"]);  // 设置总价
            if(data["status"]=="200"){

                if(data["cart_num"]==0){
                    $current_subbtn.parents("li.menuList").css("display","none");
                    if($("span#totalPrice").html().trim()=="0"){
                        $("div#selectall").children("span").children("span").html("");
                    }

                }else{
                    document.getElementById(goods_id).innerHTML=data["cart_num"];
                }
            }
        });
    });


    $("span.ischose").click(function(){
        var $outer_span = $(this);
        var cartid = $outer_span.parents("li.menuList").attr("cartid");
        $.getJSON("/changeselect/",{"cartid":cartid},function(data){
            $("span#totalPrice").html(data["totalPrice"]);  // 设置总价

            if(data["ischoose"]){   // 控制当前购物车选择状态
                $outer_span.children("span").html("√");
            }else{
                $outer_span.children("span").html("");
            }

            $inner_span = $("div#selectall").children("span").children("span");
            if(data["select_all_flag"]){  // 控制“全选”选择状态
                $inner_span.html("√");
            }else{
                $inner_span.html("");
            }
        });

    })


    $("div#selectall").click(function(){

        var $select_all =  $(this).children("span").children("span");
        var is_select = $select_all.html().trim() == ""?false:true;
        $.getJSON("/changeselectall/",{"hope_status":!is_select},function(data){
                $("span#totalPrice").html(data["totalPrice"]);  // 设置总价
                if(data["is_select"] == "true"){
                    $("span.ischose").children("span").html("√");
                    $select_all.html("√");
                }else{
                    $("span.ischose").children("span").html("");
                    $select_all.html("");
                }
        });
    });

    $("span#ok").click(function(){
        $.getJSON('/makeorders/',function(data){
             if(data["status"]=="900"){
                 window.open("/login/",target="_self");
             }
             if(data["status"]=="200"){
                 var orderid=data["orderid"];
                 window.open("/orderdetail/?order_id="+orderid,target="_self");
             }
        });
    });

})