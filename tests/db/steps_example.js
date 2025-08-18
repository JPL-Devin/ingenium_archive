'use strict';

var arangojs = require('arangojs');
var db = arangojs('http://localhost:8529');
var database_name = 'ingenium_test';
var graph_name = 'ingenium_graph'
const uuid = require('node-uuid');

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
            db.graph(graph_name).create({
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
                },
                {
                  collection: 'revision',
                  from: [
                    'element'
                  ],
                  to: [
                    'element'
                  ]
                },
                {
                  collection: 'hasResult',
                  from: [
                    'element'
                  ],
                  to: [
                    'result'
                  ]
                },
                {
                  collection: 'nextResult',
                  from: [
                    'execution',
                    'result'
                  ],
                  to: [
                    'result'
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
      .then((res) => {
          let id = id_execution_1;
          let execution = {
            '_key': id,
            'id': id,
            'venue_id': 'venue_1',
            'description': 'My first execution'
          }
          return addExecution(execution);
        }
      )
      .then((res) => {
          let elem = {
            '_key': id_section_2,
            'id': id_section_2,
            'elem_type': 'SECTION',
            'execution_id': id_execution_1,
            'description': 'Section-2'
          }
          return addElement(elem, '', '', false);
        }
      )
      .then((res) => {
          let elem = {
            '_key': id_section_3,
            'id': id_section_3,
            'elem_type': 'SECTION',
            'execution_id': id_execution_1,
            'description': 'Section-3'
          }
          return addElement(elem, id_section_2, 'SIBLING', false);
        }
      )
      .then((res) => {
          let elem = {
            '_key': id_step_2_1,
            'id': id_step_2_1,
            'elem_type': 'STEP',
            'execution_id': id_execution_1,
            'description': 'Step-2-1'
          }
          return addElement(elem, id_section_2, 'CHILD', false);
        }
      )
      .then((res) => {
          // console.log('res:', res);
          let elem = {
            '_key': id_step_2_3,
            'id': id_step_2_3,
            'elem_type': 'STEP',
            'execution_id': id_execution_1,
            'description': 'Step-2-3'
          }
          return addElement(elem, id_step_2_1, 'SIBLING', false);
        }
      )
      .then((res) => {
          // console.log('res:', res);
          let elem = {
            '_key': id_step_2_2,
            'id': id_step_2_2,
            'elem_type': 'STEP',
            'execution_id': id_execution_1,
            'description': 'Step-2-2'
          }
          return addElement(elem, id_step_2_1, 'SIBLING', false);
        }
      )
      .then((res) => {
          // console.log('res:', res);
          let elem = {
            '_key': id_step_3_1,
            'id': id_step_3_1,
            'elem_type': 'STEP',
            'execution_id': id_execution_1,
            'description': 'Step-3-1'
          }
          return addElement(elem, id_section_3, 'CHILD', false);
        }
      )
      .then((res) => {
          // console.log('res:', res);
          let elem = {
            '_key': id_step_3_2,
            'id': id_step_3_2,
            'elem_type': 'STEP',
            'execution_id': id_execution_1,
            'description': 'Step-3-2'
          }
          return addElement(elem, id_step_3_1, 'SIBLING', false);
        }
      )
      .then((res) => {
          let elem = {
            '_key': id_section_1,
            'id': id_section_1,
            'elem_type': 'SECTION',
            'execution_id': id_execution_1,
            'description': 'Section-1'
          }
          return addElement(elem, '', '', true);
        }
      )
      .then((res) => {
          let elem = {
            '_key': id_section_4,
            'id': id_section_4,
            'elem_type': 'SECTION',
            'execution_id': id_execution_1,
            'description': 'Section-4'
          }
          return addElement(elem, '', '', false);
        }
      )
      .then((res) => {
          let elem = {
            '_key': id_step_4_3,
            'id': id_step_4_3,
            'elem_type': 'STEP',
            'execution_id': id_execution_1,
            'description': 'Step-4-3'
          }
          return addElement(elem, id_section_4, '', false);
        }
      )
      .then((res) => {
          let elem = {
            '_key': id_step_4_5,
            'id': id_step_4_5,
            'elem_type': 'STEP',
            'execution_id': id_execution_1,
            'description': 'Step-4-5'
          }
          return addElement(elem, id_section_4, 'CHILD', false);
        }
      )
      .then((res) => {
          let elem = {
            '_key': id_step_4_1,
            'id': id_step_4_1,
            'elem_type': 'STEP',
            'execution_id': id_execution_1,
            'description': 'Step-4-1'
          }
          return addElement(elem, id_section_4, 'CHILD', true);
        }
      )
      .then((res) => {
          let elem = {
            '_key': id_step_4_2,
            'id': id_step_4_2,
            'elem_type': 'STEP',
            'execution_id': id_execution_1,
            'description': 'Step-4-2'
          }
          return addElement(elem, id_step_4_1, 'SIBLING', false);
        }
      )
      .then((res) => {
          let elem = {
            '_key': id_step_4_4,
            'id': id_step_4_4,
            'elem_type': 'STEP',
            'execution_id': id_execution_1,
            'description': 'Step-4-4'
          }
          return addElement(elem, id_step_4_5, 'SIBLING', true);
        }
      )
      .then((res) => {
          let elem = {
            '_key': id_section_5,
            'id': id_section_5,
            'elem_type': 'SECTION',
            'execution_id': id_execution_1,
            'description': 'Section-5'
          }
          return addElement(elem, '', '', false);
        }
      )
      .then((res) => {
          let elem = {
            '_key': id_section_5_1,
            'id': id_section_5_1,
            'elem_type': 'SECTION',
            'execution_id': id_execution_1,
            'description': 'Section-5-1'
          }
          return addElement(elem, id_section_5, 'CHILD', false);
        }
      )
      .then((res) => {
          let elem = {
            '_key': id_section_5_2,
            'id': id_section_5_2,
            'elem_type': 'SECTION',
            'execution_id': id_execution_1,
            'description': 'Section-5-2'
          }
          return addElement(elem, id_section_5, 'CHILD', false);
        }
      )
      .then((res) => {
          let elem = {
            '_key': id_step_5_1_1,
            'id': id_step_5_1_1,
            'elem_type': 'STEP',
            'execution_id': id_execution_1,
            'description': 'Section-5-1-1'
          }
          return addElement(elem, id_section_5_1, 'CHILD', false);
        }
      )
      .then((res) => {
          let elem = {
            '_key': id_step_5_1_2,
            'id': id_step_5_1_2,
            'elem_type': 'STEP',
            'execution_id': id_execution_1,
            'description': 'Section-5-1-2'
          }
          return addElement(elem, id_section_5_1, 'CHILD', false);
        }
      )
      .then((res) => {
          let elem = {
            '_key': id_section_6,
            'id': id_section_6,
            'elem_type': 'SECTION',
            'execution_id': id_execution_1,
            'description': 'Section-6'
          }
          return addElement(elem, '', '', false);
        }
      )
      .then((res) => {
          let elem = {
            '_key': id_section_6_1,
            'id': id_section_6_1,
            'elem_type': 'SECTION',
            'execution_id': id_execution_1,
            'description': 'Section-6-1'
          }
          return addElement(elem, id_section_6, 'CHILD', false);
        }
      )
      .then((res) => {
          let elem = {
            '_key': id_section_6_2,
            'id': id_section_6_2,
            'elem_type': 'SECTION',
            'execution_id': id_execution_1,
            'description': 'Section-6-2'
          }
          return addElement(elem, id_section_6, 'CHILD', false);
        }
      )
      .then((res) => {
          let elem = {
            '_key': id_step_6_2_1,
            'id': id_step_6_2_1,
            'elem_type': 'STEP',
            'execution_id': id_execution_1,
            'description': 'Section-6-2-1'
          }
          return addElement(elem, id_section_6_2, 'CHILD', false);
        }
      )
      .then((res) => {
          let elem = {
            '_key': id_step_6_2_2,
            'id': id_step_6_2_2,
            'elem_type': 'STEP',
            'execution_id': id_execution_1,
            'description': 'Section-6-2-2'
          }
          return addElement(elem, id_section_6_2, 'CHILD', false);
        }
      )
      .then(()=>{
        return getAsRun(id_execution_1, 'as_run_created.json');
      })
      .then((res) => {
          return moveElement(id_section_2, id_section_4, 'SIBLING', false);
        },(err) => {
          console.log('moveElement err: ', err);
        }
      )
      .then((res) => {
          return moveElement(id_section_6, id_section_5, 'CHILD', false);
        },(err) => {
          console.log('moveElement err: ', err);
        }
      )
      .then((res) => {
          return moveElement(id_step_3_1, id_section_4, 'CHILD', false);
        },(err) => {
          console.log('moveElement err: ', err);
        }
      )
      // undo the previous three moves
      .then((res) => {
          return moveElement(id_step_3_1, id_section_3, 'CHILD', true);
        },(err) => {
          console.log('moveElement err: ', err);
        }
      )
      .then((res) => {
          return moveElement(id_section_6, id_section_5, 'SIBLING', false);
        },(err) => {
          console.log('moveElement err: ', err);
        }
      )
      .then((res) => {
          return moveElement(id_section_2, id_section_3, 'SIBLING', true);
        },(err) => {
          console.log('moveElement err: ', err);
        }
      )
      // try to move to the top
      .then((res) => {
          return moveElement(id_section_5, '', '', true);
        },(err) => {
          console.log('moveElement err: ', err);
        }
      )
      .then((res) => {
        return getAsRun(id_execution_1, 'as_run_moved.json');
      })
      .then((res) => {
          return deleteElement(id_section_3);
        }
      )
      .then((res) => {
          return deleteElement(id_section_5_1);
        }
      )
      .then(()=>{
        return getAsRun(id_execution_1, 'as_run_part.json');
      })
      .then(()=>{
        return deleteExecution(id_execution_1);
      })
      .then((res)=>{
          console.info('Done: ', res);
      })
      .catch((err)=>{
          console.info('Error:', err);
      });
    }
  }
);


