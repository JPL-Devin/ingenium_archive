'use strict';

var fns = require('./db_functions.js');

var database_name = 'ingenium_test';

var id_execution_1 = 'id_execution_1';
var id_section_1 = 'id_section_1';
var id_section_2 = 'id_section_2';
var id_section_3 = 'id_section_3';
var id_section_4 = 'id_section_4';
var id_section_5 = 'id_section_5';
var id_section_5_1 = 'id_section_5_1';
var id_section_5_2 = 'id_section_5_2';
var id_section_6 = 'id_section_6';
var id_section_6_1 = 'id_section_6_1';
var id_section_6_2 = 'id_section_6_2';
var id_step_2_1 = 'id_step_2_1';
var id_step_2_2 = 'id_step_2_2';
var id_step_2_3 = 'id_step_2_3';
var id_step_3_1 = 'id_step_3_1';
var id_step_3_2 = 'id_step_3_2';
var id_step_4_1 = 'id_step_4_1';
var id_step_4_2 = 'id_step_4_2';
var id_step_4_3 = 'id_step_4_3';
var id_step_4_4 = 'id_step_4_4';
var id_step_4_5 = 'id_step_4_5';
var id_step_5_1_1 = 'id_step_5_1_1';
var id_step_5_1_2 = 'id_step_5_1_2';
var id_step_6_2_1 = 'id_step_6_2_1';
var id_step_6_2_2 = 'id_step_6_2_2';
var id_paragraph_1 = 'id_paragraph_1';
var id_paragraph_2 = 'id_paragraph_2';


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
      'elem_id': id,
      'venue_id': 'venue_1',
      'description': 'My first execution'
    }
    return fns.addExecution(execution);
  }
)
.then((res) => {
    let elem = {
      '_key': id_section_2,
      'elem_id': id_section_2,
      'elem_type': 'SECTION',
      'execution_id': id_execution_1,
      'description': 'Section-2'
    }
    return fns.addElement(id_execution_1, elem, '-1', '');
  }
)
.then((res) => {
    let elem = {
      '_key': id_section_1,
      'elem_id': id_section_1,
      'elem_type': 'SECTION',
      'execution_id': id_execution_1,
      'description': 'Section-1'
    }
    return fns.addElement(id_execution_1, elem, '-1', '');
  }
)
.then((res) => {
    let elem = {
      '_key': id_section_3,
      'elem_id': id_section_3,
      'elem_type': 'SECTION',
      'execution_id': id_execution_1,
      'description': 'Section-3'
    }
    return fns.addElement(id_execution_1, elem, id_section_2, 'SIBLING');
  }
)
.then((res) => {
    let elem = {
      '_key': id_step_2_1,
      'elem_id': id_step_2_1,
      'elem_type': 'STEP',
      'execution_id': id_execution_1,
      'description': 'Step-2-1'
    }
    return fns.addElement(id_execution_1, elem, id_section_2, 'CHILD');
  }
)
.then((res) => {
    // console.log('res:', res);
    let elem = {
      '_key': id_step_2_3,
      'elem_id': id_step_2_3,
      'elem_type': 'STEP',
      'execution_id': id_execution_1,
      'description': 'Step-2-3'
    }
    return fns.addElement(id_execution_1, elem, id_step_2_1, 'SIBLING');
  }
)
.then((res) => {
    // console.log('res:', res);
    let elem = {
      '_key': id_step_2_2,
      'elem_id': id_step_2_2,
      'elem_type': 'STEP',
      'execution_id': id_execution_1,
      'description': 'Step-2-2'
    }
    return fns.addElement(id_execution_1, elem, id_step_2_1, 'SIBLING');
  }
)
.then((res) => {
    // console.log('res:', res);
    let elem = {
      '_key': id_step_3_1,
      'elem_id': id_step_3_1,
      'elem_type': 'STEP',
      'execution_id': id_execution_1,
      'description': 'Step-3-1'
    }
    return fns.addElement(id_execution_1, elem, id_section_3, 'CHILD');
  }
)
.then((res) => {
    // console.log('res:', res);
    let elem = {
      '_key': id_step_3_2,
      'elem_id': id_step_3_2,
      'elem_type': 'STEP',
      'execution_id': id_execution_1,
      'description': 'Step-3-2'
    }
    return fns.addElement(id_execution_1, elem, id_step_3_1, 'SIBLING');
  }
)
.then((res) => {
    let elem = {
      '_key': id_paragraph_1,
      'elem_id': id_paragraph_1,
      'elem_type': 'PARAGRAPH',
      'execution_id': id_execution_1,
      'description': 'Paragraph-1'
    }
    return fns.addElement(id_execution_1, elem, id_section_1, 'SIBLING');
  }
)
.then((res) => {
    let elem = {
      '_key': id_paragraph_2,
      'elem_id': id_paragraph_2,
      'elem_type': 'PARAGRAPH',
      'execution_id': id_execution_1,
      'description': 'Paragraph-2'
    }
    return fns.addElement(id_execution_1, elem, id_step_3_1, 'SIBLING');
  }
)


.then((res)=>{
  return fns.setStepInput(id_step_2_1, {'temperature_input': 20.0});
})
.then((res)=>{
  return fns.setStepOutput(id_step_2_1, {'temperature_output': 25.0});
})



.then((res)=>{
  return fns.setStepInput(id_step_2_1, {'temperature_input': 21.0});
})
.then((res)=>{
  return fns.setStepOutput(id_step_2_1, {'temperature_output': 26.0});
})

/*
.then((res)=>{
  return fns.setStepInput(id_step_2_1, {'temperature_input': 22.0});
})
*/

.then((res)=>{
  return fns.setStepOutput(id_step_2_1, {'temperature_output': 27.0});
})


.then((res)=>{
  console.log('res:', res);
  return fns.getAsRun('execution/' + id_execution_1, 'as_run_created.json');
})

/*
.then(()=>{
  return fns.moveElement(id_execution_1, id_section_1, id_section_2, 'SIBLING');
})
.then(()=>{
  return fns.getAsRun('execution/' + id_execution_1, 'as_run_moved1.json');
})
.then(()=>{
  return fns.moveElement(id_execution_1, id_section_1, '-1', 'CHILD');
})
.then(()=>{
  return fns.getAsRun('execution/' + id_execution_1, 'as_run_restored1.json');
})

.then(()=>{
  return fns.moveElement(id_execution_1, id_section_1, id_section_3, 'CHILD');
})
.then(()=>{
  return fns.getAsRun('execution/' + id_execution_1, 'as_run_moved2.json');
})
.then(()=>{
  return fns.moveElement(id_execution_1, id_section_1, '-1', '');
})
.then(()=>{
  return fns.getAsRun('execution/' + id_execution_1, 'as_run_restored2.json');
})

.then(()=>{
  return fns.deleteElement(id_section_2);
})
.then(()=>{
  return fns.deleteElement(id_step_3_1);
})
.then(()=>{
  return fns.getAsRun('execution/' + id_execution_1, 'as_run_deleted.json');
})
*/
.then(()=>{
  return fns.deleteExecution(id_execution_1);
})

.then((res)=>{
    console.info('Done: ', res);
})
.catch((err)=>{
    console.info('Error:', err);
});
