/*
 * courseFiles.js
 * Copyright (C) 2017 Yongwen Zhuang <zeoman@163.com>
 *
 * Distributed under terms of the MIT license.
 */
/**
 * 学生课程文件新版
 */
var courseware = new Object;
var courseSource="0";//课程来源于课堂
var coursewareTreeList;//所有课程结构数据


/**
 * 取String 或者 object的长度
 *
 * */
function count(o){
    var t = typeof o;
    if(t == 'string'){
            return o.length;
    }else if(t == 'object'){
            var n = 0;
            for(var i in o){
                    n++;
            }
            return n;
    }
    return false;
};

//获取课程结构所有数据
courseware.getCoursewareTreeData = function(){
	$.ajax({
		"type" : 'POST',
		"url" : baseUrl+"/b/myCourse/tree/getCoursewareTreeData/"+courseId+'/'+courseSource,
		"dataType" : "json",
		"success" : function(data){
			var courTreeData= data.resultList;
			if(data[MESSAGE]==SUCCESS && count(courTreeData)===0){
				$(".parent-node-list").empty().siblings().remove();//冗余内容删除
			}else{
				coursewareTreeList = _sort(courTreeData);
				courseware.renderData();
			}
		},
		async:false
	});
};
courseware.addStatusForYidu=function(){
	$.ajax({
		"type" : 'POST',
		"url" : baseUrl+"/b/courseFileAccess/markStatusforYiDu/"+courseId,
		"dataType" : "json",
		"success" :function(data){
			if(data[MESSAGE] == SUCCESS){
				alert('一键已读成功');
			}else {
				alert('一键已读失败');
			};
		}
	});
},

//下载文件
_downloadFile = function(fileId,thisEl,fileType,resId){
	if(fileType=='video'&&(resId.indexOf("disk"))!=0){
		if(locale == "en_US"){
			alert('Not available for download');
		}else{
			alert('此课件为视频文件，不提供下载');
		}
	}else{
		$.ajax({
			"type":'POST',
			"url":baseUrl+'/b/resource/downloadFile/'+fileId,
			"dataType":"json",
			"success":function(data){
				if(data[MESSAGE]==SUCCESS){
					window.location.href = data.result;
					//点击数加1
					var downloadNum = $(thisEl).parent().siblings(".downloadNum").text();
					$(thisEl).parent().siblings(".downloadNum").text(parseInt(downloadNum)+1);
				}else if(data[MESSAGE]==FAILURE){
					if (data.hasOwnProperty("error")){
						alert(data.error.msg);
					}else{
						if(locale == "en_US"){
							alert('Download failed');
						}else{
							alert("文件下载失败");
						}
					}
				}
			}
		});
	}
};

//文件分类显示：文档，视频，一般文件，分别用不同的图标展示
_getFileType = function(fileTpye){
	var newfileTpye =  $.trim(fileTpye).toLowerCase();
	switch(newfileTpye){
	case 'flv': case 'mp4': case 'wmv': case 'asf': case 'asx': case 'rm': case 'rmvb':
	case 'mpg': case 'mpeg': case 'mpe': case '3gp': case 'mov':
	case 'm4v': case 'avi': case 'dat': case 'mkv': case 'vob':
		return 'video';
	case 'docx': case 'doc': case  'ppt': case  'pptx': case 'xls': case  'xlsx': case  'txt': case 'pdf':
		return 'doc';
	default:
		return 'other';
	}
};

