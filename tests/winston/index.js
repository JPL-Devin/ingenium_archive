const winston = require('winston');
const MESSAGE = Symbol.for('message');
const util = require('util');
var extend = require('extend');

const json_formatter = (log_entry) => {
  //console.log('log_entry', log_entry)
  const json_data = {timestamp: new Date()};
  json_data['level'] = log_entry['level'].toUpperCase();
  json_data['message'] = log_entry['message'];
  let log_entry_meta = log_entry['meta'];


  if (log_entry_meta) {
    //console.log('log_entry_meta:', log_entry_meta)
    //console.log('typeof log_entry_meta:', typeof log_entry_meta)
    //console.log('log_entry_meta instanceof String:', log_entry_meta instanceof String)
    //console.log('Object.getOwnPropertyNames(log_entry_meta):', Object.getOwnPropertyNames(log_entry_meta))
    //console.log('Object.keys(log_entry_meta):', Object.keys(log_entry_meta))

    // If the passed object is string, array, or object with no properties, 
    // add it as details.
    if (typeof log_entry_meta === 'string' || log_entry_meta instanceof String) {
      json_data['details'] = [log_entry_meta];
    } else if (Array.isArray(log_entry_meta)) {
      json_data['details'] = log_entry_meta.map(function(item) {
        let item_inspected = util.inspect(item);
        console.log('item_inspected:', item_inspected);
        return item_inspected
      });
    } else if (Object.keys(log_entry_meta).length == 0) {
      json_data['details'] = util.inspect(log_entry_meta);
    } else {
      // merge the passed object into json_data
      Object.assign(json_data, log_entry_meta);
    }
  }
  // console.log('json_data:', JSON.stringify(json_data))
  log_entry[MESSAGE] = JSON.stringify(json_data);  
  
  return log_entry;
}

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(winston.format.splat(), winston.format.simple(), winston.format(json_formatter)()),
  transports: new winston.transports.Console(),
});

/*
const logger2 = winston.createLogger({
  level: 'info',
  format: winston.format.combine(winston.format.splat(), winston.format.simple()),
  transports: new winston.transports.Console(),
});
*/
logger.info('message content 1')
logger.info('message content 2', {'service': 'EXEC_SERVER', 'event': 'ADD_STEP', 'data': {'error_type': 'USER_INPUT_ERROR'}});
logger.info('message content 3', 'abc');
logger.info('message content 4', ['ab', 'cd']);
logger.info('message content 5', 'hi', 'ho');
try {
   not_a_func();
} catch (ex) {
  logger.info('error calling a func', ex);
}

/*
console.log('--- 2 ---');

logger2.info('message content 1', { "context": "index.js", "metric": 1 })
logger2.info('message content 2');
logger2.info('message content 3: %s', 'h3h3h3');
logger2.info('message content 4:', 'h4h4h4');
*/

/*
let data = {};

for (let i=0; i < 10000; i++) {
    data['a' + i] = 'b'+ i;
}

logger.info('message content 3', data);
*/