function setNumbers(node) {
  console.log('setNumbers node: ', node._id);
  if (node.children) {
    node.children.forEach(function(child, idx) {
      var node_number = node.hasOwnProperty('number') ? node['number'] : '';

      if (node_number == '') {
        child['number'] = String(idx+1);
      }
      else {
        child['number'] = [node['number'], (idx+1)].join('-');
      }
      setNumbers(child);
    });
  }
}

function addExecution(execution) {
  return new Promise(function(resolve, reject) {
    var graph = db.graph(graph_name);
    var collection = graph.vertexCollection('execution');

    collection.save(execution)
    .then((res) => {
        // console.log('Execution created:', res);
        resolve(res);
      }, (err) => {
        reject(err);
      }
    );
  });
}

function saveElement(elem) {
  return new Promise(function(resolve, reject) {
    let element_collection = db.collection('element');
    element_collection.save(elem)
    .then((res) => {
        console.log('    Element saved');
        resolve(res);
      }, (err) => {
        console.error('Failed to add element.');
        reject(err);
      }
    )
  })
}

//  target_id  (default to execution)
//  level: CHILD (default), SIBLING
//  prepend: (default to false)
function insertElement(elem, target_id, level, prepend) {

  console.log('\ninsertElement:', elem);
  var target_id_sanitized = null;
  var level_sanitized = null;
  var execution_id = elem['execution_id'];
  var elem_id = elem['id'];

  var graph = db.graph(graph_name);
  var element_collection = graph.vertexCollection('element');
  var step_order_collection = graph.collection('stepOrder');

  var to_id = 'element/' + elem_id;
  var from_id = null;
  var relation = '';

  if (target_id == '') {
    target_id_sanitized = 'execution/' + execution_id;
  } else {
    target_id_sanitized = 'element/' + target_id;
  }

  // TODO: throw an error if level is SIBLING and insert_at_id is empty.
  if (level == '') {
    level_sanitized = 'CHILD';
  } else {
    if (target_id == '') {
      level_sanitized = 'CHILD';
    } else {
      level_sanitized = level;
    }
  }

  console.log('target_id_sanitized: %s level_sanitized: %s prepend: %s',
    target_id_sanitized, level_sanitized, prepend);

  /*
  - level: CHILD, prepend = false
      _from: Start from the target (CHILD) and find the last child if any (SIBLING)
  - level: CHILD, prepend = true
      _from: Use the target (CHILD)
  - level: SIBLING, prepend = false
      _from: Use the target (SIBLING)
  - level: SIBLING, prepend = true
      _from: Start from the target and find the previous sibling if any (SIBLING) or the parent (CHILD)
  */
  var promise = null;

  if (level_sanitized == 'CHILD' && prepend == false) {
    promise = graph.traversal(target_id_sanitized, {
      direction: 'outbound',
      init: `
      result.from_id = null;
      result.relation = 'CHILD';
      `
      ,
      visitor:
      `
      var edges = path.edges;
      if (edges.length == 0) {
        result.from_id = vertex._id;
      }

      if ( (edges.length > 0) && (edges[0]['relation'] == 'CHILD') ) {
        let num_levels = 0;

        for (var edge of edges) {
          if (edge['relation'] == 'CHILD') {
            num_levels++;
          }
        }
        if (num_levels == 1) {
          result.from_id = vertex._id;
          result.relation = 'SIBLING';
        }
      }
      `
    }).then((result) => {
        from_id = result.from_id;
        relation = result.relation;
        console.log('Case1 from_id: %s relation: %s', from_id, relation);
      },
      (err) => {console.log('Traveral error:', err)});
  } else if (level_sanitized == 'CHILD' && prepend == true) {
    promise = Promise.resolve({'from_id': target_id_sanitized, 'relation': 'CHILD'})
    .then((result) => {
        from_id = result.from_id;
        relation = result.relation;
        console.log('Case2 from_id: %s relation: %s', from_id, relation);
      },
      (err) => {console.log(err)});
  } else if (level_sanitized == 'SIBLING' && prepend == false) {
    promise = Promise.resolve({'from_id': target_id_sanitized, 'relation': 'SIBLING'})
    .then((result) => {
        from_id = result.from_id;
        relation = result.relation;
        console.log('Case3 from_id: %s relation: %s', from_id, relation);
      },
      (err) => {console.log(err)});
  } else if (level_sanitized == 'SIBLING' && prepend == true) {
      promise = step_order_collection.inEdges(target_id_sanitized)
      .then((edges) => {
        let prev_sibling = null;
        let parent = null;
        for(var edge of edges) {
          if (edge.relation == 'CHILD') {
            parent = edge._from;
          } else if (edge.relation == 'SIBLING') {
            prev_sibling = edge._from;
          }
        }
        if (prev_sibling) {
          from_id = prev_sibling;
          relation = 'SIBLING';
        } else if (parent) {
          from_id = parent;
          relation = 'CHILD';
        } else {
          // TODO: throw an error
          console.warn('Could not determine sibling.');
        }
        console.log('Case4 from_id: %s relation: %s', from_id, relation);
      },
      (err) => {console.log(err)});
  }

  return Promise.resolve(promise)
  .then((res) => {
      console.log('level_sanitized: %s prepend: %s from_id: %s relation: %s',
        level_sanitized, prepend, from_id, relation);
    },
    (err) => {
      console.error(err);
  })
  // Update current edge if needed. This needs to happen before adding new edge
  // since a new edge may change the query result.
  .then(() => {
    return new Promise(function(resolve, reject) {
      step_order_collection.firstExample({'relation': relation, '_from': from_id})
      .then((res) => {
          resolve(res);
        }, (err) => {
          resolve(null);
        }
      )
    })
  })
  .then((edge_to_update) => {
    console.log('edge_to_update:', edge_to_update);
    return new Promise(function(resolve, reject) {
      if (edge_to_update) {
        console.log('Update edge: ', edge_to_update);
        step_order_collection.update(edge_to_update, {'_from': to_id, 'relation': 'SIBLING'})
        .then((res) => {
            resolve(res);
          }, (err) => {
            reject(err);
          }
        )
      } else {
        console.log('No edge to update.');
        resolve(edge_to_update);
      }
    })
  })
  // add edge for the new element
  .then((res) => {
    return new Promise(function(resolve, reject) {
      let id = uuid.v4();
      let edge_doc = {'relation': relation, '_key': id, 'id': id, '_from': from_id, '_to': to_id};
      console.log('edge_doc:', edge_doc);
      step_order_collection.save(edge_doc)
      .then((res) => {
          console.log('    Added as', relation);
          // console.log('    res:', res);
          resolve(res);
        }, (err) => {
          console.error('Failed to add element.');
          reject(err);
        }
      )
    })
  })
}

