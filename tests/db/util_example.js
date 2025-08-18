'use strict';

let util = require('util');
let a = {'item1': 1, 'item2': 2};
console.log(typeof util.inspect('a string'));
console.log(util.inspect('a string'));

console.log(typeof util.inspect(a));
console.log(util.inspect(a));
a['a'] = a;

console.log(typeof util.inspect(a));
console.log(util.inspect(a));
