var arangojs = require('arangojs');
var base_funcs = require('./api/base_funcs');
var node_funcs = require('./api/node_funcs');
var procedure_funcs = require('./api/procedure_funcs');
var readline = require('readline');
const config = require('./config');
var get_sj_error_message = base_funcs.get_sj_error_message;
var verbose = false;

var db = arangojs(config.db_url);

// console.log(`db_user: ${db_user}`);
// console.log(`db_password: ${db_password}`);

db.useBasicAuth(config.db_user, config.db_password);
db.useDatabase(config.database_name);

function get_padded_number(number_str, delimiter) {
  const segments = number_str.split(delimiter);
  for (let i=0; i < segments.length; i++) {
    segments[i] = segments[i].padStart(4, '0');
  }
  
  return segments.join(delimiter);
}

function get_padded_last_number(number_str, delimiter) {
  const segments = number_str.split(delimiter);
  for (let i=0; i < segments.length; i++) {
    segments[i] = segments[i].padStart(4, '0');
  }
  
  return segments[segments.length-1];
}

function get_padded(str) {
  return str.padStart(4, '0');
}


function split_number(number, delimiter) {
  const segs = number.split(delimiter);
  const parent_number = segs.length == 1 ? '' : segs.slice(0, segs.length-1).join(delimiter);
  const child_number = segs.length == 1 ? number : segs[segs.length-1];
  
  return {parent_number, child_number};
}

function compare_numbers(number1, number2) {  
  // console.log(`\nnumber1: ${number1}  number2: ${number2}`);
  const segs1 = number1.split('-');
  const segs2 = number2.split('-');
  
  const limit = segs1.length < segs2.length ? segs1.length : segs2.length;
  
  for (let i=0; i < limit; i++) {
    let seg1 = segs1[i];
    let seg2 = segs2[i];
    
    if (seg1 == seg2) {
      continue;
    } else {
      return compare_seg_numbers(seg1, seg2);
    }
  }
  
  return segs1.length < segs2.length ? -1 : 1;
}

function compare_seg_numbers(seg1, seg2) {  
  // console.log(`seg1: ${seg1}  seg2: ${seg2}`);
  const sub_segs1 = seg1.split('.');
  const sub_segs2 = seg2.split('.');
  
  const limit = sub_segs1.length < sub_segs2.length ? sub_segs1.length : sub_segs2.length;
  
  for (let i=0; i < limit; i++) {
    let sub_seg1 = sub_segs1[i];
    let sub_seg2 = sub_segs2[i];
    
    if (sub_seg1 == sub_seg2) {
      continue;
    } else {
      return compare_sub_seg_numbers(sub_seg1, sub_seg2);
    }
  }
  
  return sub_segs1.length < sub_segs2.length ? -1 : 1;
}

function compare_sub_seg_numbers(child_number1, child_number2) {  
  //console.log(`child_number1:${child_number1}:  child_number2:${child_number2}:`);
  
  const code_9 = '9'.charCodeAt(0);
  
  if (child_number1.length == 0) {
    return -1;
  } else if (child_number2.length == 0) {
    return 1;
  }
    
  const numeric1 = child_number1.charCodeAt(0) <= code_9;
  const numeric2 = child_number2.charCodeAt(0) <= code_9;
    
  //console.log(`numeric1: ${numeric1}  numeric2: ${numeric2}`);
    
  if (numeric1 == true && numeric2 == false) {
    return 1;
  } else if (numeric1 == false && numeric2 == true) {
    return -1;
  } else {
    const padded1 = get_padded(child_number1);
    const padded2 = get_padded(child_number2);
    
    //console.log(`padded1: ${padded1}  padded2: ${padded2}`);
    
    return padded1 > padded2 ? 1 : -1;
  }
}

function sort_by_numbers(elements) {
  elements.sort((element1, element2) => compare_numbers(element1.number, element2.number));
}