function addElement(elem, target_id, level, prepend) {
  return new Promise(function(resolve, reject) {
    saveElement(elem)
    .then((res) => {
        insertElement(elem, target_id, level, prepend)
        .then(
          (res) => {
            resolve(res);
          },
          (err) => {
            reject(err);
          }
        )
      },
      (err) => {reject(err)}
    );
  })
}

function moveElement(elem_id, target_id, level, prepend) {
  console.log('\nmoveElement elem_id: ', elem_id);
  return new Promise(function(resolve, reject) {
    cutElement(elem_id, false)
    .then((elem) => {
        insertElement(elem, target_id, level, prepend)
        .then(
          (res) => {
            console.log('insertElement done:');
            resolve(res);
          },
          (err) => {
            console.log('insertElement failed:', err);
            reject(err);
          }
        )
      },
      (err) => {
        console.log('cutElement failed:', err);
        reject(err);
      }
    );
  })
}

function deleteExecution(execution_id) {
  return new Promise(function(resolve, reject) {
    var graph = db.graph(graph_name);
    graph.traversal('execution/' + execution_id, {
      direction: 'outbound',
      init: `
      result.ids = [];    // ids of verticies to delete
      result.edge_ids = [];
      `
      ,
      visitor:
      `
      result.ids.push(vertex._id);
      let edges = path.edges;
      if (edges.length > 0) {
        let last_edge = edges[edges.length-1];
        result.edge_ids.push(last_edge._id);
      }
      `
    })
    .then((result) => {
      let promises = [];

      let execution_ids = [];    // should be only one.
      let element_ids = [];
      let step_order_ids = [];

      console.log('result.ids: ', result.ids);
      console.log('result.edge_ids: ', result.edge_ids);

      for(var id of result.ids) {
        if (id.startsWith('execution/')) {
          execution_ids.push(id.split('/')[1]);
        } else if (id.startsWith('element/')) {
          element_ids.push(id.split('/')[1]);
        }
      }

      for(var id of result.edge_ids) {
        if (id.startsWith('stepOrder/')) {
          step_order_ids.push(id.split('/')[1]);
        }
      }

      promises.push(graph.vertexCollection('execution').removeByKeys(execution_ids));
      promises.push(graph.vertexCollection('element').removeByKeys(element_ids));
      promises.push(graph.collection('stepOrder').removeByKeys(step_order_ids));

      Promise.all(promises).then(
        (res) => {
          console.log('execution deleted: ', execution_id);
          resolve(res);
        },
        (err) => {
          console.log('Error when deleting execution: ', execution_id);
          reject(err);
        }
      );
    });
  });
}

