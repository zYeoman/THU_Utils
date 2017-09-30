/*
 * courseHomework.js
 * Copyright (C) 2017 Yongwen Zhuang <zeoman@163.com>
 *
 * Distributed under terms of the MIT license.
 */
/**
 * 学生-课程作业
 * */
var stuHomework = new Object;
var list;

//获取homework数据
stuHomework.getlist = function(){
//	window.open(baseUrl+"/b/myCourse/homework/list4Student/"+courseId+'/0');
	$.ajax( {
		"type" : 'GET',
		"url" : baseUrl+"/b/myCourse/homework/list4Student/"+courseId+'/0',
		"dataType" : "json",
		"success" : function(resp) {
			if(resp[MESSAGE] == SUCCESS){
				list = resp.resultList;
				stuHomework.rendertable(resp.resultList);
			}else {
				alert('获取数据失败');
			}
		},
		async:false
	});
};

//将获取的数据往网页里面填写
stuHomework.rendertable = function(homeworkinfolist){
	//如果数据库中没有数据
	if(homeworkinfolist.length=='0'){
		$("#homeworklist tr").remove();
		var $error = $("<tr><td align='left'><span class='gray ml20'>暂无数据</span></td></tr>");
    	$error.appendTo("#homeworklist");
	}else {//如果数据库中数据不为0
		$("#homeworklist tr").remove();
		for(var i = 0; i < homeworkinfolist.length; i++){
			homeworkinfolist[i].courseHomeworkInfo.beginDate = (homeworkinfolist[i].courseHomeworkInfo.beginDate==null)?"":homeworkinfolist[i].courseHomeworkInfo.beginDate;
			homeworkinfolist[i].courseHomeworkInfo.endDate = (homeworkinfolist[i].courseHomeworkInfo.endDate==null)?"":homeworkinfolist[i].courseHomeworkInfo.endDate;
			var newRow  = '<tr>';
				newRow += '<td width="4%" align="center">'+(i+1)+'</td>';
			//	newRow += '<td width="20%"><div class="hw-name"><a href="/f/student/homework/hw_detail/'+courseId+'/'+homeworkinfolist[i].courseHomeworkInfo.homewkId+'">'+homeworkinfolist[i].courseHomeworkInfo.title+'</a></div></td>';
				newRow += '<td width="20%"><div class="hw-name">'+homeworkinfolist[i].courseHomeworkInfo.title+'</a></div></td>';
				if(locale=="en_US"){
					if(homeworkinfolist[i].courseHomeworkRecord.status=='0'){
						newRow += '<td width="8%"><div class="gray hwStatus">No submission</div></td>';
					}else if(homeworkinfolist[i].courseHomeworkRecord.status=='1'){
						newRow += '<td width="8%"><div class="gray hwStatus">Submitted</div></td>';
					}else if(homeworkinfolist[i].courseHomeworkRecord.status=='2'||'3'){
						newRow += '<td width="8%"><div class="gray hwStatus">Graded</div></td>';
					}
				}else{
					if(homeworkinfolist[i].courseHomeworkRecord.status=='0'){
						newRow += '<td width="8%"><div class="gray hwStatus">尚未提交</div></td>';
					}else if(homeworkinfolist[i].courseHomeworkRecord.status=='1'){
						newRow += '<td width="8%"><div class="gray hwStatus">已经提交</div></td>';
					}else if(homeworkinfolist[i].courseHomeworkRecord.status=='2'||'3'){
						newRow += '<td width="8%"><div class="gray hwStatus">已经批改</div></td>';
					}
				}
//				if(homeworkinfolist[i].courseHomeworkRecord.groupName==null){
//					newRow += '<td width="10%" class="gray"></td>';
//				}else{
//					newRow += '<td width="10%" class="gray" title='+homeworkinfolist[i].courseHomeworkRecord.groupName+')>'+cutStr(homeworkinfolist[i].courseHomeworkRecord.groupName,10)+'</td>';
//				}
//				if(homeworkinfolist[i].courseHomeworkInfo.homewkGroupNum==null){
//					newRow += '<td width="10%" class="gray">全体</td>';
//				}else{
//					newRow += '<td width="10%" class="gray" title='+homeworkinfolist[i].courseHomeworkInfo.homewkGroupNum+'>'+cutStr(homeworkinfolist[i].courseHomeworkInfo.homewkGroupNum,10)+'</td>';
//				}

				if(homeworkinfolist[i].courseHomeworkRecord.resourcesMappingByHomewkAffix==null){
					newRow += '<td width="8%" class="gray">'+0+'B</td>';
				}else{
					replyFileSize = homeworkinfolist[i].courseHomeworkRecord.resourcesMappingByHomewkAffix.fileSize;
					if(replyFileSize<1024){
						newRow += '<td width="8%" class="gray">'+replyFileSize+'B</td>';
					}else if(replyFileSize>=1024 && replyFileSize<1024*1024){
						newRow += '<td width="8%" class="gray">'+(replyFileSize/1024).toFixed(2)+'KB</td>';
					}else{
						newRow += '<td width="8%" class="gray">'+(replyFileSize/1024/1024).toFixed(2)+'MB</td>';
					}
				};

				newRow += '<td width="10%" class="gray">'+new Date(homeworkinfolist[i].courseHomeworkInfo.beginDate).format("yyyy-MM-dd hh:mm")+'</td>';
				newRow += '<td width="10%" class="gray">'+new Date(homeworkinfolist[i].courseHomeworkInfo.endDate).format("yyyy-MM-dd hh:mm")+'</td>';
				if(homeworkinfolist[i].courseHomeworkInfo.answerDetail!=null||homeworkinfolist[i].courseHomeworkInfo.answerLink!=null){//有答案
					newRow += '<td width="6%" align="center"><a href="javascript:void(0);" title="查看参考答案" class="icon-pencil-orange" onclick="stuHomework.getHwAnswer(this);"></a></td>';
				}else{
					newRow += '<td width="6%" align="center"><a href="javascript:void(0);" title="暂无参考答案" class="icon-pencil" onclick="stuHomework.getHwAnswer(this);"></a></td>';
				}
	//			newRow += '<td width="6%" align="center"><a href="" class="icon-pencil"></a></td>';
				if(locale=="en_US"){
					var currentDate = new Date();
					if(currentDate.format("yyyy-MM-dd hh:mm:ss") > new Date(homeworkinfolist[i].courseHomeworkInfo.endDate).format("yyyy-MM-dd hh:mm:ss")){
					 newRow += '<td width="10%"></td>';
				}else{
					 if(homeworkinfolist[i].courseHomeworkRecord.status=='2'||homeworkinfolist[i].courseHomeworkRecord.status=='3'){
						 newRow += '<td width="10%"><span class="upload-answer" style="color:#949494;"><div class="icon-upload-answer"></div>Submit a homework</a></td>';
					 }else{
						 newRow += '<td width="10%"><a href="/f/student/homework/hw_detail/' + courseId + '/' + homeworkinfolist[i].courseHomeworkInfo.homewkId + '" class="upload-answer" style="color:#e75344;"><div class="icon-upload-answer"></div>Submit a homework</a></td>';
					  }
				     }
					newRow += '<td width="10%"><a href="/f/student/homework/hw_result/'+courseId+ '/' + homeworkinfolist[i].courseHomeworkInfo.homewkId + '" class="review-hw"><div class="icon-review"></div>View marking</a></td>';
					newRow += '</tr>';
				}else{
				var currentDate = new Date();
				if(currentDate.format("yyyy-MM-dd hh:mm:ss") > new Date(homeworkinfolist[i].courseHomeworkInfo.endDate).format("yyyy-MM-dd hh:mm:ss")){
					 newRow += '<td width="10%"></td>';
				}else{
					 if(homeworkinfolist[i].courseHomeworkRecord.status=='2'||homeworkinfolist[i].courseHomeworkRecord.status=='3'){
						 newRow += '<td width="10%"><span  class="upload-answer" style="color:#949494;"><div class="icon-upload-answer"></div>提交作业</a></td>';
					 }else{
						 newRow += '<td width="10%"><a href="/f/student/homework/hw_detail/' + courseId + '/' + homeworkinfolist[i].courseHomeworkInfo.homewkId + '" class="upload-answer" style="color:#e75344;"><div class="icon-upload-answer"></div>提交作业</a></td>';
					 }

				}
				newRow += '<td width="10%"><a href="/f/student/homework/hw_result/'+courseId+ '/' + homeworkinfolist[i].courseHomeworkInfo.homewkId + '" class="review-hw" style="padding-left:25px;"><div class="icon-review"></div>查看批阅</a></td>';
				newRow += '</tr>';
				}
			if (i==0){
				$("#homeworklist").append(newRow);
			}
			else {
				$("#homeworklist tr:last").after(newRow);
			};
		}
	}
	$("#homeworklist tr:odd").addClass("gray-bg");
};

