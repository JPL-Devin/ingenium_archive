let node_funcs = require('./api/base_funcs');

node_funcs.reset_db()
.then((res) => {
    console.log('DB was reset.');
  }, (err) => {
    console.log('Failed to reset DB:', err);
})
