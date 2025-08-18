const uuid = require('node-uuid');
var arangojs = require('arangojs');
var db = arangojs('http://localhost:8529');
db.useBasicAuth('root', 'somepassword');
var fns = require('./db_functions.js');

var database_name = 'ingenium_test';
var graph_name = 'ingenium_graph'

Promise.resolve()
.then((res) => {
    return fns.useDB(database_name);
})
.then((res) => {
    // console.log('res:', res);
    let key = uuid.v4();
    let elem = {
      '_key': key,
      'id': key,
      'elem_type': 'SECTION',
      'execution_id': 'id_execution_1',
      'description': key
    }
    return fns.addElement('id_execution_1', elem, '', '', true);
  }
)

