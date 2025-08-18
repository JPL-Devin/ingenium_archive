var testArray = ["lol", {"phone" : ["rekt", "new", "word"]}, {"ayy": ["lmao"]}, {"fkk": ["ittt"]}]

var step_list = [
    {
      "c1dc9f5c-373b-4244-907d-c5d68b72340a": [
        "ef4ae6e4-3545-49ab-83be-cca9aed7d650",
        "b353805f-fc10-4407-a3dc-b29297f75e12",
      ]
    },
    {
    	"fab560e8-7108-42b3-9c35-3467ccce320a" : ["swag", {"yass" : ["rekt"]}]
    }
  ]

var avacado = require('arangojs')
var db = avacado("http://localhost:8529");
db.useDatabase("archive");
db.useBasicAuth("root", "somepassword");

var graph = db.graph('coregraph')

var graphTrav = function(){
	graph.traversal('exeMetadata/85b8691a-e823-403b-a3a7-95d50db41eb0', {
	  direction: 'outbound',
	  // strategy: 'breadthfirst',
	  init: `
	  result.dict = [];
	  result.execution = null;
	  result.edges=[];
	  result.sections=[];
	  `
	  ,
	  visitor:
	  `
	  if(vertex._id.indexOf("exeMetadata") > -1){
	  	result.execution = vertex;
	  }
	  var edges = path.edges;
	  var last_edge = edges.length > 0 ? edges[edges.length-1] : null;
	  if (last_edge != null) {
	  	result.edges.push(last_edge);
	    if (last_edge.relationship == "CHILD") {
    		var temp = result.dict
    		var num = temp.length.toString()
    		for(var i = 0; i < result.sections.length; i++){
    			num = num + "-1"
    			for(var j = 0; j < temp.length; j++){
    				if(temp[j]._id == result.sections[i]){
    					var numArray = num.split("-")
    					numArray[numArray.length-1] = (parseInt(numArray[numArray.length-1]) + j + 1).toString()
    					num = numArray.join("-")
    					temp = temp[j]['children']
    					break
    				}
    			}
    		}
    		var numArray = num.split("-")
    		numArray[numArray.length-1] = "1"
    		num = numArray.join("-")
    		vertex['number'] = num
    		temp.push(vertex)
	    } else if (last_edge.relationship == "SIBLING") {
	    	if(result.sections.length > 0){
	    		var temp = result.dict
	    		var num = temp.length.toString()
	    		for(var i = 0; i < result.sections.length; i++){
	    			if(last_edge._from == result.sections[i]){
	    				result.sections = result.sections.slice(0, i)
	    			}
	    			if(i < result.sections.length){
	    				num = num + "-1"
	    			}
	    			for(var j = 0; j < temp.length; j++){
	    				if(i < result.sections.length && temp[j]._id == result.sections[i]){
	    					var numArray = num.split("-")
    						numArray[numArray.length-1] = (parseInt(numArray[numArray.length-1]) + j + 1).toString()
    						num = numArray.join("-")
	    					temp = temp[j]['children']
	    					break
	    				}
	    			}
	    		}
	    		if(vertex.elem_type == "SECTION"){
		      		vertex["children"] = [];
		      		result.sections.push(vertex._id)
	    		}
	    		var numArray = num.split("-")
	    		numArray[numArray.length-1] = (temp.length + 1).toString()
	    		num = numArray.join("-")
	    		vertex['number'] = num
	    		temp.push(vertex)
	    	}
	    	else{
	    		var num = ((result.sections.length > 0) ? temp.length.toString() : "1")
	    		if(vertex.elem_type == "SECTION"){
		      		vertex["children"] = [];
		      		result.sections.push(vertex._id)
	    		}
	    		vertex['number'] = num
	    		result.dict.push(vertex)
	    	}
	    }
	  }
	  `
	 }, function(err, doc){
	 	console.log(err)
	 	console.log(doc['dict'][1])
	 })
}
// db.query('FOR doc IN exeMetadata LIMIT 0, 5 RETURN doc', {}, {"count":true}, function(err, vals){
// 	console.log(err)
// 	console.log(vals)
// });
var numberStep = function(key, steps, num, depth, currentSect, callback){
	for(var i = 0; i < steps.length; i++){
		if(steps[i] instanceof Object){
			var keyz = Object.keys(steps[i])
			if(keyz[0] == key){
				if(i != 0 && i + 1 < steps.length){
					if(steps[i-1] instanceof Object){
						if(steps[i+1] instanceof Object){
							callback(num, Object.keys(steps[i+1])[0], Object.keys(steps[i-1])[0])
						}
						else{
							callback(num, steps[i+1], Object.keys(steps[i-1])[0])
						}
					}
					else{
						if(steps[i+1] instanceof Object){
							callback(num, Object.keys(steps[i+1])[0], steps[i-1])
						}
						else
							callback(num, steps[i+1], steps[i-1])
					}
				}
				else if(i != 0 ){
					if(steps[i-1] instanceof Object){
						callback(num, null, Object.keys(steps[i-1])[0])
					}
					else{
						callback(num, null, steps[i-1])
					}
				}
				else if(i + 1 < steps.length){
					if(steps[i+1] instanceof Object){
						callback(num, Object.keys(steps[i+1])[0], null)
					}
					else{
						callback(num, steps[i+1], null)
					}
				}
				else{
					callback(num, null, null)
				}
			}
			else{
				var numArray = num.split(".")
				// console.log(num)
				// console.log(depth)
				depth = depth + 1
				if(numArray.length < depth){
					num = num + ".1"
				}
				numberStep(key, steps[i][keyz[0]], num, depth, keyz[0], callback)
				depth = depth - 1
				var numArray = num.split(".")
				numArray[depth-1] = (parseInt(numArray[depth-1]) + 1).toString()
				//numArray.splice(depth,numArray.length)
				numArray = numArray.splice(0,depth)
				num = numArray.join(".")
			}
		}
		else if(key == steps[i]){
			if(steps.length > i + 1){
				if(i != 0) {
					callback(num, ((steps[i+1] instanceof Object) ? Object.keys(steps[i+1])[0] : steps[i+1]), ((steps[i-1] instanceof Object) ? Object.keys(steps[i-1])[0] : steps[i-1]))
				}
				else{
					callback(num, ((steps[i+1] instanceof Object) ? Object.keys(steps[i+1])[0] : steps[i+1]), currentSect)
				}
			}
			else{
				if(i != 0){
					callback(num, null, ((steps[i-1] instanceof Object) ? Object.keys(steps[i-1])[0] : steps[i-1]))
				}
				else{
					callback(num, null, currentSect)
				}
			}
		}
		else{
			var numArray = num.split(".")
			numArray[depth-1] = (parseInt(numArray[depth-1]) + 1).toString()
			num = numArray.join(".")
		}
	}
}