//播放文件
_playFile = function(vplayurl,fileId,type,resId){//注:fileId和resId是resourceMapping表里面的2个字段,不要弄混了
	if(type=='video'&& (resId.indexOf("disk"))>-1){
		if(locale == "en_US"){
			alert('Not available for play, please download it');
		}else{
			alert("此文件不提供播放，请尝试下载");
		}
	}else if(type=='video'){
		$.ajax({
			"type":'GET',
			"url":baseUrl+'/b/video/getVideoInfo/'+resId+"/"+courseId,//获取视频转码状态
			"dataType":"json",
			"success":function(data){
				if(data[MESSAGE]==SUCCESS){
					if(data.result==null){
						if(locale == "en_US"){
							$("#playVoD").empty().append("<p class='course-num'>Not available for play immediate, please wait for it</p>");
						}else{
							$("#playVoD").empty().append("<p class='course-num'>正在转码中，暂不提供播放</p>");
						}
						_loadplaydialog();
					}else{
						$("#playVideo").removeClass("hidden");
						_loadVideodialog();
						$("#playVideo a").css("display","block");
						flowplayer("player", "http://v.cic.tsinghua.edu.cn/player/flowplayer.swf",{
							clip: {
								url: data.result.fullUrl,
								scaling: 'fit',
								provider: 'lighttpd'
							},
							plugins: {
								lighttpd: {
									url: "flowplayer.pseudostreaming.swf"
								}
							}
						});
						$("#playVideo a:eq(1)").removeAttr("style");
					}
				}
			}
		});
	}else if(type=='doc'){
		$("#playVoD").load(baseUrl+"/f/play/gotoDocPaly/notStuCourseware",{'resourceId':fileId},function(response,status,xhr){
			if('success' == status){
				_loadplaydialog();
			}
		});
	}else{
		if(locale == "en_US"){
			alert('Not available for play');
		}else{
			alert("该文件暂不支持播放!");
		}
	}


	//加载视频播放窗口
	_loadVideodialog = function(){
		art.dialog({
			id:'loadplaydialog',
			title:'播放',
			content:document.getElementById('playVideo'),
			lock: true,
			drag: true,
			width:800,
			height:600,
			cancelValue: '关闭',
			cancel: function() {
			 $("#playVideo").addClass("hidden");
			}
		});
	};

/*	switch(type){
	case 'video':
		$.ajax({
			"type":'GET',
			"url":baseUrl+'/b/video/getVideoInfo/'+resId,//获取视频转码状态
			"dataType":"json",
			"success":function(data){
				if(data[MESSAGE]==SUCCESS){
					if(data.result==null){
						$("#playVoD").empty().append("<p class='course-num'>正在转码中，暂不提供播放</p>");
						_loadplaydialog();
					}else{
						$("#playVoD").empty().load(baseUrl+"/f/play/gotoVideoPaly",{'videoPlayUrl':data.result.relativeUrl},function(response,status,xhr){
							if('success' == status){
								_loadplaydialog();
							}
						});
					}
				}
			}
		});
		break;
	case 'doc':
		$("#playVoD").load(baseUrl+"/f/play/gotoDocPaly/notStuCourseware",{'resourceId':fileId},function(response,status,xhr){
			if('success' == status){
				_loadplaydialog();
			}
		});
		break;
	default:
		alert("该文件暂不支持播放!");
	}*/
	//}
};

//加载播放窗口
_loadplaydialog = function(){
	art.dialog({
		id:'loadplaydialog',
		title:'播放',
		content:document.getElementById('playVoD'),
		lock: true,
		id:"play-dialog",
		drag: true,
		width:800,
		height:600,
		cancelValue: '关闭',
		cancel: true
	});
	if(locale == "en_US"){
		$(artDialog.get("play-dialog").dom.buttons[0]).find("input:first").val("Close");
		art.dialog({id: 'play-dialog'}).title('Play');
	}
};

//设置文件类型图标（可以和_playFile方法合并）
_setFileTypeIcon = function(ftype,thisEl){
	switch(type){
	case 'video':
		break;
	case 'doc':
			//todo
		break;
	default:
		//todo
	}
};

_sort = function(obj){//按照position排序方法
	var jsonList = [];
	var returnList = [];
	for(var i in obj){
		var json = {'nodeId':i,'position':obj[i].position};
		jsonList.push(json);
	}
	jsonList.sort(_upSort);
	for (var j=0; j<jsonList.length; j++){
		returnList.push(obj[jsonList[j].nodeId]);
	}
	return returnList;
};
_upSort = function(a, b){//升序排序
	return a["position" ] > b["position" ] ? 1 : a["position"] == b[ "position"] ? 0 : -1;
};
_downSort = function(a, b){//降序排序
	return a["position" ] < b["position" ] ? 1 : a["position"] == b[ "position"] ? 0 : -1;
};


courseware.batchDownload = function(){
	window.location.href=baseUrl + "/b/courseCourseware/batchDownload/"+courseId;
};