function deleteElement(elem_id) {
  return new Promise(function(resolve, reject) {
    cutElement(elem_id, true)
    .then((elem) => {
        let element_collection = db.collection('element');
        element_collection.removeByKeys([elem_id]).then(
          (res) => {
            resolve(res);
          },
          (err) => {
            reject(err);
          }
        )
      },
      (err) => {reject(err)}
    );
  })
}

function cutElement(elem_id, delete_children) {
  var elem = null;
  var prev_sibling = null;
  var next_sibling = null;
  var parent = null;
  var ids_to_delete = [];
  var edge_ids_to_delete = [];
  var graph = db.graph(graph_name);
  var element_collection = db.collection('element');
  var step_order_collection = db.collection('stepOrder');

  var p1 = element_collection.lookupByKeys([elem_id])
    .then((docs) => {
        if (docs.length > 1) {
          console.warn('More than one element found for elem_id: %s', elem_id);
        }
        if (docs.length == 0) {
          console.warn('No element found for elem_id: %s', elem_id);
          elem = null;
        } else {
          elem = docs[0];
        }
      }, (err) => {
          console.warn('No element found for elem_id: %s Reason: %s', elem_id, err);
        }
      );
  var p2 = step_order_collection.firstExample({'_from': 'element/' + elem_id, 'relation': 'SIBLING'})
    .then((res) => {next_sibling = res._to; console.log('next_sibling:', next_sibling);},
      (err) => {
        // ignore
      });
  var p3 = step_order_collection.firstExample({'_to': 'element/' + elem_id, 'relation': 'SIBLING'})
    .then((res) => {
        prev_sibling = res._from; console.log('prev_sibling', prev_sibling);
      },
      (err) => {
        // ignore
        // console.log('prev_sibling err:', err);
      });
  var p4 = step_order_collection.firstExample({'_to': 'element/' + elem_id, 'relation': 'CHILD'})
    .then((res) => {parent = res._from; console.log('parent:', parent);}, (err) => {});
  var p5 = graph.traversal('element/' + elem_id, {
    direction: 'any',
    init: `
    result.vertex_id = null;
    result.edge_ids = [];  // ids of edges to delete
    result.edges = [];           // for debugging
    result.edge_to_delete = [];  // for debugging
    `
    ,
    visitor:
    `
    var edges = path.edges;
    if (edges.length == 0) {
      result.vertex_id = vertex._id;
    }

    // immediate sibling and parent relationship
    if (edges.length > 0) {
      let edge = edges[0];
      result.edges.push(edge);
      if (edge.relation == 'SIBLING') {
        result.edge_ids.push(edge._id);
        result.edge_to_delete.push(edge);
      } else if (edge.relation == 'CHILD' && edge._to == result.vertex_id) {
        result.edge_ids.push(edge._id);
        result.edge_to_delete.push(edge);
      }
    }
    `,
    minDepth: 0,
    maxDepth: 1
  })
  .then((result) => {
      // console.log('immediate edges to delete:', result);
      edge_ids_to_delete = edge_ids_to_delete.concat(result.edge_ids);
    },(err) => {
      console.log('Error when getting edges to delete: ', err);
  });
  var p6 = graph.traversal('element/' + elem_id, {
    direction: 'outbound',
    init: `
    result.ids=[];      // ids of verticies to delete
    result.edge_ids = [];  // ids of edges to delete
    `
    ,
    visitor:
    `
    var edges = path.edges;
    // children to remove
    if (edges.length > 0 && edges[0].relation == 'CHILD') {
      result.ids.push(vertex._id);
      result.edge_ids.push(edges[edges.length-1]._id);
    }
    `
  })
  .then((result) => {
      ids_to_delete = ids_to_delete.concat(result.ids);
      edge_ids_to_delete = edge_ids_to_delete.concat(result.edge_ids);
    },(err) => {
      console.log('Error when getting elements to delete: ', err);
  });

  let promises_prep = [p1, p2, p3, p4, p5];
  if (delete_children) {
    promises_prep.push(p6);
  }
  return new Promise(function(resolve, reject) {
    Promise.all(promises_prep).then(
      (res) => {
        console.log('ids_to_delete:', ids_to_delete);
        console.log('edge_ids_to_delete:', edge_ids_to_delete);
        let promises = [];

        let element_ids = [];
        let step_order_ids = [];

        for(var id of ids_to_delete) {
          if (id.startsWith('element/')) {
            element_ids.push(id.split('/')[1]);
          }
        }

        for(var id of edge_ids_to_delete) {
          if (id.startsWith('stepOrder/')) {
            step_order_ids.push(id.split('/')[1]);
          }
        }

        promises.push(graph.vertexCollection('element').removeByKeys(element_ids));
        promises.push(graph.collection('stepOrder').removeByKeys(step_order_ids));

        if (prev_sibling && next_sibling) {
          let id = uuid.v4();
          promises.push(
            graph.collection('stepOrder')
            .save({'_key': id, 'id': id, '_from': prev_sibling, '_to': next_sibling, 'relation': 'SIBLING'})
          );
        }

        if (parent && next_sibling) {
          let id = uuid.v4();
          promises.push(
            graph.collection('stepOrder')
            .save({'_key': id, 'id': id, '_from': parent, '_to': next_sibling, 'relation': 'CHILD'})
          );
        }

        Promise.all(promises).then(
          (res) => {
            if (delete_children) {
              console.log('element was cut with children: ', elem_id);
            } else {
              console.log('element was cut: ', elem_id);
            }

            // return the deleted element
            resolve(elem);
          },
          (err) => {
            console.log('Error when deleting element: ', elem_id);
            reject(err);
        });
      },
      (err) => {
        console.log('Error when preparing to delete element: ', elem_id);
        reject(err);
    });
  });
}

function getAsRun(execution_id, file_name) {
  console.log('getAsRun:');
  return new Promise(function(resolve, reject) {
    var graph = db.graph(graph_name);
    graph.traversal('execution/' + execution_id, {
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
        if (last_edge.relation == 'CHILD') {
          var parent = result.dict[last_edge._from];
          vertex.parent_id = parent._id;
          parent.children.push(vertex);
        } else if (last_edge.relation == 'SIBLING') {
          var sibling_id = last_edge._from;
          var sibling = result.dict[sibling_id];
          vertex.parent_id = sibling.parent_id;
          var parent = result.dict[sibling.parent_id];
          parent.children.push(vertex);
        }
      }
      `
    })
    .then((result) => {
        // console.log('Graph traversal result:', JSON.stringify(result, 0, 2));

        var fs = require('fs');
        // set numbers
        setNumbers(result.execution);

        fs.writeFile(file_name, JSON.stringify(result.execution, 0, 2), function(err) {
          if(err) {
            return console.log(err);
          }
        });
        resolve(result.execution);
      },
      (err) => {
        console.log(err);
      }
    );
  });
}
