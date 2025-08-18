var arangojs = require('arangojs');
var base_funcs = require('./api/base_funcs');
var node_funcs = require('./api/node_funcs');
var procedure_funcs = require('./api/procedure_funcs');
var readline = require('readline');
const config = require('./config');
const { mainModule } = require('process');
var get_sj_error_message = base_funcs.get_sj_error_message;

var db = arangojs(config.db_url);

// console.log(`db_user: ${db_user}`);
// console.log(`db_password: ${db_password}`);

db.useBasicAuth(config.db_user, config.db_password);
db.useDatabase(config.database_name);

async function main() {
    const procedure_collection = db.collection('procedure');
    console.log(`procedure_collection: ${procedure_collection}`);
    try {
        await new Promise(r => setTimeout(r, 20000));
        const proc = await procedure_collection.document('123');
        console.log(`proc: ${proc}`);
    } catch (err) {
        console.log(`err: ${err}`);

        const err_obj = base_funcs.push_error('Top level msg', err);
        console.log(JSON.stringify(err_obj));
    }
}


main();