stuHomework.getHwAnswer = function(el){
	var nodeTr = $(el).closest("tr");
	var index = nodeTr.index();
	var answerDetail = list[index].courseHomeworkInfo.answerDetail;//答案说明
	var answerLink = list[index].courseHomeworkInfo.answerLink;//答案附件
	if(answerDetail==null){
		if(locale=="en_US"){
			$("#answerDetail").text("No description");
		}else{
			$("#answerDetail").text("暂无说明");
		}
	}else{
		$("#answerDetail").html(answerDetail);
	}
	if(answerLink==null){
		if(locale=="en_US"){
			$("#answerLink").text("No file");
		}else{
			$("#answerLink").text("暂无附件");
		}
		$("#answerLinkFilename").text('');
	}else{
		$("#answerLink").text("");
		$("#answerLinkFilename").text(list[index].courseHomeworkInfo.answerLinkFilename);
	}
	art.dialog({
		 content: document.getElementById('hwAnswer'),
		 closeOnEscape: false,
		 title:'查看参考答案',
		 lock:true,
		 initialize : function(){
			 $("#hwAnswer").removeClass("hidden");
			 $('.answerLink').val(answerLink);
		 },
		 lock:true,
		 okValue:"关闭",
		 ok: function(){
			 $("#hwAnswer").addClass("hidden");
			 this.close();
		 }
	});
};


//下载文件
stuHomework.downloadFile = function(){
	var fileId = $('.answerLink').val();//答案附件
	$.ajax({
		"type":'POST',
		"url":baseUrl+'/b/resource/downloadFile/'+fileId,
		"dataType":"json",
		"success":function(data){
			if(data[MESSAGE]==SUCCESS){
				window.location.href = data.result;
			}else if(data[MESSAGE]==FAILURE){
				if (data.hasOwnProperty("error")){
					alert(data.error.msg);
				}else{
					alert("文件下载失败");
				}
			}
		},
		"async" : false
	});
};

//初始化
stuHomework.init = function(){
	$(".standord-nav a.homework").addClass("active");
	stuHomework.getlist();
};

$(function(){
	stuHomework.init();
});
