//APPROVED LIBRARY REFERENCES
//--All other libraries are blocked during sandboxed code execution.
//--For more details, visit https://www.npmjs.com/ and search for the library name.
var httpRequest = require('request');
var xPath = require('xpath');
var xmlDOM = require('@xmldom/xmldom');
var parser = require('xml2js');



//CUSTOM PARAMETERS
//--This object contains the custom parameters entered in the Custom Parameters section of the Transport tab of the data feed.
//--To access a parameter later in the script, use the following formats:
//--    Normal Text:    params.parameterName      Example: params.username or params.password
//--    Special Chars:  params["parameterName"]   Example: params["u$ername"] or params["pa$$word"]
var params = context.CustomParameters;



//DATA FEED TOKENS
//--This object contains the data feed tokens set by the system. Examples: LastRunTime, LastFileProcessed, PreviousRunContext, etc..
//--NOTE: The tokens are READ ONLY by this script, save for the "PreviousRunContext" token, which is discussed later.
//--To access a token later in the script, use the following format:
//--    tokens.tokenName    Example: tokens.PreviousRunContext or tokens.LastRunTime  
var tokens = context.Tokens;



//************************************************************************//
//      Legacy user script could return data in "output" variable         //
//************************************************************************//



//PREPARE DATA OBJECTS
//--These objects contain the in-flight and final data from your script execution.
//--The intent is you .push() data into myDataArray as it comes back from requests.
//--Then, build the myDataArray into myDataString or myDataByteArray (depending on data size and/or developer preference).
var myDataArray = [];
var myDataString = "";  //256Mb data limit, approx 12 million fields
var myDataByteArray;    //2Gb data limit, approx 96 million fields
var myDataSet;



//******************//
//  YOUR CODE HERE  //
//******************//
//--Prepare your output by scripting the appropriate JavaScript process to gather your data.
//--As data comes back, .push() it into the myDataArray object.
//--When finished, assign the final data set back to the myDataString and myDataByteArray variables with the appropriate datatype.
//--NOTE: The following code is purely to provide example functions, token and parameter access, and module utilizations. It is non-functional by design.
function makeRequest(httpEndpoint, httpMethod, httpHeaders, callback) {
    httpRequest(
        {
            method: httpMethod,
            uri: httpEndpoint,
            headers: httpHeaders
        },
        function handleResponse(error, response, body) {
            if (response.statusCode == 200) {
                callback(body);
            }
            else {
                throw new Error("The request did not return a 200 (OK) status.\r\nThe returned error was:\r\n" + error);
            }
        }
    );
}

function processData(data) {
    myDataArray.push(data);
}

function jsonToXml(jsonData) {
    var bldrOpts = {
        headless: true,
        rootName: "ROOT",
        renderOpts: {
            'pretty': true,
            'indent': '    ',
            'newline': '\r\n',
            'cdata': true
        }
    }
    var responseBuilder = new parser.Builder(bldrOpts);
    return responseBuilder.buildObject(jsonData);
}

//DO THE WORK
var someURI = "https://system.company.com/api/allthedata?startID=" + tokens.PreviousRunContext + "&startDate=" + token.LastRunTime;
var someMethod = "GET";
var someHeaders = {
    username: params.user,
    password: params.password,
}
makeRequest(someURI, someMethod, someHeaders, ProcessData);

//FINALIZE THE DATA SETS
//--As a String
myDataString = jsonToXml(myDataArray).toString();
//--As a Byte Array
myDataByteArray = new Buffer(myDataString);

//*****************//
//  END YOUR CODE  //
//*****************//



//RSA ARCHER CALLBACK
//--Take the first data set that isn't empty, preferring the largest storage first. If both are empty, return no data.
myDataSet = myDataByteArray || myDataString || "";
//--Invoke the RSAArcher callback to return your data and PreviousRunContext token to RSA Archer.
callback(null, {
    //Return the data to RSA Archer
    output: myDataSet,
    //PreviousRunContext token value; 256 char limit. If omitted, the token is cleared.
    previousRunContext: "myContextVariable"
});



//************************************************************************//
//                      End of legacy user script                         //             
//************************************************************************//


//***********************************OR***********************************//


//************************************************************************//
// New user script could write data to disk at any point from the script  //
//************************************************************************//



//CREATE "ARCHEROUTPUTWRITER" OBJECT
//--This requires the type of response(JSON/XML/CSV) and according initParams for the object instantiation.
//--This is a singleton object, and will throw error if already instantiated once.
//--The intention to make it singleton is, forcing to have a single response type through out the script.
//--This object later will be used to call the "writeItem" function.
var outputWriter = context.OutputWriter.create("JSON", { RootObj: "results" });



//******************//
//  YOUR CODE HERE  //
//******************//
//--Prepare your output by scripting the appropriate JavaScript process to gather your data.
//--As data comes back, write it to disk by consuming "writeItem" function of outputWriter.
//--"writeItem" consumes one logical set of data at a time, don't forget to convert the response to a logical set of data before passing it.
//--NOTE: The following code is purely to provide example functions, token and parameter access, and module utilization. It is non-functional by design.
function makeRequest(httpEndpoint, httpMethod, httpHeaders, callback) {
    httpRequest(
        {
            method: httpMethod,
            uri: httpEndpoint,
            headers: httpHeaders
        },
        function handleResponse(error, response, body) {
            if (response.statusCode == 200) {
                callback(body);
            }
            else {
                throw new Error("The request did not return a 200 (OK) status.\r\nThe returned error was:\r\n" + error);
            }
        }
    );
}

function processData(data) {
    data.forEach(function (item) {
        outputWriter.writeItem(item);
    });
}

//DO THE WORK
var someURI = "https://system.company.com/api/allthedata?startID=" + tokens.PreviousRunContext + "&startDate=" + token.LastRunTime;
var someMethod = "GET";
var someHeaders = {
    username: params.user,
    password: params.password,
}
makeRequest(someURI, someMethod, someHeaders, ProcessData);

//*****************//
//  END YOUR CODE  //
//*****************//



//RSA ARCHER CALLBACK
//--Invoke the RSAArcher callback to return your PreviousRunContext token to RSA Archer.
callback(null, {
    //PreviousRunContext token value; 256 char limit. If omitted, the token is cleared.
    previousRunContext: "myContextVariable"
});



//************************************************************************//
//                        End of new user script                          //             
//************************************************************************//