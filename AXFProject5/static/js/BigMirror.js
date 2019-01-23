jQuery.fn.extend({
	singleton:(function(){
			function BigMirror(obj){
				//1、初始化数据
				this.initData();
				//2、修改数据
				this.updateData(obj);
			}
			
			BigMirror.prototype.initData = function(){
				//属性
				//放大镜的dom对象
				this.mirrorDom = null;
				//放大镜的left和top是跟随鼠标变化的。
				this.left = 0;
				this.top = 0;		
				//放大效果	
				this.showBoxDom = null;
				//放大效果
				this.bigObj = {
					imgDom:null
				}		
			}
			
			BigMirror.prototype.updateData = function(obj){
				//容器的dom对象
				this.boxDom = obj.boxDom;
				//属性
				//放大镜的尺寸（宽和高）
				this.width = obj.width;
				this.height = obj.height;
				//放大的倍数
				this.mult = obj.mult;
				//透明度
				this.opacity = obj.opacity;
				//背景色
				this.bgColor = obj.bgColor;
				//位置
				this.bigObj.pos=obj.bigObj.pos;
				//计算放大效果的坐标
				let left=0;
				let top=0;
				switch(this.bigObj.pos){
					case "上":left=0;top=-1*this.bigObj.height;break;
					case "右":left=this.boxDom.offsetWidth;top=0;break;
					case "下":left=0;top=this.boxDom.offsetHeight;break;
					case "左":left=-1*this.bigObj.width;top=0;break;
					default:;
				}
				this.bigObj.left=left;
				this.bigObj.top=top;
				//计算放大效果的宽高
				this.bigObj.width=this.width*this.mult;		
				this.bigObj.height=this.height*this.mult;		
				this.bigObj.pic=obj.bigObj.pic;		
			}
			
			BigMirror.prototype.createAllDom = function(){
				//1、创建放大镜
				this.mirrorDom = $create("div");
				let cssStr = "position:absolute;border:1px solid #e4e4e4;cursor: move;";
				this.mirrorDom.style.cssText = cssStr;
				
				//2、放大效果
				//2.1放大效果的可视区域
				this.showBoxDom= $create("div");
				cssStr = "position:absolute;border:1px solid #e4e4e4;overflow:hidden;";
				this.showBoxDom.style.cssText = cssStr;
				//2.2放大的图片
				this.bigObj.imgDom = $create("img");
				cssStr  = "position:absolute;";
				this.bigObj.imgDom.style.cssText = cssStr;
				//把放大的图片放入放大效果的可视区域里
				this.showBoxDom.appendChild(this.bigObj.imgDom);
			}
			
			BigMirror.prototype.updateDomAttr = function(){
				//1、创建放大镜
				this.mirrorDom.style.width = this.width+"px";
				this.mirrorDom.style.height = this.height+"px";
				this.mirrorDom.style.backgroundColor = this.bgColor;
				this.mirrorDom.style.opacity = this.opacity;
				//改变父元素，//确定父子关系
				this.boxDom.appendChild(this.mirrorDom);
				
				//2、放大效果
				//2.1放大效果的可视区域
				this.showBoxDom.style.width = this.bigObj.width+"px";
				this.showBoxDom.style.height = this.bigObj.height+"px";
				this.showBoxDom.style.left = this.bigObj.left+"px";
				this.showBoxDom.style.top = this.bigObj.top+"px";
				//改变父元素，确定父子关系
				this.boxDom.appendChild(this.showBoxDom);
				
				//2.2放大的图片
				this.bigObj.imgDom.src=this.bigObj.pic;
				this.bigObj.imgDom.style.width=this.boxDom.offsetWidth*this.mult+"px";
				this.bigObj.imgDom.style.height=this.boxDom.offsetHeight*this.mult+"px";
			}
			
			//创建放大镜和放大效果
			BigMirror.prototype.initUI=function(){
				this.createAllDom();
				this.updateDomAttr();
			}
			
			BigMirror.prototype.initEvent = function(){
				let that = this;
				//给容器加onmouseover事件
				removeEvent1705(this.boxDom,"mouseover",boxDomonmouseover);
				//给容器里绑定onmousemove事件
				addEvent1705(this.boxDom,"mouseover",boxDomonmouseover,false);
				
				function boxDomonmouseover(event){
					let evt = event || window.event;
					let offsetX = evt.pageX-that.boxDom.offsetLeft;
					let offsetY = evt.pageY-that.boxDom.offsetTop;
					if(offsetX>0 && offsetX<that.boxDom.offsetWidth
					&& offsetY>0 && offsetY<that.boxDom.offsetHeight){
						that.mirrorDom.style.display="block";
						that.showBoxDom.style.display="block";
					}
				}
				
				removeEvent1705(this.boxDom,"mousemove",boxDomonmousemove);
				//给容器里绑定onmousemove事件
				addEvent1705(this.boxDom,"mousemove",boxDomonmousemove,false);
				function boxDomonmousemove(event){
					let evt = event || window.event;
					//1、让放大镜跟着鼠标走
					let left = evt.pageX-that.boxDom.offsetLeft-that.width/2;
					let top = evt.pageY-that.boxDom.offsetTop-that.height/2;
					if(left<0){
						left=0;
					}else if(left>that.boxDom.offsetWidth-that.width){
						left=that.boxDom.offsetWidth-that.width;
					}
					if(top<0){
						top=0;
					}else if(top>that.boxDom.offsetHeight-that.height){
						top=that.boxDom.offsetHeight-that.height;
					}			
					that.mirrorDom.style.display="block";
					that.showBoxDom.style.display="block";
					that.mirrorDom.style.left = left+"px";
					that.mirrorDom.style.top = top+"px";
					
					//2、放大效果反方向跟着走
					that.bigObj.imgDom.style.left = -1*that.mult*left+"px";
					that.bigObj.imgDom.style.top = -1*that.mult*top+"px";
					stopBubble1705(evt);
				};
				
				this.mirrorDom.onmouseout = function(){
					that.mirrorDom.style.display="none";
					that.showBoxDom.style.display="none";
				}
				
				document.body.onmousemove = function(){
					that.mirrorDom.style.display="none";
					that.showBoxDom.style.display="none";
				}
				
			}
		
			let instance;
			
			return {
				getInstance:function(obj){
					if(instance==undefined){
						instance = new BigMirror(obj);
						//创建外观
						instance.initUI();
						instance.initEvent();
					}else{
						instance.updateData(obj);
						instance.updateDomAttr();
						instance.initEvent();
					}
					return instance;
				}
			}
		})(),
	bigMirror:function(obj){
		this.singleton.getInstance(obj);
	}
});