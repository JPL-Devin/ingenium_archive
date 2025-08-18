let arangojs = require('arangojs');

db_url = process.env.ARANGODBURL ? process.env.ARANGODBURL : 'http://localhost:8529';
db_user = process.env.ARANGO_USER ? process.env.ARANGO_USER : 'root';
db_password = process.env.ARANGO_ROOT_PASSWORD ? process.env.ARANGO_ROOT_PASSWORD : 'somepassword';
db_name = 'hk';


async function update_result(db, elem_id, step_execution) {
  let step_to_update = {'execution': step_execution};

  let query_str = `FOR elem IN elems
    FILTER elem.elem_id == "${elem_id}"
    FILTER elem.execution.meta_data.status NOT IN ["PASS", "FAIL", "ERROR"]
    UPDATE elem WITH ${JSON.stringify(step_to_update)} IN elems
  `
  console.log(query_str);

  let cursor = await db.query(query_str);
  let res = await cursor.all();

  console.log(`res: ${res}`)
}

async function update_result_2(db, elem_id, step_execution) {
  let query_str = `FOR elem IN elems
    UPDATE {"_key": "${elem_id}", "execution": elem.execution.meta_data.status IN ["PASS", "FAIL", "ERROR"] ? elem.execution : ${JSON.stringify(step_execution)}} IN elems
  `
  console.log(query_str);

  let cursor = await db.query(query_str);
  let res = await cursor.all();

  console.log(`res: ${res}`)
}

async function test1() {
  let db = arangojs(db_url);
  db.useBasicAuth(db_user, db_password);

  const db_names = await db.listDatabases();

  let elems_collection = null;
  
  let elem_id_1 = 'elem_id_1';
  let elem_id_2 = 'elem_id_2';  

  if (!db_names.includes(db_name)) {
      console.log('Create a new DB');
      await db.createDatabase(db_name);

      db.useDatabase('hk');      

      elems_collection = db.collection('elems')

      console.log('Create a new collection');
      await elems_collection.create();

      console.log('Create documents');
      await elems_collection.save({'_key': elem_id_1, 'elem_id': elem_id_1});
      await elems_collection.save({'_key': elem_id_2, 'elem_id': elem_id_2});
  }

  db.useDatabase('hk');
  
  elems_collection = db.collection('elems');

  let step_execution = null;
  let elem_1 = null;
  let elem_2 = null;
  let str_with_newlines = 'abc def\nghi jk\n';

  await elems_collection.replace(elem_id_1, {'elem_id': elem_id_1, 'execution': {'meta_data': {'status': 'RUNNING', 'time': 1}}});  
  step_execution = {'meta_data': {'status': 'RUNNING', 'time': 11, 'msg': str_with_newlines}};
  await update_result_2(db, elem_id_1, step_execution)
  elem_1 = await elems_collection.document(elem_id_1);
  elem_2 = await elems_collection.document(elem_id_2);
  console.log(`elem_1: ${JSON.stringify(elem_1)}`);
  console.log(`elem_2: ${JSON.stringify(elem_2)}`);
  console.log(``);  

  await elems_collection.replace(elem_id_1, {'elem_id': elem_id_1, 'execution': {'meta_data': {'status': 'PASS', 'time': 2}}});  
  step_execution = {'meta_data': {'status': 'RUNNING', 'time': 11, 'msg': str_with_newlines}};  
  await update_result_2(db, elem_id_1, step_execution)
  elem_1 = await elems_collection.document(elem_id_1);
  elem_2 = await elems_collection.document(elem_id_2);
  console.log(`elem_1: ${JSON.stringify(elem_1)}`);
  console.log(`elem_2: ${JSON.stringify(elem_2)}`);
  console.log(``);  

  await elems_collection.replace(elem_id_1, {'elem_id': elem_id_1});  
  step_execution = {'meta_data': {'status': 'RUNNING', 'time': 11, 'msg': str_with_newlines}};
  await update_result_2(db, elem_id_1, step_execution)
  elem_1 = await elems_collection.document(elem_id_1);
  elem_2 = await elems_collection.document(elem_id_2);
  console.log(`elem_1: ${JSON.stringify(elem_1)}`);
  console.log(`elem_2: ${JSON.stringify(elem_2)}`);
  console.log(``);  
}

test1();
