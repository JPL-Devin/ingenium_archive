// A graph traversal example for Arango DB.
// USAGE: $ npm install
//        $ node traverse_example.js
//
// 1) It will create "ingenium_db_test" db if it does not exist. Then it creates a graph, add verticies and edges.
// A traverse query is made to get hierarchical json structure of an "execution".
// 2) If "ingenium_db_test" db exists, it will be dropped. This is done to reset the database for the next run.

var arangojs = require('arangojs');
var db = arangojs('http://localhost:8529');
var database_name = 'ingenium_db_test';
const uuid = require('uuid/v4');

db.useBasicAuth('root', 'somepassword');
console.log('Run script');
db.listDatabases()
  .then((names)=> {
    if (names.indexOf(database_name) > -1) {
      db.dropDatabase(database_name);
      console.log('Database dropped:', database_name);
      // db.useDatabase(database_name);
      //  console.log('Using database:', database_name);
    } else {
      db.createDatabase(database_name)
      .then((res)=>{
          console.log('Database was created:', res);
          db.useDatabase(database_name);
          console.log('Use database:', database_name);
      })
      .then(()=>{
          return new Promise(function(resolve, reject) {
            db.graph('execution-graph').create({
              edgeDefinitions: [
                  {
                      collection: 'stepOrder',
                      from: [
                          'execution',
                          'element'
                      ],
                      to: [
                          'element'
                      ]
                  }
              ]
            })
            .then((res) => {
              console.log('Graph created:', res);
              resolve(res);
            });
          });
      })
      .then(()=>{
          return new Promise(function(resolve, reject) {
            let execution_id = 'ex1';
            var graph = db.graph('execution-graph');
            var collection = graph.vertexCollection('execution');

            collection.save({
              '_key': execution_id,
              'name': 'first execution',
              'execution_id': execution_id
            })
            .then((res) => {
              console.log('Execution created:', res);
              resolve(res);
            });
          });
      })
      .then(()=>{
          return new Promise(function(resolve, reject) {
            let elems =
              [
                {'_key': 's1', 'name': 'section-1'},
                {'_key': 's2', 'name': 'section-2'},
                {'_key': 's3', 'name': 'section-3'},
                {'_key': 'st1', 'name': 'step-1'},
                {'_key': 'st2', 'name': 'step-2'},
                {'_key': 'st1-1', 'name': 'step-1-1'},
                {'_key': 'st1-2', 'name': 'step-1-2'},
                {'_key': 'st1-3', 'name': 'step-1-3'},
                {'_key': 'st2-1', 'name': 'step-2-1'},
                {'_key': 'st2-2', 'name': 'step-2-2'},
                {'_key': 'st3-1', 'name': 'step-3-1'}
              ];
            db.collection('element').import(elems)
            .then((res) => {
              console.log('elements imported:', res);
              resolve(res);
            });
          });
      })
      .then(()=>{
          return new Promise(function(resolve, reject) {
            let edges =
              [
                {'_key': 'e-c1', '_from': 'execution/ex1', '_to': 'element/s1', 'type': 'child'},
                {'_key': 'e-c2', '_from': 'element/s1', '_to': 'element/st1-1', 'type': 'child'},
                {'_key': 'e-c3', '_from': 'element/s2', '_to': 'element/st2-1', 'type': 'child'},
                {'_key': 'e-c4', '_from': 'element/s3', '_to': 'element/st3-1', 'type': 'child'},
                {'_key': 'e-s1', '_from': 'element/s1', '_to': 'element/s2', 'type': 'sibling'},
                {'_key': 'e-s2', '_from': 'element/s2', '_to': 'element/s3', 'type': 'sibling'},
                {'_key': 'e-s3', '_from': 'element/st1-1', '_to': 'element/st1-2', 'type': 'sibling'},
                {'_key': 'e-s4', '_from': 'element/st1-2', '_to': 'element/st1-3', 'type': 'sibling'},
                {'_key': 'e-s5', '_from': 'element/st2-1', '_to': 'element/st2-2', 'type': 'sibling'}
              ];
            db.collection('stepOrder').import(edges)
            .then((res) => {
              console.log('stepOrder edges imported:', res);
              resolve(res);
            });
          });
      })
      .then(()=>{
          return new Promise(function(resolve, reject) {
            var graph = db.graph('execution-graph');
            graph.traversal('execution/ex1', {
              direction: 'outbound',
              // strategy: 'breadthfirst',
              init: `
              result.dict = {};
              result.execution = null;
              // result.edges=[];
              `
              ,
              visitor:
              `
              if (result.execution === null) {
                result.execution = vertex;
              }

              if (result.dict.hasOwnProperty(vertex._id)) {
                // TODO: this should not happen. Handle error.
              } else {
                vertex.children = [];
                result.dict[vertex._id] = vertex;
              }
              var edges = path.edges;
              var last_edge = edges.length > 0 ? edges[edges.length-1] : null;
              if (last_edge != null) {
                // result.edges.push(last_edge);
                if (last_edge.type == 'child') {
                  var parent = result.dict[last_edge._from];
                  vertex.parent_id = parent._id;
                  parent.children.push(vertex);
                } else if (last_edge.type == 'sibling') {
                  var sibling_id = last_edge._from;
                  var sibling = result.dict[sibling_id];
                  vertex.parent_id = sibling.parent_id;
                  var parent = result.dict[sibling.parent_id];
                  parent.children.push(vertex);
                }
              }
              `
            })
            .then((res) => {
              console.log('Graph traversal result:', JSON.stringify(res, 0, 2));

              var fs = require('fs');
              fs.writeFile("execution.json", JSON.stringify(res.execution, 0, 2), function(err) {
                  if(err) {
                      return console.log(err);
                  }
              });

              // set numbers
              setNumbers(res.execution);

              fs.writeFile("execution_numbered.json", JSON.stringify(res.execution, 0, 2), function(err) {
                  if(err) {
                      return console.log(err);
                  }
              });
              resolve(res.execution);
            });
          });
      })
      .then(()=>{
          console.info('Done.');
      })
      .catch((ex)=>{
          console.info('Error:', ex);
      });
    }
  }
);


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
