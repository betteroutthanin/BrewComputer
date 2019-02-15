// -----------------------------------------------------------------------------------------------------
function makeid()
{
    var text = "DataString=";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for( var i=0; i < 5; i++ )
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
}

// -----------------------------------------------------------------------------------------------------
function WebButton(Name)
{
	var xmlHttp = getXMLHttp();
	
	xmlHttp.onreadystatechange = function()
	{
		if(xmlHttp.readyState == 4)
		{			
		}
	}

	Command = "ButtonName="+Name;
	xmlHttp.open("GET", "Ajax_button.pax"+"?"+Command, true); 
	xmlHttp.send(null);
}

// -----------------------------------------------------------------------------------------------------
function RequestStatus(Command)
{    
	var xmlHttp = getXMLHttp();
	
	xmlHttp.timeout = 1000

	xmlHttp.onreadystatechange = function()
	{
		if(xmlHttp.readyState == 4)
		{
			RequestStatus_HandleResponse(xmlHttp.responseText);
		}
	}
	
	xmlHttp.ontimeout = function()
	{
		document.getElementById('errorstatus').innerHTML = '<font color="red">Connection Failed</font>';
	}

	var DataString = makeid();

	xmlHttp.open("GET", Command, true);  
	xmlHttp.send(null);
}

// -----------------------------------------------------------------------------------------------------
function RequestStatus_HandleResponse(response)
{
	if (response != "")
	{
		document.getElementById('page_wrapper').innerHTML = response;
		document.getElementById('errorstatus').innerHTML = '<font color="green">Connection Good</font>';
	}
	else
	{
		document.getElementById('errorstatus').innerHTML = '<font color="red">Connection Failed</font>';
	}
}

// -----------------------------------------------------------------------------------------------------
function getXMLHttp()
{
	var xmlHttp

	try
	{
		//Firefox, Opera 8.0+, Safari
		xmlHttp = new XMLHttpRequest();
	}
	catch(e)
	{
		//Internet Explorer
		try
		{
			xmlHttp = new ActiveXObject("Msxml2.XMLHTTP");
		}
		catch(e)
		{
			try
			{
				xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
			}
			catch(e)
			{
				alert("Your browser does not support AJAX!")
				return false;
			}
		}
	}
	return xmlHttp;
}