var addToList = function(key, steps, newKey, replace, relationship, temp){
	var original = steps
	for(var i = 0; i < steps.length; i++){
		if(steps[i] instanceof Object){
			if(Object.keys(steps[i])[0] == key){
				if(replace == "move" && temp != undefined)
						newKey = temp
				if(relationship == "sibling"){
					steps.splice(i+1, 0, newKey)
					i = i + 1
				} else{
					steps[i][Object.keys(steps[i])[0]].splice(0, 0, newKey)
				}
			}
			else if(newKey == Object.keys(steps[i])[0] && replace == "move"){
				if(temp != undefined){
					steps.splice(i, 1)
					i = i - 1
				}
				else{
					addToList(key, original, newKey, replace, relationship, steps[i])
				}
			}
			else
				addToList(key, steps[i][Object.keys(steps[i])[0]], newKey, replace, relationship, temp)
		}
		else if(key == steps[i]){
			if(replace == "version"){
				steps[i] = newKey
				i = steps.length
			}
			else if(replace == "add" || replace == "move"){
				if(replace == "move" && temp != undefined)
					newKey = temp
				steps.splice(i+1, 0, newKey)
				i = i + 1
			}
		}
		else if(newKey == steps[i] && replace == "move"){
			if(temp != undefined){
				steps.splice(i, 1)
				i = i - 1
			}
			else{
				addToList(key, original, newKey, replace, relationship, steps[i])
			}
		}
	}
}
// numberStep("yass", step_list, "1", 1, "", function(num, post, prev){
// 	console.log(num)
// })
graphTrav()

// addToList("b353805f-fc10-4407-a3dc-b29297f75e12", step_list, "swag", "version", "SIBLING", undefined)
// console.log(step_list)