function sort_test() {
  const elements = [
    {'number': '2'},
    {'number': '1'},
    {'number': '3'},
    {'number': '2.10'},
    {'number': '2.b'},
    {'number': '2.2'},
    {'number': '2.1'},
    {'number': '2.a'},
    {'number': '2.3'},
    {'number': '2.c'},
    {'number': '2.4'}, 
    {'number': '2.5'}, 
    {'number': '2.6'},
    {'number': '2.7'}, 
    {'number': '2.8'}, 
    {'number': '2.9'},    
    {'number': '2.11'},     
    {'number': '4'},
    {'number': '1-2'},
    {'number': '1-1'},
    {'number': '1-3'},
    {'number': '1-2.10'},
    {'number': '1-2.b'},
    {'number': '1-2.2'},
    {'number': '1-2.1'},
    {'number': '1-2.a'},
    {'number': '1-2.3'},
    {'number': '1-2.c'},
    {'number': '1-2.4'}, 
    {'number': '1-2.5'}, 
    {'number': '1-2.6'},
    {'number': '1-2.7'}, 
    {'number': '1-2.8'}, 
    {'number': '1-2.9'},    
    {'number': '1-2.11'},        
  ];  
  
  const elements2 = [
    {'number': '1'},
    {'number': '0.1'},
    {'number': '1.1'},
    {'number': '2'},
  ]
  
  sort_by_numbers(elements2);
  console.log(JSON.stringify(elements2, 0, 2));
}


async function get_off_elems (root_type, root_id) {
  // console.log(`get_off_elems root_type: ${root_type} root_id: ${root_id}`);
  let var_dict = base_funcs.get_root_specific_variables(root_type);
  
  const target_parent_idd = `${var_dict.root_prefix}${root_id}`;
  // console.log(`target_parent_idd: ${target_parent_idd}`);
  
  let rels = [];

  try {
    let cursor = await db.query(
      {
        query:
        `
        FOR vertex, edge
          IN 0..10000
          OUTBOUND '${target_parent_idd}'
          GRAPH '${var_dict.graph_name}'
          OPTIONS {bfs: true}
          RETURN {
              v: vertex, 
              e: edge
          }
        `
      },
      {count: true}
    );
    rels = await cursor.all();
  } catch (err) {
    return Promise.reject('Failed to get elements of target parent from DB: ' + get_sj_error_message(err));
  }
  
  // console.log(`res.length: ${rels.length}`);
  
  const vertex_infos = [];
  const vertex_map = {};
  const rels_map = {};
  const elems_off = [];
  const rels_off = [];
  
  for (let i=0; i < rels.length; i++) {
    let rel = rels[i];
        
    // console.log(JSON.stringify(rel));
    
    // skip the root
    if (rel.e) {
      // console.log(`rel.e._id ${rel.e._id} rel.e._from ${rel.e._from} rel.e._to ${rel.e._to} rel.e.idx ${rel.e.idx}`);
        
      // skin run record edge
      if (rel.e._id.startsWith('runRecord/')) {
        continue;
      }
            
      if (!rels_map.hasOwnProperty(rel.e._from)) {
        rels_map[rel.e._from] = [];
      }
      
      // console.log(i);
      // console.log(JSON.stringify(vertex_map, 0, 2));
      
      let parent_derived_number = rel.e._from == target_parent_idd ? '' : vertex_map[rel.e._from].derived_number;
      let derived_number = parent_derived_number == '' ? `${rel.e.idx + 1}` : `${parent_derived_number}-${rel.e.idx + 1}`;
      
      const vertex_info = {
        idx: rel.e.idx,    
        derived_number: derived_number,
        from: rel.e._from,
        _key: rel.e._key,     
        elem: {
          number: rel.v.number,
          elem_id: rel.v.elem_id, 
          elem_type: rel.v.elem_type,
          title: rel.v.title,
          procedure_id: rel.v.procedure_id,
          procedure_section_id: rel.v.procedure_section_id,
          procedure_modification_status: rel.v.procedure_modification_status
        }        
      };
      
      vertex_map[rel.e._to] = vertex_info;
      vertex_infos.push(vertex_info);
      rels_map[rel.e._from].push(vertex_info);
      
      // derived number is not applicable for procedure element in execution
      if (root_type == 'PROCEDURE') {
        if (vertex_info.derived_number != vertex_info.elem.number) {
          elems_off.push(vertex_info);
        }        
      }
    }
  }
  
  for (const key in rels_map) {
    let rels = rels_map[key];
    //console.log('rels before sort');
    //console.log(JSON.stringify(rels, 0, 2));
    rels.sort((a, b) => compare_numbers(a.elem.number, b.elem.number));
    if (verbose) console.log('rels after sort');
    if (verbose) console.log(JSON.stringify(rels, 0, 2));    
    
    for (let i=0; i < rels.length; i++) {
      let rel = rels[i];
      rel.i = i;
    }
        
    for (let i=0; i < rels.length; i++) {
      let rel = rels[i];
      if (rel.i != rel.idx) {
        rels_off.push(rels);
        break;
      }
    }
  }
  
  vertex_infos.sort((a, b) => compare_numbers(a.elem.number, b.elem.number));
  // console.log('vertex_infos:');
  // console.log(JSON.stringify(vertex_infos, 0, 2));
  
  const num_elems = Object.keys(vertex_map).length;
  
  return {num_elems, elems_off, rels_off};
}

