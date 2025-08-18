var arangojs = require('arangojs');
var db = arangojs('http://localhost:8529');
var database_name = 'graph_db_test';
const uuid = require('uuid/v4');

db.useBasicAuth('root', 'somepassword');
console.log('Run script');
db.listDatabases()
  .then((names)=> {
    if (names.indexOf(database_name) > -1) {
      db.dropDatabase(database_name);
      console.log('Database dropped:', database_name);
    } else {
      db.createDatabase(database_name)
      .then((res)=>{
          console.log('Database was created:', res);
          db.useDatabase(database_name);
          console.log('Use database:', database_name);
      })
      .then(()=>{
          return new Promise(function(resolve, reject) {
            db.graph('executions-graph').create({
              edgeDefinitions: [
                  {
                      collection: 'children',
                      from: [
                          'executions',
                          'elements'
                      ],
                      to: [
                          'elements'
                      ]
                  },
                  {
                      collection: 'siblings',
                      from: [
                          'elements'
                      ],
                      to: [
                          'elements'
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
            var graph = db.graph('executions-graph');
            var collection = graph.vertexCollection('executions');

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
            db.collection('elements').import(elems)
            .then((res) => {
              console.log('Elements imported:', res);
              resolve(res);
            });
          });
      })
      .then(()=>{
          return new Promise(function(resolve, reject) {
            let edges =
              [
                {'_key': 'e-c1', '_from': 'executions/ex1', '_to': 'elements/s1'},
                {'_key': 'e-c2', '_from': 'elements/s1', '_to': 'elements/st1-1'},
                {'_key': 'e-c3', '_from': 'elements/s2', '_to': 'elements/st2-1'},
                {'_key': 'e-c4', '_from': 'elements/s3', '_to': 'elements/st3-1'},
              ];
            db.collection('children').import(edges)
            .then((res) => {
              console.log('Child edges imported:', res);
              resolve(res);
            });
          });
      })
      .then(()=>{
          return new Promise(function(resolve, reject) {
            let edges =
              [
                {'_key': 'e-s1', '_from': 'elements/s1', '_to': 'elements/s2'},
                {'_key': 'e-s2', '_from': 'elements/s2', '_to': 'elements/s3'},
                {'_key': 'e-s3', '_from': 'elements/st1-1', '_to': 'elements/st1-2'},
                {'_key': 'e-s4', '_from': 'elements/st1-2', '_to': 'elements/st1-3'},
                {'_key': 'e-s5', '_from': 'elements/st2-1', '_to': 'elements/st2-2'}
              ];
            db.collection('siblings').import(edges)
            .then((res) => {
              console.log('Sibling edges imported:', res);
              resolve(res);
            });
          });
      })
      .then(()=>{
          return new Promise(function(resolve, reject) {
            var graph = db.graph('executions-graph');
            var graph_vertex_collection = graph.vertexCollection('elements');

            graph_vertex_collection.remove('elements/s2')
            .then((res) => {
              console.log('Vertex removed:', JSON.stringify(res, 0, 2));
              resolve(res);
            });
          });
      })
      .then(()=>{
          return new Promise(function(resolve, reject) {
            var graph = db.graph('executions-graph');
            var collection = graph.vertexCollection('elements');

            collection.all()
            .then((res) => {
              console.log('elements:', JSON.stringify(res._result, 0, 2));
              resolve(res._result);
            });
          });
      })
      .then(()=>{
          return new Promise(function(resolve, reject) {
            var graph = db.graph('executions-graph');
            var graph_edge_collection = graph.collection('children');

            graph_edge_collection.all()
            .then((res) => {
              console.log('children edges:', JSON.stringify(res._result, 0, 2));
              resolve(res._result);
            });
          });
      })
      .then(()=>{
          return new Promise(function(resolve, reject) {
            var graph = db.graph('executions-graph');
            var graph_edge_collection = graph.collection('siblings');

            graph_edge_collection.all()
            .then((res) => {
              console.log('siblings edges:', JSON.stringify(res._result, 0, 2));
              resolve(res._result);
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
