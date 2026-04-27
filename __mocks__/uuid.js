'use strict';

let counter = 0;

const v4 = jest.fn(() => `mock-uuid-${++counter}`);
const v1 = jest.fn(() => `mock-uuid-v1-${++counter}`);

module.exports = {
  v4,
  v1,
  MAX: '00000000-0000-0000-0000-000000000000',
  NIL: '00000000-0000-0000-0000-000000000000',
  parse: jest.fn(),
  stringify: jest.fn(),
  validate: jest.fn(() => true),
  version: jest.fn(() => 4),
};