//render-数据
courseware.renderData = function(){
	$(".parent-node-list").empty().siblings().remove();//冗余内容删除
	if(coursewareTreeList==''){
		if(locale=="en_US"){
			var $error = $("<p class='gray pt20 txtCenter ml20 f36'>No data</p>");
		}else{
			var $error = $("<p class='gray pt20 txtCenter ml20 f36'>暂无数据</p>");
		}
		$error.insertAfter($('.parent-node-list'));
	}else{
		for(var i=0;i<coursewareTreeList.length;i++){
			var row = $(".firstTemplate>li").clone(true);//一级节点模板
			row.find(".firstNodeName").text(coursewareTreeList[i].nodeName);//一级节点名称
			row.find(".children-node-list").attr('id','secondNodeBox'+coursewareTreeList[i].nodeId);//二级容器命名
			row.appendTo($('.parent-node-list'));//一级内容填充
			var secondNodeList = _sort(coursewareTreeList[i].childMapData);//二级节点数据
			for(var j=0;j<secondNodeList.length;j++){
				var secRow = $(".secondTemplate>li").clone(true);
				secRow.find(".secondNodeName").text(secondNodeList[j].courseOutlines.lastNodeName+"  "+secondNodeList[j].courseOutlines.title);//二级节点名称
//				secRow.find(".mainTeacher").text(secondNodeList[j].teacherInfoView.name);//二级节点主讲教师
				secRow.find(".addRes").bind('click',{nodeId:secondNodeList[j].courseOutlines.noteId,status:'add'},function(event){
					courseware.coursewareFn(event.data.nodeId,'',event.data.status);//新增课程资源
				});
				secRow.appendTo($('#secondNodeBox'+coursewareTreeList[i].nodeId));//二级内容填充
				secRow.find(".share-list").attr('id','fileList'+secondNodeList[j].courseOutlines.noteId);//三级文件容器命名
				_renderCoursewareList(secondNodeList[j].courseCoursewareList);
			}
		}
	}
	_slideNode();
};
//展开收缩事件
_slideNode = function(){
	var $clickNode = $('.clickNode');
	$clickNode.click(function(){
		if($(this).next('.children-node-list').is(":visible")){
			$(this).removeClass('down').next('.children-node-list').slideUp();
		}else{
			$(this).addClass('down').next('.children-node-list').slideDown();
			$(this).next('.children-node-list').find('.table-outer').slideDown();
		}
	});
	var $clickSecNode = $('.grandchild-node-list h6');
	$clickSecNode.click(function(){
		if($(this).next('.table-outer').is(":visible")){
			$(this).next('.table-outer').slideUp();
		}else{
			$(this).next('.table-outer').slideDown();
		}
	});
};
//render课程文件
_renderCoursewareList = function(coursewareList){
	for(var k=0;k<coursewareList.length;k++){
		var fileRow = $(".thirdTemplate tr").clone(true);
		fileRow.attr('id','file'+coursewareList[k].id);//主键id
		fileRow.find(".filePosition").text(k+1);//位序
		fileRow.find(".fileName").text(coursewareList[k].title).attr("title",coursewareList[k].detail);//文件名
		fileRow.find(".file-jysm").text(cutStr(coursewareList[k].detail==null?"":coursewareList[k].detail,40)).attr("title",coursewareList[k].detail);//简要说明
		if(coursewareList[k].resourcesMappingByFileId!==null){//文件大小
		if(coursewareList[k].resourcesMappingByFileId.fileSize==null){//文件大小
			fileRow.find(".fileSize").text('0B');
		}else{
			var fileSize = coursewareList[k].resourcesMappingByFileId.fileSize;
			if(fileSize<1024){
				fileRow.find(".fileSize").text(fileSize+'B');
			}else if(fileSize>=1024 && fileSize<1024*1024){
				fileRow.find(".fileSize").text((fileSize/1024).toFixed(2)+'KB');
			}else{
				fileRow.find(".fileSize").text((fileSize/1024/1024).toFixed(2)+'MB');
			}
		}
		fileRow.find(".fileUploadTime").text(_dateFormat(coursewareList[k].resourcesMappingByFileId.regDate));//上传时间
		fileRow.find(".fileUploader").text(coursewareList[k].regUser);//上传人
		fileRow.find(".downloadNum").text(coursewareList[k].resourcesMappingByFileId.downloadNum);//下载量
		if( _getFileType(coursewareList[k].resourcesMappingByFileId.extension) != 'video'){
			fileRow.find(".downloadFile").bind("click",{fileId:coursewareList[k].resourcesMappingByFileId.fileId,ftype:_getFileType(coursewareList[k].resourcesMappingByFileId.extension),resId:coursewareList[k].resourcesMappingByFileId.resourcesId},function(event){
				$.ajax({
					"type" : 'GET',
					"url" : baseUrl+"/b/courseFileAccess/markReadFile/"+event.data.fileId,
					"dataType" : "json",
					"success":function(data){
						if(data[MESSAGE]=SUCCESS){
						}
					}
				});
				_downloadFile(event.data.fileId,this,event.data.ftype,event.data.resId);
			});//下载文件
		}else{
			fileRow.find(".downloadFile").remove();
		}
//		if(_getFileType(coursewareList[k].resourcesMappingByFileId.extension)=='video'){//video
//			fileRow.find(".fileType").attr("title","视频").children(".fileTypeImg").attr("src",baseUrl+"/res/fzjx/images/teacher/zh_CN/movie.png");
//		}else if(_getFileType(coursewareList[k].resourcesMappingByFileId.extension)=='doc'){
//			fileRow.find(".fileType").attr("title","文档").children(".fileTypeImg").attr("src",baseUrl+"/res/fzjx/images/teacher/zh_CN/text.png");
//		}else{
//			fileRow.find(".fileType").attr("title","文件").children(".fileTypeImg").attr("src",baseUrl+"/res/fzjx/images/discuss/common/zh_CN/topicnew.gif");
//		}
		fileRow.find(".file-type").text($.trim(coursewareList[k].resourcesMappingByFileId.extension).toLowerCase());
		fileRow.find(".fileType").bind("click",{ftype:_getFileType(coursewareList[k].resourcesMappingByFileId.extension)},function(event){
			_setFileTypeIcon(event.data.ftype,this);
		});//文件类型
		if(_getFileType(coursewareList[k].resourcesMappingByFileId.extension) == 'doc' || _getFileType(coursewareList[k].resourcesMappingByFileId.extension) == 'video'){
			fileRow.find(".playFile").bind("click",{vurl:coursewareList[k].resourcesMappingByFileId.playUrl,fileId:coursewareList[k].resourcesMappingByFileId.fileId,resId:coursewareList[k].resourcesMappingByFileId.resourcesId,ftype:_getFileType(coursewareList[k].resourcesMappingByFileId.extension)},function(event){
				$.ajax({
					"type" : 'GET',
					"url" : baseUrl+"/b/courseFileAccess/markReadFile/"+event.data.fileId,
					"dataType" : "json",
					"success":function(data){
						if(data[MESSAGE]=SUCCESS){
						}
					}
				});
				_playFile(event.data.vurl,event.data.fileId,event.data.ftype,event.data.resId);
			});//播放文件
		}else{
			fileRow.find(".playFile").remove();
		}

		fileRow.find(".playFile").bind("click",{vurl:coursewareList[k].resourcesMappingByFileId.playUrl,fileId:coursewareList[k].resourcesMappingByFileId.fileId,resId:coursewareList[k].resourcesMappingByFileId.resourcesId,ftype:_getFileType(coursewareList[k].resourcesMappingByFileId.extension)},function(event){
			_playFile(event.data.vurl,event.data.fileId,event.data.ftype,event.data.resId);
		});//播放文件
		fileRow.find(".viewComment").bind("click",{fileId:coursewareList[k].resourcesMappingByFileId.fileId},function(event){
			_viewComment(courseId,event.data.fileId);
		});//查看评论
		fileRow.find(".position").val(coursewareList[k].position);//位序
		fileRow.appendTo("#fileList"+coursewareList[k].noteId);
	}
	}
};


$(function(){
	$(".standord-nav a.courseware").addClass("active");
	courseware.getCoursewareTreeData();
	$(".parent-node-list").find("li:first").find('.children-node-list').slideDown().end().find(".clickNode").addClass('down');
});

/**201504013课程文件**/
function expandAll(){
	$(".courseware-catalog").find(".children-node-list").slideDown().end().find('.table-outer').slideDown().end().find('.clickNode').addClass("down");
};

function shrinkAll(){
	$(".courseware-catalog").find(".children-node-list").slideUp().end().find('.table-outer').slideUp().end().find('.clickNode').removeClass("down");
};
