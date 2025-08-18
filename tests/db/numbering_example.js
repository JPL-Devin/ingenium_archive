

function setNumbers(node) {
  node.children.forEach(function(child, idx) {
    node_number = node.hasOwnProperty('number') ? node['number'] : '';

    if (node_number == '') {
      child['number'] = String(idx+1);
    }
    else {
      child['number'] = [node['number'], (idx+1)].join('-');
    }
    setNumbers(child);
  });
}

var fsp = require('fs-promise');
var obj;

fsp.readFile('execution.json', 'utf8')
  .then((data)=>{
      return new Promise(function(resolve, reject) {
        execution = JSON.parse(data);
        console.log('execution:', JSON.stringify(execution, 0, 2));
        resolve(execution);
      });
  })
  .then((execution)=>{
      return new Promise(function(resolve, reject) {
        setNumbers(execution);
        console.log('execution_numbered:', JSON.stringify(execution, 0, 2));
        resolve(execution);
      });
  })
  .then((execution)=>{
      return new Promise(function(resolve, reject) {
        var fs = require('fs');
        fsp.writeFile("execution_numbered.json", JSON.stringify(execution, 0, 2), function(err) {
          if(err) {
            return console.log(err);
          }
          resolve(execution);
        });
      });
  });
