function myelem (value, options) {
    var el = document.createElement("tr");
    var td_el = document.createElement("td");
    var td_text = document.createTextNode("test");
    td_el.appendChild(td_text);
    el.appendChild(td_el);
    //alert("myelem: "+value);
    return el;
}

function myvalue(elem, operation, value) {
    //alert("myvalue: "+value);
    if(operation === 'get') {
	return $(elem).val();
    } else if(operation === 'set') {
	$(elem).val(value);
    }
}

var food_name = jQuery("#food_caption").val();

jQuery("#addtree").jqGrid({
    url: '?q=tree',
    datatype: "json",
    treedatatype: "json",
    mtype: "GET",
    colNames:["id","组成部分", "包含添加剂"],
    colModel:[
	{name:'id',index:'id', width:1,hidden:true,key:true, editable:true},
	{name:'name',index:'name', width:100, editable:true},
	{name:'addis',index:'addis', width:350, align:"left",editable:true},
    ],

    jsonReader: {
	repeatitems: false,
    },
    height:'auto',
    width:800,
    pager : "#paddtree",
    ExpandColumn : 'name',
    editurl:'?q=submit',
//    caption: food_name,

});

function fn_editSubmit(response,postdata)
{
    var json=response.responseText; //in my case response text form server is "{status:ok, content:''}"
    var result=eval("("+json+")"); //create js object from server reponse
//    alert(result.status);
    if (result.status == 'ok') {
	return [true, "", null];
    }
    else {
	return [false, result.content, null];
    }
};

var editOptions={
    closeOnEscape: true,
    closeAfterEdit: true,
    closeAfterAdd: true,
    width:700,
    afterSubmit: fn_editSubmit};

var addOptions={
    closeOnEscape: true,
    closeAfterEdit: true,
    closeAfterAdd: true,
    width:700,
    afterSubmit: fn_editSubmit};

jQuery("#addtree").jqGrid('navGrid',"#paddtree", { edit: true, add:true, del:true, search: false }, editOptions, addOptions);

