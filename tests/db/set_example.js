'use strict';

var s = new Set();

s.add('ab');
s.add('cd');
s.add(1);
s.add('abc');
s.add('abc');

console.log(s.values());

for (let v of s.values()) {
  console.log(v);
}


var ar = ['dfa', 'gr', 'afasdfa'];
ar.sort();
console.log('ar:', ar);