function check_orders(rels_off) {
  let status = rels_off.length > 0 ? 'FAIL': 'PASS';
  const results = [];
  
  for (const rels of rels_off) {
    let idx_status = 'OK';    
    let number_status = 'OK';
        
    let prev_idx = null;
    for (const rel of rels) {
      if (prev_idx != null && rel.idx <= prev_idx) {
        number_status = 'NUMBER_OFF';    // out of order
        break;
      }
      prev_idx = rel.idx;
    }

    const idx_list = rels.map(rel => rel.idx);
    idx_list.sort((a, b) => {return (a > b ? 1 : -1)});
    for (let i=0; i < idx_list.length; i++) {
      if (i != idx_list[i]) {
        idx_status = 'IDX_OFF';
        break;
      }
    }
    
    results.push({
      idx_status: idx_status,      
      number_status: number_status,
      rels: rels
    });
  }
  return {status, results};
}

function read_input(message) {
  const rl = readline.createInterface({input: process.stdin, output: process.stdout});
  
  return new Promise((resolve, reject) => {
    rl.question(message, (response) => {
      rl.close();
      resolve(response);
    });    
  })
}


async function check_procedure_version(version_id, procedure_id, version, fix) {
  if (version_id === null) {
    const procedure_version_info = await procedure_funcs.getProcedureVersion(procedure_id, version);
    version_id = procedure_version_info.version_id;    
  }
  
  const procedure_info = await procedure_funcs.getProcedure(procedure_id);

  const {num_elems, elems_off, rels_off} = await get_off_elems('PROCEDURE', version_id);
  const num_off_elems = elems_off.length;
  const num_off_rels = rels_off.length;
    
  const {status, results} = check_orders(rels_off);
  
  console.log(`procedure_id: ${procedure_id} version: ${version} title: ${procedure_info.title} num_elems: ${num_elems} num_off_elems: ${num_off_elems} num_off_rels: ${num_off_rels} status: ${status}`);
  for (result of results) {
    console.log(`idx_status: ${result.idx_status} number_status: ${result.number_status}`);  
    console.log(JSON.stringify(result.rels, 0, 2));
  }
  
  if (elems_off.length > 0) {
    //console.log('elems_off');
    //console.log(JSON.stringify(elems_off, 0, 2));    
  }
  
  if (status == 'FAIL' && fix) {
    const response = await read_input(`Do you want to fix the element order? procedure_id: ${procedure_id} version: ${version}   (y/n)`);
    
    if (response == 'y') {
      await update_edges('PROCEDURE', results);
    }
  }
}

async function check_execution(execution_id, fix) {
  const {num_elems, elems_off, rels_off} = await get_off_elems('EXECUTION', execution_id);
  const num_off_elems = elems_off.length;
  const num_off_rels = rels_off.length;
    
  const {status, results} = check_orders(rels_off);
  
  console.log(`execution_id: ${execution_id} num_elems: ${num_elems} num_off_elems: ${num_off_elems} num_off_rels: ${num_off_rels} status: ${status}`);
  
  for (result of results) {
    console.log(`idx_status: ${result.idx_status} number_status: ${result.number_status}`);  
    console.log(JSON.stringify(result.rels, 0, 2));
  }
    
  if (elems_off.length > 0) {
    //console.log('elems_off');
    //console.log(JSON.stringify(elems_off, 0, 2));    
  }
  
  if (status == 'FAIL' && fix) {
    const response = await read_input(`Do you want to fix the element order? execution_id: ${execution_id}  (y/n)`);
    
    if (response == 'y') {
      await update_edges('EXECUTION', results);
    }
  }  
}

