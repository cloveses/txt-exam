$(function(){
	$("#pageup").attr("disabled","disabled");
	$("#pagedown").attr("disabled","disabled");
    $("#select").click(function(){
		var test_type,key,tid;
		test_type = $(":input[name='test_type']").val();
		if (test_type=='1' || test_type=='3') {
			if (! $.isEmptyObject($(':input:radio:checked'))) {
				key=$(':input:radio:checked').val();
				tid = $(":input[name='test_tid']").val();
				$.get('/gettest/1/1',{kt_type:test_type,kt_tid:tid,key:key},function(data){$("#test").html(data);});
			}else{
				$.get('/gettest/1/1',function(data){$("#test").html(data);});
			};
		}else{
			if ( $(":input[name='key_input']").val()) {
				key=$(":input[name='key_input']").val();
				tid = $(":input[name='test_tid']").val();
				$.get('/gettest/1/1',{kt_type:test_type,kt_tid:tid,key:key},function(data){$("#test").html(data);});
			}else{
				$.get('/gettest/1/1',function(data){$("#test").html(data);});
			};
		};
		//$.get('/gettest/1/1',function(data){$("#test").html(data);});
		$("#select").attr("disabled","disabled");
		$("#fill").removeAttr("disabled");
		$("#yorn").removeAttr("disabled");
		$("#pageup").removeAttr("disabled");
		$("#pagedown").removeAttr("disabled");});
    $("#fill").click(function(){
		var test_type,key,tid;
		test_type = $(":input[name='test_type']").val();
		if (test_type=='1' || test_type=='3') {
			if (! $.isEmptyObject($(':input:radio:checked'))) {
				key=$(':input:radio:checked').val();
				tid = $(":input[name='test_tid']").val();
				$.get('/gettest/2/1',{kt_type:test_type,kt_tid:tid,key:key},function(data){$("#test").html(data);});
			}else{
				$.get('/gettest/2/1',function(data){$("#test").html(data);});
			};
		}else{
			if ( $(":input[name='key_input']").val()) {
				key=$(":input[name='key_input']").val();
				tid = $(":input[name='test_tid']").val();
				$.get('/gettest/2/1',{kt_type:test_type,kt_tid:tid,key:key},function(data){$("#test").html(data);});
			}else{
				$.get('/gettest/2/1',function(data){$("#test").html(data);});
			};
		};
		//$.get('/gettest/2/1',function(data){$("#test").html(data);});
		$("#fill").attr("disabled","disabled");
		$("#select").removeAttr("disabled");
		$("#yorn").removeAttr("disabled");
		$("#pageup").removeAttr("disabled");
		$("#pagedown").removeAttr("disabled");});
    $("#yorn").click(function(){
				var test_type,key,tid;
		test_type = $(":input[name='test_type']").val();
		if (test_type=='1' || test_type=='3') {
			if (! $.isEmptyObject($(':input:radio:checked'))) {
				key=$(':input:radio:checked').val();
				tid = $(":input[name='test_tid']").val();
				$.get('/gettest/3/1',{kt_type:test_type,kt_tid:tid,key:key},function(data){$("#test").html(data);});
			}else{
				$.get('/gettest/3/1',function(data){$("#test").html(data);});
			};
		}else{
			if ( $(":input[name='key_input']").val()) {
				key=$(":input[name='key_input']").val();
				tid = $(":input[name='test_tid']").val();
				$.get('/gettest/3/1',{kt_type:test_type,kt_tid:tid,key:key},function(data){$("#test").html(data);});
			}else{
				$.get('/gettest/3/1',function(data){$("#test").html(data);});
			};
		};
		//$.get('/gettest/3/1',function(data){$("#test").html(data);});
		$("#yorn").attr("disabled","disabled");
		$("#fill").removeAttr("disabled");
		$("#select").removeAttr("disabled");
		$("#pageup").removeAttr("disabled");
		$("#pagedown").removeAttr("disabled");});

	$("#pageup").click(function(){
		var key,test_type,t_no,tid;
		test_type = $(":input[name='test_type']").val();
		t_no = parseInt($(":input[name='test_no']").val())-1;
		if (t_no > 0) {
			if (test_type=='1' || test_type=='3') {
				tid = $(":input[name='test_tid']").val();
				if (! $.isEmptyObject($(':input:radio:checked'))) {
					key=$(':input:radio:checked').val();
					$.get('/gettest/'+test_type+'/'+t_no,{kt_type:test_type,kt_tid:tid,key:key},function(data){$("#test").html(data);});
				}else{
					$.get('/gettest/'+test_type+'/'+t_no,function(data){$("#test").html(data);});
				}
			}else{
				if ( $(":input[name='key_input']").val()) {
				key=$(":input[name='key_input']").val();
				tid = $(":input[name='test_tid']").val();
					$.get('/gettest/'+test_type+'/'+t_no,{kt_type:test_type,kt_tid:tid,key:key},function(data){$("#test").html(data);});
				}else{
					$.get('/gettest/'+test_type+'/'+t_no,function(data){$("#test").html(data);});
				}
			};
		}else{
			if (test_type=='1' || test_type=='3') {
				tid = $(":input[name='test_tid']").val();
				if (! $.isEmptyObject($(':input:radio:checked'))) {
					key=$(':input:radio:checked').val();
					$.get('/gettest/'+test_type+'/'+t_no,{kt_type:test_type,kt_tid:tid,key:key});
				}
			}else{
				if ( $(":input[name='key_input']").val()) {
				key=$(":input[name='key_input']").val();
				tid = $(":input[name='test_tid']").val();
					$.get('/gettest/'+test_type+'/'+t_no,{kt_type:test_type,kt_tid:tid,key:key});
				}
			};
			alert("已经是第一题，没有上一题！");
			$("#pageup").attr("disabled","disabled");
			
		};
		$("#pagedown").removeAttr("disabled");
			});
	$("#pagedown").click(function(){
		var key,test_type,t_no,tid,t_no_max;
		test_type = $(":input[name='test_type']").val();
		t_no = parseInt($(":input[name='test_no']").val())+1;
		t_no_max = parseInt($(":input[name='test_num']").val());
		if (test_type=='1' || test_type=='3') {
			tid = $(":input[name='test_tid']").val();
			if (! $.isEmptyObject($(':input:radio:checked'))) {
				key=$(':input:radio:checked').val();
				$.get('/gettest/'+test_type+'/'+t_no,{kt_type:test_type,kt_tid:tid,key:key},function(data){$("#test").html(data);});
			}else{
				$.get('/gettest/'+test_type+'/'+t_no,function(data){$("#test").html(data);});
			}
		}else{
			if ( $(":input[name='key_input']").val()) {
			key=$(":input[name='key_input']").val();
			tid = $(":input[name='test_tid']").val();
				$.get('/gettest/'+test_type+'/'+t_no,{kt_type:test_type,kt_tid:tid,key:key},function(data){$("#test").html(data);});
			}else{
				$.get('/gettest/'+test_type+'/'+t_no,function(data){$("#test").html(data);});
			}
		};		

		$("#pageup").removeAttr("disabled");
		if (t_no==t_no_max) {$("#pagedown").attr("disabled","disabled");};
			});
	$("#handpaper").click(function(){
		var test_type,key,tid;
		test_type = $(":input[name='test_type']").val();
		if (test_type=='1' || test_type=='3') {
			if (! $.isEmptyObject($(':input:radio:checked'))) {
				key=$(':input:radio:checked').val();
				tid = $(":input[name='test_tid']").val();
				$.get('/gettest/1/1',{kt_type:test_type,kt_tid:tid,key:key});
				$.get('/submit',function(data){$("#test").html(data);});
			}else{
				$.get('/submit',function(data){$("#test").html(data);});
			};
		}else{
			if ( $(":input[name='key_input']").val()) {
				key=$(":input[name='key_input']").val();
				tid = $(":input[name='test_tid']").val();
				$.get('/gettest/1/1',{kt_type:test_type,kt_tid:tid,key:key});
				$.get('/submit',function(data){$("#test").html(data);});
			}else{
				$.get('/submit',function(data){$("#test").html(data);});
			};
		};
		//$.get('/gettest/1/1',function(data){$("#test").html(data);});
		$("#select").attr("disabled","disabled");
		$("#fill").attr("disabled","disabled");
		$("#yorn").attr("disabled","disabled");
		$("#pageup").attr("disabled","disabled");
		$("#pagedown").attr("disabled","disabled");
		$("#handpaper").attr("disabled","disabled");
		alert('考试结束!');
		window.open('','_parent','');
		window.close();});
		
	})