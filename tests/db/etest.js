var util = require('util')

function push_error(message, err) {
  if (typeof err == 'string') {
    err = {'message': err};
  }

  let err_json_ok = true;
  try {
    JSON.stringify(err);
  } catch (ex) {
    console.log(ex);
    err_json_ok = false;
  }

  console.log(`err_json_ok: ${err_json_ok}`);

  if (err_json_ok) {
    const err_new = extend(true, {}, err);
    err_new.message = message;
    if (!err_new.hasOwnProperty('details') || !Array.isArray(err_new.details)) {
      err_new.details = [];
    }

    if (err.message) {
      if (typeof err.message === 'string') {
        err_new.details.push(err.message);
      } else {
        err_new.details.push(util.inspect(err.message));
      }
    }

    if (err_new.details.length === 0) {
      err_new.details.push(util.inspect(err));
    }

    return err_new;
  } else {
    return {message: message, details: [util.inspect(err)]}
  }
}

const nestedObject = {};
nestedObject.a = [nestedObject];
nestedObject.b = [['a', ['b']], 'b', 'c', 'd'];
nestedObject.b = {};
nestedObject.b.inner = nestedObject.b;
nestedObject.b.obj = nestedObject;
  
// JSON.stringify(nestedObject);

let result = push_error('my message', nestedObject);

console.log(JSON.stringify(result));