async function update_edges(root_type, results) {
  const edges_to_update = [];
  for (const result of results) {
    for (const rel of result.rels) {
      let edge = {
        _key: rel._key,
        idx: rel.i
      };
      edges_to_update.push(edge);
    }
  }
  
  console.log(`Updating edges. count: ${edges_to_update.length}`);  
  if (verbose) console.log(JSON.stringify(edges_to_update, 0, 2));  
  if (edges_to_update.length > 0) {
    let var_dict = base_funcs.get_root_specific_variables(root_type);
    await var_dict.step_order_collection.updateAll(edges_to_update);      
  }  
}

function print_usage(msg) {
  if (msg) {
    console.log(msg);
  }
  console.log('USAGE: node check_elem_order.js procedure procedure_id version');
  console.log('Example: node check_elem_order.js procedure europa-procedure-10001 1');
  console.log('Example: node check_elem_order.js procedure europa-procedure-10001');
  console.log('Example: node check_elem_order.js procedure all');
  console.log('USAGE: node check_elem_order.js execution execution_id');
  console.log('Example: node check_elem_order.js execution europa-ingenium-10022');
  console.log('Example: node check_elem_order.js execution all');
  process.exit(-1);     
}

async function main() {  
  let fix = false;
  const args = [];
  for (let i=2; i < process.argv.length; i++) {
    let arg = process.argv[i];
    if (arg.startsWith('-')) {
      if (arg == '--fix') {
        fix = true;
      } else if (arg == '--verbose') {
        verbose = true;
      } else {
        print_usage(`invalid option: ${arg}`); 
      }
    } else {
      args.push(arg);  
    }
  }
  
  if (args.length < 1) {
    print_usage();     
  }
    
  const command = args[0];
  
  if (command == 'procedure') {
    if (args.length == 2) {
      if (args[1] == 'all') {
        const res = await procedure_funcs.getProcedures(0, 100000, null, null, null, null, null, null, null, null, 'ASC', 'PROCEDURE_ID');
        const procedure_infos = res.data;
        for (let j=0; j < procedure_infos.length; j++) {
          let procedure_id = procedure_infos[j].procedure_id;
          // console.log(`Checking procedure: ${procedure_id}`);
          let res = await procedure_funcs.getProcedureVersions(procedure_id, 0, 10000, null, null, null, null, 'ASC', 'VERSION');
          let procedure_versions = res.data;
          
          for (let i=0; i < procedure_versions.length; i++) {
            let procedure_version = procedure_versions[i];
            await check_procedure_version(procedure_version.version_id, procedure_version.procedure_id, procedure_version.version, fix);      
          }
        }
      } else {
        const procedure_id = args[1];
        const res = await procedure_funcs.getProcedureVersions(procedure_id, 0, 10000, null, null, null, null, 'ASC', 'VERSION');
        const procedure_versions = res.data;
        // console.log(procedure_versions);
        // procedure_versions.sort((a, b) => (a.version > b.version ? 1 : -1));
        
        for (let i=0; i < procedure_versions.length; i++) {
          let procedure_version = procedure_versions[i];
          await check_procedure_version(procedure_version.version_id, procedure_version.procedure_id, procedure_version.version, fix);      
        }
      }  
    } else if (args.length == 3) {
      const procedure_id = args[1];
      const version = parseInt(args[2]);
      await check_procedure_version(null, procedure_id, version, fix);
    } else {
      print_usage();
    }    
  } else if (command == 'execution') {
    if (args.length == 2) {
      if (args[1] == 'all') {
        const res = await node_funcs.getExecutions(0, 100000, 'ASC', 'EXECUTION_ID', null, null, 
          null, null, 
          null, null, 
          null, null, null, 
          null, null, null, null, 
          null, null);
        const execution_infos = res.data;
        for (let j=0; j < execution_infos.length; j++) {
          let execution_info = execution_infos[j];
          await check_execution(execution_info.execution_id, fix);
        }
      } else {
        const execution_id = args[1];
        await check_execution(execution_id, fix);      
      }  
    } else {
      print_usage();  
    }      
  } else {
    print_usage();
  }
}

console.log('Checking elements order...');

//sort_test();

main();
