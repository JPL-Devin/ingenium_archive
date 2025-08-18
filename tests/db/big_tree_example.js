'use strict';

const uuid = require('node-uuid');
var fns = require('./db_functions.js');

var database_name = 'ingenium_test';

var id_execution_1 = 'id_execution_1';


function add_section(i, max_count, id_prefix, insert_after_id, level) {
  console.log('add_section i: %s max_count: %s', i, max_count);

  if (i < 0) {
    return Promise.resolve(i);
  }

  let elem_id = id_prefix + i
  let elem = {
    '_key': elem_id,
    'elem_id': elem_id,
    'elem_type': 'SECTION',
    'execution_id': id_execution_1,
    'description': elem_id
  }

  // create a branch of promise chain
  return fns.addElement(id_execution_1, elem, insert_after_id, level)
  .then(
    function(res) {
      // console.log('updated_numbers: ', JSON.stringify(res));
      return add_section(i-1, max_count, id_prefix, insert_after_id, level);
    }
  );
}

function add_step(i, max_count, id_prefix, insert_after_id, level) {
  console.log('add_section i: %s max_count: %s', i, max_count);

  if (i < 0) {
    return Promise.resolve(i);
  }

  let elem_id = id_prefix + i
  let elem = {
    '_key': elem_id,
    'elem_id': elem_id,
    'elem_type': 'STEP',
    'execution_id': id_execution_1,
    'description': elem_id
  }

  // create a branch of promise chain
  return fns.addElement(id_execution_1, elem, insert_after_id, level)
  .then(
    function(res) {
      // console.log('updated_numbers: ', JSON.stringify(res));
      return add_step(i-1, max_count, id_prefix, insert_after_id, level);
    }
  );
}

console.time('main');

let size = 20;

fns.dropDB(database_name)
.then((res) => {
    return fns.setupDB(database_name)
  }, (err) => {
    console.error(err)
})
.then((res) => {
    let id = id_execution_1;
    let execution = {
      '_key': id,
      'id': id,
      'venue_id': 'venue_1',
      'description': 'My big execution'
    }
    return fns.addExecution(execution);
  }
)
.then((res) => {
    return add_section(size-1, size, 'id_section_', '-1', 'CHILD');
  }
)
.then((res) => {
    let promises = [];

    for (let i=0; i < size; i++) {
      promises.push(add_section(size-1, size, 'id_section_' + i + '_', 'id_section_' + i, 'CHILD'))
    }

    return Promise.all(promises);
  }
)
.then((res) => {
    let promises = [];

    for (let i1=0; i1 < size; i1++) {
      for (let i2=0; i2 < size; i2++) {
        promises.push(add_step(size-1, size, 'id_step_' + i1 + '_' + i2 + '_', 'id_section_' + i1 + '_' + i2, 'CHILD'))
      }
    }

    return Promise.all(promises);
  }
)


/*
.then((res) => {
    return add_section(0, 1, 'id_section0_', '', 'CHILD', true);
  }
)
.then((res) => {
    return add_section(0, 1, 'id_section1_', '', 'CHILD', false);
  }
)
*/
.then(()=>{
  console.log('getAsRun()');
  return fns.getAsRun('execution/' + id_execution_1, 'big_as_run_created.json');
})
.then((res)=>{
    console.info('Done: ');
    console.timeEnd('main');
})
.catch((err)=>{
    console.info('Error:', err);
});
