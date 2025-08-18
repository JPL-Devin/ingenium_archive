const uuid = require('node-uuid');
var arangojs = require('arangojs');
var db = arangojs('http://localhost:8529');
db.useBasicAuth('root', 'somepassword');
var fns = require('./db_functions.js');

var database_name = 'ingenium_test';
var graph_name = 'ingenium_graph';

var id_execution_1 = 'id_execution_1';
var id_section_1 = 'id_section_1';

Promise.resolve()
.then((res) => {
    return fns.useDB(database_name);
})

/*
.then((res) => {
    let elem = {
      '_key': 'id_section_new1',
      'id': 'id_section_new1',
      'elem_type': 'SECTION',
      'execution_id': id_execution_1,
      'description': 'Section-new1'
    }
    return fns.addElement(id_execution_1, elem, 'id_section_1', 'SIBLING', false);
  }
)
*/
/*
.then((res) => {
    return fns.traversalTest(database_name);
})

.then((res) => {
    return fns.traversalQueryTest('execution/' + id_execution_1);
})

.then((res) => {
    return fns.deleteElement(id_section_1);
})
*/

/*
.then((res) => {
    return fns.getAsRun('execution/' + id_execution_1, 'as_run_new.json');
})
*/
.then((res) => {
    return fns.shortedPathTest('element/id_step_2_2', 'element/id_step_3_1');
})
.then((res) => {
    console.log('DONE:', res);
  }, (err) => {
    console.log('ERROR:', err)
})

/*
.then((res) => {
    return fns.deleteExecution(id_execution_1);
})

.then((res) => {
    return fns.collectionQueryTest(database_name);
})
*/
