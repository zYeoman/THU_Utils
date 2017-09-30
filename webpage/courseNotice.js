/*
 * courseNotice.js
 * Copyright (C) 2017 Yongwen Zhuang <zeoman@163.com>
 *
 * Distributed under terms of the MIT license.
 */
var CourseNotice = function(){

	return {

		/*
		 * paramList:获取数据传输参数
		 * pageSize:每页条数
		 * currentPage:当前页
		 */
		paramList:{
			currentPage:1,
			pageSize:50
		},

		/**
		 * 初始化方法
		 * 2014年10月13日下午2:41:34
		 */
		init:function(){
			$(".standord-nav a.coursenotice").addClass("active");
			CourseNotice.getData();
		},

		/**
		 * 获取数据
		 * 2014年10月13日下午2:41:47
		 */
		getData:function(){
			$.ajax({
				"type" : 'GET',
				"url" : baseUrl+"/b/myCourse/notice/listForStudent/"+courseId,
				"dataType" : "json",
				"data":CourseNotice.paramList,
				"success" :function(data){
					if(data[MESSAGE] == SUCCESS){
						CourseNotice.renderData(data.paginationList.recordList);
						CourseNotice.pagination.initData(data.paginationList);
					}else {
						alert('获取数据失败');
					};
				}
			});
		},

		addStatusForYidu:function(){
			$.ajax({
				"type" : 'POST',
				"url" : baseUrl+"/b/myCourse/notice/addStatusforYiDu/"+courseId,
				"dataType" : "json",
				"success" :function(data){
					if(data[MESSAGE] == SUCCESS){
						alert('一键已读成功');
						CourseNotice.init();
					}else {
						alert('一键已读失败');
					};
				}
			});
		},

		/**
		 * 渲染数据
		 * 2014年10月13日下午2:42:00
		 * dataList:公告数据
		 */
		renderData:function(dataList){
			$("#topicList").empty();
			if(dataList==''){
				$("<tr><td><span class='gray ml20'>暂无数据</span></td></tr>").appendTo("#topicList");
			}else{
				var currentPage = CourseNotice.paramList['currentPage'];
				var pageSize = CourseNotice.paramList['pageSize'];
				$.each(dataList,function(i,val){
					var rows = "<tr>";
					//序号
					rows += "<td align='center' width='5%'>"+((currentPage-1)*pageSize+i+1)+"</td>";
					//标题
					rows += "<td align='left' width='45%'>";
					if(val.courseNotice.msgPriority==1){
						rows += "<a href='javascript:;' onclick='CourseNotice.viewNotice("+val.courseNotice.id+");' style='color:red;' title='查看公告'>"+val.courseNotice.title+"</a>";
					}else{
						rows += "<a href='javascript:;' onclick='CourseNotice.viewNotice("+val.courseNotice.id+");' title='查看公告'>"+val.courseNotice.title+"</a>";
					}
					if(val.status==0 ||val.status==null){//未读
						rows += "<span class='red fb fi ml5 f14' title='新公告'>new</span>";
					}
					rows += "</td>";
					//发布人
					rows += "<td align='center' class='gray' width='15%'>"+val.courseNotice.owner+"</td>";
					//发布时间
					rows += "<td align='center' class='gray' width='10%'>"+val.courseNotice.regDate+"</td>";
					//浏览次数
					rows += "<td align='center' class='gray' width='10%'>"+val.courseNotice.browseTimes+"</td>";
					$("#topicList").append(rows);
			    });
			}
		},

		/**
		 * 分页功能
		 */
		pagination : {

			/**
			 * 赋值及分页数据填充
			 * data:分页数据
			 * module:分页容器
			 */
			initData : function(data){
				$(".hw-list-footer").find(".totalNum").text(data.recordCount).end()
					.find(".currentPage").text(data.currentPage).end()
					.find(".totalPage").text(Math.ceil(data.recordCount/data.pageSize));
			},

			/**
			 * 改变每页显示条数
			 * str:每页显示条数
			 * el:this
			 * module:分页容器
			 * moduleName:模块名称
			 */
			changeSizePerPage : function(str,el){
				$(".list-num li a.active").removeClass('active');
				$(el).addClass('active');
				CourseNotice.paramList['pageSize'] = parseInt(str);
				CourseNotice.paramList['currentPage'] = 1;
				CourseNotice.getData();
			},

			/**
			 * 翻页
			 * str:+下一页|-上一页|end最后一页
			 */
			turnPage : function(str){
				var currentPage = parseInt($(".currentPage").text());
				var totalPage = parseInt($(".totalPage").text());
				if(str=='+'){//next page
					currentPage = Math.min((currentPage+1),totalPage);
				}else if(str=='-'){//previous page
					currentPage = Math.max((currentPage-1),1);
				}else if(str=='end'){//last page
					currentPage = totalPage;
				}else{
					currentPage = parseInt(str);
				}
				CourseNotice.paramList['currentPage']=currentPage;
				CourseNotice.getData();
			}
		},

		/**
		 * 获取单条公告数据
		 * id:公告id
		 * 返回公告信息
		 */
		getSingleData:function(id){
			CourseNotice.singleData=null;
			$.ajax({
				"type" : 'GET',
				"url" : baseUrl+"/b/myCourse/notice/studDetail/"+id,
				"dataType" : "json",
				"success" :function(data){
					if(data[MESSAGE] == SUCCESS){
						CourseNotice.singleData = data.dataSingle;
					}else {
						alert('获取数据失败');
					};
				},
				async:false
			});
		},

		/*
		 * 查看公告
		 * id:公告id
		 */
		viewNotice : function(id){
			$("#details_title,#details_owner,#details_regDate,#details_detail").empty();//初始化清空内容
			CourseNotice.getSingleData(id);//获取数据
			$("#details_title").text(CourseNotice.singleData.title);
			$("#details_owner").text(CourseNotice.singleData.owner);
			$("#details_regDate").text(CourseNotice.singleData.regDate);
			$("#details_detail").html(CourseNotice.singleData.detail);
			art.dialog({
				content: document.getElementById('dialog-notice-view'),
				zIndex:100,
				lock: true,
				drag:true,
				id:"view-notice-dialog",
				width:600,
				title:'查看公告',
				button : [{
		  	       value : '给教师发送邮件',
		  	       focus : true,
		  	       callback : function(){
				  	   	$.ajax({
							"type" : 'POST',
							"url" : baseUrl+"/b/mycourse/SpeakTeacher/list/"+courseId,
							"dataType" : "json",
							"success" :function(data){
								if(data[MESSAGE] == SUCCESS){
									CourseNotice.sendEmail(data.resultList.teacherInfo.name,"回复："+CourseNotice.singleData.title,data.resultList.teacherInfo.email);
								}else{
									alert('获取数据失败');
								};
							},
							async:false
						});
		  	       }
				 }],
				 cancelValue:"关闭",
				 cancel:function(){
					 this.close();
					 CourseNotice.getData();
				 }

			});
			if(locale == "en_US"){
				$(artDialog.get("view-notice-dialog").dom.buttons[0]).find("input:first").val("Send Mail to Teacher");
				$(artDialog.get("view-notice-dialog").dom.buttons[0]).find("input:last").val("Close");
				art.dialog({id: 'view-notice-dialog'}).title('View Notice');
			}
		},

		/*
		 * 发送邮件
		 */
		sendEmail:function(userName,title,email){
			var $form = $('#notice-send-email-form');
			$("#teacher-name").val(userName);
			$form.find("input[name='toEmailsStr']").val(email);
			$form.find("input[name='subject']").val(title);
  	   		art.dialog({
	  	  		content: document.getElementById('dialog-notice-send-email'),
	  	  		zIndex:100,
	  	  		lock: true,
	  	  		id:"send-mail-dialog",
	  	  		drag:true,
	  	  		width:'auto',
	  	  		title:'发送邮件',
	  	  		initialize:function(){//对话框初始化完成后执行的函数
		  	  		editorEmail.setContent(null);//为了解决IE兼容问题
				    editorEmail.addListener('ready', function(){
				    	editorEmail.setContent(null);//支持其他浏览器
				    });
	  	  		},
	  	  		button: [{
	  	  	    	value:'发送',
	  	  	        focus:true,
	  	  	        callback: function(){
		  	  	        $.ajax({
							"type" : 'POST',
							"url" : baseUrl+"/b/myCourse/notice/sendMailToTeacher/"+courseId,
							"dataType" : "json",
							"data": $form.serialize(),
							"success":function(data){
								if(data[MESSAGE] == SUCCESS){
									if(locale == "en_US"){
										alert("Send mail successfully！");
									}else{
										alert("发送邮件成功！");
									}

								}else{
									if(locale == "en_US"){
										alert("Send mail failure！");
									}else{
										alert("发送邮件失败！");
									}
								};
							}
						});
	  	  	        }
	  	  	    }],
	  	  		cancel: true
	  	  	});
	  	   	if(locale == "en_US"){
				$(artDialog.get("send-mail-dialog").dom.buttons[0]).find("input:first").val("Send");
				$(artDialog.get("send-mail-dialog").dom.buttons[0]).find("input:last").val("Cancel");
				art.dialog({id: 'send-mail-dialog'}).title('Send Mail');
			}
		}

	};

}();

$(function(){
	CourseNotice.init();
	editorEmail = new UE.ui.Editor({wordCount: true,initialFrameHeight:500,maximumWords:4000});//声明邮件编辑器
	editorEmail.render("email-editor");//初始化
});
